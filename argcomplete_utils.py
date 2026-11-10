"""Shell tab completion utilities wrapping the standard library `argcomplete` module.

This module provides input validation and safe access to argcomplete functionality.
"""

from __future__ import annotations

import sys
from typing import Any

# These are set at runtime; mypy will see them as Any due to the conditional import
argcomplete: Any = None
ChoicesCompleter: Any = None
FilesCompleter: Any = None

try:
    import argcomplete as _argcomplete
    from argcomplete.completers import ChoicesCompleter as _ChoicesCompleter
    from argcomplete.completers import FilesCompleter as _FilesCompleter

    argcomplete = _argcomplete
    ChoicesCompleter = _ChoicesCompleter
    FilesCompleter = _FilesCompleter
except ImportError:  # pragma: no cover - optional dependency
    pass


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
    always_complete_options: bool | str = True,
    exit_method: Any = sys.exit,
    print_suppressed: bool = False,
) -> None:
    """Enable shell tab completion for an argparse parser.

    Args:
        parser: An argparse.ArgumentParser instance.
        always_complete_options: Complete options even when the cursor is not at the start.
        exit_method: Callable to exit after completion (default: sys.exit).
        print_suppressed: Print suppressed options to stderr.

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
        print_suppressed=print_suppressed,
    )


def get_completer(choices: dict[str, str]) -> Any:
    """Create a choices completer for static options.

    Args:
        choices: Mapping of string choices to their completions.

    Returns:
        A ChoicesCompleter instance.

    Raises:
        ImportError: If argcomplete is not installed.
        TypeError: If choices is not a dict of strings.
    """
    _check_argcomplete_available()
    if not isinstance(choices, dict):
        raise TypeError(f"choices must be dict, got {type(choices).__name__}")
    if not all(isinstance(k, str) and isinstance(v, str) for k, v in choices.items()):
        raise TypeError("all choices keys and values must be strings")

    return ChoicesCompleter(choices)


def get_files_completer(
    allowednames: list[str] | tuple[str, ...] = (),
    directories: bool = True,
) -> Any:
    """Create a file system completer.

    Args:
        allowednames: Allowed file names or extensions.
        directories: Include directories in completions.

    Returns:
        A completer function.

    Raises:
        ImportError: If argcomplete is not installed.
    """
    _check_argcomplete_available()

    return FilesCompleter(allowednames=allowednames, directories=directories)


__all__ = [
    "autocomplete",
    "get_completer",
    "get_files_completer",
    "is_available",
]
