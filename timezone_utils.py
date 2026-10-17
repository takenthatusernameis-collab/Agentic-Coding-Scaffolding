"""Timezone utilities.

This module provides utilities for working with time zones using the
standard library :mod:`zoneinfo` module. It supports looking up time zones
by IANA name, validating time zone identifiers, converting datetimes between
time zones, formatting datetimes for a time zone, and inspecting UTC offsets
and daylight saving time status.
"""

from __future__ import annotations

import datetime as _dt
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones

# A curated list of commonly used IANA time zone identifiers.
_COMMON_TIMEZONES: tuple[str, ...] = (
    "UTC",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
    "US/Eastern",
    "US/Central",
    "US/Mountain",
    "US/Pacific",
    "Asia/Tokyo",
    "Asia/Shanghai",
    "Asia/Kolkata",
    "Australia/Sydney",
    "America/Sao_Paulo",
    "America/Los_Angeles",
    "America/New_York",
)


def _format_offset(offset: _dt.timedelta) -> str:
    """Format a :class:`datetime.timedelta` as an ISO-style ``[±]HH:MM`` string."""
    total_seconds = int(offset.total_seconds())
    sign = "-" if total_seconds < 0 else "+"
    total_seconds = abs(total_seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{sign}{hours:02d}:{minutes:02d}"


def get_timezone(name: str) -> Optional[ZoneInfo]:
    """Return the :class:`zoneinfo.ZoneInfo` for *name*, or ``None`` if unknown.

    Args:
        name: An IANA time zone identifier (e.g. ``"UTC"``, ``"US/Eastern"``).

    Returns:
        A :class:`zoneinfo.ZoneInfo` instance, or ``None`` if *name* is not a
        known time zone.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a string, got {type(name).__name__}")
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return None


def is_valid_timezone(name: object) -> bool:
    """Return True if *name* is a known IANA time zone identifier.

    Args:
        name: The value to validate.

    Returns:
        True if *name* is a string identifying a known time zone.
    """
    if not isinstance(name, str):
        return False
    return get_timezone(name) is not None


def get_utc_now() -> _dt.datetime:
    """Return the current UTC date and time as a timezone-aware datetime."""
    return _dt.datetime.now(_dt.timezone.utc)


def get_local_timezone() -> Optional[ZoneInfo]:
    """Return the system's local time zone, or ``None`` if it cannot be determined."""
    local = _dt.datetime.now().astimezone()
    tz = local.tzinfo
    return tz if isinstance(tz, ZoneInfo) else None


def convert_datetime(dt: _dt.datetime, target: str) -> Optional[_dt.datetime]:
    """Convert *dt* to the *target* time zone.

    Naive datetimes are interpreted as UTC. Returns ``None`` if *target* is
    not a known time zone.

    Args:
        dt: A :class:`datetime.datetime` (naive or aware).
        target: An IANA time zone identifier to convert to.

    Returns:
        The converted, timezone-aware datetime, or ``None`` if *target* is
        unknown.

    Raises:
        TypeError: If *dt* is not a :class:`datetime.datetime` or *target* is
            not a string.
    """
    if not isinstance(dt, _dt.datetime):
        raise TypeError(f"dt must be a datetime, got {type(dt).__name__}")
    if not isinstance(target, str):
        raise TypeError(f"target must be a string, got {type(target).__name__}")
    tz = get_timezone(target)
    if tz is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_dt.timezone.utc)
    return dt.astimezone(tz)


def format_datetime(
    dt: _dt.datetime,
    tz_name: str,
    fmt: str = "%Y-%m-%d %H:%M:%S %Z",
) -> Optional[str]:
    """Format *dt* for the *tz_name* time zone using *fmt*.

    Returns ``None`` if *tz_name* is not a known time zone.

    Args:
        dt: A :class:`datetime.datetime` (naive or aware).
        tz_name: An IANA time zone identifier.
        fmt: A :meth:`datetime.datetime.strftime` format string.

    Returns:
        The formatted datetime string, or ``None`` if *tz_name* is unknown.

    Raises:
        TypeError: If *dt* is not a :class:`datetime.datetime` or *tz_name*
            / *fmt* is not a string.
    """
    if not isinstance(tz_name, str):
        raise TypeError(f"tz_name must be a string, got {type(tz_name).__name__}")
    if not isinstance(fmt, str):
        raise TypeError(f"fmt must be a string, got {type(fmt).__name__}")
    converted = convert_datetime(dt, tz_name)
    if converted is None:
        return None
    return converted.strftime(fmt)


def utc_offset(dt: _dt.datetime, tz_name: str) -> Optional[str]:
    """Return the UTC offset of *dt* in *tz_name* as a string (e.g. ``"+01:00"``).

    Returns ``None`` if *tz_name* is not a known time zone.

    Args:
        dt: A :class:`datetime.datetime` (naive or aware).
        tz_name: An IANA time zone identifier.

    Returns:
        The UTC offset string, or ``None`` if *tz_name* is unknown.

    Raises:
        TypeError: If *dt* is not a :class:`datetime.datetime` or *tz_name* is
            not a string.
    """
    if not isinstance(tz_name, str):
        raise TypeError(f"tz_name must be a string, got {type(tz_name).__name__}")
    converted = convert_datetime(dt, tz_name)
    if converted is None:
        return None
    offset = converted.utcoffset()
    return _format_offset(offset) if offset is not None else None


def is_dst(dt: _dt.datetime, tz_name: str) -> Optional[bool]:
    """Return True if daylight saving time is in effect for *dt* in *tz_name*.

    Returns ``None`` if *tz_name* is not a known time zone.

    Args:
        dt: A :class:`datetime.datetime` (naive or aware).
        tz_name: An IANA time zone identifier.

    Returns:
        True if DST is in effect, False otherwise, or ``None`` if *tz_name*
        is unknown.

    Raises:
        TypeError: If *dt* is not a :class:`datetime.datetime` or *tz_name* is
            not a string.
    """
    if not isinstance(tz_name, str):
        raise TypeError(f"tz_name must be a string, got {type(tz_name).__name__}")
    converted = convert_datetime(dt, tz_name)
    if converted is None:
        return None
    return bool(converted.dst() != _dt.timedelta(0))


def get_common_timezones() -> list[str]:
    """Return a curated list of commonly used IANA time zone identifiers."""
    return list(_COMMON_TIMEZONES)


def get_all_timezones() -> list[str]:
    """Return all known IANA time zone identifiers, sorted alphabetically."""
    return sorted(available_timezones())
