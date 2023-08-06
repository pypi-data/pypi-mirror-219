#!/usr/bin/env python3

import os
import sys
import time
import datetime
import logging
import typing
import argparse

import serial
from confattr import Config

logger = logging.getLogger(__name__)


# ------- virtual bus -------

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class ReadFromFileBus:

	timestamp: 'datetime.datetime|None' = None

	def __init__(self, fn: 'str|typing.TextIO') -> None:
		'''
		:param fn: file name of file containing data to be read. Data is in the output format of `serialtools dump`, hex values separated by spaces and optionally lines starting with a time stamps in parentheses.
		'''
		if isinstance(fn, str):
			fn = open(fn, 'rt')
		self.f = fn

	def read(self, n: int) -> bytes:
		out = []
		for i in range(n):
			h = ''
			while True:
				try:
					c = self.f.read(1)
				except:
					# ValueError: I/O operation on closed file.
					return bytes()
				if not c:
					self.close()
					return bytes()
				if not h and c.isspace():
					continue
				if not h and c == '(':
					timestamp = ''
					while True:
						c = self.f.read(1)
						if not c:
							self.close()
							return bytes()
						elif c == ')':
							self.timestamp = datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)
							break
						elif c == '(':
							raise ValueError("syntax error in {self.f.name!r}: {c!r} in timestamp")
						timestamp += c
					continue
				if not h and c == '#':
					while self.f.read(1) != '\n':
						pass
					continue
				h += c
				if len(h) >= 2:
					break

			b = int(h, base=16)
			out.append(b)
		return bytes(out)

	def write(self, data: bytes) -> None:
		raise NotImplementedError("This virtual bus implements reading only, no writing")

	def cancel_read(self) -> None:
		#TODO
		pass

	def cancel_write(self) -> None:
		pass

	def close(self) -> None:
		self.f.close()

class ReadFromParameterBus(ReadFromFileBus):

	def __init__(self, content: str) -> None:
		import io
		self.f = io.StringIO(content)


class WriteToFileBus:

	timestamp: 'datetime.datetime|None' = None

	def __init__(self, f: 'str|typing.TextIO|None', *, break_time_ms: int) -> None:
		self.f: 'typing.TextIO|None'
		if isinstance(f, str):
			self.f = open(f, 'wt')
		else:
			self.f = f
		self.break_time_s = break_time_ms / 1000
		self.last_time = 0.0
		self.vmode = True

	def read(self, n: int) -> bytes:
		raise NotImplementedError("This virtual bus implements writing only, no reading")

	def write(self, data: bytes) -> None:
		t = time.time()
		if self.break_time_s >=0 and t >= self.last_time + self.break_time_s:
			if not self.vmode:
				print('', file=self.f)
			print('(%s)' % datetime.datetime.now().strftime(TIMESTAMP_FORMAT), end=' ', file=self.f)
			self.vmode = False
		self.last_time = t

		for b in data:

			print('%02X' % b, end=' ', file=self.f, flush=True)

	def cancel_read(self) -> None:
		pass

	def cancel_write(self) -> None:
		#TODO
		pass

	def close(self) -> None:
		if self.f:
			self.f.close()


Bus: 'typing.TypeAlias' = 'serial.Serial|ReadFromFileBus|WriteToFileBus'


# ------- time stamps -------

def get_timestamp(bus: Bus) -> 'datetime.datetime|None':
	if isinstance(bus, serial.Serial):
		return datetime.datetime.now()
	else:
		return bus.timestamp


# ------- create bus -------

