import argparse
import sys
import logging
from har2postman.har2postman import Har2Postman
from har2postman import __version__


def main():
    parser = argparse.ArgumentParser(description='har to postman collection')
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")
    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")
    parser.add_argument(
        'har_path', nargs='?',
        help="har file path")

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    if len(sys.argv) == 1:
        # no argument passed
        parser.print_help()
        return 0

    if args.version:
        print("Version:{}".format(__version__))
        return 0

    har_path = args.har_path
    if not har_path or not har_path.endswith('.har'):
        logging.error('HAR file not specified.')
        sys.exit(1)
    har2 = Har2Postman(har_path)
    har2.run()
    return 0
