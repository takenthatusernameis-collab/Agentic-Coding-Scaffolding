"""Time utility functions for working with timestamps and durations."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Optional

__all__ = [
    "now_epoch",
    "now_iso",
    "epoch_to_iso",
    "iso_to_epoch",
    "format_duration",
    "parse_duration",
]


def now_epoch() -> int:
    """Return the current Unix timestamp in seconds."""
    return int(time.time())


def now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()


def epoch_to_iso(timestamp: int) -> str:
    """Convert a Unix timestamp to an ISO 8601 UTC string."""
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()


def iso_to_epoch(value: str) -> Optional[int]:
    """Parse an ISO 8601 string into a Unix timestamp."""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def format_duration(seconds: int) -> str:
    """Format a non-negative number of seconds as ``Hh Mm Ss``.

    >>> format_duration(0)
    '0s'
    >>> format_duration(65)
    '1m 5s'
    >>> format_duration(3661)
    '1h 1m 1s'
    """
    if isinstance(seconds, bool) or not isinstance(seconds, int):
        raise TypeError("seconds must be an int")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def parse_duration(text: str) -> int:
    """Parse a duration string like ``"1h 2m 3s"`` into total seconds.

    Components may be given in any order and any subset; missing components
    default to zero. Whitespace is ignored.

    >>> parse_duration("0s")
    0
    >>> parse_duration("1m 5s")
    65
    >>> parse_duration("1h 1m 1s")
    3661
    >>> parse_duration("2h")
    7200
    """
    if isinstance(text, bool) or not isinstance(text, str):
        raise TypeError("text must be a str")
    import re
    total = 0
    found = False
    for value, unit in re.findall(r"(\d+)\s*([hms])", text):
        found = True
        n = int(value)
        if unit == "h":
            total += n * 3600
        elif unit == "m":
            total += n * 60
        else:
            total += n
    if not found:
        raise ValueError("invalid duration string")
    return total
