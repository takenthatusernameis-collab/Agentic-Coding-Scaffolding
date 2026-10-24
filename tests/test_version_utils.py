"""Tests for version_utils module."""

import unittest

from version_utils import (
    bump_major,
    bump_minor,
    bump_patch,
    compare_versions,
    is_equal,
    is_greater,
    is_less,
    is_version_equal,
    is_version_greater,
    is_version_greater_equal,
    is_version_less,
    is_version_less_equal,
    normalize_version,
    parse_version,
    tuple_to_version,
    version_to_tuple,
)


class TestParseVersion(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(parse_version("1.2.3"), (1, 2, 3))

    def test_single_component(self):
        self.assertEqual(parse_version("5"), (5,))

    def test_empty_raises(self):
        with self.assertRaises(TypeError):
            parse_version("")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            parse_version(123)  # type: ignore[arg-type]

    def test_invalid_component_raises(self):
        with self.assertRaises(ValueError):
            parse_version("1.2.a")


class TestVersionToTuple(unittest.TestCase):
    def test_alias(self):
        self.assertEqual(version_to_tuple("2.0.1"), parse_version("2.0.1"))


class TestCompareVersions(unittest.TestCase):
    def test_less(self):
        self.assertEqual(compare_versions("1.0.0", "2.0.0"), -1)

    def test_equal(self):
        self.assertEqual(compare_versions("1.2.3", "1.2.3"), 0)

    def test_greater(self):
        self.assertEqual(compare_versions("2.0.0", "1.0.0"), 1)

    def test_different_lengths(self):
        self.assertEqual(compare_versions("1.2", "1.2.0"), -1)


class TestBooleanComparisons(unittest.TestCase):
    def test_is_greater(self):
        self.assertTrue(is_greater("2.0.0", "1.0.0"))
        self.assertFalse(is_greater("1.0.0", "2.0.0"))

    def test_is_less(self):
        self.assertTrue(is_less("1.0.0", "2.0.0"))
        self.assertFalse(is_less("2.0.0", "1.0.0"))

    def test_is_equal(self):
        self.assertTrue(is_equal("1.2.3", "1.2.3"))
        self.assertFalse(is_equal("1.2.3", "1.2.4"))


class TestNormalizeVersion(unittest.TestCase):
    def test_pads(self):
        self.assertEqual(normalize_version("1", 3), "1.0.0")

    def test_truncates(self):
        self.assertEqual(normalize_version("1.2.3.4", 2), "1.2")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            normalize_version(1, 3)  # type: ignore[arg-type]

    def test_negative_length_raises(self):
        with self.assertRaises(ValueError):
            normalize_version("1", -1)


class TestTupleToVersion(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(tuple_to_version((1, 2, 3)), "1.2.3")

    def test_non_tuple_raises(self):
        with self.assertRaises(TypeError):
            tuple_to_version([1, 2])  # type: ignore[arg-type]

    def test_non_int_component_raises(self):
        with self.assertRaises(TypeError):
            tuple_to_version((1, "2"))


class TestBump(unittest.TestCase):
    def test_bump_major(self):
        self.assertEqual(bump_major("1.2.3"), "2.0.0")

    def test_bump_minor(self):
        self.assertEqual(bump_minor("1.2.3"), "1.3.0")

    def test_bump_patch(self):
        self.assertEqual(bump_patch("1.2.3"), "1.2.4")


class TestVersionAliases(unittest.TestCase):
    def test_is_version_greater(self):
        self.assertTrue(is_version_greater("2.0.0", "1.0.0"))

    def test_is_version_less(self):
        self.assertTrue(is_version_less("1.0.0", "2.0.0"))

    def test_is_version_equal(self):
        self.assertTrue(is_version_equal("1.2.3", "1.2.3"))

    def test_is_version_greater_equal(self):
        self.assertTrue(is_version_greater_equal("2.0.0", "1.0.0"))
        self.assertTrue(is_version_greater_equal("1.0.0", "1.0.0"))

    def test_is_version_less_equal(self):
        self.assertTrue(is_version_less_equal("1.0.0", "2.0.0"))
        self.assertTrue(is_version_less_equal("1.0.0", "1.0.0"))


if __name__ == "__main__":
    unittest.main()
