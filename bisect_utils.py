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
    "is_sorted",
]


def _require_sequence(a: object, name: str = "a") -> Sequence[Any]:
    if not isinstance(a, Sequence):
        raise TypeError(f"{name} must be a sequence")
    return a


def _require_list(a: object, name: str = "a") -> list[Any]:
    if not isinstance(a, list):
        raise TypeError(f"{name} must be a list")
    return a


def _normalize_hi(a: Sequence[Any], hi: int | None) -> int:
    if hi is None:
        return len(a)
    if isinstance(hi, bool) or not isinstance(hi, int):
        raise TypeError("hi must be an int or None")
    return hi


def _normalize_lo(lo: int) -> int:
    if isinstance(lo, bool) or not isinstance(lo, int):
        raise TypeError("lo must be an int")
    return lo


def bisect_left(a: Sequence[Any], x: Any, lo: int = 0, hi: int | None = None) -> int:
    """Return the leftmost insertion point for *x* in sorted sequence *a*.

    Args:
        a: A sorted sequence.
        x: The value to locate.
        lo: Lower bound of the slice to search (default 0).
        hi: Upper bound of the slice to search (default ``len(a)``).

    Returns:
        int: Insertion index.
    """
    _require_sequence(a)
    lo = _normalize_lo(lo)
    hi = _normalize_hi(a, hi)
    return bisect.bisect_left(a, x, lo, hi)


def bisect_right(a: Sequence[Any], x: Any, lo: int = 0, hi: int | None = None) -> int:
    """Return the rightmost insertion point for *x* in sorted sequence *a*.

    Args:
        a: A sorted sequence.
        x: The value to locate.
        lo: Lower bound of the slice to search (default 0).
        hi: Upper bound of the slice to search (default ``len(a)``).

    Returns:
        int: Insertion index.
    """
    _require_sequence(a)
    lo = _normalize_lo(lo)
    hi = _normalize_hi(a, hi)
    return bisect.bisect_right(a, x, lo, hi)


def insort_left(a: list[Any], x: Any, lo: int = 0, hi: int | None = None) -> None:
    """Insert *x* into sorted list *a* in place, keeping existing entries left.

    Args:
        a: A sorted list to mutate.
        x: The value to insert.
        lo: Lower bound of the slice (default 0).
        hi: Upper bound of the slice (default ``len(a)``).
    """
    _require_list(a)
    lo = _normalize_lo(lo)
    hi = _normalize_hi(a, hi)
    bisect.insort_left(a, x, lo, hi)


def insort_right(a: list[Any], x: Any, lo: int = 0, hi: int | None = None) -> None:
    """Insert *x* into sorted list *a* in place, keeping existing entries right.

    Args:
        a: A sorted list to mutate.
        x: The value to insert.
        lo: Lower bound of the slice (default 0).
        hi: Upper bound of the slice (default ``len(a)``).
    """
    _require_list(a)
    lo = _normalize_lo(lo)
    hi = _normalize_hi(a, hi)
    bisect.insort_right(a, x, lo, hi)


def find_leftmost(a: Sequence[Any], x: Any) -> int | None:
    """Return the index of the first occurrence of *x* in sorted *a*, or None.

    Args:
        a: A sorted sequence.
        x: The value to find.

    Returns:
        int | None: Index of the leftmost match, or ``None`` if absent.
    """
    _require_sequence(a)
    i = bisect.bisect_left(a, x)
    if i < len(a) and a[i] == x:
        return i
    return None


def find_rightmost(a: Sequence[Any], x: Any) -> int | None:
    """Return the index of the last occurrence of *x* in sorted *a*, or None.

    Args:
        a: A sorted sequence.
        x: The value to find.

    Returns:
        int | None: Index of the rightmost match, or ``None`` if absent.
    """
    _require_sequence(a)
    i = bisect.bisect_right(a, x) - 1
    if i >= 0 and a[i] == x:
        return i
    return None


def is_sorted(a: Sequence[Any], *, reverse: bool = False) -> bool:
    """Return True if *a* is sorted in non-decreasing (or non-increasing) order.

    Args:
        a: A sequence to inspect.
        reverse: If True, check non-increasing order.

    Returns:
        bool: True when *a* is sorted.
    """
    _require_sequence(a)
    if reverse:
        return all(a[i] >= a[i + 1] for i in range(len(a) - 1))
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))
