#!/usr/bin/env python3

'''
Dump hex values read from serial bus
'''

import sys
import typing
import argparse

import serial
from confattr import Config

from serialtools.bus import bus_creator, Bus, WriteToFileBus


break_time_ms = Config('dump.break-time', 100, unit='ms', help="When nothing is received for this time span a line break and time stamp are written, a negative value disables line breaks and time stamps")

def add_parser(subparsers: 'argparse._SubParsersAction[typing.Any]') -> None:
	parser = subparsers.add_parser(__name__.rsplit('.', 1)[-1], help=__doc__)
	parser.add_argument('--break-time', default=break_time_ms.value, help=typing.cast(str, break_time_ms.help))
	bus_creator.add_arguments(parser)
	parser.set_defaults(func=main)

def main(args: 'argparse.Namespace') -> None:
	bus = bus_creator.create_bus(args)
	dump(bus, break_time_ms=args.break_time)

def dump(bus: Bus, *, break_time_ms: int = break_time_ms.value, file: 'typing.TextIO|None' = None) -> None:
	out = WriteToFileBus(file, break_time_ms=break_time_ms)
	while True:
		try:
			read_bytes = bus.read(1)
		except serial.serialutil.SerialException as e:
			print("", file=sys.stderr)
			print(e, file=sys.stderr)
			return

		if not read_bytes:
			print("", file=sys.stderr)
			print("Bus has been closed", file=sys.stderr)
			return

		out.write(read_bytes)
