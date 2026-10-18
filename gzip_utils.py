"""Gzip utility functions wrapping the standard library 'gzip' module."""

from __future__ import annotations

import gzip
from typing import IO

__all__: list[str] = [
    "gzip_compress",
    "gzip_decompress",
    "gzip_open",
    "gzip_write",
    "gzip_read",
]


def gzip_compress(data: bytes, compresslevel: int = 9) -> bytes:
    """Compress bytes using gzip."""
    return gzip.compress(data, compresslevel=compresslevel)


def gzip_decompress(data: bytes) -> bytes:
    """Decompress gzip-compressed bytes."""
    return gzip.decompress(data)


def gzip_open(filename: str, mode: str = "rb", compresslevel: int = 9) -> IO[bytes] | IO[str]:
    """Open a gzip file."""
    return gzip.open(filename, mode, compresslevel=compresslevel)  # type: ignore[return-value]


def gzip_write(filename: str, data: bytes, compresslevel: int = 9) -> None:
    """Write data to a gzip file."""
    with gzip.open(filename, "wb", compresslevel=compresslevel) as f:
        f.write(data)


def gzip_read(filename: str) -> bytes:
    """Read and decompress a gzip file."""
    with gzip.open(filename, "rb") as f:
        return f.read()
