"""Utilities wrapping the standard library ``mmap`` module."""

from __future__ import annotations

import mmap as _mmap
import os as _os
from typing import Any, Optional

__all__ = [
    "ACCESS_READ",
    "ACCESS_WRITE",
    "ACCESS_COPY",
    "PAGESIZE",
    "ALLOCATIONGRANULARITY",
    "create_anonymous",
    "create_file_mmap",
    "access_read",
    "access_write",
    "access_copy",
    "pagesize",
    "allocation_granularity",
    "constants",
    "is_mmap",
    "write_bytes",
    "read_bytes",
    "find_bytes",
    "close_mmap",
]


def access_read() -> int:
    """Return the :mod:`mmap` read-only access flag."""
    return _mmap.ACCESS_READ


def access_write() -> int:
    """Return the :mod:`mmap` write access flag."""
    return _mmap.ACCESS_WRITE


def access_copy() -> int:
    """Return the :mod:`mmap` copy-on-write access flag."""
    return _mmap.ACCESS_COPY


def pagesize() -> int:
    """Return the memory-mapping page size in bytes."""
    return _mmap.PAGESIZE


def allocation_granularity() -> int:
    """Return the memory-mapping allocation granularity in bytes."""
    return _mmap.ALLOCATIONGRANULARITY


def constants() -> dict[str, int]:
    """Return the :mod:`mmap` constants as a dictionary."""
    return {
        "PAGESIZE": _mmap.PAGESIZE,
        "ALLOCATIONGRANULARITY": _mmap.ALLOCATIONGRANULARITY,
        "ACCESS_READ": _mmap.ACCESS_READ,
        "ACCESS_WRITE": _mmap.ACCESS_WRITE,
        "ACCESS_COPY": _mmap.ACCESS_COPY,
    }


ACCESS_READ = _mmap.ACCESS_READ
ACCESS_WRITE = _mmap.ACCESS_WRITE
ACCESS_COPY = _mmap.ACCESS_COPY
PAGESIZE = _mmap.PAGESIZE
ALLOCATIONGRANULARITY = _mmap.ALLOCATIONGRANULARITY


def create_anonymous(length: int) -> _mmap.mmap:
    """Create an anonymous, zero-initialized memory-mapped region.

    Args:
        length: Size of the region in bytes. Must be positive.

    Returns:
        An :class:`mmap.mmap` instance backed by anonymous memory.

    Raises:
        TypeError: If *length* is not an int.
        ValueError: If *length* is not positive.
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an int")
    if length <= 0:
        raise ValueError("length must be positive")
    return _mmap.mmap(-1, length)


def create_file_mmap(
    filename: str,
    length: int,
    access: int = ACCESS_WRITE,
    offset: int = 0,
) -> _mmap.mmap:
    """Create a memory-mapped file backed by *filename*.

    Args:
        filename: Path to the file to map.
        length: Size of the mapping in bytes.
        access: One of :data:`ACCESS_READ`, :data:`ACCESS_WRITE`, or
            :data:`ACCESS_COPY`. Defaults to :data:`ACCESS_WRITE`.
        offset: File offset at which to start the mapping.

    Returns:
        An :class:`mmap.mmap` instance backed by *filename*.

    Raises:
        TypeError: If arguments have invalid types.
        ValueError: If *length* is not positive or *offset* is negative.
        OSError: If the file cannot be opened or mapped.
    """
    if not isinstance(filename, str):
        raise TypeError("filename must be a str")
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an int")
    if length <= 0:
        raise ValueError("length must be positive")
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise TypeError("offset must be an int")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    fd = _os.open(filename, _os.O_RDWR | _os.O_CREAT, 0o644)
    try:
        if _os.fstat(fd).st_size < length:
            _os.ftruncate(fd, length)
        return _mmap.mmap(fd, length, access=access, offset=offset)
    except Exception:
        _os.close(fd)
        raise


def is_mmap(obj: Any) -> bool:
    """Return ``True`` if *obj* is an :class:`mmap.mmap` instance."""
    return isinstance(obj, _mmap.mmap)


def write_bytes(mmap_obj: _mmap.mmap, data: bytes, offset: int = 0) -> None:
    """Write *data* into *mmap_obj* beginning at *offset*.

    Args:
        mmap_obj: The memory-mapped region to write into.
        data: The bytes to write.
        offset: The byte offset at which to start writing.

    Raises:
        TypeError: If *mmap_obj* is not an mmap or *data* is not bytes-like.
    """
    if not isinstance(mmap_obj, _mmap.mmap):
        raise TypeError("mmap_obj must be an mmap.mmap instance")
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError("data must be bytes-like")
    mmap_obj[offset : offset + len(data)] = data


def read_bytes(mmap_obj: _mmap.mmap, length: int, offset: int = 0) -> bytes:
    """Read *length* bytes from *mmap_obj* beginning at *offset*.

    Args:
        mmap_obj: The memory-mapped region to read from.
        length: Number of bytes to read.
        offset: The byte offset at which to start reading.

    Returns:
        The bytes read from the region.

    Raises:
        TypeError: If *mmap_obj* is not an mmap.
    """
    if not isinstance(mmap_obj, _mmap.mmap):
        raise TypeError("mmap_obj must be an mmap.mmap instance")
    return bytes(mmap_obj[offset : offset + length])


def find_bytes(
    mmap_obj: _mmap.mmap,
    sub: bytes,
    start: int = 0,
    stop: Optional[int] = None,
) -> int:
    """Return the lowest index in *mmap_obj* where *sub* is found.

    Args:
        mmap_obj: The memory-mapped region to search.
        sub: The byte subsequence to find.
        start: The index at which to start the search.
        stop: The index at which to end the search (exclusive).

    Returns:
        The index of the first occurrence, or ``-1`` if not found.

    Raises:
        TypeError: If *mmap_obj* is not an mmap.
    """
    if not isinstance(mmap_obj, _mmap.mmap):
        raise TypeError("mmap_obj must be an mmap.mmap instance")
    return mmap_obj.find(sub, start, stop if stop is not None else len(mmap_obj))


def close_mmap(mmap_obj: _mmap.mmap) -> None:
    """Close *mmap_obj*, releasing the underlying memory mapping."""
    if not isinstance(mmap_obj, _mmap.mmap):
        raise TypeError("mmap_obj must be an mmap.mmap instance")
    mmap_obj.close()
