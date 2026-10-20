"""Utilities for deterministic profiling of Python programs (wrapping :mod:`profile`).

The :mod:`profile` module provides a profiler that records how often and for
how long every function was called. This wrapper exposes a small, validated
surface over that functionality.
"""

from __future__ import annotations

import profile as _profile
from typing import Any, Callable, Optional

__all__ = ["Profile", "run", "runctx", "new_profiler"]


def new_profiler() -> _profile.Profile:
    """Create a new profiler instance."""
    return _profile.Profile()


def run(command: str, filename: Optional[str] = None) -> None:
    """Profile *command* executed in the ``__main__`` namespace."""
    if not isinstance(command, str):
        raise TypeError(f"command must be a str, got {type(command).__name__}")
    if filename is None:
        _profile.run(command)
    else:
        if not isinstance(filename, str):
            raise TypeError(f"filename must be a str, got {type(filename).__name__}")
        _profile.run(command, filename)


def runctx(
    command: str,
    globals_: dict,
    locals_: dict,
    filename: Optional[str] = None,
) -> None:
    """Profile *command* executed with the given globals and locals."""
    if not isinstance(command, str):
        raise TypeError(f"command must be a str, got {type(command).__name__}")
    if filename is None:
        _profile.runctx(command, globals_, locals_)
    else:
        if not isinstance(filename, str):
            raise TypeError(f"filename must be a str, got {type(filename).__name__}")
        _profile.runctx(command, globals_, locals_, filename)


Profile = _profile.Profile
"""Alias for :class:`profile.Profile`."""
