import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from mutantlens import __version__
from mutantlens.assess import format_survey, survey


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
        path = Path(args.path)
        if not path.exists():
            print(f"error: path not found: {path}", file=sys.stderr)
            return 2
        print(format_survey(path, survey(path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
