#!/usr/bin/env python3

import threading
import logging
import enum
import typing
import datetime
from collections.abc import Sequence, Mapping, Callable, Iterator

import serial
import bitstruct

from .bus import Bus, get_timestamp
from confattr import Config

logger = logging.getLogger(__name__)


# ------- parse messages -------

def format_bytes(data: bytes) -> str:
	return ' '.join('%02x' % b for b in data)


class ByteSpec:

	def __init__(self, name: str, *, length: 'int|str|None' = None, allowed_values: 'Sequence[bytes]|bytes|int|None' = None) -> None:
		'''
		:paramref length: Either the number of bytes or the name of a previous byte spec which specifies the length of this byte spec
		'''
		if allowed_values is not None:
			if isinstance(allowed_values, int):
				allowed_values = bytes([allowed_values])
			if isinstance(allowed_values, bytes):
				allowed_values = [allowed_values]

			lengths = [len(val) for val in allowed_values]
			if length is None:
				if min(lengths) != max(lengths):
					raise ValueError("The allowed_values have different lengths")
				length = lengths[0]
			elif isinstance(length, str):
				if min(lengths) == max(lengths):
					raise ValueError("The length cannot be variable because all allowed_values have the same length")
			elif min(lengths) != max(lengths) or length != lengths[0]:
				raise ValueError("The length does not match the allowed_values")
		elif length is None:
			raise TypeError("Missing argument for length or allowed_values")

		if isinstance(length, int) and length <= 0:
			raise ValueError(f"length must be a positive number, the number of bytes, not {length}")

		self.name: 'typing.Final[str]' = name
		self.length: 'typing.Final[int|str]' = length
		self.allowed_values: 'typing.Final[Sequence[bytes]|None]' = allowed_values

	def get_length(self, values: 'Mapping[str, bytes]') -> int:
		if isinstance(self.length, int):
			return self.length
		length, = values[self.length]
		return length

	def format_allowed_values(self) -> str:
		if self.allowed_values is None:
			return ""
		return " or ".join(format_bytes(val) for val in self.allowed_values)

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self.name!r}, length={self.length!r}, allowed_values={self.format_allowed_values()})"

class MessageSpec:

	ADDRESS = 'address'

	def __init__(self, params: 'Sequence[ByteSpec]', *, implicit_address: 'int|None' = None) -> None:
		self.params = params
		self.implicit_address = implicit_address

	def __len__(self) -> int:
		return len(self.params)

	@typing.overload
	def __getitem__(self, index: int) -> ByteSpec:
		pass

	@typing.overload
	def __getitem__(self, index: slice) -> 'Sequence[ByteSpec]':
		pass

	def __getitem__(self, index: 'int|slice') -> 'ByteSpec|Sequence[ByteSpec]':
		return self.params[index]

	def __iter__(self) -> 'Iterator[ByteSpec]':
		return iter(self.params)


class Message:

	def __init__(self, db: 'Database', timestamp: 'datetime.datetime|None', values: 'Mapping[str, bytes]') -> None:
		self.db = db
		self.timestamp = timestamp
		self.values = values

	def format_timestamp(self) -> str:
		if self.timestamp is None:
			return ''
		return self.timestamp.strftime('%H:%M:%S.%f')

	def format_raw(self) -> str:
		timestamp = self.format_timestamp()
		if timestamp:
			timestamp += ' '

		values = ' '.join(format_bytes(b) for b in self.values.values())
		return timestamp + values

	def format(self) -> str:
		out = self.format_raw()
		if 'address' in self.values:
			address, = self.values['address']
		else:
			implicit_address = self.db.message_spec.implicit_address
			if implicit_address is None:
				raise ValueError(f"Message has neither explicit nor implicit address")
			address = implicit_address

		data = self.values['data']
		for sig, val in self.db.decode(address, data).items():
			out += f"\n\t{sig.name}: {val}{sig.unit}"
		return out


