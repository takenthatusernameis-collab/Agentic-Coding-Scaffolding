"""Shell tab completion utilities wrapping the standard library `argcomplete` module.

This module provides input validation and safe access to argcomplete functionality.
"""

from __future__ import annotations

import sys
from typing import Any

try:
    import argcomplete
    from argcomplete.completers import ChoicesCompleter
except ImportError:  # pragma: no cover - optional dependency
    argcomplete = None  # type: ignore[assignment]
    ChoicesCompleter = None  # type: ignore[assignment]


def _check_argcomplete_available() -> None:
    """Raise ImportError if argcomplete is not installed."""
    if argcomplete is None:
        raise ImportError(
            "argcomplete is not installed. Install with: pip install argcomplete"
        )


def is_available() -> bool:
    """Return True if argcomplete is installed and importable."""
    return argcomplete is not None


def autocomplete(
    parser: Any,
    always_complete_options: bool = True,
    exit_method: Any = sys.exit,
    print_errors: bool = True,
) -> None:
    """Enable shell tab completion for an argparse parser.

    Args:
        parser: An argparse.ArgumentParser instance.
        always_complete_options: Complete options even when the cursor is not at the start.
        exit_method: Callable to exit after completion (default: sys.exit).
        print_errors: Print errors to stderr.

    Raises:
        ImportError: If argcomplete is not installed.
        TypeError: If parser is not an argparse.ArgumentParser instance.
    """
    _check_argcomplete_available()
    import argparse

    if not isinstance(parser, argparse.ArgumentParser):
        raise TypeError(f"Expected argparse.ArgumentParser, got {type(parser).__name__}")

    argcomplete.autocomplete(
        parser,
        always_complete_options=always_complete_options,
        exit_method=exit_method,
        print_errors=print_errors,
    )


def get_completer(choices: list[str] | tuple[str, ...]) -> Any:
    """Create a choices completer for static options.

    Args:
        choices: List or tuple of string choices to complete.

    Returns:
        A ChoicesCompleter instance.

    Raises:
        ImportError: If argcomplete is not installed.
        TypeError: If choices is not a list or tuple of strings.
    """
    _check_argcomplete_available()
    if not isinstance(choices, (list, tuple)):
        raise TypeError(f"choices must be list or tuple, got {type(choices).__name__}")
    if not all(isinstance(c, str) for c in choices):
        raise TypeError("all choices must be strings")

    return ChoicesCompleter(choices)


def get_files_completer(
    directories: bool = True,
    filter_func: Any = None,
) -> Any:
    """Create a file system completer.

    Args:
        directories: Include directories in completions.
        filter_func: Optional callable to filter completions.

    Returns:
        A completer function.

    Raises:
        ImportError: If argcomplete is not installed.
    """
    _check_argcomplete_available()
    from argcomplete.completers import FilesCompleter

    return FilesCompleter(directories=directories, filter_func=filter_func)


__all__ = [
    "autocomplete",
    "get_completer",
    "get_files_completer",
    "is_available",
]