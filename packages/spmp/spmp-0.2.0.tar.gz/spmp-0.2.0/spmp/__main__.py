"""
spmp
Satellite Products Metadata Parser

Copyright (C) <2023>  <Manchon Pierre>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import re
import sys
from argparse import ArgumentParser

try:
    from _version import __version__
    from naming_convention import naming_convention
except ImportError:
    from spmp._version import __version__
    from spmp.naming_convention import naming_convention


def parse(product: str) -> dict:
    result = None
    for k in naming_convention.keys():
        if match := re.search(k, product):
            result = dict(zip(naming_convention[k].keys(), match.groups()))
            break
    if result is None:
        msg = f'Could not find matching regex for product "{product}"'
        print(msg)
    return result


def run():
    parser = ArgumentParser(prog=f"$ python spmp",
                            description="Satellite Product Metadata Parser",
                            add_help=False,
                            epilog="\n")
    # Create the basic arguments
    parser.add_argument("-h", "--help",
                        dest="help", action="help",
                        help="Show this help message and exit")
    parser.add_argument("-v", "--version",
                        dest="version", action="store_true",
                        help="Show the program's version and exit")

    # Create the program's arguments
    parser.add_argument("-p", "--product", dest="product",
                        help="Parse any satellite product name")

    # If no arguments are given, print the help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)  # print the help
        sys.exit(1)

    # Parse the arguments
    args = parser.parse_args()

    # Based on the dest vars execute methods with the arguments
    try:
        if args.product:
            result = parse(args.product)
            print(result)
        elif args.version:
            print(__version__)
        elif args.help:
            parser.print_help(sys.stderr)  # print the help
    except AttributeError as _:
        # parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    run()
