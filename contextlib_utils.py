"""Contextlib utility functions wrapping stdlib contextlib."""

from __future__ import annotations

import contextlib
import os
from contextlib import contextmanager
from typing import Any, Iterator

__all__: list[str] = [
    "suppress",
    "nullcontext",
    "closing",
    "redirect_stdout",
    "redirect_stderr",
    "chdir",
    "ExitStack",
]


def suppress(*exceptions: type[BaseException]) -> contextlib.suppress:
    return contextlib.suppress(*exceptions)


def nullcontext(enter_result: Any = None) -> contextlib.nullcontext:
    return contextlib.nullcontext(enter_result)


def closing(thing: Any) -> contextlib.closing:
    return contextlib.closing(thing)


def redirect_stdout(new_target: Any) -> contextlib.redirect_stdout:
    return contextlib.redirect_stdout(new_target)


def redirect_stderr(new_target: Any) -> contextlib.redirect_stderr:
    return contextlib.redirect_stderr(new_target)


@contextmanager
def chdir(path: Any) -> Iterator[None]:
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
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or os.PathLike")
    previous = os.getcwd()
    os.chdir(os.fspath(path))
    try:
        yield
    finally:
        os.chdir(previous)


class ExitStack(contextlib.ExitStack):
    pass
