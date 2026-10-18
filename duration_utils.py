"""Time duration utilities for parsing, formatting, and converting durations.

This module provides helpers for working with time durations, including
parsing human-readable duration strings (e.g. ``"1h30m"``, ``"90s"``,
``"2.5 days"``), formatting seconds into a compact display, converting
between time units, and computing durations between datetimes.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Tuple, Union

__all__: list[str] = [
    "SECONDS_PER_MINUTE",
    "SECONDS_PER_HOUR",
    "SECONDS_PER_DAY",
    "SECONDS_PER_WEEK",
    "DURATION_UNITS",
    "is_valid_duration",
    "parse_duration",
    "format_duration",
    "seconds_to_hms",
    "hms_to_seconds",
    "to_seconds",
    "duration_between",
    "add_duration",
]

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600
SECONDS_PER_DAY = 86400
SECONDS_PER_WEEK = 604800

# Mapping of accepted unit suffixes to their multiplier in seconds.
DURATION_UNITS: dict[str, float] = {
    "s": 1,
    "sec": 1,
    "secs": 1,
    "second": 1,
    "seconds": 1,
    "m": 60,
    "min": 60,
    "mins": 60,
    "minute": 60,
    "minutes": 60,
    "h": 3600,
    "hr": 3600,
    "hrs": 3600,
    "hour": 3600,
    "hours": 3600,
    "d": 86400,
    "day": 86400,
    "days": 86400,
    "w": 604800,
    "week": 604800,
    "weeks": 604800,
}

# Matches a number followed by an optional unit, e.g. "1h30m", "90s", "2.5 days".
_DURATION_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)")

# Largest units first so the formatter greets the biggest applicable unit.
_ORDERED_UNITS: tuple[tuple[str, float], ...] = (
    ("week", SECONDS_PER_WEEK),
    ("day", SECONDS_PER_DAY),
    ("hour", SECONDS_PER_HOUR),
    ("minute", SECONDS_PER_MINUTE),
    ("second", 1),
)


def is_valid_duration(duration_str: str) -> bool:
    """Return ``True`` if ``duration_str`` is a parseable duration string.

    Args:
        duration_str: The duration string to validate.

    Returns:
        ``True`` if the string can be parsed by :func:`parse_duration`,
        otherwise ``False``.

    Examples:
        >>> is_valid_duration("1h30m")
        True
        >>> is_valid_duration("90s")
        True
        >>> is_valid_duration("not a duration")
        False
    """
    if not isinstance(duration_str, str):
        return False
    stripped = duration_str.strip()
    if not stripped:
        return False
    try:
        parse_duration(duration_str)
        return True
    except (TypeError, ValueError):
        return False


def parse_duration(duration_str: str) -> float:
    """Parse a human-readable duration string into total seconds.

    Args:
        duration_str: A duration string such as ``"1h30m"``, ``"90s"``,
            ``"2.5 days"``, or ``"1 week 2 days"``. Units may be abbreviated
            (``s``, ``m``, ``h``, ``d``, ``w``) or spelled out.

    Returns:
        The total duration in seconds as a float.

    Raises:
        TypeError: If ``duration_str`` is not a string.
        ValueError: If ``duration_str`` is empty or contains unparseable
            parts, or if any numeric value is negative.

    Examples:
        >>> parse_duration("1h30m")
        5400.0
        >>> parse_duration("90s")
        90.0
        >>> parse_duration("2.5 days")
        216000.0
    """
    if not isinstance(duration_str, str):
        raise TypeError("duration_str must be a string")

    stripped = duration_str.strip()
    if not stripped:
        raise ValueError("duration_str must not be empty")

    total_seconds = 0.0
    pos = 0

    for match in _DURATION_PATTERN.finditer(stripped):
        # Any non-whitespace text between matches makes the string invalid.
        gap = stripped[pos : match.start()].strip()
        if gap:
            raise ValueError(f"Unable to parse duration segment {gap!r} in {duration_str!r}")
        value = float(match.group(1))
        unit = match.group(2).lower()
        if value < 0:
            raise ValueError(f"Duration values must be non-negative, got {value!r}")
        if unit not in DURATION_UNITS:
            raise ValueError(f"Unknown duration unit {unit!r} in {duration_str!r}")
        total_seconds += value * DURATION_UNITS[unit]
        pos = match.end()

    trailing = stripped[pos:].strip()
    if trailing:
        raise ValueError(f"Unable to parse duration segment {trailing!r} in {duration_str!r}")

    if pos == 0:
        raise ValueError(f"Unable to parse duration string {duration_str!r}")

    return total_seconds


def format_duration(
    seconds: Union[int, float],
    max_units: int = 2,
) -> str:
    """Format a duration in seconds into a human-readable string.

    Args:
        seconds: The duration in seconds. Must be non-negative.
        max_units: The maximum number of time units to include in the output
            (default: 2).

    Returns:
        A human-readable duration string such as ``"1h 30m"`` or ``"90s"``.
        A duration of zero returns ``"0s"``.

    Raises:
        TypeError: If ``seconds`` is not an int or float.
        ValueError: If ``seconds`` is negative or ``max_units`` is not a
            positive integer.

    Examples:
        >>> format_duration(5400)
        '1h 30m'
        >>> format_duration(90)
        '1m 30s'
        >>> format_duration(0)
        '0s'
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise TypeError("seconds must be an int or float")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    if not isinstance(max_units, int) or isinstance(max_units, bool) or max_units < 1:
        raise ValueError("max_units must be a positive integer")

    remaining = float(seconds)
    parts: list[str] = []

    for unit_name, unit_seconds in _ORDERED_UNITS:
        if len(parts) >= max_units:
            break
        if remaining >= unit_seconds:
            count = int(remaining // unit_seconds)
            remaining -= count * unit_seconds
            parts.append(f"{count}{unit_name[0]}")

    if not parts:
        return "0s"

    return " ".join(parts)


def seconds_to_hms(seconds: Union[int, float]) -> Tuple[int, int, int]:
    """Convert a duration in seconds to ``(hours, minutes, seconds)``.

    Args:
        seconds: The duration in seconds. Must be non-negative.

    Returns:
        A tuple of ``(hours, minutes, seconds)``.

    Raises:
        TypeError: If ``seconds`` is not an int or float.
        ValueError: If ``seconds`` is negative.

    Examples:
        >>> seconds_to_hms(3661)
        (1, 1, 1)
        >>> seconds_to_hms(90)
        (0, 1, 30)
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise TypeError("seconds must be an int or float")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, SECONDS_PER_HOUR)
    minutes, secs = divmod(remainder, SECONDS_PER_MINUTE)
    return hours, minutes, secs


def hms_to_seconds(
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
) -> float:
    """Convert ``(hours, minutes, seconds)`` into total seconds.

    Args:
        hours: Number of hours (default: 0).
        minutes: Number of minutes (default: 0).
        seconds: Number of seconds (default: 0).

    Returns:
        The total duration in seconds.

    Raises:
        TypeError: If any argument is not an int.
        ValueError: If any argument is negative.

    Examples:
        >>> hms_to_seconds(1, 1, 1)
        3661.0
        >>> hms_to_seconds(minutes=30)
        1800.0
    """
    for name, value in (("hours", hours), ("minutes", minutes), ("seconds", seconds)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    return float(hours * SECONDS_PER_HOUR + minutes * SECONDS_PER_MINUTE + seconds)


def to_seconds(
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    milliseconds: int = 0,
) -> float:
    """Convert time components into total seconds.

    Args:
        hours: Number of hours (default: 0).
        minutes: Number of minutes (default: 0).
        seconds: Number of seconds (default: 0).
        milliseconds: Number of milliseconds (default: 0).

    Returns:
        The total duration in seconds as a float.

    Raises:
        TypeError: If any argument is not an int.
        ValueError: If any argument is negative.

    Examples:
        >>> to_seconds(hours=1, minutes=30)
        5400.0
        >>> to_seconds(milliseconds=500)
        0.5
    """
    for name, value in (
        ("hours", hours),
        ("minutes", minutes),
        ("seconds", seconds),
        ("milliseconds", milliseconds),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
        if value < 0:
            raise ValueError(f"{name} must be non-negative")

    return float(
        hours * SECONDS_PER_HOUR + minutes * SECONDS_PER_MINUTE + seconds + milliseconds / 1000.0
    )


def duration_between(
    start: datetime,
    end: datetime,
) -> timedelta:
    """Return the duration between two datetimes.

    Args:
        start: The start datetime.
        end: The end datetime.

    Returns:
        A :class:`~datetime.timedelta` representing ``end - start``. May be
        negative if ``end`` is before ``start``.

    Raises:
        TypeError: If either argument is not a :class:`~datetime.datetime`.

    Examples:
        >>> from datetime import datetime
        >>> start = datetime(2024, 1, 1, 10, 0, 0)
        >>> end = datetime(2024, 1, 1, 11, 30, 0)
        >>> duration_between(start, end)
        datetime.timedelta(seconds=5400)
    """
    if not isinstance(start, datetime):
        raise TypeError("start must be a datetime")
    if not isinstance(end, datetime):
        raise TypeError("end must be a datetime")

    return end - start


def add_duration(
    dt: datetime,
    duration_str: str,
) -> datetime:
    """Add a parsed duration to a datetime and return the result.

    Args:
        dt: The base datetime.
        duration_str: A duration string parseable by :func:`parse_duration`.

    Returns:
        A new :class:`~datetime.datetime` equal to ``dt + duration``.

    Raises:
        TypeError: If ``dt`` is not a datetime.
        ValueError: If ``duration_str`` cannot be parsed.

    Examples:
        >>> from datetime import datetime
        >>> dt = datetime(2024, 1, 1, 10, 0, 0)
        >>> add_duration(dt, "1h30m")
        datetime(2024, 1, 1, 11, 30)
    """
    if not isinstance(dt, datetime):
        raise TypeError("dt must be a datetime")

    seconds = parse_duration(duration_str)
    return dt + timedelta(seconds=seconds)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
