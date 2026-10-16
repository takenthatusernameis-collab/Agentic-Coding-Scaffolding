"""Tests for version_utils module."""

import unittest

from version_utils import compare_versions, is_greater, normalize_version, parse_version


class TestParseVersion(unittest.TestCase):
    def test_simple(self) -> None:
        self.assertEqual(parse_version("1.2.3"), (1, 2, 3))

    def test_two_components(self) -> None:
        self.assertEqual(parse_version("1.0"), (1, 0))

    def test_invalid(self) -> None:
        with self.assertRaises(ValueError):
            parse_version("1.2.x")
        with self.assertRaises(TypeError):
            parse_version("")  # type: ignore[arg-type]


class TestCompareVersions(unittest.TestCase):
    def test_equal(self) -> None:
        self.assertEqual(compare_versions("1.2.3", "1.2.3"), 0)

    def test_less(self) -> None:
        self.assertEqual(compare_versions("1.2.3", "1.2.4"), -1)

    def test_greater(self) -> None:
        self.assertEqual(compare_versions("2.0.0", "1.9.9"), 1)


class TestIsGreater(unittest.TestCase):
    def test_greater(self) -> None:
        self.assertTrue(is_greater("2.0.0", "1.0.0"))
        self.assertFalse(is_greater("1.0.0", "2.0.0"))


class TestNormalizeVersion(unittest.TestCase):
    def test_pad(self) -> None:
        self.assertEqual(normalize_version("1.2", 3), "1.2.0")

    def test_truncate(self) -> None:
        self.assertEqual(normalize_version("1.2.3.4", 3), "1.2.3")