class Reader:

	ignore_bytes_between_messages = Config('reader.ignore-bytes-between-messages', [0xFF], unit='', help="If these bytes are encountered between two messages they are ignored instead of printing an error.")

	def __init__(self, bus: Bus, db: 'Database') -> None:
		self._stopped = False
		self.bus = bus
		self.db = db

	def read_in_other_thread(self, callback: 'Callable[[Message], None]') -> None:
		threading.Thread(target=self._read_in_other_thread, args=(callback,)).start()

	def _read_in_other_thread(self, callback: 'Callable[[Message], None]') -> None:
		for msg in self.read():
			callback(msg)

	def read(self) -> 'Iterator[Message]':
		try:
			while not self._stopped:
				try:
					msg = self.read_msg()
					if not msg:
						return
					yield msg
				except ValueError as e:
					logger.error(str(e))
		except EOFError:
			pass

	def read_msg(self) -> 'Message|None':
		values: 'dict[str, bytes]' = {}
		first_byte = True
		for spec in self.db.message_spec:
			val = []
			for i in range(spec.get_length(values)):
				allowed_values = spec.allowed_values
				while True:
					read_byte = self.read_n_bytes(1)
					if not read_byte:
						if first_byte:
							return None
						raise ValueError(f"Bus closed before message was complete")
					b, = read_byte

					if allowed_values is not None:
						allowed_values = [val for val in allowed_values if val[i]==b]
						if not allowed_values:
							if first_byte and b in self.ignore_bytes_between_messages:
								continue
							raise ValueError(f"Received unexpected value for byte {i} of {spec.name}: {b:02x}, should be {spec.format_allowed_values()}")
					break
				val.append(b)
				first_byte = False
			values[spec.name] = bytes(val)

		return Message(self.db, values=values, timestamp=get_timestamp(self.bus))

	def send_msg(self, msg: Message) -> None:
		values = dict(msg.values)
		out: 'list[int]' = []
		for spec in self.db.message_spec:
			if spec.name in values:
				out.extend(values.pop(spec.name))
			elif spec.allowed_values and len(spec.allowed_values) == 1:
				out.extend(spec.allowed_values[0])
			else:
				raise TypeError(f"Missing value for {spec.name!r}")
		if values:
			raise TypeError(f"Invalid value(s) passed: " + ", ".join(values.keys()))

		self.bus.write(bytes(out))

	def read_byte(self) -> int:
		out = self.read_n_bytes(1)
		assert len(out) == 1
		b = out[0]
		return b

	def read_n_bytes(self, n: int) -> bytes:
		if self._stopped:
			raise EOFError
		out = typing.cast(bytes, self.bus.read(n))
		if self._stopped:
			raise EOFError
		return out

	def stop(self) -> None:
		self._stopped = True
		self.bus.cancel_read()
		self.bus.cancel_write()
		self.bus.close()


# ------- parse data -------

class Endianness(enum.Enum):
	BIG = enum.auto()
	LITTLE = enum.auto()

class Type(enum.Enum):
	INT = 's'
	UINT = 'u'
	BOOL = 'b'
	FLOAT = 'f'
	TEXT = 't'

