"""Plistlib utility functions wrapping the standard library 'plistlib' module."""

from __future__ import annotations

import plistlib
from typing import Any, BinaryIO


def plist_load(fp: BinaryIO) -> Any:
    """Load a plist from a binary file object."""
    return plistlib.load(fp)


def plist_loads(data: bytes) -> Any:
    """Load a plist from bytes."""
    return plistlib.loads(data)


def plist_dump(obj: Any, fp: BinaryIO) -> None:
    """Write an object as a plist to a binary file object."""
    plistlib.dump(obj, fp)


def plist_dumps(obj: Any) -> bytes:
    """Serialize an object to plist bytes."""
    return plistlib.dumps(obj)


__all__ = ["plist_load", "plist_loads", "plist_dump", "plist_dumps"]
