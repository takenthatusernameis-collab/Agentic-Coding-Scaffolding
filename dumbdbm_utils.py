"""dumbdbm database utilities wrapping :mod:`dbm.dumb`."""

from __future__ import annotations

import dbm.dumb as _dumbdbm
import os
from typing import Any, Iterator

__all__ = [
    "dumbdbm",
    "error",
    "open",
    "open_dbm",
    "create_dbm",
    "close",
    "get",
    "set",
    "delete",
    "keys",
    "items",
    "values",
    "clear",
    "update",
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


def close(db) -> None:
    """Close a dumbdbm database if it has a close method."""
    if db is None:
        return
    close_fn = getattr(db, "close", None)
    if callable(close_fn):
        close_fn()


def get(db, key: bytes | str, default: Any = None) -> Any:
    """Get a value from a dumbdbm database with an optional default."""
    if db is None:
        raise TypeError("db must not be None")
    try:
        return db[key]
    except KeyError:
        return default


def set(db, key: bytes | str, value: bytes | str) -> None:
    """Set a value in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    db[key] = value


def delete(db, key: bytes | str) -> None:
    """Delete a key from a dumbdbm database if present."""
    if db is None:
        raise TypeError("db must not be None")
    try:
        del db[key]
    except KeyError:
        pass


def keys(db) -> list[bytes]:
    """Return all keys in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    try:
        return list(db.keys())
    except Exception:
        return []


def items(db) -> list[tuple[bytes, bytes]]:
    """Return all items in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    try:
        return list(db.items())
    except Exception:
        result = []
        for k in keys(db):
            try:
                result.append((k, db[k]))
            except Exception:
                continue
        return result


def values(db) -> list[bytes]:
    """Return all values in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    try:
        return list(db.values())
    except Exception:
        result = []
        for k in keys(db):
            try:
                result.append(db[k])
            except Exception:
                continue
        return result


def clear(db) -> None:
    """Remove all items from a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    for k in list(keys(db)):
        try:
            del db[k]
        except Exception:
            pass


def update(db, other: Any = None, **kwargs) -> None:
    """Update a dumbdbm database from another mapping or kwargs."""
    if db is None:
        raise TypeError("db must not be None")
    if other is not None:
        if hasattr(other, "items"):
            for k, v in other.items():
                db[k] = v
        else:
            for k, v in other:
                db[k] = v
    for k, v in kwargs.items():
        db[k] = v


def is_available() -> bool:
    """Return True if :mod:`dbm.dumb` is available."""
    return True
