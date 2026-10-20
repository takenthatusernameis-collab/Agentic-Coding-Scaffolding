"""Utilities wrapping the standard library ``timeit`` module.

This module provides convenient helpers for benchmarking small code snippets
using :mod:`timeit`, including :func:`timeit`, :func:`repeat`,
:func:`default_timer`, and the :class:`Timer` class.
"""

from __future__ import annotations

import timeit as _timeit
from typing import Any, Callable, Optional

__all__: list[str] = ["timeit", "repeat", "default_timer", "Timer"]


def default_timer() -> float:
    """Return the default timer used by :mod:`timeit`.

    Returns:
        Current time in seconds as a float.
    """
    return _timeit.default_timer()


def timeit(
    stmt: str = "pass",
    setup: str = "pass",
    timer: Callable[[], float] = default_timer,
    number: int = 1000000,
    globals: Optional[dict[str, Any]] = None,
) -> float:
    """Time execution of *stmt* and return the elapsed seconds.

    Args:
        stmt: Statement to time.
        setup: Setup code run once before timing.
        timer: Timer callable.
        number: Number of executions.
        globals: Optional globals dict.

    Returns:
        Elapsed time in seconds.
    """
    return _timeit.timeit(stmt, setup=setup, timer=timer, number=number, globals=globals)


def repeat(
    stmt: str = "pass",
    setup: str = "pass",
    timer: Callable[[], float] = default_timer,
    repeat: int = 5,
    number: int = 1000000,
    globals: Optional[dict[str, Any]] = None,
) -> list[float]:
    """Repeat timing of *stmt* and return list of elapsed times.

    Args:
        stmt: Statement to time.
        setup: Setup code run once before timing.
        timer: Timer callable.
        repeat: Number of repeats.
        number: Executions per repeat.
        globals: Optional globals dict.

    Returns:
        List of elapsed times.
    """
    return _timeit.repeat(
        stmt, setup=setup, timer=timer, repeat=repeat, number=number, globals=globals
    )


Timer = _timeit.Timer
