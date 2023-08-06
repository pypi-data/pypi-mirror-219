#!/usr/bin/env python3

import os
import sys
import argparse
from collections.abc import Sequence, Callable

from . import __version__, __doc__
from . import apps

from confattr import ConfigFile

APPNAME = 'serialtools'

class CallAction(argparse.Action):

	def __init__(self, option_strings: 'Sequence[str]', dest: str, callback: 'Callable[[], None]', help: str) -> None:
		argparse.Action.__init__(self, option_strings, dest, nargs=0, help=help)
		self.callback = callback

	def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: object, option_string: 'str|None' = None) -> None:
		self.callback()


def main(argv: 'list[str]|None' = None) -> None:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-v', '--version', action=CallAction, callback=print_version_and_exit, help="show the version and exit")
	parser.add_argument('-c', '--config', help="An additional config file to be loaded")
	apps.add_arguments(parser)
	args = parser.parse_args(argv)

	cf = ConfigFile(appname=APPNAME)
	cf.set_ui_callback(lambda msg: print(msg, file=sys.stderr))
	cf.load()
	if args.config:
		cf.load_file(os.path.abspath(os.path.expanduser(args.config)))

	if not hasattr(args, 'func'):
		print("missing command")
		print()
		parser.print_help()
		exit(1)
	args.func(args)


def print_version_and_exit() -> None:
	print(f"{APPNAME} {__version__}")
	sys.exit(0)


if __name__ == '__main__':
	main()