class Database:

	#: The parts that a message consists of, e.g. an address to be read, the length of the data, the data itself
	message_spec: 'MessageSpec'

	#: The possible signals which can be encoded in the data
	signals: 'Sequence[Signal]'

	#: The byte order
	endianness: Endianness

	#: The default length of a signal
	word_length_in_bits: int

	def __init__(self, message_spec: 'MessageSpec', signals: 'Sequence[Signal]', *, endianness: Endianness, word_length_in_bits: int = 8):
		self.message_spec = message_spec
		self.endianness = endianness
		self.word_length_in_bits = word_length_in_bits

		signals = list(signals)
		for s in signals:
			s.init(self)

		signals.sort(key=lambda s: s.address*word_length_in_bits + s.startbit)

		self.signals = signals

		for i in range(len(self.message_spec)):
			length = self.message_spec[i].length
			if isinstance(length, str):
				if length not in [_s.name for _s in self.message_spec[:i]]:
					spec = self.message_spec[i]
					raise ValueError("{spec.name!r} has invalid length {spec.length!}, there is no previous byte spec with that name")

		last_i1 = 0
		last_signal = None
		used_names: 'set[str]' = set()
		for s in signals:
			if s.name in used_names:
				raise ValueError(f"there are two signals with the same name {s.name!r}")

			i0 = self.get_start_bit(s)
			i1 = i0 + s.bits
			if i0 < last_i1:
				assert last_signal is not None
				raise ValueError(f"{s.name!r} overlaps with {last_signal.name!r}")

			last_signal = s
			last_i1 = i1

	def get_endianness_fmt(self) -> str:
		# "where > means most significant byte first and < means least significant byte first."
		#https://bitstruct.readthedocs.io/en/latest/#bitstruct.pack
		if self.endianness is Endianness.BIG:
			return '>'
		elif self.endianness is Endianness.LITTLE:
			return '<'
		else:
			assert False, "Invalid endianness: %r" % self.endianness


	def decode(self, address: int, data: bytes) -> 'dict[Signal, float]':
		data_bit_first = address * self.word_length_in_bits
		data_bit_after = data_bit_first + 8*len(data)
		fmtl = []
		sigs = []
		expected_next_bit = data_bit_first
		for s in self.signals:
			s_bit_first = self.get_start_bit(s)
			if s_bit_first < data_bit_first:
				continue
			s_bit_after = s_bit_first + s.bits
			if s_bit_after > data_bit_after:
				break

			if s_bit_first > expected_next_bit:
				undefined_bits = s_bit_first - expected_next_bit
				fmtl.append('p%s' % undefined_bits)
			expected_next_bit = s_bit_after

			fmtl.append(s.get_bitstruct_fmt())
			sigs.append(s)

		fmtl.append(self.get_endianness_fmt())

		fmt = ' '.join(fmtl)
		out: 'Sequence[float]' = bitstruct.unpack(fmt, data)
		out_dict = dict(zip(sigs, out))
		for s in out_dict.keys():
			if s.type is not Type.TEXT:
				#https://github.com/cantools/cantools/blob/master/cantools/database/conversion.py#L192
				out_dict[s] = out_dict[s] * s.scale + s.offset
		return out_dict

	def get_start_bit(self, signal: 'Signal') -> int:
		return signal.address * self.word_length_in_bits + signal.startbit


	def encode_range(self, address: int, length_in_bytes: int, value: 'Callable[[Signal], int|float|str]') -> bytes:
		'''
		Encode all signals which are completely within the given range
		'''
		bit_first = address * self.word_length_in_bits
		bit_after = bit_first + 8*length_in_bytes
		data: 'dict[Signal, int|float|str]' = {}
		for s in self.signals:
			s_bit_first = self.get_start_bit(s)
			if s_bit_first < bit_first:
				continue
			s_bit_after = s_bit_first + s.bits
			if s_bit_after > bit_after:
				break
			data[s] = value(s)

		out = self.encode(data)
		while len(out) < length_in_bytes:
			out += bytes([0])
		assert len(out) == length_in_bytes
		return out

	def encode(self, data: 'Mapping[Signal, int|float|str]|Mapping[str, int|float|str]') -> bytes:
		signals: 'list[Signal]' = []
		sig_to_val: 'dict[Signal, int|float|str]' = {}
		for s, val in data.items():
			if not isinstance(s, Signal):
				s = self.get_signal(s)
			if not isinstance(val, str):
				#https://github.com/cantools/cantools/blob/master/cantools/database/conversion.py#L206
				val = (val - s.offset) / s.scale
			sig_to_val[s] = val
			signals.append(s)
		del data

		if not signals:
			return bytes()

		signals.sort(key=lambda s: self.get_start_bit(s))

		fmtl = []
		vall = []
		expected_next_bit = signals[0].address * self.word_length_in_bits
		for s in signals:
			s_bit_first = self.get_start_bit(s)
			if s_bit_first > expected_next_bit:
				undefined_bits = s_bit_first - expected_next_bit
				fmtl.append('p%s' % undefined_bits)

			fmtl.append(s.get_bitstruct_fmt())
			vall.append(sig_to_val[s])

			expected_next_bit = s_bit_first + s.bits

		remainder = expected_next_bit % self.word_length_in_bits
		if remainder:
			undefined_bits = self.word_length_in_bits - remainder
			fmtl.append('p%s' % undefined_bits)

		fmtl.append(self.get_endianness_fmt())

		fmt = ' '.join(fmtl)
		out: bytes = bitstruct.pack(fmt, *vall)
		return out

	def get_signal(self, name: str) -> 'Signal':
		for s in self.signals:
			if s.name == name:
				return s

		raise ValueError(f"no signal with name {name!r}")


