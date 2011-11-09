# Copyright (C) 2011 Dan Colish
# All rights reserved.
#
# This file is part of 'Timer' and is distributed under the GPLv3 license.
# See LICENSE for more details.

from argparse import ArgumentParser
from inspect import getargspec
from os.path import expanduser

from timer.events import EventManager


def main():
    event_manager = EventManager(expanduser('~/.timer'))
    func_map = {'start': event_manager.start,
                'list': event_manager.list,
                'stop': event_manager.stop,
                }
    parser = ArgumentParser()
    subparser = parser.add_subparsers(
        dest='command', help='available commands for timer')
    subparser.add_parser('list', help='show all things')

    start = subparser.add_parser('start', help='start a timed event')
    start.add_argument('name')

    stop = subparser.add_parser('stop', help='stop a timed event')
    stop.add_argument('name')

    args = parser.parse_args()
    fn = func_map.get(args.command)
    fn_args = getargspec(fn).args
    kw_args = {}
    for fn_arg in fn_args:
        if fn_arg == 'self':
            continue
        kw_args.update({fn_arg: getattr(args, fn_arg)})
    fn(**kw_args)

if __name__ == '__main__':
    main()
