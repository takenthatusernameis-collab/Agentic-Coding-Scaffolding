"""Utilities for profiling Python program execution (wrapping :mod:`profile`).

The :mod:`profile` module provides a deterministic profiler. This wrapper
exposes a small, validated surface so callers can create a profiler, run code
under it, and inspect the collected statistics.
"""

from __future__ import annotations

import profile as _profile
from typing import Any, Callable, Optional, Tuple

__all__ = [
    "new_profiler",
    "run_profiled",
    "runctx_profiled",
    "print_stats",
    "get_stats",
    "Profile",
]


def new_profiler(
    timer: Optional[Callable[[], float]] = None,
    bias: Optional[float] = None,
) -> _profile.Profile:
    """Create a new profiler.

    Args:
        timer: Callable returning the current time. Defaults to ``time.perf_counter``.
        bias: Correction bias subtracted from the timer values.

    Returns:
        A profiler ready to run code under.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    if timer is not None and not callable(timer):
        raise TypeError(f"timer must be callable, got {type(timer).__name__}")
    if bias is not None and not isinstance(bias, (int, float)):
        raise TypeError(f"bias must be a number, got {type(bias).__name__}")
    kwargs: dict[str, Any] = {}
    if timer is not None:
        kwargs["timer"] = timer
    if bias is not None:
        kwargs["bias"] = bias
    return _profile.Profile(**kwargs)


def run_profiled(
    command: str,
    profiler: Optional[_profile.Profile] = None,
    globals_dict: Optional[dict[str, Any]] = None,
    locals_dict: Optional[dict[str, Any]] = None,
) -> Tuple[Any, _profile.Profile]:
    """Run *command* under a profiler and return ``(result, profiler)``.

    Args:
        command: Python source to execute.
        profiler: Profiler to use. A new one is created when ``None``.
        globals_dict: Globals namespace. Defaults to a fresh dict.
        locals_dict: Locals namespace. Defaults to *globals_dict*.

    Returns:
        A tuple of the execution result and the profiler.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    if not isinstance(command, str):
        raise TypeError(f"command must be a string, got {type(command).__name__}")
    active = new_profiler() if profiler is None else profiler
    if not isinstance(active, _profile.Profile):
        raise TypeError(f"profiler must be a profile.Profile, got {type(active).__name__}")
    g = {} if globals_dict is None else globals_dict
    if not isinstance(g, dict):
        raise TypeError(f"globals_dict must be a dict, got {type(g).__name__}")
    locals_ns = g if locals_dict is None else locals_dict
    if not isinstance(locals_ns, dict):
        raise TypeError(f"locals_dict must be a dict, got {type(locals_ns).__name__}")
    active.runctx(command, g, locals_ns)
    return None, active


def runctx_profiled(
    command: str,
    globals_dict: dict[str, Any],
    locals_dict: dict[str, Any],
    profiler: Optional[_profile.Profile] = None,
) -> _profile.Profile:
    """Run *command* under a profiler with explicit namespaces.

    Args:
        command: Python source to execute.
        globals_dict: Globals namespace.
        locals_dict: Locals namespace.
        profiler: Profiler to use. A new one is created when ``None``.

    Returns:
        The profiler used.

    Raises:
        TypeError: If an argument has an unsupported type.
    """
    if not isinstance(command, str):
        raise TypeError(f"command must be a string, got {type(command).__name__}")
    if not isinstance(globals_dict, dict):
        raise TypeError(f"globals_dict must be a dict, got {type(globals_dict).__name__}")
    if not isinstance(locals_dict, dict):
        raise TypeError(f"locals_dict must be a dict, got {type(locals_dict).__name__}")
    active = new_profiler() if profiler is None else profiler
    if not isinstance(active, _profile.Profile):
        raise TypeError(f"profiler must be a profile.Profile, got {type(active).__name__}")
    active.runctx(command, globals_dict, locals_dict)
    return active


def print_stats(profiler: object, sort: Optional[str] = None) -> None:
    """Print the statistics collected by *profiler*.

    Args:
        profiler: The profiler whose statistics are printed.
        sort: Optional sort key passed to ``print_stats``.

    Raises:
        TypeError: If *profiler* is not a profiler.
    """
    if not isinstance(profiler, _profile.Profile):
        raise TypeError(f"profiler must be a profile.Profile, got {type(profiler).__name__}")
    if sort is None:
        profiler.print_stats()
    else:
        if not isinstance(sort, str):
            raise TypeError(f"sort must be a string, got {type(sort).__name__}")
        profiler.print_stats(sort)


def get_stats(profiler: object) -> Any:
    """Return the raw statistics collected by *profiler*.

    Args:
        profiler: The profiler whose statistics are returned.

    Returns:
        The stats object held by the profiler.

    Raises:
        TypeError: If *profiler* is not a profiler.
    """
    if not isinstance(profiler, _profile.Profile):
        raise TypeError(f"profiler must be a profile.Profile, got {type(profiler).__name__}")
    return getattr(profiler, "stats", None)


Profile = _profile.Profile
"""Alias for :class:`profile.Profile`."""
