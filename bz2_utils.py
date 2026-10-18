"""Bz2 utility functions wrapping the standard library 'bz2' module."""

from __future__ import annotations

import bz2
from typing import IO

__all__: list[str] = [
    "bz2_compress",
    "bz2_decompress",
    "bz2_open",
    "bz2_write",
    "bz2_read",
]


def bz2_compress(data: bytes, compresslevel: int = 9) -> bytes:
    """Compress bytes using bz2."""
    return bz2.compress(data, compresslevel=compresslevel)


def bz2_decompress(data: bytes) -> bytes:
    """Decompress bz2-compressed bytes."""
    return bz2.decompress(data)


def bz2_open(filename: str, mode: str = "rb", compresslevel: int = 9) -> IO[bytes] | IO[str]:
    """Open a bz2 file."""
    return bz2.open(filename, mode, compresslevel=compresslevel)  # type: ignore[return-value]


def bz2_write(filename: str, data: bytes, compresslevel: int = 9) -> None:
    """Write data to a bz2 file."""
    with bz2.open(filename, "wb", compresslevel=compresslevel) as f:
        f.write(data)


def bz2_read(filename: str) -> bytes:
    """Read and decompress a bz2 file."""
    with bz2.open(filename, "rb") as f:
        return f.read()
