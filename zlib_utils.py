"""Zlib utility functions wrapping the standard library 'zlib' module."""

from __future__ import annotations

import zlib as _zlib
from typing import Any

__all__: list[str] = [
    "zlib_compress",
    "zlib_decompress",
    "zlib_compressobj",
    "zlib_decompressobj",
    "zlib_crc32",
    "zlib_adler32",
]


def zlib_compress(data: bytes, level: int = -1) -> bytes:
    """Compress bytes using zlib."""
    return _zlib.compress(data, level=level)


def zlib_decompress(data: bytes) -> bytes:
    """Decompress zlib-compressed bytes."""
    return _zlib.decompress(data)


def zlib_compressobj(level: int = -1) -> Any:
    """Create a compression object."""
    return _zlib.compressobj(level=level)


def zlib_decompressobj() -> Any:
    """Create a decompression object."""
    return _zlib.decompressobj()


def zlib_crc32(data: bytes) -> int:
    """Compute the CRC-32 checksum of data."""
    return _zlib.crc32(data)


def zlib_adler32(data: bytes) -> int:
    """Compute the Adler-32 checksum of data."""
    return _zlib.adler32(data)
