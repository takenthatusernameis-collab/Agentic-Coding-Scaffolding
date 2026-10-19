"""Zlib compression and checksum utilities wrapping the standard library ``zlib``.

The :mod:`zlib` module provides DEFLATE compression and the CRC-32 and Adler-32
checksums. This module wraps those primitives in a small, validated layer: every
helper checks its arguments and raises ``TypeError`` on invalid input.
"""

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
    """
    Compress bytes using zlib DEFLATE.

    Args:
        data: Bytes to compress.
        level: Compression level (-1 default, 0 none, 9 max).

    Returns:
        The compressed bytes.

    Raises:
        TypeError: If data is not bytes.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"data must be bytes, got {type(data).__name__}")
    return _zlib.compress(bytes(data), level=level)


def zlib_decompress(data: bytes) -> bytes:
    """
    Decompress zlib-compressed bytes.

    Args:
        data: Compressed bytes.

    Returns:
        The decompressed bytes.

    Raises:
        TypeError: If data is not bytes.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"data must be bytes, got {type(data).__name__}")
    return _zlib.decompress(bytes(data))


def zlib_compressobj(level: int = -1) -> Any:
    """
    Create a compression object for streaming compression.

    Args:
        level: Compression level (-1 default, 0 none, 9 max).

    Returns:
        A ``zlib.compressobj`` instance.
    """
    return _zlib.compressobj(level=level)


def zlib_decompressobj() -> Any:
    """
    Create a decompression object for streaming decompression.

    Returns:
        A ``zlib.decompressobj`` instance.
    """
    return _zlib.decompressobj()


def zlib_crc32(data: bytes) -> int:
    """
    Compute the CRC-32 checksum of data.

    Args:
        data: Bytes to checksum.

    Returns:
        The CRC-32 checksum as an unsigned integer.

    Raises:
        TypeError: If data is not bytes.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"data must be bytes, got {type(data).__name__}")
    return _zlib.crc32(bytes(data)) & 0xFFFFFFFF


def zlib_adler32(data: bytes) -> int:
    """
    Compute the Adler-32 checksum of data.

    Args:
        data: Bytes to checksum.

    Returns:
        The Adler-32 checksum as an unsigned integer.

    Raises:
        TypeError: If data is not bytes.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"data must be bytes, got {type(data).__name__}")
    return _zlib.adler32(bytes(data)) & 0xFFFFFFFF
