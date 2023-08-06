#!/usr/bin/env python3

'''
Decode hex values read from serial bus or dump output
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
from serialtools.database import Reader, Database
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
		db = get_database()
	except (ValueError, TypeError) as e:
		error(str(e))
	decode(bus, db)

def error(msg: str) -> 'typing.NoReturn':
	print(msg, file=sys.stderr)
	sys.exit(1)

def decode(bus: Bus, db: Database, *, file: 'typing.TextIO|None' = None) -> None:
	reader = Reader(bus, db)
	for msg in reader.read():
		print(msg.format(), file=file)
