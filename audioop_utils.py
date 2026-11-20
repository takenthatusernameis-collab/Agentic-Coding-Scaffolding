"""Audioop utility functions wrapping the standard library 'audioop' module."""

from __future__ import annotations

import audioop
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

__all__: list[str] = [
    "audioop_add",
    "audioop_mul",
    "audioop_rms",
    "audioop_max",
    "audioop_minmax",
]


def audioop_add(fragment1: bytes, fragment2: bytes, width: int) -> bytes:
    """Add two audio fragments."""
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    return audioop.add(fragment1, fragment2, width)


def audioop_mul(fragment: bytes, width: int, factor: float) -> bytes:
    """Multiply an audio fragment by a factor."""
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    if isinstance(factor, bool) or not isinstance(factor, (int, float)):
        raise TypeError("factor must be a number")
    return audioop.mul(fragment, width, factor)


def audioop_rms(fragment: bytes, width: int) -> int:
    """Return the root-mean-square of an audio fragment."""
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    return audioop.rms(fragment, width)


def audioop_max(fragment: bytes, width: int) -> int:
    """Return the maximum absolute value of an audio fragment."""
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    return audioop.max(fragment, width)


def audioop_minmax(fragment: bytes, width: int) -> tuple[int, int]:
    """Return the minimum and maximum values of an audio fragment."""
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    return audioop.minmax(fragment, width)