class BusCreator:

	# https://pythonhosted.org/pyserial/pyserial_api.html
	port = Config('bus.port', '/dev/ttyUSB0')
	vport = Config('bus.virtual-port', '/tmp/vserial1')
	vport_other = Config('bus.virtual-port-other', '/tmp/vserial2')
	auto_create_virtual_bus = Config('bus.auto-create', True, help="If the default virtual port does not exist create it with socat")
	virtual = Config('bus.virtual', False)
	baudrate = Config('bus.baudrate', 9600, unit='')
	bytesize = Config('bus.bytesize', serial.EIGHTBITS, allowed_values={
		'5': serial.FIVEBITS,
		'6': serial.SIXBITS,
		'7': serial.SEVENBITS,
		'8': serial.EIGHTBITS,
	})
	parity = Config('bus.parity', serial.PARITY_EVEN, allowed_values={
		'none': serial.PARITY_NONE,
		'even': serial.PARITY_EVEN,
		'odd': serial.PARITY_ODD,
		'mark': serial.PARITY_MARK,
		'space': serial.PARITY_SPACE,
	})
	stopbits = Config('bus.stopbits', serial.STOPBITS_ONE, allowed_values={
		'1': serial.STOPBITS_ONE,
		'1.5': serial.STOPBITS_ONE_POINT_FIVE,
		'2': serial.STOPBITS_TWO,
	})
	xonxoff = Config('bus.xonxoff', False, help="Enable software flow control")
	rtscts = Config('bus.rtscts', False, help="Enable hardware (RTS/CTS) flow control.")
	dsrdtr = Config('bus.dsrdtr', False, help="Enable hardware (DSR/DTR) flow control.")


	def add_arguments(self, parser: 'argparse.ArgumentParser', *, rx_only: bool = False) -> None:
		parser.add_argument('-v', '--virtual', action='store_true', default=None)
		parser.add_argument('-V', '--no-virtual', action='store_false', dest='virtual', default=None)
		g: 'argparse.ArgumentParser|argparse._MutuallyExclusiveGroup'
		if rx_only:
			g = parser.add_mutually_exclusive_group()
		else:
			g = parser
		help_port = "the serial port device"
		if rx_only:
			help_port += ", a log file or '-' to read from stdin"
		g.add_argument('-p', '-c', '--port', '--channel', help=help_port)
		if rx_only:
			g.add_argument('-m', '--message')
		parser.add_argument('-b', '--baudrate', type=int)
		parser.set_defaults(rx_only=rx_only)

	def create_args(self, *, port: 'str|None' = None, baudrate: 'int|None' = None, virtual: 'bool|None' = None) -> argparse.Namespace:
		parser = argparse.ArgumentParser()
		self.add_arguments(parser)
		args: 'list[str]' = []
		if port:
			args.append('--port')
			args.append(port)
		if baudrate:
			args.append('--baudrate')
			args.append(str(baudrate))
		if virtual:
			args.append('--virtual')
		return parser.parse_args(args)

	def create_bus(self, args: 'argparse.Namespace') -> Bus:
		if args.rx_only:
			if args.message:
				return ReadFromParameterBus(args.message)
			if args.port == '-':
				return ReadFromFileBus(sys.stdin)
			if args.port and os.path.isfile(args.port):
				return ReadFromFileBus(args.port)

		if args.virtual is None:
			args.virtual = self.virtual
		if args.virtual:
			if not args.port:
				args.port = self.vport
				if not os.path.exists(args.port):
					if self.auto_create_virtual_bus:
						import subprocess, shlex
						cmd = ['socat', '-d', '-d', 'pty,link=%s,raw,echo=0' % args.port, 'pty,link=%s,raw,echo=0' % self.vport_other]
						print("creating new virtual bus with %r" % shlex.join(cmd))
						print("please connect the other side to %r" % self.vport_other)
						subprocess.Popen(cmd)
						time.sleep(1)
					else:
						raise FileNotFoundError(f"serial bus {args.port!r} does not exist, you can create it with `$ socat -d -d pty,link={args.port},raw,echo=0 pty,link={self.vport_other},raw,echo=0`. Then rerun this program with --port={args.port}.")
			return serial.Serial(port=args.port)

		if not args.port:
			args.port = self.port
		if not args.baudrate:
			args.baudrate = self.baudrate
		logger.info(f"initializing serial bus {args.port} with baudrate={args.baudrate}")
		return serial.Serial(
			port = args.port,
			baudrate = args.baudrate,
			bytesize = self.bytesize,
			parity = self.parity,
			stopbits = self.stopbits,
			timeout = None,
			xonxoff = self.xonxoff,
			rtscts = self.rtscts,
			write_timeout = None,
			dsrdtr = self.dsrdtr,
			inter_byte_timeout = None,
		)

#: Use this to create a new bus
bus_creator = BusCreator()
