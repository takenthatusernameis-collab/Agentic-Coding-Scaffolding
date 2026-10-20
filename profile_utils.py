"""Utilities for profiling Python program execution (wrapping :mod:`profile`).

The :mod:`profile` module implements a deterministic profiler of Python
programs. This wrapper exposes a small, validated surface over that
functionality so callers can run code under the profiler, inspect the
collected statistics, and render them as readable reports.
"""

from __future__ import annotations

import profile as _profile
from typing import Any, Callable, Optional, TextIO

__all__ = [
    "new_profiler",
    "run",
    "runctx",
    "Profile",
    "main",
]


def run(
    statement: str,
    filename: Optional[str] = None,
    sort: int = -1,
) -> None:
    """Profile a single statement."""
    if not isinstance(statement, str):
        raise TypeError(f"statement must be a str, got {type(statement).__name__}")
    if filename is not None and not isinstance(filename, str):
        raise TypeError(f"filename must be a str or None, got {type(filename).__name__}")
    _profile.run(statement, filename=filename, sort=sort)


def runctx(
    statement: str,
    globals: Any,
    locals: Any,
    filename: Optional[str] = None,
    sort: int = -1,
) -> None:
    """Profile a statement in the given namespaces."""
    if not isinstance(statement, str):
        raise TypeError(f"statement must be a str, got {type(statement).__name__}")
    if filename is not None and not isinstance(filename, str):
        raise TypeError(f"filename must be a str or None, got {type(filename).__name__}")
    _profile.runctx(statement, globals, locals, filename=filename, sort=sort)


def new_profiler(timer: Any = None, bias: Any = None) -> _profile.Profile:
    """Create a new profiler."""
    return _profile.Profile(timer=timer, bias=bias)


Profile = _profile.Profile


def main() -> None:
    """Run the profile module's command-line entry point."""
    _profile.main()
