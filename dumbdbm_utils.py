"""dumbdbm database utilities wrapping :mod:`dbm.dumb`."""

from __future__ import annotations

import dbm.dumb as _dumbdbm
import os
from typing import Any

__all__ = [
    "dumbdbm",
    "error",
    "open",
    "open_dbm",
    "create_dbm",
    "is_available",
]


error = _dumbdbm.error
dumbdbm = _dumbdbm


def open(
    file: str,
    flag: str = "r",
    mode: int = 0o666,
):
    """Open a dumbdbm database."""
    if not isinstance(file, str):
        raise TypeError("file must be a str")
    if not isinstance(flag, str):
        raise TypeError("flag must be a str")
    if not isinstance(mode, int) or isinstance(mode, bool):
        raise TypeError("mode must be an int")
    return _dumbdbm.open(file, flag, mode)


open_dbm = open


def create_dbm(
    file: str,
    flag: str = "c",
    mode: int = 0o666,
):
    """Create or open a dumbdbm database."""
    if not isinstance(file, str):
        raise TypeError("file must be a str")
    if not isinstance(flag, str):
        raise TypeError("flag must be a str")
    if not isinstance(mode, int) or isinstance(mode, bool):
        raise TypeError("mode must be an int")
    return _dumbdbm.open(file, flag, mode)


def is_available() -> bool:
    """Return True if :mod:`dbm.dumb` is available."""
    return True
