"""Debugger framework utilities wrapping the standard library :mod:`bdb` module.

The :mod:`bdb` module is the framework the interactive debugger of the
standard library is built on.  It keeps the breakpoints of a debugging
session, decides whether a line of code stops the program, and calls back into
the debugger when it does.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It re-exports the classes :class:`Bdb` and
:class:`Breakpoint` together with the error :class:`BdbQuit`, and it adds the
helpers that manage the breakpoints of a session: setting, enabling, disabling
and removing them, listing them, and finding the breakpoint that is effective
for a line of code.

The breakpoints of the standard library live in the class attributes of
:class:`bdb.Breakpoint`, so every debugger of the process shares them.  The
helpers of this module work on that registry, and :func:`clear_all_breakpoints`
empties it again.
"""

from __future__ import annotations

import bdb as _bdb
import os
import types
from typing import Any, Dict, List, Optional, Sequence, Tuple

__all__: list[str] = [
    "Bdb",
    "BdbQuit",
    "Breakpoint",
    "breakpoint_hits",
    "canonical_filename",
    "checkfuncname",
    "clear_all_breakpoints",
    "clear_breakpoint",
    "clear_breakpoints",
    "create_bdb",
    "disable_breakpoint",
    "effective_breakpoint",
    "enable_breakpoint",
    "get_breakpoint",
    "get_breakpoints",
    "get_file_breakpoints",
    "is_bdb_instance",
    "is_breakpoint",
    "is_breakpoint_enabled",
    "set_breakpoint",
]

#: The debugger framework of the standard library.
Bdb = _bdb.Bdb

#: A breakpoint of a debugging session.
Breakpoint = _bdb.Breakpoint

#: The error the standard library raises when a debugger quits.
BdbQuit = _bdb.BdbQuit


def _require_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 1:
        raise ValueError(f"{name} must be a positive number, got {value}")
    return value


def _require_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_frame(value: object) -> types.FrameType:
    if not isinstance(value, types.FrameType):
        raise TypeError(f"frame must be a frame, got {type(value).__name__}")
    return value


def _require_breakpoint(value: object) -> Breakpoint:
    if not isinstance(value, Breakpoint):
        raise TypeError(f"breakpoint must be a bdb.Breakpoint, got {type(value).__name__}")
    return value


def canonical_filename(filename: str) -> str:
    """Return the canonical form of a file name.

    The standard library stores a breakpoint under the absolute name of its
    file, so a lookup of a breakpoint has to use the same form.

    Args:
        filename: The name of a file.

    Returns:
        The absolute name of the file, normalized for the case of the platform.
    """
    name = _require_str(filename, "filename")
    if not name:
        raise ValueError("filename must not be empty")
    return os.path.normcase(os.path.abspath(name))


def create_bdb(skip: Optional[Sequence[str]] = None) -> Bdb:
    """Create a debugger of the standard library framework.

    Args:
        skip: The names of the modules the debugger does not trace.

    Returns:
        A new debugger.
    """
    if skip is not None:
        if isinstance(skip, (str, bytes)):
            raise TypeError("skip must be a sequence of strings, not a single string")
        if not isinstance(skip, (list, tuple)):
            raise TypeError(f"skip must be a list or a tuple, got {type(skip).__name__}")
        for name in skip:
            if not isinstance(name, str):
                raise TypeError(f"skip entries must be strings, got {type(name).__name__}")
    return Bdb(skip=list(skip) if skip is not None else None)


def is_bdb_instance(obj: Any) -> bool:
    """Return ``True`` if *obj* is a debugger of the standard library framework.

    Args:
        obj: The object to check.

    Returns:
        ``True`` if the object is a debugger.
    """
    return isinstance(obj, Bdb)


def is_breakpoint(obj: Any) -> bool:
    """Return ``True`` if *obj* is a breakpoint of the standard library.

    Args:
        obj: The object to check.

    Returns:
        ``True`` if the object is a breakpoint.
    """
    return isinstance(obj, Breakpoint)


def get_breakpoints() -> Dict[int, Breakpoint]:
    """Return every breakpoint of the process, indexed by its number.

    Returns:
        The breakpoints of the registry of the standard library.
    """
    return {number: bp for number, bp in enumerate(Breakpoint.bpbynumber) if bp is not None}


