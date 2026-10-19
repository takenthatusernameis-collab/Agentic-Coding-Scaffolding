import shelve
from typing import Any, Literal, Optional


def open_shelf(
    filename: str,
    flag: Literal["r", "w", "c", "n"] = "c",
    protocol: Optional[int] = None,
    writeback: bool = False,
) -> shelve.Shelf:
    """
    Open a persistent shelf at the given filename.

    Args:
        filename: Path to the shelf database file.
        flag: Open mode ('r', 'w', 'c', 'n').
        protocol: Pickle protocol version (default None = highest available).
        writeback: Enable writeback caching.

    Returns:
        A shelve.Shelf instance (context manager).

    Raises:
        TypeError: If filename is not a str.
        ValueError: If flag is invalid.
    """
    if not isinstance(filename, str):
        raise TypeError(f"filename must be str, got {type(filename).__name__}")
    if flag not in ("r", "w", "c", "n"):
        raise ValueError(f"flag must be one of 'r','w','c','n', got {flag!r}")
    if protocol is not None:
        return shelve.open(filename, flag=flag, protocol=protocol, writeback=writeback)
    return shelve.open(filename, flag=flag, writeback=writeback)


def close(shelf: Any) -> None:
    """
    Close a shelf.

    Args:
        shelf: A shelve.Shelf instance.

    Raises:
        AttributeError: If shelf lacks a close method.
    """
    if not hasattr(shelf, "close"):
        raise AttributeError("shelf must have a 'close' method")
    shelf.close()


def sync(shelf: Any) -> None:
    """
    Write back any pending changes to a shelf with writeback enabled.

    Args:
        shelf: A shelve.Shelf instance.

    Raises:
        AttributeError: If shelf lacks a sync method.
    """
    if not hasattr(shelf, "sync"):
        raise AttributeError("shelf must have a 'sync' method")
    shelf.sync()


def keys(shelf: Any):
    """Return the keys of a shelf."""
    return list(shelf.keys())


def get(shelf: Any, key: str, default: Any = None) -> Any:
    """
    Get a value from a shelf with a default fallback.

    Args:
        shelf: A shelve.Shelf instance.
        key: Key to look up.
        default: Value returned if key is missing.

    Returns:
        The stored value or default.
    """
    if not isinstance(key, str):
        raise TypeError(f"key must be str, got {type(key).__name__}")
    if hasattr(shelf, "get"):
        return shelf.get(key, default)
    if key in shelf:
        return shelf[key]
    return default


def set_value(shelf: Any, key: str, value: Any) -> None:
    """
    Set a value in a shelf.

    Args:
        shelf: A shelve.Shelf instance.
        key: Key to store under.
        value: Value to store.
    """
    if not isinstance(key, str):
        raise TypeError(f"key must be str, got {type(key).__name__}")
    shelf[key] = value


def delete(shelf: Any, key: str) -> None:
    """
    Delete a key from a shelf.

    Args:
        shelf: A shelve.Shelf instance.
        key: Key to delete.

    Raises:
        KeyError: If key is not present.
    """
    if not isinstance(key, str):
        raise TypeError(f"key must be str, got {type(key).__name__}")
    if key not in shelf:
        raise KeyError(key)
    del shelf[key]


def contains(shelf: Any, key: str) -> bool:
    """Return True if key is in shelf."""
    if not isinstance(key, str):
        raise TypeError(f"key must be str, got {type(key).__name__}")
    return key in shelf


def is_shelf(obj: Any) -> bool:
    """Return True if obj is a shelve.Shelf instance."""
    return isinstance(obj, shelve.Shelf)
