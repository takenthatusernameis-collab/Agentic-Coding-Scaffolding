import unittest
from datetime import datetime, timedelta

from duration_utils import (
    DURATION_UNITS,
    SECONDS_PER_DAY,
    SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE,
    SECONDS_PER_WEEK,
    add_duration,
    duration_between,
    format_duration,
    format_timedelta,
    hms_to_seconds,
    is_valid_duration,
    parse_duration,
    parse_timedelta,
    seconds_to_hms,
    subtract_duration,
    to_seconds,
)


class TestIsValidDuration(unittest.TestCase):
    def test_valid_durations(self):
        for duration in ["1h30m", "90s", "2.5 days", "1 week 2 days", "30m", "1h", "1d", "1w"]:
            self.assertTrue(is_valid_duration(duration))

    def test_invalid_durations(self):
        for duration in ["not a duration", "", "1x", "abc", "-5s", "1h 30"]:
            self.assertFalse(is_valid_duration(duration))

    def test_non_string_returns_false(self):
        self.assertFalse(is_valid_duration(None))  # type: ignore[arg-type]
        self.assertFalse(is_valid_duration(123))  # type: ignore[arg-type]


class TestParseDuration(unittest.TestCase):
    def test_seconds(self):
        self.assertEqual(parse_duration("90s"), 90.0)
        self.assertEqual(parse_duration("90 seconds"), 90.0)
        self.assertEqual(parse_duration("90 sec"), 90.0)
        self.assertEqual(parse_duration("90 secs"), 90.0)

    def test_minutes(self):
        self.assertEqual(parse_duration("30m"), 1800.0)
        self.assertEqual(parse_duration("30 minutes"), 1800.0)
        self.assertEqual(parse_duration("30 min"), 1800.0)
        self.assertEqual(parse_duration("30 mins"), 1800.0)

    def test_hours(self):
        self.assertEqual(parse_duration("1h"), 3600.0)
        self.assertEqual(parse_duration("1 hour"), 3600.0)
        self.assertEqual(parse_duration("1 hr"), 3600.0)
        self.assertEqual(parse_duration("1 hrs"), 3600.0)

    def test_days(self):
        self.assertEqual(parse_duration("1d"), SECONDS_PER_DAY)
        self.assertEqual(parse_duration("2 days"), 2 * SECONDS_PER_DAY)
        self.assertEqual(parse_duration("2 day"), 2 * SECONDS_PER_DAY)

    def test_weeks(self):
        self.assertEqual(parse_duration("1w"), SECONDS_PER_WEEK)
        self.assertEqual(parse_duration("2 weeks"), 2 * SECONDS_PER_WEEK)

    def test_combined(self):
        self.assertEqual(parse_duration("1h30m"), 5400.0)
        self.assertEqual(parse_duration("1h 30m"), 5400.0)
        self.assertEqual(parse_duration("1h30m15s"), 5415.0)
        self.assertEqual(parse_duration("2.5 days"), 216000.0)
        self.assertEqual(parse_duration("1 week 2 days"), 9 * SECONDS_PER_DAY)

    def test_float_value(self):
        self.assertEqual(parse_duration("1.5h"), 5400.0)

    def test_float_value_with_leading_dot(self):
        self.assertEqual(parse_duration(".5s"), 0.5)
        self.assertEqual(parse_duration(".5 seconds"), 0.5)
        self.assertEqual(parse_duration("1.5h"), 5400.0)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("")
        with self.assertRaises(ValueError):
            parse_duration("   ")

    def test_unknown_unit_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("5x")

    def test_negative_value_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("-5s")

    def test_unparseable_segment_raises(self):
        with self.assertRaises(ValueError):
            parse_duration("1h 30")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            parse_duration(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            parse_duration(None)  # type: ignore[arg-type]


class TestFormatDuration(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_duration(0), "0s")

    def test_seconds_only(self):
        self.assertEqual(format_duration(45), "45s")

    def test_minutes_and_seconds(self):
        self.assertEqual(format_duration(90), "1m 30s")

    def test_hours_and_minutes(self):
        self.assertEqual(format_duration(5400), "1h 30m")

    def test_days_and_hours(self):
        self.assertEqual(format_duration(90000), "1d 1h")

    def test_max_units(self):
        self.assertEqual(format_duration(5400, max_units=1), "1h")
        self.assertEqual(format_duration(90, max_units=1), "1m")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            format_duration("90")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            format_duration(True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            format_duration(-1)

    def test_format_duration_rejects_nan(self):
        with self.assertRaises(ValueError):
            format_duration(float("nan"))

    def test_format_duration_rejects_infinity(self):
        with self.assertRaises(ValueError):
            format_duration(float("inf"))
            format_duration(float("-inf"))

    def test_invalid_max_units(self):
        with self.assertRaises(ValueError):
            format_duration(90, max_units=0)
        with self.assertRaises(ValueError):
            format_duration(90, max_units=True)  # type: ignore[arg-type]


class TestSecondsToHms(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(seconds_to_hms(3661), (1, 1, 1))
        self.assertEqual(seconds_to_hms(90), (0, 1, 30))
        self.assertEqual(seconds_to_hms(0), (0, 0, 0))
        self.assertEqual(seconds_to_hms(3600), (1, 0, 0))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            seconds_to_hms("90")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            seconds_to_hms(True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            seconds_to_hms(-1)

    def test_seconds_to_hms_rejects_nan(self):
        with self.assertRaises(ValueError):
            seconds_to_hms(float("nan"))

    def test_seconds_to_hms_rejects_infinity(self):
        with self.assertRaises(ValueError):
            seconds_to_hms(float("inf"))
            seconds_to_hms(float("-inf"))


class TestHmsToSeconds(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(hms_to_seconds(1, 1, 1), 3661.0)
        self.assertEqual(hms_to_seconds(minutes=30), 1800.0)
        self.assertEqual(hms_to_seconds(), 0.0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            hms_to_seconds(hours="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            hms_to_seconds(hours=True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            hms_to_seconds(hours=-1)


class TestToSeconds(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(to_seconds(hours=1, minutes=30), 5400.0)
        self.assertEqual(to_seconds(milliseconds=500), 0.5)
        self.assertEqual(to_seconds(), 0.0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            to_seconds(hours="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            to_seconds(hours=True)  # type: ignore[arg-type]

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            to_seconds(hours=-1)


class TestDurationBetween(unittest.TestCase):
    def test_basic(self):
        start = datetime(2024, 1, 1, 10, 0, 0)
        end = datetime(2024, 1, 1, 11, 30, 0)
        self.assertEqual(duration_between(start, end).total_seconds(), 5400.0)

    def test_negative_duration(self):
        start = datetime(2024, 1, 1, 11, 30, 0)
        end = datetime(2024, 1, 1, 10, 0, 0)
        self.assertEqual(duration_between(start, end).total_seconds(), -5400.0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            duration_between("start", datetime(2024, 1, 1))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            duration_between(datetime(2024, 1, 1), "end")  # type: ignore[arg-type]


class TestAddDuration(unittest.TestCase):
    def test_basic(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        result = add_duration(dt, "1h30m")
        self.assertEqual(result, datetime(2024, 1, 1, 11, 30, 0))

    def test_days(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        result = add_duration(dt, "2 days")
        self.assertEqual(result, datetime(2024, 1, 3, 10, 0, 0))

    def test_type_error_on_dt(self):
        with self.assertRaises(TypeError):
            add_duration("not a datetime", "1h")  # type: ignore[arg-type]

    def test_invalid_duration_raises(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        with self.assertRaises(ValueError):
            add_duration(dt, "not a duration")


class TestSubtractDuration(unittest.TestCase):
    def test_basic(self):
        dt = datetime(2024, 1, 1, 11, 30, 0)
        self.assertEqual(subtract_duration(dt, "1h30m"), datetime(2024, 1, 1, 10, 0, 0))

    def test_days(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        self.assertEqual(subtract_duration(dt, "2 days"), datetime(2023, 12, 30, 10, 0, 0))

    def test_combined(self):
        dt = datetime(2024, 1, 1, 12, 0, 0)
        self.assertEqual(subtract_duration(dt, "1h30m15s"), datetime(2024, 1, 1, 10, 29, 45))

    def test_roundtrip(self):
        dt = datetime(2024, 6, 15, 8, 0, 0)
        self.assertEqual(add_duration(subtract_duration(dt, "3h"), "3h"), dt)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            subtract_duration("not a datetime", "1h")  # type: ignore[arg-type]

    def test_invalid_duration(self):
        dt = datetime(2024, 1, 1, 10, 0, 0)
        with self.assertRaises(ValueError):
            subtract_duration(dt, "not a duration")


class TestDurationConstants(unittest.TestCase):
    def test_second_aliases(self):
        self.assertEqual(SECONDS_PER_MINUTE, 60)
        self.assertEqual(SECONDS_PER_HOUR, 3600)
        self.assertEqual(SECONDS_PER_DAY, 86400)
        self.assertEqual(SECONDS_PER_WEEK, 604800)

    def test_duration_units_is_a_multiplication_table(self):
        self.assertIsInstance(DURATION_UNITS, dict)
        self.assertEqual(DURATION_UNITS["s"], 1)
        self.assertEqual(DURATION_UNITS["m"], SECONDS_PER_MINUTE)
        self.assertEqual(DURATION_UNITS["h"], SECONDS_PER_HOUR)
        self.assertEqual(DURATION_UNITS["d"], SECONDS_PER_DAY)
        self.assertEqual(DURATION_UNITS["w"], SECONDS_PER_WEEK)

    def test_duration_units_aliases_agree(self):
        for alias, canonical in (
            ("sec", "second"),
            ("secs", "second"),
            ("min", "minute"),
            ("mins", "minute"),
            ("hr", "hour"),
            ("hrs", "hour"),
            ("day", "day"),
            ("week", "week"),
        ):
            self.assertEqual(DURATION_UNITS[alias], DURATION_UNITS[canonical])


class TestParseTimedelta(unittest.TestCase):
    def test_parse_timedelta_seconds(self):
        self.assertEqual(parse_timedelta("90s"), timedelta(seconds=90))

    def test_parse_timedelta_minutes(self):
        self.assertEqual(parse_timedelta("30m"), timedelta(minutes=30))

    def test_parse_timedelta_hours(self):
        self.assertEqual(parse_timedelta("1h30m"), timedelta(hours=1, minutes=30))

    def test_parse_timedelta_days(self):
        self.assertEqual(parse_timedelta("2.5 days"), timedelta(days=2, seconds=43200))

    def test_parse_timedelta_weeks(self):
        self.assertEqual(parse_timedelta("1 week 2 days"), timedelta(weeks=1, days=2))

    def test_parse_timedelta_rejects_non_string(self):
        with self.assertRaises(TypeError):
            parse_timedelta(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            parse_timedelta(None)  # type: ignore[arg-type]

    def test_parse_timedelta_rejects_empty(self):
        with self.assertRaises(ValueError):
            parse_timedelta("")

    def test_parse_timedelta_rejects_invalid_unit(self):
        with self.assertRaises(ValueError):
            parse_timedelta("5x")


class TestFormatTimedelta(unittest.TestCase):
    def test_format_timedelta_zero(self):
        self.assertEqual(format_timedelta(timedelta(0)), "0s")

    def test_format_timedelta_seconds(self):
        self.assertEqual(format_timedelta(timedelta(seconds=90)), "1m 30s")

    def test_format_timedelta_minutes(self):
        self.assertEqual(format_timedelta(timedelta(minutes=90)), "1h 30m")

    def test_format_timedelta_hours(self):
        self.assertEqual(format_timedelta(timedelta(hours=1, minutes=30)), "1h 30m")

    def test_format_timedelta_days(self):
        self.assertEqual(format_timedelta(timedelta(days=2, hours=3)), "2d 3h")

    def test_format_timedelta_rejects_non_timedelta(self):
        with self.assertRaises(TypeError):
            format_timedelta(90)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            format_timedelta("90s")  # type: ignore[arg-type]

    def test_format_timedelta_matches_format_duration(self):
        td = timedelta(hours=1, minutes=30, seconds=45)
        self.assertEqual(format_timedelta(td), format_duration(td.total_seconds()))


class TestHugeIntNoOverflow(unittest.TestCase):
    """Huge integer inputs must not leak an undocumented ``OverflowError``.

    Values beyond the finite float range (e.g. ``10**400``) cannot be converted
    to a :class:`float`. Helpers that must produce a ``float`` report the
    out-of-range result as ``ValueError`` (matching the module contract); helpers
    that can represent the result exactly as integers (``seconds_to_hms``) do so.
    """

    HUGE = 10 ** 400

    def test_format_duration_huge_int_raises_value_error(self):
        with self.assertRaises(ValueError):
            format_duration(self.HUGE)

    def test_seconds_to_hms_huge_int_is_exact(self):
        hours, minutes, secs = seconds_to_hms(self.HUGE)
        self.assertEqual(hours * SECONDS_PER_HOUR + minutes * SECONDS_PER_MINUTE + secs, self.HUGE)

    def test_hms_to_seconds_huge_int_raises_value_error(self):
        with self.assertRaises(ValueError):
            hms_to_seconds(hours=self.HUGE)

    def test_to_seconds_huge_hours_raises_value_error(self):
        with self.assertRaises(ValueError):
            to_seconds(hours=self.HUGE)

    def test_to_seconds_huge_milliseconds_raises_value_error(self):
        with self.assertRaises(ValueError):
            to_seconds(milliseconds=self.HUGE)


if __name__ == "__main__":
    unittest.main()
