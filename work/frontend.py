# Copyright (C) 2011 Dan Colish
# All rights reserved.
#
# This file is part of 'Work' and is distributed under the GPLv3 license.
# See LICENSE for more details.

from argparse import ArgumentParser, SUPPRESS
from inspect import getargspec
from os.path import abspath, expanduser

from work.events import EventManager


def main():

    parser = ArgumentParser(prog='work')

    parser.add_argument('--data', default='~/.work')
    subparser = parser.add_subparsers(
        dest='command', help='available commands for %(prog)s')
    subparser.add_parser('list', help='show all work events')

    start = subparser.add_parser('start', help='start a work event')
    start.add_argument('name', nargs='?')
    subparser.add_parser('stop', help='stop a work event')

    args = parser.parse_args()
    event_manager = EventManager(abspath(expanduser(args.data)))
    func_map = {'start': event_manager.start,
                'list': event_manager.list,
                'stop': event_manager.stop,
                }
    fn = func_map.get(args.command)
    fn_args = getargspec(fn).args
    kw_args = {}
    for fn_arg in fn_args:
        if fn_arg == 'self':
            continue
        kw_args.update({fn_arg: getattr(args, fn_arg)})
    fn(**kw_args)
