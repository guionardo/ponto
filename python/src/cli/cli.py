import argparse

from .parser import setup_parser


def main():
    parser: argparse.ArgumentParser = setup_parser()

    args = parser.parse_args()
    if args.func:
        args.func(args)
    pass
