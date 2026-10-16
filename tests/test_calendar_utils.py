import calendar
import datetime

import calendar_utils as m


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
