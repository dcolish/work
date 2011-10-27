from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('-l', '--list', help='show all things')

    start = parser.sub_parser('start')
    start.add_argument('event_name')

    stop = parser.sub_parser('stop')
    stop.add_argument('--hash')
    stop.add_argument('--name')

    options = parser.parse_args()

    options.foo  # STOPPED:dc: parse those args and run something
