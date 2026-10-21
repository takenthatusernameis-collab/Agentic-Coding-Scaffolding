"""Debugger utilities wrapping the standard library :mod:`pdb` module."""

from __future__ import annotations

from typing import Any, Callable, Dict, Optional

try:
    import pdb as _pdb
except ImportError:  # pragma: no cover
    _pdb = None  # type: ignore[assignment]


def _pdb_module() -> Any:
    if _pdb is None:
        raise RuntimeError("the standard library module 'pdb' is not available")
    return _pdb


if _pdb is not None:
    Pdb = _pdb.Pdb
    pm = _pdb.pm
    post_mortem = _pdb.post_mortem
    set_trace = _pdb.set_trace
else:  # pragma: no cover
    Pdb = Any  # type: ignore[misc,assignment]
    pm = None  # type: ignore[assignment]
    post_mortem = None  # type: ignore[assignment]
    set_trace = None  # type: ignore[assignment]


def run(statement: str, globals_: Optional[Dict[str, Any]] = None, locals_: Optional[Dict[str, Any]] = None) -> None:
    if not isinstance(statement, str):
        raise TypeError("statement must be a string")
    if globals_ is not None and not isinstance(globals_, dict):
        raise TypeError("globals_ must be a dict or None")
    if locals_ is not None and not isinstance(locals_, dict):
        raise TypeError("locals_ must be a dict or None")
    return _pdb_module().run(statement, globals_, locals_)


def runeval(expression: str, globals_: Optional[Dict[str, Any]] = None, locals_: Optional[Dict[str, Any]] = None) -> Any:
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    if globals_ is not None and not isinstance(globals_, dict):
        raise TypeError("globals_ must be a dict or None")
    if locals_ is not None and not isinstance(locals_, dict):
        raise TypeError("locals_ must be a dict or None")
    return _pdb_module().runeval(expression, globals_, locals_)


def runcall(function: Callable[..., Any], *args: Any, **kwds: Any) -> Any:
    if not callable(function):
        raise TypeError("function must be callable")
    return _pdb_module().runcall(function, *args, **kwds)


def set_trace(*, header: Optional[str] = None) -> None:
    if header is not None and not isinstance(header, str):
        raise TypeError("header must be a string or None")
    module = _pdb_module()
    if header is None:
        return module.set_trace()
    return module.set_trace(header=header)


def post_mortem(t: Any = None) -> None:
    return _pdb_module().post_mortem(t)


__all__ = [
    "Pdb",
    "pm",
    "post_mortem",
    "run",
    "runcall",
    "runeval",
    "set_trace",
]
