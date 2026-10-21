"""Debugger utilities wrapping the standard library :mod:`bdb` module."""

from __future__ import annotations

from typing import Any, Callable, Optional

try:
    import bdb as _bdb
except ImportError:  # pragma: no cover
    _bdb = None  # type: ignore[assignment]


def _bdb_module() -> Any:
    if _bdb is None:
        raise RuntimeError("the standard library module 'bdb' is not available")
    return _bdb


if _bdb is not None:
    Bdb = _bdb.Bdb
    BdbQuit = _bdb.BdbQuit
    Breakpoint = _bdb.Breakpoint
    Tdb = _bdb.Tdb
    set_trace = _bdb.set_trace
    checkfuncname = _bdb.checkfuncname
    effective = _bdb.effective
else:  # pragma: no cover
    Bdb = Any  # type: ignore[misc,assignment]
    BdbQuit = None  # type: ignore[assignment]
    Breakpoint = Any  # type: ignore[misc,assignment]
    Tdb = Any  # type: ignore[misc,assignment]
    set_trace = None  # type: ignore[assignment]
    checkfuncname = None  # type: ignore[assignment]
    effective = None  # type: ignore[assignment]


__all__ = [
    "Bdb",
    "BdbQuit",
    "Breakpoint",
    "Tdb",
    "checkfuncname",
    "effective",
    "set_trace",
]