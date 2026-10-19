"""Zoneinfo timezone utilities wrapping the standard library ``zoneinfo``.

The :mod:`zoneinfo` module provides IANA timezone support. This module wraps
those primitives in a small, validated layer.
"""

from __future__ import annotations

from zoneinfo import ZoneInfo, available_timezones

__all__: list[str] = [
    "zoneinfo_get",
    "zoneinfo_available_timezones",
]


def zoneinfo_get(key: str) -> ZoneInfo:
    """Return a ``ZoneInfo`` for the given IANA key.

    Args:
        key: IANA timezone name (e.g. ``"UTC"``).

    Returns:
        A ``ZoneInfo`` instance.

    Raises:
        TypeError: If key is not a str.
        ZoneInfoNotFoundError: If key is unknown.
    """
    if not isinstance(key, str):
        raise TypeError(f"key must be str, got {type(key).__name__}")
    return ZoneInfo(key)


def zoneinfo_available_timezones() -> set[str]:
    """Return the set of available IANA timezone keys."""
    return set(available_timezones())
