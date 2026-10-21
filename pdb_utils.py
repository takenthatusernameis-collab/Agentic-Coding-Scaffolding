"""Python debugger utilities wrapping the standard library :mod:`pdb` module.

The :mod:`pdb` module is the interactive debugger of the standard library.  It
runs a statement, an expression, or a function under the control of a prompt,
and it inspects the frame of a program after an exception was raised.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It re-exports the class :class:`Pdb` together with the
error :class:`Restart`, and it adds the helpers that run a program under the
debugger.

Every helper of this module opens the prompt of the debugger on the standard
input of the process, so a program that calls one of them has to answer the
prompt.  The tests of the project patch the standard library instead, so the
suite never waits for a prompt.
"""

from __future__ import annotations

import pdb as _pdb
import types
from typing import IO, Any, Callable, Dict, Mapping, Optional, Sequence

__all__: list[str] = [
    "Pdb",
    "Restart",
    "create_pdb",
    "is_pdb_instance",
    "pm",
    "post_mortem",
    "run",
    "runcall",
    "runctx",
    "runeval",
    "set_trace",
]

#: The interactive debugger of the standard library.
Pdb = _pdb.Pdb

#: The error the standard library raises when a debugger is restarted.
Restart = _pdb.Restart


def _require_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_optional_dict(value: object, name: str) -> Optional[Dict[str, Any]]:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict or None, got {type(value).__name__}")
    return value


def _require_mapping(value: object, name: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping, got {type(value).__name__}")
    return value


def create_pdb(
    completekey: str = "tab",
    stdin: Optional[IO[str]] = None,
    stdout: Optional[IO[str]] = None,
    skip: Optional[Sequence[str]] = None,
    nosigint: bool = False,
    readrc: bool = True,
) -> Pdb:
    """Create an interactive debugger.

    Args:
        completekey: The key that completes a name.
        stdin: The stream the debugger reads its commands from.
        stdout: The stream the debugger writes its output to.
        skip: The names of the modules the debugger does not trace.
        nosigint: Whether the debugger leaves the handling of ``SIGINT`` to
            the program.
        readrc: Whether the debugger reads the files of the user.

    Returns:
        A new debugger.
    """
    if not isinstance(completekey, str):
        raise TypeError(f"completekey must be a str, got {type(completekey).__name__}")
    if stdin is not None and not hasattr(stdin, "read"):
        raise TypeError("stdin must have a read method or None")
    if stdout is not None and not hasattr(stdout, "write"):
        raise TypeError("stdout must have a write method or None")
    if skip is not None:
        if isinstance(skip, (str, bytes)):
            raise TypeError("skip must be a sequence of strings, not a single string")
        if not isinstance(skip, (list, tuple)):
            raise TypeError(f"skip must be a list or a tuple, got {type(skip).__name__}")
        for name in skip:
            if not isinstance(name, str):
                raise TypeError(f"skip entries must be strings, got {type(name).__name__}")
    if not isinstance(nosigint, bool):
        raise TypeError(f"nosigint must be a bool, got {type(nosigint).__name__}")
    if not isinstance(readrc, bool):
        raise TypeError(f"readrc must be a bool, got {type(readrc).__name__}")
    return Pdb(
        completekey=completekey,
        stdin=stdin,
        stdout=stdout,
        skip=list(skip) if skip is not None else None,
        nosigint=nosigint,
        readrc=readrc,
    )


def is_pdb_instance(obj: Any) -> bool:
    """Return ``True`` if *obj* is an interactive debugger.

    Args:
        obj: The object to check.

    Returns:
        ``True`` if the object is a debugger.
    """
    return isinstance(obj, Pdb)


def set_trace(header: Optional[str] = None) -> None:
    """Enter the debugger at the frame of the caller.

    Args:
        header: The message the debugger prints before it waits for a command.
    """
    if header is not None and not isinstance(header, str):
        raise TypeError(f"header must be a str or None, got {type(header).__name__}")
    _pdb.set_trace(header=header)


def post_mortem(traceback: Optional[types.TracebackType] = None) -> None:
    """Enter the debugger with the frame of a traceback.

    Args:
        traceback: The traceback the debugger inspects.  The traceback of the
            exception that is handled at the moment is used when it is
            ``None``.
    """
    if traceback is not None and not isinstance(traceback, types.TracebackType):
        raise TypeError(f"traceback must be a traceback or None, got {type(traceback).__name__}")
    _pdb.post_mortem(traceback)


def pm() -> None:
    """Enter the debugger with the traceback of the last exception."""
    _pdb.pm()


def run(
    statement: str,
    globals: Optional[Dict[str, Any]] = None,
    locals: Optional[Mapping[str, object]] = None,
) -> Any:
    """Run a statement under the control of the debugger.

    Args:
        statement: The statement the debugger runs.
        globals: The global namespace of the statement.
        locals: The local namespace of the statement.

    Returns:
        The value of the last expression of the statement.
    """
    _require_str(statement, "statement")
    namespace = _require_optional_dict(globals, "globals")
    local_namespace = None if locals is None else _require_mapping(locals, "locals")
    return _pdb.run(statement, namespace, local_namespace)


def runeval(
    expression: str,
    globals: Optional[Dict[str, Any]] = None,
    locals: Optional[Mapping[str, object]] = None,
) -> Any:
    """Evaluate an expression under the control of the debugger.

    Args:
        expression: The expression the debugger evaluates.
        globals: The global namespace of the expression.
        locals: The local namespace of the expression.

    Returns:
        The value of the expression.
    """
    _require_str(expression, "expression")
    namespace = _require_optional_dict(globals, "globals")
    local_namespace = None if locals is None else _require_mapping(locals, "locals")
    return _pdb.runeval(expression, namespace, local_namespace)


def runctx(
    statement: str,
    globals: Dict[str, Any],
    locals: Mapping[str, object],
) -> None:
    """Run a statement in the given namespaces under the control of the debugger.

    Args:
        statement: The statement the debugger runs.
        globals: The global namespace of the statement.
        locals: The local namespace of the statement.
    """
    _require_str(statement, "statement")
    namespace = _require_optional_dict(globals, "globals")
    if namespace is None:
        raise TypeError("globals must be a dict")
    _require_mapping(locals, "locals")
    _pdb.runctx(statement, namespace, locals)


def runcall(function: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
    """Call a function under the control of the debugger.

    Args:
        function: The function the debugger calls.
        args: The positional arguments of the call.
        kwargs: The keyword arguments of the call.

    Returns:
        The value the function returned.
    """
    if not callable(function):
        raise TypeError(f"function must be callable, got {type(function).__name__}")
    return _pdb.runcall(function, *args, **kwargs)
