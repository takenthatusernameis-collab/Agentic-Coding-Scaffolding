"""Tests for antigravity_utils."""

import inspect
import re
import unittest
from unittest.mock import patch

import antigravity_utils
from antigravity_utils import (
    XKCD_URL,
    fly,
    geohash,
    get_xkcd_url,
)

#: The geohash the standard library documents for its example.
DOCUMENTED_GEOHASH = "37.857713 -122.544543"

#: The bytes the standard library documents for its example.
DOCUMENTED_DATEDOW = b"2005-05-26-10458.68"


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(antigravity_utils.__all__, sorted(set(antigravity_utils.__all__)))

    def test_every_name_exists(self):
        for name in antigravity_utils.__all__:
            self.assertTrue(hasattr(antigravity_utils, name), name)

    def test_the_standard_library_module_is_not_imported(self):
        """The standard library module opens a browser when it is imported."""
        source = inspect.getsource(antigravity_utils)
        self.assertIsNone(re.search(r"^\s*import\s+antigravity\b", source, re.MULTILINE))


class TestGeohash(unittest.TestCase):
    """Verify the computation of the geohash."""

    def test_the_documented_geohash_is_computed(self):
        self.assertEqual(
            geohash(37.421542, -122.085589, DOCUMENTED_DATEDOW),
            DOCUMENTED_GEOHASH,
        )

    def test_the_geohash_holds_the_integer_parts_of_the_coordinates(self):
        result = geohash(-12, 34, DOCUMENTED_DATEDOW)
        latitude, longitude = result.split(" ")
        self.assertTrue(latitude.startswith("-12"))
        self.assertTrue(longitude.startswith("34"))

    def test_the_fractions_are_six_digits_long(self):
        result = geohash(37.421542, -122.085589, DOCUMENTED_DATEDOW)
        latitude, longitude = result.split(" ")
        self.assertEqual(len(latitude.split(".")[1]), 6)
        self.assertEqual(len(longitude.split(".")[1]), 6)

    def test_the_geohash_depends_on_the_bytes(self):
        first = geohash(37.421542, -122.085589, b"2005-05-26-10458.68")
        second = geohash(37.421542, -122.085589, b"2005-05-26-10458.69")
        self.assertNotEqual(first, second)

    def test_integers_are_accepted(self):
        self.assertEqual(
            geohash(37, -122, DOCUMENTED_DATEDOW),
            geohash(37.0, -122.0, DOCUMENTED_DATEDOW),
        )

    def test_a_latitude_that_is_not_a_number_is_rejected(self):
        with self.assertRaises(TypeError):
            geohash("37.421542", -122.085589, DOCUMENTED_DATEDOW)
        with self.assertRaises(TypeError):
            geohash(None, -122.085589, DOCUMENTED_DATEDOW)
        with self.assertRaises(TypeError):
            geohash(True, -122.085589, DOCUMENTED_DATEDOW)

    def test_a_longitude_that_is_not_a_number_is_rejected(self):
        with self.assertRaises(TypeError):
            geohash(37.421542, "-122.085589", DOCUMENTED_DATEDOW)
        with self.assertRaises(TypeError):
            geohash(37.421542, None, DOCUMENTED_DATEDOW)
        with self.assertRaises(TypeError):
            geohash(37.421542, False, DOCUMENTED_DATEDOW)

    def test_a_coordinate_that_is_not_finite_is_rejected(self):
        with self.assertRaises(ValueError):
            geohash(float("nan"), -122.085589, DOCUMENTED_DATEDOW)
        with self.assertRaises(ValueError):
            geohash(37.421542, float("inf"), DOCUMENTED_DATEDOW)
        with self.assertRaises(ValueError):
            geohash(float("-inf"), -122.085589, DOCUMENTED_DATEDOW)

    def test_bytes_that_are_not_bytes_are_rejected(self):
        with self.assertRaises(TypeError):
            geohash(37.421542, -122.085589, "2005-05-26-10458.68")
        with self.assertRaises(TypeError):
            geohash(37.421542, -122.085589, None)


class TestXkcdComic(unittest.TestCase):
    """Verify the helpers that open the comic about Python."""

    def test_the_address_of_the_comic_is_returned(self):
        self.assertEqual(get_xkcd_url(), "https://xkcd.com/353/")

    def test_the_constant_holds_the_address_of_the_comic(self):
        self.assertEqual(XKCD_URL, get_xkcd_url())

    @patch("webbrowser.open")
    def test_the_comic_is_opened_in_a_browser(self, mock_open):
        self.assertEqual(fly(), "https://xkcd.com/353/")
        mock_open.assert_called_once_with("https://xkcd.com/353/")


if __name__ == "__main__":
    unittest.main()
