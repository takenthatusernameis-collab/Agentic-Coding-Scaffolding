"""Utilities wrapping the standard library ``warnings`` module."""

import warnings
from contextlib import contextmanager
from typing import Iterator, Optional, Type


def warn(message: str, category: Type[Warning] = UserWarning, stacklevel: int = 1) -> None:
    if not isinstance(message, str):
        raise TypeError("message must be str")
    warnings.warn(message, category=category, stacklevel=stacklevel)


def simplefilter(action: str, category: Type[Warning] = Warning) -> None:
    if action not in {"error", "ignore", "always", "default", "module", "once"}:
        raise ValueError("invalid action")
    warnings.simplefilter(action, category=category)  # type: ignore[arg-type]


@contextmanager
def catch_warnings(record: bool = False) -> Iterator[Optional[list]]:
    with warnings.catch_warnings(record=record) as w:
        yield w


def filterwarnings(action: str, message: str = "", category: Type[Warning] = Warning,
                  module: str = "", lineno: int = 0, append: bool = False) -> None:
    warnings.filterwarnings(action, message=message, category=category, module=module,  # type: ignore[arg-type]
                           lineno=lineno, append=append)


def resetwarnings() -> None:
    warnings.resetwarnings()
