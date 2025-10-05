"""Console entry point for ios-simulator-cleaner."""

from __future__ import annotations

import argparse
import sys
from importlib import metadata

from .core import main_menu


def build_parser() -> argparse.ArgumentParser:
  """Create the CLI argument parser."""
  parser = argparse.ArgumentParser(
    prog="ios-simulator-cleaner",
    description="List and clean iOS simulators and SwiftUI previews.",
  )
  parser.add_argument(
    "--version",
    action="store_true",
    help="Print version information and exit.",
  )
  return parser


def main(argv: list[str] | None = None) -> int:
  """Run the CLI returning an exit code."""
  parser = build_parser()
  args = parser.parse_args(argv)

  if args.version:
    version = metadata.version("ios-simulator-cleaner")
    print(version)
    return 0

  try:
    main_menu()
  except KeyboardInterrupt:
    print("\nGoodbye!", file=sys.stderr)
  return 0


if __name__ == "__main__":
  sys.exit(main())