class Signal:

	def __init__(self, name: str, type: Type, address: int, *, bits: 'int|None' = None, startbit: 'int|None' = None, lsb: 'int|None' = None, scale: float = 1, offset: float = 0, unit: str = ''):
		'''
		:paramref name: The name of the signal
		:paramref type: The data type, e.g. INT, UINT, FLOAT
		:paramref address: The address which is used to request this value from the battery
		:paramref bits: The size of this signal in bits, defaults to :attr:`Database.word_length_in_bits <serialtools.database.Database.word_length_in_bits>`
		:paramref startbit: If the word identified by :paramref:`~serialtools.database.Signal.address` contains several smaller values the startbit specifies the first transmitted bit in the word belonging to the signal. Bit 0 is the first bit transmitted, not the least significant bit.
		:paramref lsb: If the word identified by :paramref:`~serialtools.database.Signal.address` contains several smaller values the lsb specifies where the list significant bit of the signal is inside of the word. :paramref:`~serialtools.database.Signal.startbit` and :paramref:`~serialtools.database.Signal.lsb` are mutually exclusive, only one of them may be passed.
		:paramref scale: A factor which is multiplied to the raw value received on the bus in order to get a value of :paramref:`~serialtools.database.Signal.unit`
		:paramref offset: A summand which is added to the raw value received on the bus in order to get a value of :paramref:`~serialtools.database.Signal.unit`
		:paramref unit: The unit of the value

		When decoding data from bytes received on the bus to human readable floats in the given unit
		the raw value is first multiplied with :paramref:`~serialtools.database.Signal.scale` and then :paramref:`~serialtools.database.Signal.offset` is added to it
		as in `cantools <https://github.com/cantools/cantools/blob/1ca17757c89ae1c1a97076e684e6aaa808b2d221/cantools/database/conversion.py#L197>`_.
		'''
		if startbit is None and lsb is None:
			startbit = 0
		elif startbit is not None and lsb is not None:
			raise TypeError('got values for startbit and lsb but only one of them may be given')
		elif startbit is None:
			assert isinstance(lsb, int)
			self._lsb = lsb
		self.name = name
		self.type = type
		self.address = address
		if startbit is not None:
			self.startbit = startbit
		self.scale = scale
		self.offset = offset
		self.unit = unit

		if bits is not None:
			self.bits = bits
		elif type is Type.BOOL:
			self.bits = 1

	def init(self, db: Database) -> None:
		if not hasattr(self, 'bits'):
			self.bits = db.word_length_in_bits

		if not hasattr(self, 'startbit'):
			startbit = 8 - self.bits - self._lsb
			if startbit < 0:
				raise ValueError(f'lsb is not implemented for signals spanning multiple bytes (lsb={self._lsb}, bits={self.bits})')
			self.startbit = startbit


	def get_bitstruct_fmt(self) -> str:
		return '%s%s' % (self.type.value, self.bits)


	def __repr__(self) -> str:
		return '%s(%s)' % (type(self).__name__, ', '.join('%s=%r' % (a, getattr(self, a)) for a in ('name', 'type', 'address', 'bits', 'startbit', 'offset', 'scale', 'unit')))
