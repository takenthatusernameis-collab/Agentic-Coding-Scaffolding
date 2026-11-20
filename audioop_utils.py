"""Audioop utility functions wrapping the standard library 'audioop' module."""

from __future__ import annotations

import audioop
import math
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

__all__: list[str] = [
    "audioop_add",
    "audioop_mul",
    "audioop_rms",
    "audioop_max",
    "audioop_minmax",
]


def _validate_fragment(fragment) -> bytes:
    if not isinstance(fragment, (bytes, bytearray)):
        raise TypeError("fragment must be bytes")
    return bytes(fragment)


def _validate_width(width: int) -> int:
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an int")
    if width not in (1, 2, 3, 4):
        raise ValueError("width must be 1, 2, 3, or 4")
    return width


def audioop_add(fragment1, fragment2, width: int) -> bytes:
    """Add two audio fragments."""
    f1 = _validate_fragment(fragment1)
    f2 = _validate_fragment(fragment2)
    w = _validate_width(width)
    return audioop.add(f1, f2, w)


def audioop_mul(fragment, width: int, factor: float) -> bytes:
    """Multiply an audio fragment by a factor."""
    f = _validate_fragment(fragment)
    w = _validate_width(width)
    if isinstance(factor, bool) or not isinstance(factor, (int, float)):
        raise TypeError("factor must be a number")
    if not math.isfinite(factor):
        raise ValueError("factor must be finite")
    return audioop.mul(f, w, factor)


def audioop_rms(fragment, width: int) -> int:
    """Return the root-mean-square of an audio fragment."""
    f = _validate_fragment(fragment)
    w = _validate_width(width)
    return audioop.rms(f, w)


def audioop_max(fragment, width: int) -> int:
    """Return the maximum absolute value of an audio fragment."""
    f = _validate_fragment(fragment)
    w = _validate_width(width)
    return audioop.max(f, w)


def audioop_minmax(fragment, width: int) -> tuple[int, int]:
    """Return the minimum and maximum values of an audio fragment."""
    f = _validate_fragment(fragment)
    w = _validate_width(width)
    return audioop.minmax(f, w)
