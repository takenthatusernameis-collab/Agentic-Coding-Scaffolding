"""Utilities for system error numbers (wrapping :mod:`errno`)."""

import errno as _errno
import os as _os

__all__ = [
    "errorcode",
    "errno_code",
    "errno_name",
    "is_errno",
    "strerror",
]


def errorcode(code: int) -> str | None:
    if isinstance(code, bool) or not isinstance(code, int):
        raise TypeError("code must be an int")
    return _errno.errorcode.get(code)


def strerror(code: int) -> str:
    if isinstance(code, bool) or not isinstance(code, int):
        raise TypeError("code must be an int")
    return _os.strerror(code)


def is_errno(code: int, name: str) -> bool:
    if isinstance(code, bool) or not isinstance(code, int):
        raise TypeError("code must be an int")
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    return getattr(_errno, name, None) == code


def errno_code(name: str) -> int | None:
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    value = getattr(_errno, name, None)
    return value if isinstance(value, int) else None


def errno_name(code: int) -> str | None:
    if isinstance(code, bool) or not isinstance(code, int):
        raise TypeError("code must be an int")
    return _errno.errorcode.get(code)
