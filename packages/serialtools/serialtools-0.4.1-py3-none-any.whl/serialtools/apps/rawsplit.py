#!/usr/bin/env python3

'''
Split a message into the parts it consists of
'''

import sys
import time
import datetime
import typing
import argparse
from collections.abc import Sequence

import serial
from confattr import Config

from serialtools.bus import Bus, bus_creator
from serialtools.database import Reader, Database, format_bytes
from serialtools.database_config import get_database


def add_parser(subparsers: 'argparse._SubParsersAction[typing.Any]') -> None:
	parser = subparsers.add_parser(__name__.rsplit('.', 1)[-1], help=__doc__)
	add_arguments(parser)
	parser.set_defaults(func=main)

def add_arguments(parser: 'argparse.ArgumentParser') -> None:
	bus_creator.add_arguments(parser, rx_only=True)

def main(args: 'argparse.Namespace') -> None:
	bus = bus_creator.create_bus(args)
	try:
		db = get_database(require_signals=False)
	except (ValueError, TypeError) as e:
		error(str(e))
	decode(bus, db)

def error(msg: str) -> 'typing.NoReturn':
	print(msg, file=sys.stderr)
	sys.exit(1)

def decode(bus: Bus, db: Database, *, file: 'typing.TextIO|None' = None) -> None:
	reader = Reader(bus, db)
	for msg in reader.read():
		#timestamp = msg.format_timestamp()
		#if timestamp:
		#	prefix = "[%s] " % timestamp
		#else:
		#	prefix = ""
		print(msg.format_raw(), file=file)
		for name, val in msg.values.items():
			print(f"\t{name}: {format_bytes(val)}")
