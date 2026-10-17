"""Bisect utility functions for binary search on sorted sequences."""

from __future__ import annotations

import bisect
from typing import Any, Sequence

__all__: list[str] = [
    "bisect_left",
    "bisect_right",
    "insort_left",
    "insort_right",
    "find_leftmost",
    "find_rightmost",
]


def bisect_left(a: Sequence[Any], x: Any, lo: int = 0, hi: int | None = None) -> int:
    return bisect.bisect_left(a, x, lo, len(a) if hi is None else hi)


def bisect_right(a: Sequence[Any], x: Any, lo: int = 0, hi: int | None = None) -> int:
    return bisect.bisect_right(a, x, lo, len(a) if hi is None else hi)


def insort_left(a: list[Any], x: Any, lo: int = 0, hi: int | None = None) -> None:
    bisect.insort_left(a, x, lo, len(a) if hi is None else hi)


def insort_right(a: list[Any], x: Any, lo: int = 0, hi: int | None = None) -> None:
    bisect.insort_right(a, x, lo, len(a) if hi is None else hi)


def find_leftmost(a: Sequence[Any], x: Any) -> int | None:
    i = bisect.bisect_left(a, x)
    if i < len(a) and a[i] == x:
        return i
    return None


def find_rightmost(a: Sequence[Any], x: Any) -> int | None:
    i = bisect.bisect_right(a, x) - 1
    if i >= 0 and a[i] == x:
        return i
    return None
