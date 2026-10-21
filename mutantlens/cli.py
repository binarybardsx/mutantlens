import argparse
import sys
from collections.abc import Sequence

from mutantlens import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mutantlens")
    parser.add_argument(
        "--version", action="version", version=f"mutantlens {__version__}"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    assess = commands.add_parser(
        "assess", help="measure how well a test suite catches bugs"
    )
    assess.add_argument("path", help="project to assess")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "assess":
        print("not implemented")
    return 0


if __name__ == "__main__":
    sys.exit(main())
