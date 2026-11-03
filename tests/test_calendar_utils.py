import calendar
import datetime
import unittest

import calendar_utils as m


class TestDaysBetween(unittest.TestCase):
    def test_positive_span(self):
        self.assertEqual(m.days_between(datetime.date(2024, 1, 1), datetime.date(2024, 1, 10)), 9)

    def test_negative_span(self):
        self.assertEqual(m.days_between(datetime.date(2024, 12, 31), datetime.date(2024, 1, 1)), -365)  # noqa: E501

    def test_same_day(self):
        self.assertEqual(m.days_between(datetime.date(2024, 3, 1), datetime.date(2024, 3, 1)), 0)

    def test_leap_year_span(self):
        self.assertEqual(m.days_between(datetime.date(2024, 2, 1), datetime.date(2024, 3, 1)), 29)

    def test_datetime_inputs(self):
        start = datetime.datetime(2024, 1, 1, 12, 0, 0)
        end = datetime.datetime(2024, 1, 3, 8, 0, 0)
        self.assertEqual(m.days_between(start, end), 2)

    def test_type_error_date1(self):
        with self.assertRaises(TypeError):
            m.days_between("2024-01-01", datetime.date(2024, 1, 10))  # type: ignore[arg-type]

    def test_type_error_date2(self):
        with self.assertRaises(TypeError):
            m.days_between(datetime.date(2024, 1, 1), None)  # type: ignore[arg-type]


def test_is_leap_year():
    assert m.is_leap_year(2024) is True
    assert m.is_leap_year(2023) is False


def test_days_in_month():
    assert m.days_in_month(2024, 2) == 29
    assert m.days_in_month(2023, 2) == 28


def test_first_day():
    assert m.first_day_of_month(2024, 1) == calendar.monthrange(2024, 1)[0]


def test_month_name():
    assert m.month_name(1) == "January"


def test_day_name():
    assert m.day_name(0) == "Monday"


def test_weekend():
    assert m.is_weekend(datetime.date(2024, 10, 12)) is True


def test_add_months():
    assert m.add_months(datetime.date(2024, 1, 31), 1) == datetime.date(2024, 2, 29)


def test_type_errors():
    try:
        m.is_leap_year("x")
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")
