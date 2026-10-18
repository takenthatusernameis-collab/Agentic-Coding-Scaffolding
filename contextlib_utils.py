"""Contextlib utility functions wrapping stdlib contextlib."""

from __future__ import annotations

import contextlib
from typing import Any

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


def chdir(path: Any) -> contextlib.chdir:
    return contextlib.chdir(path)


class ExitStack(contextlib.ExitStack):
    pass
