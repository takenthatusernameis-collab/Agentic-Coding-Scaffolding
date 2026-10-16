"""Command-line interface utility functions.

This module provides helpers for building simple command-line applications:
creating an :mod:`argparse` parser with standard options, parsing arguments,
and wrapping a main function so it returns consistent process exit codes.
"""

from __future__ import annotations

import argparse
from functools import wraps
from typing import Callable, List, Optional

__all__: List[str] = [
    "create_parser",
    "parse_arguments",
    "main_wrapper",
]


def create_parser(
    prog: str,
    description: str,
    epilog: Optional[str] = None,
) -> argparse.ArgumentParser:
    """Create an ArgumentParser with standard options.

    Args:
        prog: The name of the program.
        description: A brief description of the program.
        epilog: Optional text displayed after the argument help.

    Returns:
        An ArgumentParser configured with ``--verbose`` and ``--version``.

    Examples:
        >>> parser = create_parser("my-tool", "A sample CLI tool.")
        >>> parser.prog
        'my-tool'
    """
    parser = argparse.ArgumentParser(prog=prog, description=description, epilog=epilog)
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("--version", action="version", version=f"{prog} 0.1.0")
    return parser


def parse_arguments(
    parser: argparse.ArgumentParser,
    args: Optional[List[str]] = None,
) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        parser: The ArgumentParser to use.
        args: Optional list of argument strings (defaults to sys.argv[1:]).

    Returns:
        The parsed arguments namespace.
    """
    return parser.parse_args(args)


def main_wrapper(func: Callable[[List[str]], int]) -> Callable[[List[str]], int]:
    """Wrap a main function to handle errors and return exit codes.

    Args:
        func: A function taking ``argv`` and returning an exit code.

    Returns:
        A wrapped function that returns ``0`` on success, ``1`` on error,
        and ``130`` on keyboard interrupt.

    Examples:
        >>> def main(argv):
        ...     print("running")
        ...     return 0
        >>> wrapped = main_wrapper(main)
        >>> wrapped([])
        running
        0
    """

    @wraps(func)
    def wrapper(argv: List[str]) -> int:
        try:
            return func(argv)
        except KeyboardInterrupt:
            return 130
        except Exception:
            return 1

    return wrapper
