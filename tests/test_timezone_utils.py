import datetime
import unittest
from datetime import timedelta

from timezone_utils import (
    convert_datetime,
    format_datetime,
    get_all_timezones,
    get_common_timezones,
    get_local_timezone,
    get_timezone,
    get_utc_now,
    is_dst,
    is_valid_timezone,
    utc_offset,
)


class TestGetTimezone(unittest.TestCase):
    def test_known_timezone(self):
        self.assertIsNotNone(get_timezone("UTC"))
        self.assertIsNotNone(get_timezone("US/Eastern"))
        self.assertIsNotNone(get_timezone("Europe/London"))

    def test_utc_is_utc(self):
        self.assertEqual(get_timezone("UTC").key, "UTC")

    def test_unknown_timezone_returns_none(self):
        self.assertIsNone(get_timezone("Not/AZone"))
        self.assertIsNone(get_timezone(""))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            get_timezone(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_timezone(None)  # type: ignore[arg-type]


class TestIsValidTimezone(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_valid_timezone("UTC"))
        self.assertTrue(is_valid_timezone("Asia/Tokyo"))

    def test_invalid(self):
        self.assertFalse(is_valid_timezone("Not/AZone"))
        self.assertFalse(is_valid_timezone(""))

    def test_non_string(self):
        self.assertFalse(is_valid_timezone(123))
        self.assertFalse(is_valid_timezone(None))
        self.assertFalse(is_valid_timezone(True))


class TestGetUtcNow(unittest.TestCase):
    def test_returns_aware_utc(self):
        now = get_utc_now()
        self.assertIsNotNone(now.tzinfo)
        self.assertEqual(now.utcoffset(), timedelta(0))


class TestGetLocalTimezone(unittest.TestCase):
    def test_returns_zoneinfo_or_none(self):
        tz = get_local_timezone()
        # On most systems this resolves to a ZoneInfo; tolerate None.
        self.assertTrue(tz is None or isinstance(tz, type(get_timezone("UTC"))))


class TestConvertDatetime(unittest.TestCase):
    def test_utc_to_eastern(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        result = convert_datetime(dt, "US/Eastern")
        self.assertIsNotNone(result)
        self.assertEqual(result.hour, 7)  # EST is UTC-5

    def test_naive_treated_as_utc(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        result = convert_datetime(dt, "Europe/London")
        self.assertIsNotNone(result)
        self.assertEqual(result.hour, 12)  # London is UTC+0 in January

    def test_unknown_target_returns_none(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        self.assertIsNone(convert_datetime(dt, "Not/AZone"))

    def test_non_datetime_raises(self):
        with self.assertRaises(TypeError):
            convert_datetime("2024-01-15", "UTC")  # type: ignore[arg-type]

    def test_non_string_target_raises(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        with self.assertRaises(TypeError):
            convert_datetime(dt, 123)  # type: ignore[arg-type]


class TestFormatDatetime(unittest.TestCase):
    def test_formats_in_target_zone(self):
        dt = datetime.datetime(2024, 7, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        result = format_datetime(dt, "US/Eastern")
        self.assertIsNotNone(result)
        self.assertIn("2024-07-15", result)
        # EDT is UTC-4, so 12:00 UTC -> 08:00 EDT
        self.assertIn("08:00:00", result)

    def test_unknown_zone_returns_none(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        self.assertIsNone(format_datetime(dt, "Not/AZone"))

    def test_custom_format(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        result = format_datetime(dt, "UTC", fmt="%Y/%m/%d")
        self.assertEqual(result, "2024/01/15")

    def test_non_string_zone_raises(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        with self.assertRaises(TypeError):
            format_datetime(dt, 123)  # type: ignore[arg-type]

    def test_non_string_fmt_raises(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        with self.assertRaises(TypeError):
            format_datetime(dt, "UTC", fmt=123)  # type: ignore[arg-type]


class TestUtcOffset(unittest.TestCase):
    def test_utc_offset_zero(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        self.assertEqual(utc_offset(dt, "UTC"), "+00:00")

    def test_known_offset(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        # US/Eastern is UTC-5 in January (EST).
        result = utc_offset(dt, "US/Eastern")
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("-05"))

    def test_unknown_zone_returns_none(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        self.assertIsNone(utc_offset(dt, "Not/AZone"))


class TestIsDst(unittest.TestCase):
    def test_summer_dst(self):
        dt = datetime.datetime(2024, 7, 15, 12, 0, 0)
        self.assertTrue(is_dst(dt, "US/Eastern"))

    def test_winter_no_dst(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        self.assertFalse(is_dst(dt, "US/Eastern"))

    def test_utc_no_dst(self):
        dt = datetime.datetime(2024, 7, 15, 12, 0, 0)
        self.assertFalse(is_dst(dt, "UTC"))

    def test_unknown_zone_returns_none(self):
        dt = datetime.datetime(2024, 1, 15, 12, 0, 0)
        self.assertIsNone(is_dst(dt, "Not/AZone"))


class TestCommonAndAllTimezones(unittest.TestCase):
    def test_common_timezones_non_empty(self):
        zones = get_common_timezones()
        self.assertIsInstance(zones, list)
        self.assertGreater(len(zones), 0)
        self.assertIn("UTC", zones)

    def test_all_timezones_includes_common(self):
        all_zones = get_all_timezones()
        self.assertIsInstance(all_zones, list)
        self.assertGreater(len(all_zones), 0)
        self.assertIn("UTC", all_zones)
        self.assertIn("US/Eastern", all_zones)
        for zone in get_common_timezones():
            self.assertIn(zone, all_zones)


if __name__ == "__main__":
    unittest.main()
