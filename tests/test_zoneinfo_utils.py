"""Tests for zoneinfo_utils."""

import unittest

from zoneinfo import ZoneInfo

from zoneinfo_utils import zoneinfo_available_timezones, zoneinfo_get


class TestZoneinfoGet(unittest.TestCase):
    def test_get_utc(self) -> None:
        z = zoneinfo_get("UTC")
        self.assertIsInstance(z, ZoneInfo)
        self.assertEqual(z.key, "UTC")

    def test_get_valid_timezone(self) -> None:
        z = zoneinfo_get("America/New_York")
        self.assertIsInstance(z, ZoneInfo)

    def test_non_str_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            zoneinfo_get(123)  # type: ignore[arg-type]

    def test_invalid_timezone_raises(self) -> None:
        from zoneinfo import ZoneInfoNotFoundError

        with self.assertRaises(ZoneInfoNotFoundError):
            zoneinfo_get("Not/A/Real/Zone")


class TestZoneinfoAvailableTimezones(unittest.TestCase):
    def test_returns_set(self) -> None:
        tzs = zoneinfo_available_timezones()
        self.assertIsInstance(tzs, set)
        self.assertIn("UTC", tzs)