def get_breakpoint(number: int) -> Optional[Breakpoint]:
    """Return the breakpoint with a number, if the registry holds one.

    Args:
        number: The number of the breakpoint.

    Returns:
        The breakpoint, or ``None`` when the registry holds no such number.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError(f"number must be an int, got {type(number).__name__}")
    if number < 0:
        raise ValueError(f"number must not be negative, got {number}")
    if number >= len(Breakpoint.bpbynumber):
        return None
    return Breakpoint.bpbynumber[number]


def get_file_breakpoints(filename: str) -> List[Breakpoint]:
    """Return the breakpoints that are set in a file.

    Args:
        filename: The name of the file.

    Returns:
        The breakpoints of the file, ordered by the line they stop at.
    """
    canonical = canonical_filename(filename)
    found: List[Breakpoint] = []
    for (name, _line), breakpoints in Breakpoint.bplist.items():
        if name == canonical:
            found.extend(breakpoints)
    return sorted(found, key=lambda bp: (bp.line, bp.number))


def set_breakpoint(
    filename: str,
    lineno: int,
    temporary: bool = False,
    cond: Optional[str] = None,
    funcname: Optional[str] = None,
) -> Breakpoint:
    """Set a breakpoint in a file.

    The breakpoint is registered in the registry of the standard library, so
    every debugger of the process sees it.

    Args:
        filename: The name of the file the breakpoint belongs to.
        lineno: The line the breakpoint stops at.
        temporary: Whether the breakpoint is removed once it was hit.
        cond: The condition that has to hold for the breakpoint to stop.
        funcname: The name of the function the breakpoint belongs to.

    Returns:
        The new breakpoint.
    """
    canonical = canonical_filename(filename)
    line = _require_positive_int(lineno, "lineno")
    _require_bool(temporary, "temporary")
    if cond is not None and not isinstance(cond, str):
        raise TypeError(f"cond must be a str or None, got {type(cond).__name__}")
    if funcname is not None and not isinstance(funcname, str):
        raise TypeError(f"funcname must be a str or None, got {type(funcname).__name__}")
    return Breakpoint(canonical, line, temporary, cond, funcname)


def clear_breakpoint(breakpoint: Breakpoint) -> bool:
    """Remove a breakpoint from the registry of the standard library.

    Args:
        breakpoint: The breakpoint to remove.

    Returns:
        ``True`` if the breakpoint was registered, ``False`` if it was not.
    """
    bp = _require_breakpoint(breakpoint)
    index = (bp.file, bp.line)
    if bp not in Breakpoint.bplist.get(index, []):
        return False
    bp.deleteMe()
    return True


def clear_breakpoints(filename: str) -> int:
    """Remove every breakpoint of a file from the registry.

    Args:
        filename: The name of the file.

    Returns:
        The number of removed breakpoints.
    """
    canonical = canonical_filename(filename)
    removed = 0
    for breakpoints in list(Breakpoint.bplist.values()):
        for bp in list(breakpoints):
            if bp.file == canonical:
                bp.deleteMe()
                removed += 1
    return removed


def clear_all_breakpoints() -> int:
    """Remove every breakpoint of the process from the registry.

    The registry starts over, the way the standard library restarts it: the
    numbers of the breakpoints begin at one again.

    Returns:
        The number of removed breakpoints.
    """
    removed = len(get_breakpoints())
    Breakpoint.bpbynumber = [None]
    Breakpoint.bplist = {}
    Breakpoint.next = 1
    return removed


def enable_breakpoint(breakpoint: Breakpoint) -> None:
    """Enable a breakpoint, so that it stops the program again.

    Args:
        breakpoint: The breakpoint to enable.
    """
    _require_breakpoint(breakpoint).enable()


def disable_breakpoint(breakpoint: Breakpoint) -> None:
    """Disable a breakpoint, so that it does not stop the program.

    Args:
        breakpoint: The breakpoint to disable.
    """
    _require_breakpoint(breakpoint).disable()


def is_breakpoint_enabled(breakpoint: Breakpoint) -> bool:
    """Return ``True`` if a breakpoint is enabled.

    Args:
        breakpoint: The breakpoint to check.

    Returns:
        ``True`` if the breakpoint stops the program.
    """
    return bool(_require_breakpoint(breakpoint).enabled)


def breakpoint_hits(breakpoint: Breakpoint) -> int:
    """Return the number of times a breakpoint was hit.

    Args:
        breakpoint: The breakpoint to check.

    Returns:
        The number of hits the breakpoint counted.
    """
    return int(_require_breakpoint(breakpoint).hits)


def effective_breakpoint(
    file: str,
    line: int,
    frame: types.FrameType,
) -> Tuple[Optional[Breakpoint], Optional[bool]]:
    """Return the breakpoint that is effective for a line of code.

    The standard library returns the breakpoint that stops the program and
    whether the breakpoint is to be removed afterwards.  A location without a
    breakpoint has no effective breakpoint at all.

    Args:
        file: The name of the file the line belongs to.
        line: The line of the code.
        frame: The frame the code runs in.

    Returns:
        The effective breakpoint and whether it is temporary, or a pair of
        ``None`` values when no breakpoint is effective.
    """
    canonical = canonical_filename(file)
    number = _require_positive_int(line, "line")
    stack_frame = _require_frame(frame)
    if (canonical, number) not in Breakpoint.bplist:
        return (None, None)
    return _bdb.effective(canonical, number, stack_frame)


def checkfuncname(breakpoint: Breakpoint, frame: types.FrameType) -> bool:
    """Return ``True`` if a breakpoint matches the line a frame runs.

    Args:
        breakpoint: The breakpoint to check.
        frame: The frame the code runs in.

    Returns:
        ``True`` if the breakpoint stops at the line of the frame.
    """
    bp = _require_breakpoint(breakpoint)
    stack_frame = _require_frame(frame)
    return _bdb.checkfuncname(bp, stack_frame)
