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


def _validate_positive_int(value: Any, name: str) -> None:
    """Validate that *value* is a positive integer, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is not a positive integer.
    """
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise TypeError(f"{name} must be a positive integer")


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

    Raises:
        TypeError: If number is not a positive integer.
    """
    _validate_positive_int(number, "number")
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

    Raises:
        TypeError: If repeat or number is not a positive integer.
    """
    _validate_positive_int(repeat, "repeat")
    _validate_positive_int(number, "number")
    return _timeit.repeat(
        stmt, setup=setup, timer=timer, repeat=repeat, number=number, globals=globals
    )


Timer = _timeit.Timer
