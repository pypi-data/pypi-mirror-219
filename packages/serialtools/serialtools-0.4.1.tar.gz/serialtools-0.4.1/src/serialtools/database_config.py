#!/usr/bin/env python3

import argparse
import math
from collections.abc import Sequence

from confattr import ConfigFileArgparseCommand, ParseException, Config, ExplicitConfig

from . import database as db


def integer(val: str) -> int:
	if '*' in val:
		vals = [int(v, base=0) for v in val.split('*')]
		product = 1
		for v in vals:
			product *= v
		return product

	return int(val, base=0)


class Param(ConfigFileArgparseCommand):

	'''
	Define a parameter that can be used in the message command.
	'''

	defined_parameters: 'dict[str, db.ByteSpec]' = {}

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('name', help="The name of this parameter")
		parser.add_argument('-l', '--length', help="The length in bytes or the name of previous parameter which specifies the length in bytes")
		g = parser.add_mutually_exclusive_group()
		g.add_argument('-v', '--allowed-values', help="A comma seperated list of allowed values, each value is either an integer in python 3 syntax or a space separated list of bytes in hexadecimal notation")
		#g.add_argument('-c', '--calc', help="An expression to calculate the expected value based on previous parameters")
		#parser.add_argument('-p', '--preprocess', help="A unary operator or a binary operator followed by a constant or parameter name with which the received raw value will be preprocessed. Transmitted values will be postprocessed with the inverse of this.")

	def run_parsed(self, args: argparse.Namespace) -> None:
		name: str = args.name
		length: 'int|str|None'
		if args.length is None:
			length = None
		else:
			try:
				length = integer(args.length)
			except ValueError:
				length = args.length
		
		allowed_values = self.parse_allowed_values(args.allowed_values, length)

		if name in self.defined_parameters:
			raise ParseException(f"Parameter {name!r} has already been defined")

		try:
			self.defined_parameters[name] = db.ByteSpec(name, length=length, allowed_values=allowed_values)
		except (ValueError, TypeError) as e:
			raise ParseException(e)

	def parse_allowed_values(self, allowed_values: 'str|None', length: 'int|str|None') -> 'Sequence[bytes]|None':
		if not allowed_values:
			return None

		out: 'list[bytes]' = []
		for val in allowed_values.split(','):
			if ' ' in val:
				v = bytes(int(b, base=0) if b.startswith('0x') else int(b, base=16) for b in val.split(' '))
			else:
				i = integer(val)
				if not isinstance(length, int):
					length = math.ceil(i.bit_length() / 8)
					if length == 0:
						length = 1
				v = i.to_bytes(length, 'little' if DatabaseCreator.endianness.value is db.Endianness.LITTLE else 'big')
			out.append(v)

		return out


class Message(ConfigFileArgparseCommand):

	message: 'db.MessageSpec|None' = None

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('--implicit-address', '-a', type=int)
		parser.add_argument('parameters', nargs="+")

	def run_parsed(self, args: argparse.Namespace) -> None:
		out: 'list[db.ByteSpec]' = []
		for param_name in args.parameters:
			if not param_name in Param.defined_parameters:
				raise ParseException(f"Undefined parameter: {param_name!r}")
			out.append(Param.defined_parameters[param_name])
		type(self).message = db.MessageSpec(out, implicit_address=args.implicit_address)

class Signal(ConfigFileArgparseCommand):

	signals: 'list[db.Signal]' = []

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('name', help="The name of the signal")
		self.add_enum_argument(parser, 'type', type=db.Type)
		parser.add_argument('address', type=integer, help="The address which is used to request this value from the battery")
		parser.add_argument('--bits', type=integer, help="The size of this signal in bits")
		group = parser.add_mutually_exclusive_group()
		group.add_argument('--startbit', default=None, type=integer, help="If the word identified by address contains several smaller values the startbit specifies the first transmitted bit belonging to the signal")
		group.add_argument('--lsb', default=None, type=integer, help="If the word identified by address contains several smaller values the lsb specifies where the leat significant bit of the signal is inside of the word")
		parser.add_argument('--scale', type=float, default=1, help="A factor which is multiplied to the raw value received on the bus in order to get a value in the specified unit")
		parser.add_argument('--offset', type=float, default=0, help="A summand which is added to the raw value received on the bus in order to get a value in the specified unit")
		parser.add_argument('--unit', default='', help="The unit of the value")

	def run_parsed(self, args: argparse.Namespace) -> None:
		self.signals.append(db.Signal(args.name, args.type, args.address, bits=args.bits, startbit=args.startbit, lsb=args.lsb, scale=args.scale, offset=args.offset, unit=args.unit))

class DatabaseCreator:

	word_length_in_bits = Config('db.word-size', 8, unit='bits')
	endianness = ExplicitConfig('db.endianness', db.Endianness)

	def get(self, *, require_signals: bool = True) -> db.Database:
		if not Message.message:
			raise ValueError(f"message structure not defined")
		if require_signals and not Signal.signals:
			raise ValueError("no signals defined")
		return db.Database(Message.message, Signal.signals, endianness=self.endianness, word_length_in_bits=self.word_length_in_bits)

_db_creator = DatabaseCreator()
get_database = _db_creator.get
