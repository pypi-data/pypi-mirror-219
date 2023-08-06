# -*- coding:utf-8 -*-

# This file is part of devpm.
#
# Copyright (c) 2023 wequick
# This software is distributed under the MIT license.

from argparse import ArgumentParser
import os
import sys

def create_argument_parser():
    """Create the argument parser."""

    parser = ArgumentParser(add_help=False)
    parser.usage = "devpm <commands> [options]"
    parser.description = "Development package manager."
    parser.epilog = "See <http://github.com/wequick/devpm> for the full manual."

    parser.add_argument('-h', '--help', action="help")
    parser.add_argument('-v', '--version', dest='version', action="store_true", default=False)

    subparsers = parser.add_subparsers(dest='command', help='commands')
    command_parser = subparsers.add_parser('install', help='install packages by devpackage.json')
    command_parser.usage = 'devpm install [options]'

    return parser


def version():
  try:
    import pkg_resources
    return pkg_resources.get_distribution('devpm').version
  except Exception as e:
    return ''


def main(args = None):
    parser = create_argument_parser()
    parser.version = 'devpm ' + version()
    options = parser.parse_args(args)
    if options.version:
        sys.stdout.write(parser.version)
        sys.stdout.write(os.linesep)
        sys.exit()
    if not options.command:
        parser.print_help()
        sys.exit(1)
    from devpm._internal.commands import create_command
    command = create_command(options.command)
    command.main(args)


if __name__ == '__main__':
    main()
