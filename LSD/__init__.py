"""The functions to handle the main function"""
from argparse import ArgumentParser


__version__ = "0.1"
"""The version of the package"""


def main():
    """The main function that loads the commands."""
    parser = ArgumentParser(prog='lsd', description="A simple tool to detect superbubbles.")
    
    add_global(parser)

    args = parser.parse_args()
    args.func(args)


def add_global(parser):
    """Add the global arguments to the parser.

    :param parser: The global ArgumentParser
    """
    parser.set_defaults(func=lambda x: parser.print_help())
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', '--verbose', action='store_true', dest="verbose", help="Create verbose output")
