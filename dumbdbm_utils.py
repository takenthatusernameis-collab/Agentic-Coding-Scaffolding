"""dumbdbm database utilities wrapping :mod:`dbm.dumb`."""

from __future__ import annotations

import dbm.dumb as _dumbdbm
from typing import Any


def _require_bytes(value: object, name: str = "value") -> bytes:
    """Validate that *value* is bytes."""
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes, got {type(value).__name__}")
    return bytes(value)


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


def get(db, key: bytes, default: Any = None) -> Any:
    """Get a value from a dumbdbm database with an optional default."""
    if db is None:
        raise TypeError("db must not be None")
    key = _require_bytes(key)
    try:
        return db[key]
    except KeyError:
        return default


def set(db, key: bytes, value: bytes) -> None:
    """Set a value in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    key = _require_bytes(key)
    value = _require_bytes(value)
    db[key] = value


def delete(db, key: bytes) -> None:
    """Delete a key from a dumbdbm database if present."""
    if db is None:
        raise TypeError("db must not be None")
    key = _require_bytes(key)
    try:
        del db[key]
    except KeyError:
        pass


def keys(db) -> list[bytes]:
    """Return all keys in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    return list(db.keys())


def items(db) -> list[tuple[bytes, bytes]]:
    """Return all items in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    return list(db.items())


def values(db) -> list[bytes]:
    """Return all values in a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    return list(db.values())


def clear(db) -> None:
    """Remove all items from a dumbdbm database."""
    if db is None:
        raise TypeError("db must not be None")
    for k in list(keys(db)):
        del db[k]


def update(db, other: Any = None, **kwargs) -> None:
    """Update a dumbdbm database from another mapping or kwargs."""
    if db is None:
        raise TypeError("db must not be None")
    if other is not None:
        if isinstance(other, (str, bytes, bytearray)):
            raise TypeError("other must be a mapping or an iterable of key/value pairs")
        if hasattr(other, "items"):
            for k, v in other.items():
                db[_require_bytes(k)] = _require_bytes(v)
        else:
            for k, v in other:
                db[_require_bytes(k)] = _require_bytes(v)
    for k, v in kwargs.items():
        if isinstance(k, str):
            k = k.encode()
        db[_require_bytes(k)] = _require_bytes(v)


def is_available() -> bool:
    """Return True if :mod:`dbm.dumb` is available."""
    return True
