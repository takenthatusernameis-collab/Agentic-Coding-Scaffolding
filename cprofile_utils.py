"""Profiling utilities wrapping the standard library :mod:`cProfile` module.

The :mod:`cProfile` module is the C implementation of the deterministic
profiler: it counts how often every function of a program was called and
measures the time spent in that function.

The wrapper keeps the standard library as the single source of truth and adds
three conveniences the standard library does not offer: every helper validates
the types of its arguments before the standard library is reached, the report of
a profiling run is returned as text instead of being printed to standard
output, and a profiled call returns its result together with its statistics.
"""

from __future__ import annotations

import cProfile as _cProfile
import io
import os
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Literal,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
    cast,
)

__all__: list[str] = [
    "Profile",
    "collect_stats",
    "dump_stats",
    "format_report",
    "main",
    "new_profiler",
    "profile_call",
    "run",
    "runcall",
    "runctx",
]

_T = TypeVar("_T")

#: The key of a statistics entry: the file, the first line, and the name of a
#: function.
StatKey = Tuple[str, int, str]

#: The callers of a statistics entry, keyed by the entry of the caller.
Callers = Dict[StatKey, Tuple[int, int, float, float]]

#: The value of a statistics entry: the primitive calls, the total calls, the
#: time spent in the function, the time spent in the function and in the
#: functions it called, and the callers of the function.
StatValue = Tuple[int, int, float, float, Callers]

#: The statistics of a profiling run, keyed by the profiled function.
Stats = Dict[StatKey, StatValue]

#: The indexes of the columns a report can be sorted by.
_SORT_INDEXES = (-1, 0, 1, 2)


