"""Date and time utility functions."""

from datetime import datetime, timedelta
from typing import Union

DateTimeLike = Union[str, datetime]
__all__ = [
    "add_days",
    "add_hours",
    "add_weeks",
    "days_between",
    "format_datetime",
    "get_weekday_name",
    "is_leap_year",
    "parse_datetime",
]


def parse_datetime(value: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse a string into a datetime object.

    Args:
        value: The string to parse.
        fmt: The expected format string. Defaults to ``%Y-%m-%d %H:%M:%S``.

    Returns:
        The parsed datetime object.

    Raises:
        ValueError: If the string does not match the format.
    """
    return datetime.strptime(value, fmt)


def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string.

    Args:
        dt: The datetime to format.
        fmt: The desired format string. Defaults to ``%Y-%m-%d %H:%M:%S``.

    Returns:
        The formatted string.
    """
    return dt.strftime(fmt)


def days_between(start: DateTimeLike, end: DateTimeLike) -> int:
    """Return the absolute number of whole days between two dates.

    Args:
        start: A datetime or parseable string (format ``%Y-%m-%d``).
        end: A datetime or parseable string (format ``%Y-%m-%d``).

    Returns:
        The absolute difference in days.

    Raises:
        ValueError: If a string argument cannot be parsed.
    """
    start_dt = _coerce_datetime(start, "%Y-%m-%d")
    end_dt = _coerce_datetime(end, "%Y-%m-%d")
    delta = end_dt - start_dt
    return abs(delta.days)


def is_leap_year(year: int) -> bool:
    """Return True if *year* is a leap year.

    Args:
        year: The year to check.

    Returns:
        True if the year is a leap year, False otherwise.

    Raises:
        ValueError: If year is less than 1.
    """
    if year < 1:
        raise ValueError("Year must be a positive integer.")
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def add_days(dt: DateTimeLike, days: int) -> datetime:
    """Add (or subtract, if negative) a number of days to a datetime.

    Args:
        dt: A datetime or a string parseable with ``%Y-%m-%d``/``%Y-%m-%d %H:%M:%S``.
        days: The number of days to add. May be negative.

    Returns:
        A new datetime shifted by the given number of days.

    Raises:
        ValueError: If a string argument cannot be parsed.
    """
    dt_val = _coerce_datetime(dt, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S")
    return dt_val + timedelta(days=days)


def add_hours(dt: DateTimeLike, hours: int) -> datetime:
    """Add (or subtract, if negative) a number of hours to a datetime.

    A companion to :func:`add_days` that shifts *dt* forward by *hours*
    hours (or backward when *hours* is negative).

    Args:
        dt: A datetime or a string parseable with ``%Y-%m-%d`` or
            ``%Y-%m-%d %H:%M:%S``.
        hours: The number of hours to add. May be negative.

    Returns:
        A new datetime shifted by the given number of hours.

    Raises:
        TypeError: If *hours* is not an int.
        ValueError: If a string argument cannot be parsed.

    Examples:
        >>> add_hours("2024-01-01", 1)
        datetime.datetime(2024, 1, 1, 1, 0)
        >>> add_hours("2024-01-01", 0)
        datetime.datetime(2024, 1, 1, 0, 0)
        >>> add_hours("2024-01-01", -1)
        datetime.datetime(2023, 12, 31, 23, 0)
    """
    if isinstance(hours, bool) or not isinstance(hours, int):
        raise TypeError("hours must be an int")
    dt_val = _coerce_datetime(dt, "%Y-%m-%d", "%Y-%m-%d %H:%M:%S")
    return dt_val + timedelta(hours=hours)


def add_weeks(dt: DateTimeLike, weeks: int) -> datetime:
    """Add (or subtract, if negative) a number of weeks to a datetime.

    A companion to :func:`add_days` that shifts *dt* forward by *weeks*
    weeks (or backward when *weeks* is negative).

    Args:
        dt: A datetime or a string parseable with ``%Y-%m-%d`` or
            ``%Y-%m-%d %H:%M:%S``.
        weeks: The number of weeks to add. May be negative.

    Returns:
        A new datetime shifted by the given number of weeks.

    Raises:
        TypeError: If *weeks* is not an int.
        ValueError: If a string argument cannot be parsed.

    Examples:
        >>> add_weeks("2024-01-01", 1)
        datetime.datetime(2024, 1, 8, 0, 0)
        >>> add_weeks("2024-01-01", 0)
        datetime.datetime(2024, 1, 1, 0, 0)
        >>> add_weeks("2024-01-01", -1)
        datetime.datetime(2023, 12, 25, 0, 0)
    """
    if isinstance(weeks, bool) or not isinstance(weeks, int):
        raise TypeError("weeks must be an int")
    return add_days(dt, weeks * 7)


def get_weekday_name(dt: DateTimeLike) -> str:
    """Return the full weekday name for a given date.

    Args:
        dt: A datetime or a string parseable with ``%Y-%m-%d``.

    Returns:
        The weekday name (e.g. ``Monday``).

    Raises:
        ValueError: If a string argument cannot be parsed.
    """
    dt_val = _coerce_datetime(dt, "%Y-%m-%d")
    return dt_val.strftime("%A")


def _coerce_datetime(value: DateTimeLike, *formats: str) -> datetime:
    """Coerce a value into a datetime, trying multiple formats if needed.

    Args:
        value: A datetime (returned as-is) or a string to parse.
        *formats: Format strings to try when parsing.

    Returns:
        The resulting datetime.

    Raises:
        ValueError: If value is a string that matches none of the formats.
    """
    if isinstance(value, datetime):
        return value
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Could not parse '{value}'. Expected formats: {list(formats)}")
