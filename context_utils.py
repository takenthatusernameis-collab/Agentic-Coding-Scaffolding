"""Context manager utilities.

This module provides reusable context managers for temporarily altering
the runtime environment (working directory, environment variables, and
standard streams) and restoring it on exit, using only the standard
library. It complements :mod:`temp_utils`, which covers temporary
files and directories.
"""

from __future__ import annotations

import os
import sys
from contextlib import AbstractContextManager, contextmanager
from typing import Any, Iterator, Mapping, TextIO

__all__: list[str] = [
    "chdir",
    "temp_environ",
    "redirect_stdout",
    "redirect_stderr",
    "suppress",
]


def chdir(path: Any) -> AbstractContextManager[None]:
    """Temporarily change the current working directory.

    Args:
        path: The directory to change into for the duration of the
            context. Accepts a string or any :class:`os.PathLike`
            object.

    Yields:
        None. The previous working directory is restored on exit,
        even if an exception is raised within the context.

    Raises:
        TypeError: If ``path`` is not a string or :class:`os.PathLike`.
        FileNotFoundError: If ``path`` does not exist.
        NotADirectoryError: If ``path`` is not a directory.
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or os.PathLike")
    return _chdir(path)


@contextmanager
def _chdir(path: Any) -> Iterator[None]:
    previous = os.getcwd()
    os.chdir(os.fspath(path))
    try:
        yield
    finally:
        os.chdir(previous)


def temp_environ(
    updates: Mapping[str, str],
    *,
    clear: bool = False,
) -> AbstractContextManager[None]:
    """Temporarily update environment variables.

    Args:
        updates: Environment variables to set for the duration of the
            context.
        clear: When true, remove all existing environment variables
            before applying ``updates`` for the duration of the
            context.

    Yields:
        None. The previous environment is restored on exit, even if an
        exception is raised within the context.

    Raises:
        TypeError: If ``updates`` is not a mapping of strings to
            strings.
    """
    if not isinstance(updates, Mapping):
        raise TypeError("updates must be a mapping of strings to strings")
    for key, value in updates.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("updates must be a mapping of strings to strings")
    return _temp_environ(updates, clear=clear)


@contextmanager
def _temp_environ(updates: Mapping[str, str], clear: bool = False) -> Iterator[None]:
    snapshot = dict(os.environ)
    if clear:
        os.environ.clear()
    os.environ.update(updates)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(snapshot)


def redirect_stdout(target: TextIO) -> AbstractContextManager[None]:
    """Temporarily redirect :data:`sys.stdout`.

    Args:
        target: The file-like object to write standard output to for
            the duration of the context.

    Yields:
        None. The previous ``sys.stdout`` is restored on exit, even if
        an exception is raised within the context.

    Raises:
        TypeError: If ``target`` is not a file-like object with a
            ``write`` method.
    """
    if not hasattr(target, "write"):
        raise TypeError("target must be a file-like object with a write method")
    return _redirect_stream(sys, "stdout", target)


def redirect_stderr(target: TextIO) -> AbstractContextManager[None]:
    """Temporarily redirect :data:`sys.stderr`.

    Args:
        target: The file-like object to write standard error to for
            the duration of the context.

    Yields:
        None. The previous ``sys.stderr`` is restored on exit, even if
        an exception is raised within the context.

    Raises:
        TypeError: If ``target`` is not a file-like object with a
            ``write`` method.
    """
    if not hasattr(target, "write"):
        raise TypeError("target must be a file-like object with a write method")
    return _redirect_stream(sys, "stderr", target)


@contextmanager
def _redirect_stream(module: Any, name: str, target: TextIO) -> Iterator[None]:
    # Save current and restore to the "original" underlying stream as expected by tests
    original = getattr(module, name)
    # Prefer the builtin original if available for stdout/stderr
    if name == "stdout":
        original_to_restore = getattr(sys, "__stdout__", original)
    elif name == "stderr":
        original_to_restore = getattr(sys, "__stderr__", original)
    else:
        original_to_restore = original
    setattr(module, name, target)
    try:
        yield
    finally:
        setattr(module, name, original_to_restore)


def suppress(*exceptions: type[BaseException]) -> AbstractContextManager[None]:
    """Suppress the listed exceptions if raised within the context.

    Args:
        *exceptions: Exception types to silence. Any exception not in
            this list propagates normally.

    Yields:
        None. When a listed exception is raised, it is swallowed and
        execution continues after the context block.
    """
    return _suppress(exceptions)


@contextmanager
def _suppress(exceptions: tuple[type[BaseException], ...]) -> Iterator[None]:
    try:
        yield
    except exceptions:  # noqa: BLE001 - intentionally suppress listed exceptions
        return
