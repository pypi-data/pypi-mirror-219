#!/usr/bin/env python3

'''
Write hex values to serial bus
'''

import time
import datetime
import typing
import argparse

from serial import Serial
from confattr import Config

from serialtools.bus import bus_creator


def add_parser(subparsers: 'argparse._SubParsersAction[typing.Any]') -> None:
	parser = subparsers.add_parser(__name__.rsplit('.', 1)[-1], help=__doc__)
	parser.add_argument('msg')
	bus_creator.add_arguments(parser)
	parser.set_defaults(func=main)

def main(args: 'argparse.Namespace') -> None:
	bus = bus_creator.create_bus(args)
	send(bus, msg=args.msg)

def send(bus: Serial, *, msg: str) -> None:
	if ' ' in msg:
		smsg = msg.split(' ')
	else:
		if len(msg) % 2 != 0:
			print("ERROR: incomplete byte, odd number of hex digits")
			return
		smsg = [msg[i:i+2] for i in range(0, len(msg), 2)]
	data = bytes([int(b, base=16) for b in smsg])
	bus.write(data)
