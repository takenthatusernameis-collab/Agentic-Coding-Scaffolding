"""Database utilities wrapping the standard library ``dbm``.

The :mod:`dbm` module provides a dictionary-like interface to simple
database files, selecting the best available backend (``dbm.ndbm``,
``dbm.gnu``, or ``dbm.dumb``). This module wraps that interface in a
small, validated layer: every helper checks its arguments and raises
``TypeError`` on invalid input. Keys and values are bytes, matching the
:mod:`dbm` contract.
"""

from __future__ import annotations

import dbm as _dbm
from pathlib import Path
from typing import Any, List, Literal, Optional, Union, cast

__all__ = [
    "dbm_error",
    "delete_record",
    "has_key",
    "is_valid_flag",
    "list_keys",
    "open_database",
    "read_record",
    "sync_database",
    "write_record",
    "which_database",
]

ValidFlag = Literal["r", "w", "c", "n"]

Database = Any

# The exception class raised by :mod:`dbm` operations.
dbm_error = _dbm.error


def is_valid_flag(flag: object) -> bool:
    """Return ``True`` when *flag* is a valid :mod:`dbm` open mode."""
    return flag in ("r", "w", "c", "n")


def _require_path(value: object, name: str = "file") -> Union[str, Path]:
    if not isinstance(value, (str, Path)):
        raise TypeError(f"{name} must be a str or Path, got {type(value).__name__}")
    return value


def _require_flag(flag: str) -> str:
    if not is_valid_flag(flag):
        raise TypeError(f"flag must be one of 'r','w','c','n', got {flag!r}")
    return flag


def _require_bytes(value: object, name: str = "value") -> bytes:
    if not isinstance(value, (bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be bytes, got {type(value).__name__}")
    return bytes(value)


def open_database(
    file: Union[str, Path],
    flag: ValidFlag = "c",
    mode: int = 0o644,
) -> Database:
    """
    Open a dbm database at *file*.

    Args:
        file: Path to the database file.
        flag: Open mode ('r' read-only, 'w' read-write, 'c' create if
            missing, 'n' always create a new empty database).
        mode: File permissions used when creating a new database.

    Returns:
        An open database object supporting mapping-style access.

    Raises:
        TypeError: If *file* is not a str or Path, or *flag* is invalid.
        dbm.error: If the database cannot be opened.
    """
    path = _require_path(file)
    _require_flag(flag)
    return _dbm.open(str(path), flag=flag, mode=mode)


def close(database: Database) -> None:
    """
    Close an open database.

    Args:
        database: An open database object.

    Raises:
        AttributeError: If *database* lacks a close method.
    """
    if not hasattr(database, "close"):
        raise AttributeError("database must have a 'close' method")
    database.close()


def which_database(file: Union[str, Path]) -> Optional[str]:
    """
    Guess which dbm backend module should be used for *file*.

    Args:
        file: Path to the database file.

    Returns:
        The backend module name (e.g. ``"dbm.ndbm"``), an empty string
        when the file format cannot be determined, or ``None`` when the
        file does not exist.
    """
    path = _require_path(file)
    result = _dbm.whichdb(str(path))
    if result is None or result == "":
        return None if not Path(path).exists() else ""
    return result


def available_backends() -> List[str]:
    """Return the dbm backend modules available on this platform."""
    backends: List[str] = []
    for name in ("dbm.ndbm", "dbm.gnu", "dbm.dumb"):
        try:
            __import__(name)
        except ImportError:
            continue
        backends.append(name)
    return backends


def read_record(database: Database, key: bytes) -> Optional[bytes]:
    """
    Read the value stored under *key*.

    Args:
        database: An open database object.
        key: Key to look up (bytes).

    Returns:
        The stored value, or ``None`` when the key is absent.

    Raises:
        TypeError: If *key* is not bytes.
    """
    key = _require_bytes(key)
    if key in database:
        return cast(Optional[bytes], database[key])
    return None


def write_record(database: Database, key: bytes, value: bytes) -> None:
    """
    Store *value* under *key* in the database.

    Args:
        database: An open database object.
        key: Key to store under (bytes).
        value: Value to store (bytes).

    Raises:
        TypeError: If *key* or *value* is not bytes.
    """
    key = _require_bytes(key)
    value = _require_bytes(value)
    database[key] = value


def delete_record(database: Database, key: bytes) -> None:
    """
    Remove *key* from the database.

    Args:
        database: An open database object.
        key: Key to delete (bytes).

    Raises:
        TypeError: If *key* is not bytes.
        KeyError: If *key* is not present.
    """
    key = _require_bytes(key)
    if key not in database:
        raise KeyError(key)
    del database[key]


def has_key(database: Database, key: bytes) -> bool:
    """Return ``True`` when *key* is present in the database."""
    key = _require_bytes(key)
    return key in database


def list_keys(database: Database) -> List[bytes]:
    """Return all keys stored in the database."""
    return [key for key in database.keys()]


def sync_database(database: Database) -> None:
    """
    Write any pending changes to disk.

    Args:
        database: An open database object.

    Raises:
        AttributeError: If *database* lacks a sync method.
    """
    if not hasattr(database, "sync"):
        raise AttributeError("database must have a 'sync' method")
    database.sync()
