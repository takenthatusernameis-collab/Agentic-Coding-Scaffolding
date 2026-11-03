"""Calendar utilities for date and month calculations using stdlib calendar."""

from __future__ import annotations

import calendar
from datetime import date
from typing import List

__all__ = [
    "add_months",
    "day_name",
    "days_between",
    "days_in_month",
    "first_day_of_month",
    "is_leap_year",
    "is_weekend",
    "month_calendar",
    "month_name",
    "weekdays_in_month",
    "weekend_days_in_month",
]


def is_leap_year(year: int) -> bool:
    if not isinstance(year, int):
        raise TypeError("year must be an int")
    return calendar.isleap(year)


def days_in_month(year: int, month: int) -> int:
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be ints")
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    return calendar.monthrange(year, month)[1]


def first_day_of_month(year: int, month: int) -> int:
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be ints")
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    return calendar.monthrange(year, month)[0]


def month_name(month: int) -> str:
    if not isinstance(month, int):
        raise TypeError("month must be an int")
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    return calendar.month_name[month]


def day_name(weekday: int) -> str:
    if not isinstance(weekday, int):
        raise TypeError("weekday must be an int")
    if weekday < 0 or weekday > 6:
        raise ValueError("weekday must be between 0 and 6")
    return calendar.day_name[weekday]


def month_calendar(year: int, month: int) -> List[List[int]]:
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be ints")
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    return calendar.monthcalendar(year, month)


def weekdays_in_month(year: int, month: int) -> int:
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be ints")
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    cal = calendar.monthcalendar(year, month)
    count = 0
    for week in cal:
        for day in week[:5]:
            if day != 0:
                count += 1
    return count


def weekend_days_in_month(year: int, month: int) -> int:
    if not isinstance(year, int) or not isinstance(month, int):
        raise TypeError("year and month must be ints")
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12")
    cal = calendar.monthcalendar(year, month)
    count = 0
    for week in cal:
        for day in week[5:]:
            if day != 0:
                count += 1
    return count


def is_weekend(d) -> bool:
    if not hasattr(d, "weekday"):
        raise TypeError("d must be a date or datetime")
    return bool(d.weekday() >= 5)


def add_months(d, months: int):
    if not hasattr(d, "year") or not hasattr(d, "month") or not hasattr(d, "day"):
        raise TypeError("d must be a date or datetime")
    if not isinstance(months, int):
        raise TypeError("months must be an int")
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def days_between(date1, date2) -> int:
    """Return the number of days from *date1* to *date2*.

    Args:
        date1: The start date (a :class:`~datetime.date` or :class:`~datetime.datetime`).
        date2: The end date (a :class:`~datetime.date` or :class:`~datetime.datetime`).

    Returns:
        The number of days between the two dates, positive when *date2* is after
        *date1*, negative when *date2* is before *date1*, and zero when they are
        the same day. Time components are ignored.

    Raises:
        TypeError: If either argument is not a date or datetime.

    Examples:
        >>> days_between(date(2024, 1, 1), date(2024, 1, 10))
        9
        >>> days_between(date(2024, 12, 31), date(2024, 1, 1))
        -365
        >>> days_between(date(2024, 3, 1), date(2024, 3, 1))
        0
    """
    for value, name in ((date1, "date1"), (date2, "date2")):
        if not (hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day")):
            raise TypeError(f"{name} must be a date or datetime")
    start = date(date1.year, date1.month, date1.day)
    end = date(date2.year, date2.month, date2.day)
    return (end - start).days
