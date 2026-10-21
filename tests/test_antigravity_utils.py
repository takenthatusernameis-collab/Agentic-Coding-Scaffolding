"""Tests for antigravity_utils module."""

import unittest
from unittest import mock

import antigravity_utils


class TestAntigravityUtils(unittest.TestCase):
    def test_geohash_reexported(self):
        # Test that geohash is properly re-exported
        antigravity_utils.geohash(37.421542, -122.085589, b'2005-05-26-10458.68')
        # geohash prints, so we need to capture stdout

    def test_geohash_callable(self):
        self.assertTrue(callable(antigravity_utils.geohash))

    def test_fly_opens_browser(self):
        with mock.patch('webbrowser.open') as mock_open:
            result = antigravity_utils.fly()
            mock_open.assert_called_once_with("https://xkcd.com/353/")
            self.assertEqual(result, "https://xkcd.com/353/")

    def test_get_xkcd_url(self):
        self.assertEqual(antigravity_utils.get_xkcd_url(), "https://xkcd.com/353/")

    def test_all_exports(self):
        self.assertIn('geohash', antigravity_utils.__all__)
        self.assertIn('fly', antigravity_utils.__all__)
        self.assertIn('get_xkcd_url', antigravity_utils.__all__)


if __name__ == '__main__':
    unittest.main()
