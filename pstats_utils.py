"""Utilities for stats objects from profile runs (wrapping :mod:`pstats`).

The :mod:`pstats` module provides tools for managing and printing the
statistics produced by the :mod:`profile` and :mod:`cProfile` modules.
This wrapper exposes a validated surface for creating and manipulating
:class:`pstats.Stats` objects.
"""

from __future__ import annotations

import pstats as _pstats
from typing import Any, Optional, Union

__all__ = [
    "Stats",
    "SortKey",
    "new_stats",
    "load_stats",
    "add_stats",
    "print_stats",
    "sort_stats",
    "strip_dirs",
    "reverse_order",
    "dump_stats",
]


def _require_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_optional_str(value: object, name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    return value


def _require_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


Stats = _pstats.Stats
SortKey = _pstats.SortKey


def new_stats(
    *filenames: Union[str, _pstats.Stats],
    stream: Any = None,
) -> _pstats.Stats:
    """Create a new Stats object."""
    if stream is not None and not hasattr(stream, "write"):
        raise TypeError("stream must have a write method or None")
    if not filenames:
        return _pstats.Stats(stream=stream)
    return _pstats.Stats(*filenames, stream=stream)


def load_stats(*filenames: Union[str, _pstats.Stats]) -> _pstats.Stats:
    """Load statistics from files."""
    if not filenames:
        raise ValueError("at least one filename or Stats object is required")
    return _pstats.Stats(*filenames)


def add_stats(stats: _pstats.Stats, *filenames: Union[str, _pstats.Stats]) -> _pstats.Stats:
    """Add statistics from other files to an existing Stats object."""
    if not isinstance(stats, _pstats.Stats):
        raise TypeError(f"stats must be a pstats.Stats, got {type(stats).__name__}")
    if not filenames:
        raise ValueError("at least one filename or Stats object is required")
    stats.add(*filenames)
    return stats


def print_stats(
    stats: _pstats.Stats,
    *restrictions: Any,
    sort: Any = -1,
) -> _pstats.Stats:
    """Print the stats report."""
    if not isinstance(stats, _pstats.Stats):
        raise TypeError(f"stats must be a pstats.Stats, got {type(stats).__name__}")
    stats.print_stats(*restrictions)
    if sort != -1:
        stats.sort_stats(sort)
        stats.print_stats(*restrictions)
    return stats


def sort_stats(stats: _pstats.Stats, *field: Any) -> _pstats.Stats:
    """Sort the stats by the given criteria."""
    if not isinstance(stats, _pstats.Stats):
        raise TypeError(f"stats must be a pstats.Stats, got {type(stats).__name__}")
    stats.sort_stats(*field)
    return stats


def strip_dirs(stats: _pstats.Stats) -> _pstats.Stats:
    """Remove leading path information from file names."""
    if not isinstance(stats, _pstats.Stats):
        raise TypeError(f"stats must be a pstats.Stats, got {type(stats).__name__}")
    stats.strip_dirs()
    return stats


def reverse_order(stats: _pstats.Stats) -> _pstats.Stats:
    """Reverse the sorting order."""
    if not isinstance(stats, _pstats.Stats):
        raise TypeError(f"stats must be a pstats.Stats, got {type(stats).__name__}")
    stats.reverse_order()
    return stats


def dump_stats(stats: _pstats.Stats, filename: str) -> None:
    """Save the stats to a file."""
    if not isinstance(stats, _pstats.Stats):
        raise TypeError(f"stats must be a pstats.Stats, got {type(stats).__name__}")
    _require_str(filename, "filename")
    stats.dump_stats(filename)
