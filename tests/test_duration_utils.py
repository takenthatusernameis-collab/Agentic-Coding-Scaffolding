import unittest
from datetime import datetime

from duration_utils import (
    SECONDS_PER_DAY,
    SECONDS_PER_WEEK,
    add_duration,
    duration_between,
    format_duration,
    hms_to_seconds,
    is_valid_duration,
    parse_duration,
    seconds_to_hms,
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


if __name__ == "__main__":
    unittest.main()