def _require_str(value: object, name: str) -> str:
    """Return *value* when it is a string.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The string value.

    Raises:
        TypeError: If the value is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_optional_str(value: object, name: str) -> Optional[str]:
    """Return *value* when it is a string or ``None``.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The string value or ``None``.

    Raises:
        TypeError: If the value is neither a string nor ``None``.
    """
    if value is None:
        return None
    return _require_str(value, name)


def _require_sort(value: object, name: str = "sort") -> Union[str, int]:
    """Return *value* when it is a sort key or a sort index.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The sort key or the sort index.

    Raises:
        TypeError: If the value is neither a string nor an integer.
    """
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise TypeError(f"{name} must be a str or an int, got {type(value).__name__}")
    return value


def _require_profiler(value: object, name: str = "profiler") -> _cProfile.Profile:
    """Return *value* when it is a profiler.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The profiler.

    Raises:
        TypeError: If the value is not a profiler.
    """
    if not isinstance(value, _cProfile.Profile):
        raise TypeError(f"{name} must be a cProfile.Profile, got {type(value).__name__}")
    return value


def new_profiler(
    timer: Optional[Callable[[], float]] = None,
    timeunit: Optional[float] = None,
    subcalls: bool = True,
    builtins: bool = True,
) -> _cProfile.Profile:
    """Create a profiler.

    Args:
        timer: A callable that returns the current time as a number of ticks.
            The standard library expects the timer to return an integer; a
            timer that returns a float is rejected with a clear message
            instead of failing inside the profiler.
        timeunit: The number of seconds a single tick of the timer represents.
        subcalls: Whether the profiler records the calls of the profiled
            functions.
        builtins: Whether the profiler records the calls of the built-in
            functions.

    Returns:
        The profiler.

    Raises:
        TypeError: If an argument is not of the expected type.
        ValueError: If *timeunit* is not a positive number.
    """
    if timer is not None and not callable(timer):
        raise TypeError(f"timer must be callable or None, got {type(timer).__name__}")
    if timeunit is not None:
        if isinstance(timeunit, bool) or not isinstance(timeunit, (int, float)):
            raise TypeError(f"timeunit must be a number or None, got {type(timeunit).__name__}")
        if timeunit <= 0:
            raise ValueError(f"timeunit must be a positive number, got {timeunit!r}")
    if not isinstance(subcalls, bool):
        raise TypeError(f"subcalls must be a bool, got {type(subcalls).__name__}")
    if not isinstance(builtins, bool):
        raise TypeError(f"builtins must be a bool, got {type(builtins).__name__}")

    kwargs: dict[str, Any] = {"subcalls": subcalls, "builtins": builtins}
    if timer is not None:
        _check_timer(timer)
        kwargs["timer"] = timer
    if timeunit is not None:
        kwargs["timeunit"] = float(timeunit)
    return _cProfile.Profile(**kwargs)


def _check_timer(timer: Callable[[], float]) -> None:
    """Check that *timer* returns the integer number of ticks the profiler needs.

    Args:
        timer: The timer to check.

    Raises:
        TypeError: If the timer does not return an integer.
    """
    value = timer()
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(
            "timer must return an integer number of ticks, "
            f"got {type(value).__name__}; use time.monotonic_ns with a timeunit of 1e-9"
        )


def run(statement: str, filename: Optional[str] = None, sort: Union[str, int] = -1) -> None:
    """Profile a single statement and report the result.

    Args:
        statement: The statement to profile.
        filename: The file the statistics are written to. The report is
            printed to standard output when no file is given.
        sort: The sort key or the sort index of the report.

    Raises:
        TypeError: If an argument is not of the expected type.
    """
    _require_str(statement, "statement")
    _require_optional_str(filename, "filename")
    _require_sort(sort)
    _cProfile.run(statement, filename=filename, sort=sort)


def runctx(
    statement: str,
    globals: Mapping[str, Any],
    locals: Mapping[str, Any],
    filename: Optional[str] = None,
    sort: Union[str, int] = -1,
) -> None:
    """Profile a statement in the given namespaces and report the result.

    Args:
        statement: The statement to profile.
        globals: The global namespace the statement runs in. It must be a
            dictionary, the kind of namespace the standard library uses.
        locals: The local namespace the statement runs in.
        filename: The file the statistics are written to. The report is
            printed to standard output when no file is given.
        sort: The sort key or the sort index of the report.

    Raises:
        TypeError: If an argument is not of the expected type.
    """
    _require_str(statement, "statement")
    if not isinstance(globals, dict):
        raise TypeError(f"globals must be a dict, got {type(globals).__name__}")
    if not isinstance(locals, Mapping):
        raise TypeError(f"locals must be a mapping, got {type(locals).__name__}")
    _require_optional_str(filename, "filename")
    _require_sort(sort)
    _cProfile.runctx(
        statement,
        globals,
        locals,
        filename=filename,
        sort=sort,
    )


def runcall(func: Callable[..., _T], /, *args: Any, **kwargs: Any) -> _T:
    """Profile a single call and return its result.

    The statistics of the call are discarded; use :func:`profile_call` to get
    them together with the result.

    Args:
        func: The callable to profile.
        args: The positional arguments of the call.
        kwargs: The keyword arguments of the call.

    Returns:
        The result of the call.

    Raises:
        TypeError: If *func* is not callable.
    """
    result, _ = _profile_call(func, args, kwargs)
    return result


def profile_call(
    func: Callable[..., _T], /, *args: Any, **kwargs: Any
) -> Tuple[_T, Stats]:
    """Profile a single call and return its result together with its statistics.

    Args:
        func: The callable to profile.
        args: The positional arguments of the call.
        kwargs: The keyword arguments of the call.

    Returns:
        The result of the call and the statistics of the call.

    Raises:
        TypeError: If *func* is not callable.
    """
    return _profile_call(func, args, kwargs)


def _profile_call(
    func: Callable[..., _T], args: Tuple[Any, ...], kwargs: Dict[str, Any]
) -> Tuple[_T, Stats]:
    """Profile a call and return its result together with its statistics.

    Args:
        func: The callable to profile.
        args: The positional arguments of the call.
        kwargs: The keyword arguments of the call.

    Returns:
        The result of the call and the statistics of the call.

    Raises:
        TypeError: If *func* is not callable.
    """
    if not callable(func):
        raise TypeError(f"func must be callable, got {type(func).__name__}")
    profiler = new_profiler()
    result = profiler.runcall(func, *args, **kwargs)
    return result, collect_stats(profiler)


def collect_stats(profiler: _cProfile.Profile) -> Stats:
    """Return the statistics a profiler collected.

    Args:
        profiler: The profiler to read the statistics from.

    Returns:
        The statistics of the profiler, keyed by the profiled function.

    Raises:
        TypeError: If *profiler* is not a profiler.
    """
    _require_profiler(profiler)
    profiler.create_stats()
    return cast(Stats, profiler.stats)


def format_report(
    profiler: _cProfile.Profile,
    sort: Union[str, int] = "cumulative",
    limit: Optional[int] = None,
) -> str:
    """Return the report of a profiling run as text.

    The standard library prints the report to standard output; the wrapper
    returns it, so the caller decides where it goes.

    Args:
        profiler: The profiler to report on.
        sort: The sort key of the report, such as ``"cumulative"``, or the
            index of the column the report is sorted by. The standard library
            knows the indexes ``-1`` (the name of the function), ``0`` (the
            number of calls), ``1`` (the time in the function), and ``2`` (the
            cumulative time).
        limit: The number of rows of the report. The whole report is returned
            when no limit is given.

    Returns:
        The report.

    Raises:
        TypeError: If an argument is not of the expected type.
        ValueError: If the sort key is unknown or the limit is not positive.
    """
    import pstats

    _require_profiler(profiler)
    _require_sort(sort)
    if limit is not None:
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise TypeError(f"limit must be an int or None, got {type(limit).__name__}")
        if limit <= 0:
            raise ValueError(f"limit must be a positive number, got {limit!r}")
    if isinstance(sort, str):
        if sort not in pstats.Stats.sort_arg_dict_default:
            raise ValueError(
                f"unknown sort key {sort!r}, expected one of "
                f"{sorted(pstats.Stats.sort_arg_dict_default)}"
            )
    elif sort not in _SORT_INDEXES:
        raise ValueError(f"unknown sort index {sort!r}, expected one of {sorted(_SORT_INDEXES)}")

    buffer = io.StringIO()
    stats = pstats.Stats(profiler, stream=buffer)
    if isinstance(sort, str):
        stats.sort_stats(sort)
    else:
        stats.sort_stats(cast(Literal[-1, 0, 1, 2], sort))
    if limit is None:
        stats.print_stats()
    else:
        stats.print_stats(limit)
    return buffer.getvalue()


def dump_stats(profiler: _cProfile.Profile, path: Union[str, "os.PathLike[str]"]) -> str:
    """Write the statistics of a profiling run to a file.

    Args:
        profiler: The profiler to read the statistics from.
        path: The file the statistics are written to.

    Returns:
        The path of the file the statistics were written to.

    Raises:
        TypeError: If an argument is not of the expected type.
    """
    _require_profiler(profiler)
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError(f"path must be a str or a path, got {type(path).__name__}")
    target = os.fspath(path)
    profiler.dump_stats(target)
    return target


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Run the ``cProfile`` command-line interface and return its exit code.

    ``argv`` accepts any iterable of strings; ``None`` runs the interface with
    the real process arguments. The standard library entry point reads
    ``sys.argv`` directly, so the arguments are installed temporarily.

    Args:
        argv: The arguments of the command-line interface.

    Returns:
        The exit code of the command-line interface.

    Raises:
        TypeError: If *argv* is neither an iterable of strings nor ``None``.
    """
    if argv is not None and not isinstance(argv, (list, tuple)):
        raise TypeError(f"argv must be a list, tuple, or None, got {type(argv).__name__}")
    original_argv = sys.argv
    if argv is None:
        sys.argv = list(sys.argv)
    else:
        sys.argv = ["cProfile", *[str(item) for item in argv]]
    try:
        _cProfile.main()  # type: ignore[attr-defined]
    except SystemExit as exit_error:
        code = exit_error.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        print(code, file=sys.stderr)
        return 1
    finally:
        sys.argv = original_argv
    return 0


#: The profiler class of the standard library.
Profile = _cProfile.Profile
