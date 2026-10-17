"""Interval utilities.

This module provides utilities for working with closed numeric intervals
of the form ``(low, high)`` where ``low <= high``. It supports
normalization, containment, overlap, intersection, union/merge, length,
and validation operations.
"""

from __future__ import annotations

from typing import Optional, Tuple

Interval = Tuple[float, float]


def _is_number(value: object) -> bool:
    """Return True if *value* is a real int or float (excluding booleans)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def normalize_interval(low: float, high: float) -> Interval:
    """Return ``(low, high)`` with ``low <= high``.

    The two endpoints are swapped when necessary so the result is always a
    valid, ordered interval.

    Args:
        low: One endpoint of the interval.
        high: The other endpoint of the interval.

    Returns:
        A tuple ``(min, max)`` representing the normalized interval.

    Raises:
        TypeError: If either endpoint is not a real number.
    """
    if not _is_number(low):
        raise TypeError(f"low must be a real number, got {type(low).__name__}")
    if not _is_number(high):
        raise TypeError(f"high must be a real number, got {type(high).__name__}")
    return (min(low, high), max(low, high))


def is_valid_interval(interval: object) -> bool:
    """Return True if *interval* is a well-formed ``(low, high)`` interval.

    A valid interval is a two-element tuple/list of real numbers with
    ``low <= high``.
    """
    if not isinstance(interval, (tuple, list)) or len(interval) != 2:
        return False
    low, high = interval
    if not _is_number(low) or not _is_number(high):
        return False
    return bool(low <= high)


def interval_contains(interval: Interval, value: float) -> bool:
    """Return True if *value* lies within the closed interval *interval*.

    Args:
        interval: A ``(low, high)`` interval.
        value: The value to test.

    Returns:
        True if ``low <= value <= high``.

    Raises:
        TypeError: If *interval* is malformed or *value* is not a real number.
        ValueError: If *interval* is not valid (``low > high``).
    """
    if not is_valid_interval(interval):
        raise ValueError(f"invalid interval: {interval!r}")
    if not _is_number(value):
        raise TypeError(f"value must be a real number, got {type(value).__name__}")
    low, high = interval
    return low <= value <= high


def interval_overlaps(a: Interval, b: Interval) -> bool:
    """Return True if intervals *a* and *b* share at least one point.

    Args:
        a: A ``(low, high)`` interval.
        b: A ``(low, high)`` interval.

    Returns:
        True if the intervals overlap (including touching at an endpoint).

    Raises:
        ValueError: If either interval is not valid.
    """
    if not is_valid_interval(a) or not is_valid_interval(b):
        raise ValueError(f"invalid interval: {a!r} or {b!r}")
    return max(a[0], b[0]) <= min(a[1], b[1])


def interval_intersection(a: Interval, b: Interval) -> Optional[Interval]:
    """Return the overlapping portion of intervals *a* and *b*.

    Args:
        a: A ``(low, high)`` interval.
        b: A ``(low, high)`` interval.

    Returns:
        The intersection interval, or ``None`` if the intervals are disjoint.

    Raises:
        ValueError: If either interval is not valid.
    """
    if not is_valid_interval(a) or not is_valid_interval(b):
        raise ValueError(f"invalid interval: {a!r} or {b!r}")
    low = max(a[0], b[0])
    high = min(a[1], b[1])
    if low > high:
        return None
    return (low, high)


def interval_union(a: Interval, b: Interval) -> Optional[Interval]:
    """Return the smallest interval covering both *a* and *b*.

    The union is only defined when the intervals overlap or touch; disjoint
    intervals return ``None``.

    Args:
        a: A ``(low, high)`` interval.
        b: A ``(low, high)`` interval.

    Returns:
        The merged interval, or ``None`` if the intervals are disjoint.

    Raises:
        ValueError: If either interval is not valid.
    """
    if not is_valid_interval(a) or not is_valid_interval(b):
        raise ValueError(f"invalid interval: {a!r} or {b!r}")
    if not interval_overlaps(a, b):
        return None
    return (min(a[0], b[0]), max(a[1], b[1]))


def merge_intervals(intervals: list[Interval]) -> list[Interval]:
    """Merge overlapping intervals into a sorted list of disjoint intervals.

    Args:
        intervals: An iterable of ``(low, high)`` intervals.

    Returns:
        A list of disjoint, sorted intervals covering the same points.

    Raises:
        TypeError: If *intervals* is not a list.
        ValueError: If any interval is not valid.
    """
    if not isinstance(intervals, list):
        raise TypeError(f"intervals must be a list, got {type(intervals).__name__}")
    for interval in intervals:
        if not is_valid_interval(interval):
            raise ValueError(f"invalid interval: {interval!r}")
    sorted_intervals = sorted(intervals, key=lambda item: (item[0], item[1]))
    merged: list[Interval] = []
    for interval in sorted_intervals:
        if merged and interval_overlaps(merged[-1], interval):
            low = merged[-1][0]
            high = max(merged[-1][1], interval[1])
            merged[-1] = (low, high)
        else:
            merged.append(interval)
    return merged


def interval_length(interval: Interval) -> float:
    """Return the length ``high - low`` of *interval*.

    Args:
        interval: A ``(low, high)`` interval.

    Returns:
        The length of the interval as a float.

    Raises:
        ValueError: If *interval* is not valid.
    """
    if not is_valid_interval(interval):
        raise ValueError(f"invalid interval: {interval!r}")
    return float(interval[1] - interval[0])
