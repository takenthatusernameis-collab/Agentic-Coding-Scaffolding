"""Image format detection utilities wrapping the standard library 'imghdr' module."""

from __future__ import annotations

import imghdr
import warnings
from pathlib import Path
from typing import Any, BinaryIO

__all__: list[str] = ["what", "tests"]


def what(file: str | Path | BinaryIO, h: bytes | None = None) -> str | None:
    """Return the type of image contained in a file or byte stream."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        return imghdr.what(file, h=h)


tests: list[Any] = list(imghdr.tests)
"""The list of image format test functions used by ``what``."""


def available_tests() -> list[str]:
    """Return the names of the registered image format test functions."""
    return [getattr(t, "__name__", repr(t)) for t in tests]
