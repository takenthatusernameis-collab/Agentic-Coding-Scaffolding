"""Tests for datetime_utils module."""

import unittest
from datetime import datetime

from datetime_utils import (
    add_days,
    days_between,
    format_datetime,
    get_weekday_name,
    is_leap_year,
    parse_datetime,
)


class TestParseDatetime(unittest.TestCase):
    def test_parse_default_format(self) -> None:
        result = parse_datetime("2024-03-15 10:30:00")
        self.assertEqual(result, datetime(2024, 3, 15, 10, 30, 0))

    def test_parse_custom_format(self) -> None:
        result = parse_datetime("15/03/2024", "%d/%m/%Y")
        self.assertEqual(result, datetime(2024, 3, 15))

    def test_parse_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_datetime("not-a-date")


class TestFormatDatetime(unittest.TestCase):
    def test_format_default(self) -> None:
        dt = datetime(2024, 3, 15, 10, 30, 0)
        self.assertEqual(format_datetime(dt), "2024-03-15 10:30:00")

    def test_format_custom(self) -> None:
        dt = datetime(2024, 3, 15, 10, 30, 0)
        self.assertEqual(format_datetime(dt, "%Y-%m-%d"), "2024-03-15")

    def test_format_iso(self) -> None:
        dt = datetime(2024, 3, 15, 10, 30, 0)
        self.assertEqual(format_datetime(dt, "%Y%m%dT%H%M%S"), "20240315T103000")


class TestDaysBetween(unittest.TestCase):
    def test_days_between_basic(self) -> None:
        self.assertEqual(days_between("2024-01-01", "2024-01-10"), 9)

    def test_days_between_negative(self) -> None:
        self.assertEqual(days_between("2024-01-10", "2024-01-01"), 9)

    def test_days_between_same_day(self) -> None:
        self.assertEqual(days_between("2024-01-01", "2024-01-01"), 0)

    def test_days_between_different_months(self) -> None:
        self.assertEqual(days_between("2024-02-01", "2024-03-01"), 29)

    def test_days_between_with_datetime_objects(self) -> None:
        d1 = datetime(2024, 1, 1)
        d2 = datetime(2024, 1, 10)
        self.assertEqual(days_between(d1, d2), 9)

    def test_days_between_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            days_between("not-a-date", "2024-01-01")


class TestIsLeapYear(unittest.TestCase):
    def test_leap_year_divisible_by_4(self) -> None:
        self.assertTrue(is_leap_year(2024))
        self.assertTrue(is_leap_year(2020))

    def test_leap_year_divisible_by_100_not_400(self) -> None:
        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(2100))

    def test_leap_year_divisible_by_400(self) -> None:
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2400))

    def test_non_leap_year(self) -> None:
        self.assertFalse(is_leap_year(2023))
        self.assertFalse(is_leap_year(2025))

    def test_invalid_year_raises(self) -> None:
        with self.assertRaises(ValueError):
            is_leap_year(0)
        with self.assertRaises(ValueError):
            is_leap_year(-1)


class TestAddDays(unittest.TestCase):
    def test_add_positive_days(self) -> None:
        result = add_days("2024-01-01", 10)
        self.assertEqual(result, datetime(2024, 1, 11))

    def test_add_negative_days(self) -> None:
        result = add_days("2024-01-10", -5)
        self.assertEqual(result, datetime(2024, 1, 5))

    def test_add_zero_days(self) -> None:
        result = add_days("2024-01-01", 0)
        self.assertEqual(result, datetime(2024, 1, 1))

    def test_add_with_datetime_object(self) -> None:
        dt = datetime(2024, 1, 1, 12, 0, 0)
        result = add_days(dt, 15)
        self.assertEqual(result, datetime(2024, 1, 16, 12, 0, 0))

    def test_add_crosses_month_boundary(self) -> None:
        result = add_days("2024-01-25", 10)
        self.assertEqual(result, datetime(2024, 2, 4))

    def test_add_crosses_year_boundary(self) -> None:
        result = add_days("2024-12-25", 10)
        self.assertEqual(result, datetime(2025, 1, 4))

    def test_add_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            add_days("not-a-date", 5)


class TestGetWeekdayName(unittest.TestCase):
    def test_weekday_name_monday(self) -> None:
        result = get_weekday_name("2024-03-11")
        self.assertEqual(result, "Monday")

    def test_weekday_name_friday(self) -> None:
        result = get_weekday_name("2024-03-15")
        self.assertEqual(result, "Friday")

    def test_weekday_name_with_datetime_object(self) -> None:
        dt = datetime(2024, 3, 15)
        result = get_weekday_name(dt)
        self.assertEqual(result, "Friday")

    def test_weekday_name_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            get_weekday_name("not-a-date")


if __name__ == "__main__":
    unittest.main()
