"""Lzma utility functions wrapping the standard library 'lzma' module."""

from __future__ import annotations

import lzma
from typing import IO

__all__: list[str] = [
    "lzma_compress",
    "lzma_decompress",
    "lzma_open",
    "lzma_write",
    "lzma_read",
]


def lzma_compress(data: bytes, preset: int = 6) -> bytes:
    """Compress bytes using lzma."""
    if isinstance(preset, bool) or not isinstance(preset, int):
        raise TypeError("preset must be an int")
    return lzma.compress(data, preset=preset)


def lzma_decompress(data: bytes) -> bytes:
    """Decompress lzma-compressed bytes."""
    return lzma.decompress(data)


def lzma_open(filename: str, mode: str = "rb", preset: int | None = None) -> IO[bytes] | IO[str]:
    """Open an lzma file.

    Args:
        filename: Path to the file.
        mode: File mode ('rb', 'wb', etc.).
        preset: Compression preset (0-9), only used when writing.

    Returns:
        An lzma file object.
    """
    if preset is not None and "r" not in mode:
        if isinstance(preset, bool) or not isinstance(preset, int):
            raise TypeError("preset must be an int")
        return lzma.open(filename, mode, preset=preset)
    return lzma.open(filename, mode)


def lzma_write(filename: str, data: bytes, preset: int = 6) -> None:
    """Write data to an lzma file."""
    if isinstance(preset, bool) or not isinstance(preset, int):
        raise TypeError("preset must be an int")
    with lzma.open(filename, "wb", preset=preset) as f:
        f.write(data)


def lzma_read(filename: str) -> bytes:
    """Read and decompress an lzma file."""
    with lzma.open(filename, "rb") as f:
        return f.read()
