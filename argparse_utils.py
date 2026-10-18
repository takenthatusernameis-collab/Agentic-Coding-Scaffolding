"""Argument parsing utility functions."""

import argparse
from typing import Any, Callable, List, Optional


def make_parser(
    prog: Optional[str] = None,
    description: Optional[str] = None,
    epilog: Optional[str] = None,
) -> argparse.ArgumentParser:
    """Create an ArgumentParser with common defaults."""
    return argparse.ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )


def add_flag(
    parser: argparse.ArgumentParser,
    name: str,
    help_text: str = "",
    default: bool = False,
) -> None:
    """Add a boolean store_true flag to a parser."""
    parser.add_argument(name, action="store_true", default=default, help=help_text)


def add_option(
    parser: argparse.ArgumentParser,
    name: str,
    type_: Callable[[str], Any] = str,
    default: Any = None,
    help_text: str = "",
    required: bool = False,
) -> None:
    """Add a single-value option to a parser."""
    parser.add_argument(name, type=type_, default=default, help=help_text, required=required)


def add_positional(
    parser: argparse.ArgumentParser,
    name: str,
    type_: Callable[[str], Any] = str,
    nargs: Optional[str] = None,
    help_text: str = "",
) -> None:
    """Add a positional argument to a parser."""
    if nargs is None:
        parser.add_argument(name, type=type_, help=help_text)
    else:
        parser.add_argument(name, type=type_, nargs=nargs, help=help_text)


def add_subparsers(
    parser: argparse.ArgumentParser,
    title: str = "subcommands",
    dest: str = "command",
    required: bool = True,
) -> argparse._SubParsersAction:
    """Add a subparsers action to a parser."""
    return parser.add_subparsers(title=title, dest=dest, required=required)


def parse_args(
    parser: argparse.ArgumentParser, args: Optional[List[str]] = None
) -> argparse.Namespace:
    """Parse arguments, returning a namespace."""
    return parser.parse_args(args)


def int_positive(value: str) -> int:
    """argparse type: positive integer."""
    iv = int(value)
    if iv <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return iv


def float_range(minimum: float, maximum: float) -> Callable[[str], float]:
    """argparse type factory: float within [minimum, maximum]."""

    def _convert(value: str) -> float:
        fv = float(value)
        if fv < minimum or fv > maximum:
            raise argparse.ArgumentTypeError(f"must be between {minimum} and {maximum}")
        return fv

    return _convert
