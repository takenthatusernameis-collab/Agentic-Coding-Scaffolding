"""Tests for version_utils module."""

import unittest

from version_utils import (
    bump_major,
    bump_minor,
    bump_patch,
    bump_version,
    compare_versions,
    get_major_version,
    get_minor_version,
    get_patch_version,
    is_equal,
    is_greater,
    is_less,
    is_stable,
    is_valid_version,
    is_version_equal,
    is_version_greater,
    is_version_greater_equal,
    is_version_less,
    is_version_less_equal,
    max_version,
    min_version,
    normalize_version,
    parse_version,
    sort_versions,
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


class TestSortVersions(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            sort_versions(["2.0.0", "1.0.0", "1.2.3"]),
            ["1.0.0", "1.2.3", "2.0.0"],
        )

    def test_single_component(self):
        self.assertEqual(sort_versions(["5", "1", "3"]), ["1", "3", "5"])

    def test_different_lengths(self):
        self.assertEqual(
            sort_versions(["1.2", "1.2.0", "1.2.1"]),
            ["1.2", "1.2.0", "1.2.1"],
        )

    def test_empty_list(self):
        self.assertEqual(sort_versions([]), [])

    def test_single_element(self):
        self.assertEqual(sort_versions(["1.0.0"]), ["1.0.0"])

    def test_rejects_non_list(self):
        with self.assertRaises(TypeError):
            sort_versions("1.0.0")  # type: ignore[arg-type]

    def test_rejects_non_string_element(self):
        with self.assertRaises(TypeError):
            sort_versions([1, "2.0"])  # type: ignore[list-item]

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            sort_versions(["1.0", "a.b"])


class TestBumpVersion(unittest.TestCase):
    def test_default_is_patch(self):
        self.assertEqual(bump_version("1.2.3"), "1.2.4")

    def test_major(self):
        self.assertEqual(bump_version("1.2.3", "major"), "2.0.0")

    def test_minor(self):
        self.assertEqual(bump_version("1.2.3", "minor"), "1.3.0")

    def test_patch(self):
        self.assertEqual(bump_version("1.2.3", "patch"), "1.2.4")

    def test_case_insensitive(self):
        self.assertEqual(bump_version("1.2.3", "MAJOR"), "2.0.0")
        self.assertEqual(bump_version("1.2.3", "Minor"), "1.3.0")

    def test_single_component_major(self):
        self.assertEqual(bump_version("5", "major"), "6")

    def test_single_component_minor(self):
        self.assertEqual(bump_version("5", "minor"), "5.1")

    def test_single_component_patch(self):
        self.assertEqual(bump_version("5", "patch"), "5.0.1")

    def test_non_string_version_raises(self):
        with self.assertRaises(TypeError):
            bump_version(1, "patch")  # type: ignore[arg-type]

    def test_non_string_part_raises(self):
        with self.assertRaises(TypeError):
            bump_version("1.2.3", 2)  # type: ignore[arg-type]

    def test_invalid_part_raises(self):
        with self.assertRaises(ValueError):
            bump_version("1.2.3", "build")

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            bump_version("1.2.a", "patch")


class TestMaxMinVersion(unittest.TestCase):
    def test_max(self):
        self.assertEqual(max_version(["1.0.0", "2.5.0", "1.9.9"]), "2.5.0")

    def test_min(self):
        self.assertEqual(min_version(["1.0.0", "2.5.0", "1.9.9"]), "1.0.0")

    def test_single(self):
        self.assertEqual(max_version(["3.0.0"]), "3.0.0")
        self.assertEqual(min_version(["3.0.0"]), "3.0.0")

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            max_version([])
        with self.assertRaises(ValueError):
            min_version([])

    def test_non_list_raises(self):
        with self.assertRaises(TypeError):
            max_version("1.0.0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            min_version("1.0.0")  # type: ignore[arg-type]

    def test_non_string_element_raises(self):
        with self.assertRaises(TypeError):
            max_version(["1.0.0", 2])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            min_version(["1.0.0", 2])  # type: ignore[list-item]

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            max_version(["1.0.0", "bad"])
        with self.assertRaises(ValueError):
            min_version(["1.0.0", "bad"])




class TestIsValidVersion(unittest.TestCase):
    def test_valid(self):
        for v in ("1", "1.0", "1.0.0", "0.0.0"):
            self.assertTrue(is_valid_version(v))

    def test_invalid(self):
        for v in ("", "1.", ".1", "1.0.0a", "abc", "1.2.3.4x"):
            self.assertFalse(is_valid_version(v))

    def test_non_string(self):
        self.assertFalse(is_valid_version(123))  # type: ignore[arg-type]
        self.assertFalse(is_valid_version(None))  # type: ignore[arg-type]


class TestGetVersionComponents(unittest.TestCase):
    def test_major(self):
        self.assertEqual(get_major_version("1.2.3"), 1)
        self.assertEqual(get_major_version("5"), 5)

    def test_minor(self):
        self.assertEqual(get_minor_version("1.2.3"), 2)
        self.assertEqual(get_minor_version("1"), 0)

    def test_patch(self):
        self.assertEqual(get_patch_version("1.2.3"), 3)
        self.assertEqual(get_patch_version("1.2"), 0)
        self.assertEqual(get_patch_version("1"), 0)

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            get_major_version(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_minor_version(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_patch_version([])  # type: ignore[arg-type]

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            get_major_version("1.2.a")


class TestIsStable(unittest.TestCase):
    def test_stable(self):
        self.assertTrue(is_stable("1.0.0"))
        self.assertTrue(is_stable("2.3.4"))
        self.assertTrue(is_stable("1"))

    def test_unstable(self):
        self.assertFalse(is_stable("0.1.0"))
        self.assertFalse(is_stable("0.0.1"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_stable(1)  # type: ignore[arg-type]

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            is_stable("1.2.a")


if __name__ == "__main__":
    unittest.main()
