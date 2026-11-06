"""Tests for version_utils module."""

import unittest

from version_utils import (
    at_least,
    at_most,
    between,
    bump,
    bump_major,
    bump_minor,
    bump_patch,
    bump_version,
    cmp,
    cmp_versions,
    compare,
    compare_versions,
    count_components,
    dec,
    decrement,
    decrement_major,
    decrement_minor,
    decrement_patch,
    decrement_version,
    equal_to,
    from_tuple,
    get_build,
    get_build_metadata,
    get_major_version,
    get_minor_version,
    get_patch_version,
    get_prerelease,
    get_prerelease_tag,
    greater_than,
    has_build_metadata,
    has_metadata,
    has_prerelease,
    increment,
    increment_major,
    increment_minor,
    increment_patch,
    increment_version,
    is_between,
    is_compatible,
    is_dev_version,
    is_beta,
    is_equal,
    is_greater,
    is_initial_release,
    is_less,
    is_newer,
    is_older,
    is_prerelease,
    is_release,
    is_semver,
    is_stable,
    is_valid_version,
    is_version_at_least,
    is_version_at_most,
    is_version_between,
    is_version_equal,
    is_version_greater,
    is_version_greater_equal,
    is_version_less,
    is_version_less_equal,
    less_than,
    major,
    max_version,
    min_version,
    minor,
    normalize_version,
    parse,
    parse_version,
    parse_version_alias,
    patch,
    remove_build_metadata,
    remove_prerelease,
    sort_versions,
    strip_build,
    strip_build_metadata,
    strip_metadata,
    strip_prerelease,
    strip_prerelease_suffix,
    to_tuple,
    tuple_to_version,
    version_satisfies_major,
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


class TestIsInitialRelease(unittest.TestCase):
    def test_initial(self):
        self.assertTrue(is_initial_release("0.1.0"))
        self.assertTrue(is_initial_release("0.0.1"))
        self.assertTrue(is_initial_release("0"))

    def test_not_initial(self):
        self.assertFalse(is_initial_release("1.0.0"))
        self.assertFalse(is_initial_release("2.3.4"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_initial_release(1)  # type: ignore[arg-type]

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            is_initial_release("1.2.a")


class TestIsCompatible(unittest.TestCase):
    def test_same_major(self):
        self.assertTrue(is_compatible("1.2.3", "1.9.0"))

    def test_different_major(self):
        self.assertFalse(is_compatible("1.2.3", "2.0.0"))

    def test_zero_major(self):
        self.assertTrue(is_compatible("0.1.0", "0.9.9"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_compatible(1, "1.0.0")  # type: ignore[arg-type]

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            is_compatible("1.2.a", "1.0.0")


class TestVersionSatisfiesMajor(unittest.TestCase):
    def test_same_major(self):
        self.assertTrue(version_satisfies_major("1.2.3", 1))

    def test_different_major(self):
        self.assertFalse(version_satisfies_major("2.0.0", 1))

    def test_zero_major(self):
        self.assertTrue(version_satisfies_major("0.1.0", 0))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            version_satisfies_major(1, 1)  # type: ignore[arg-type]

    def test_non_int_raises(self):
        with self.assertRaises(TypeError):
            version_satisfies_major("1.0.0", 1.0)  # type: ignore[arg-type]

    def test_bool_raises(self):
        with self.assertRaises(TypeError):
            version_satisfies_major("1.0.0", True)  # type: ignore[arg-type]


class TestDecrementMajor(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(decrement_major("1.2.3"), "0.0.0")

    def test_single_component(self):
        self.assertEqual(decrement_major("5"), "4")

    def test_zero_major_raises(self):
        with self.assertRaises(ValueError):
            decrement_major("0.1.0")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            decrement_major(1)  # type: ignore[arg-type]

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            decrement_major("1.2.a")


class TestDecrementMinor(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(decrement_minor("1.2.3"), "1.1.0")

    def test_zero_minor_raises(self):
        with self.assertRaises(ValueError):
            decrement_minor("1.0.0")

    def test_single_component_raises(self):
        with self.assertRaises(ValueError):
            decrement_minor("5")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            decrement_minor(1)  # type: ignore[arg-type]


class TestDecrementPatch(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(decrement_patch("1.2.3"), "1.2.2")

    def test_zero_patch_raises(self):
        with self.assertRaises(ValueError):
            decrement_patch("1.2.0")

    def test_single_component_raises(self):
        with self.assertRaises(ValueError):
            decrement_patch("5")

    def test_two_components_raises(self):
        with self.assertRaises(ValueError):
            decrement_patch("1.2")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            decrement_patch(1)  # type: ignore[arg-type]


class TestDecrementVersion(unittest.TestCase):
    def test_default_is_patch(self):
        self.assertEqual(decrement_version("1.2.3"), "1.2.2")

    def test_major(self):
        self.assertEqual(decrement_version("1.2.3", "major"), "0.0.0")

    def test_minor(self):
        self.assertEqual(decrement_version("1.2.3", "minor"), "1.1.0")

    def test_patch(self):
        self.assertEqual(decrement_version("1.2.3", "patch"), "1.2.2")

    def test_case_insensitive(self):
        self.assertEqual(decrement_version("1.2.3", "MAJOR"), "0.0.0")
        self.assertEqual(decrement_version("1.2.3", "Minor"), "1.1.0")

    def test_single_component_major(self):
        self.assertEqual(decrement_version("5", "major"), "4")

    def test_single_component_minor_raises(self):
        with self.assertRaises(ValueError):
            decrement_version("5", "minor")

    def test_single_component_patch_raises(self):
        with self.assertRaises(ValueError):
            decrement_version("5", "patch")

    def test_non_string_version_raises(self):
        with self.assertRaises(TypeError):
            decrement_version(1, "patch")  # type: ignore[arg-type]

    def test_non_string_part_raises(self):
        with self.assertRaises(TypeError):
            decrement_version("1.2.3", 2)  # type: ignore[arg-type]

    def test_invalid_part_raises(self):
        with self.assertRaises(ValueError):
            decrement_version("1.2.3", "build")

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            decrement_version("1.2.a", "patch")

    def test_zero_component_raises(self):
        with self.assertRaises(ValueError):
            decrement_version("1.0.0", "minor")
        with self.assertRaises(ValueError):
            decrement_version("1.2.0", "patch")
        with self.assertRaises(ValueError):
            decrement_version("0.1.0", "major")


class TestIsPrerelease(unittest.TestCase):
    def test_prerelease_true(self):
        self.assertTrue(is_prerelease("1.2.3-rc1"))
        self.assertTrue(is_prerelease("1.0.0-alpha"))

    def test_prerelease_false(self):
        self.assertFalse(is_prerelease("1.2.3"))
        self.assertFalse(is_prerelease("2.0.0"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_prerelease(123)  # type: ignore[arg-type]


class TestGetPrerelease(unittest.TestCase):
    def test_returns_tag(self):
        self.assertEqual(get_prerelease("1.2.3-rc1"), "rc1")
        self.assertEqual(get_prerelease("1.0.0-alpha.1"), "alpha.1")

    def test_returns_none_when_not_prerelease(self):
        self.assertIsNone(get_prerelease("1.2.3"))
        self.assertIsNone(get_prerelease("2.0.0"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            get_prerelease(123)  # type: ignore[arg-type]

    def test_alias(self):
        self.assertEqual(get_prerelease_tag("1.2.3-beta"), "beta")


class TestIsDevVersion(unittest.TestCase):
    def test_dev_tags(self):
        self.assertTrue(is_dev_version("1.2.3-dev0"))
        self.assertTrue(is_dev_version("2.0.0-dev.1"))
        self.assertTrue(is_dev_version("1.0.0-DEV5"))

    def test_non_dev_prerelease(self):
        self.assertFalse(is_dev_version("1.2.3-rc1"))
        self.assertFalse(is_dev_version("1.0.0-alpha"))

    def test_no_prerelease(self):
        self.assertFalse(is_dev_version("1.2.3"))
        self.assertFalse(is_dev_version("2.0.0"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_dev_version(123)  # type: ignore[arg-type]


class TestIsBeta(unittest.TestCase):
    def test_beta_tag_true(self):
        self.assertTrue(is_beta("1.2.3-beta1"))
        self.assertTrue(is_beta("1.0.0-BETA.2"))
        self.assertTrue(is_beta("2.0.0-beta"))

    def test_non_beta_prerelease_false(self):
        self.assertFalse(is_beta("1.2.3-rc1"))
        self.assertFalse(is_beta("1.0.0-alpha"))
        self.assertFalse(is_beta("1.2.3-dev0"))

    def test_no_prerelease_false(self):
        self.assertFalse(is_beta("1.2.3"))
        self.assertFalse(is_beta("2.0.0"))
        self.assertFalse(is_beta(""))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_beta(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_beta(None)  # type: ignore[arg-type]


class TestVersionComparisonAliases(unittest.TestCase):
    def test_cmp_versions_alias(self):
        self.assertEqual(cmp_versions("1.2.3", "1.2.3"), 0)
        self.assertEqual(cmp_versions("2.0.0", "1.0.0"), 1)
        self.assertEqual(cmp_versions("1.0.0", "2.0.0"), -1)

    def test_cmp_and_compare_aliases(self):
        self.assertEqual(cmp("1.2.3", "1.2.3"), 0)
        self.assertEqual(compare("2.0.0", "1.0.0"), 1)

    def test_is_semver_alias(self):
        self.assertTrue(is_semver("1.2.3"))
        self.assertFalse(is_semver("1.2.3-rc1"))
        self.assertFalse(is_semver("a.b.c"))
        self.assertFalse(is_semver(123))  # type: ignore[arg-type]

    def test_is_newer_is_older_aliases(self):
        self.assertTrue(is_newer("2.0.0", "1.0.0"))
        self.assertFalse(is_newer("1.0.0", "2.0.0"))
        self.assertTrue(is_older("1.0.0", "2.0.0"))
        self.assertFalse(is_older("2.0.0", "1.0.0"))

    def test_from_tuple_alias(self):
        self.assertEqual(from_tuple((1, 2, 3)), "1.2.3")
        self.assertEqual(from_tuple((5,)), "5")

    def test_increment_aliases(self):
        self.assertEqual(increment_version("1.2.3"), "1.2.4")
        self.assertEqual(increment("1.2.3", "major"), "2.0.0")
        self.assertEqual(increment("1.2.3", "minor"), "1.3.0")


class TestVersionUtilsAliasesComprehensive(unittest.TestCase):
    def test_parse_version_alias_matches_parse_version(self):
        self.assertEqual(parse_version_alias("1.2.3"), parse_version("1.2.3"))
        self.assertEqual(parse_version_alias("10"), parse_version("10"))
        self.assertEqual(parse_version_alias("v1.2.3"), parse_version("1.2.3"))
        self.assertEqual(parse_version_alias("V2.0.0"), parse_version("2.0.0"))

    def test_parse_version_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            parse_version_alias(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            parse_version_alias(None)  # type: ignore[arg-type]

    def test_parse_version_alias_rejects_invalid(self):
        with self.assertRaises((ValueError, TypeError)):
            parse_version_alias("")
        with self.assertRaises(ValueError):
            parse_version_alias("1.2.a")
        with self.assertRaises(ValueError):
            parse_version_alias("v")

    def test_greater_than_matches_is_greater(self):
        self.assertTrue(greater_than("2.0.0", "1.0.0"))
        self.assertFalse(greater_than("1.0.0", "2.0.0"))
        self.assertFalse(greater_than("1.2.3", "1.2.3"))
        self.assertTrue(greater_than("v2.0.0", "v1.9.9"))
        self.assertTrue(greater_than("10.0.0", "2.0.0"))

    def test_greater_than_rejects_non_string(self):
        with self.assertRaises(TypeError):
            greater_than(1, "1.0.0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            greater_than("1.0.0", 2)  # type: ignore[arg-type]
        with self.assertRaises((ValueError, TypeError)):
            greater_than("bad", "1.0.0")

    def test_greater_than_rejects_invalid_comparisons(self):
        with self.assertRaises(ValueError):
            greater_than("1.2.a", "1.2.3")
        with self.assertRaises((ValueError, TypeError)):
            greater_than("", "1.0.0")

    def test_less_than_matches_is_less(self):
        self.assertTrue(less_than("1.0.0", "2.0.0"))
        self.assertFalse(less_than("2.0.0", "1.0.0"))
        self.assertFalse(less_than("1.2.3", "1.2.3"))
        self.assertTrue(less_than("v1.0.0", "v2.0.0"))
        self.assertTrue(less_than("1.0.0", "10.0.0"))

    def test_less_than_rejects_non_string(self):
        with self.assertRaises(TypeError):
            less_than(1, "1.0.0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            less_than("1.0.0", 2)  # type: ignore[arg-type]
        with self.assertRaises((ValueError, TypeError)):
            less_than("bad", "1.0.0")

    def test_less_than_rejects_invalid_comparisons(self):
        with self.assertRaises(ValueError):
            less_than("1.2.3", "1.2.a")

    def test_equal_to_matches_is_equal(self):
        self.assertTrue(equal_to("1.2.3", "1.2.3"))
        self.assertFalse(equal_to("1.2.3", "1.2.4"))
        self.assertTrue(equal_to("v1.2.3", "1.2.3"))
        self.assertTrue(equal_to("01.02.03", "1.2.3"))

    def test_equal_to_rejects_non_string(self):
        with self.assertRaises(TypeError):
            equal_to(1, "1.0.0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            equal_to("1.0.0", 2)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            equal_to("1.0.a", "1.0.0")

    def test_equal_to_rejects_invalid_comparisons(self):
        with self.assertRaises(ValueError):
            equal_to("1.0.0", "1.0.b")

    def test_increment_major_matches_bump_major(self):
        self.assertEqual(increment_major("1.2.3"), bump_major("1.2.3"))
        self.assertEqual(increment_major("1.2.3"), "2.0.0")
        self.assertEqual(increment_major("v1.2.3"), "2.0.0")
        self.assertEqual(increment_major("0.9.9"), "1.0.0")

    def test_increment_major_rejects_non_string(self):
        with self.assertRaises(TypeError):
            increment_major(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            increment_major(None)  # type: ignore[arg-type]

    def test_increment_major_rejects_invalid(self):
        with self.assertRaises((ValueError, TypeError)):
            increment_major("")
        with self.assertRaises(ValueError):
            increment_major("1.2.a")

    def test_increment_minor_matches_bump_minor(self):
        self.assertEqual(increment_minor("1.2.3"), bump_minor("1.2.3"))
        self.assertEqual(increment_minor("1.2.3"), "1.3.0")
        self.assertEqual(increment_minor("v1.2.3"), "1.3.0")
        self.assertEqual(increment_minor("1.0.9"), "1.1.0")

    def test_increment_minor_rejects_non_string(self):
        with self.assertRaises(TypeError):
            increment_minor(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            increment_minor([])  # type: ignore[arg-type]

    def test_increment_minor_rejects_invalid(self):
        with self.assertRaises((ValueError, TypeError)):
            increment_minor("")
        with self.assertRaises(ValueError):
            increment_minor("1.a.0")

    def test_increment_patch_matches_bump_patch(self):
        self.assertEqual(increment_patch("1.2.3"), bump_patch("1.2.3"))
        self.assertEqual(increment_patch("1.2.3"), "1.2.4")
        self.assertEqual(increment_patch("v1.2.3"), "1.2.4")
        self.assertEqual(increment_patch("1.2.0"), "1.2.1")

    def test_increment_patch_rejects_non_string(self):
        with self.assertRaises(TypeError):
            increment_patch(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            increment_patch({})  # type: ignore[arg-type]

    def test_increment_patch_rejects_invalid(self):
        with self.assertRaises((ValueError, TypeError)):
            increment_patch("")
        with self.assertRaises(ValueError):
            increment_patch("1.2.b")


if __name__ == "__main__":
    unittest.main()


class TestGetBuildMetadata(unittest.TestCase):
    def test_returns_metadata(self):
        self.assertEqual(get_build_metadata("1.2.3+20130313144700"), "20130313144700")
        self.assertEqual(get_build_metadata("1.0.0+build.123"), "build.123")

    def test_returns_none_when_not_present(self):
        self.assertIsNone(get_build_metadata("1.2.3"))
        self.assertIsNone(get_build_metadata("2.0.0"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            get_build_metadata(123)  # type: ignore[arg-type]

    def test_alias(self):
        self.assertEqual(get_build("1.2.3+beta"), "beta")


class TestHasBuildMetadata(unittest.TestCase):
    def test_returns_true_when_present(self):
        self.assertTrue(has_build_metadata("1.2.3+20130313144700"))
        self.assertTrue(has_build_metadata("1.0.0+build.123"))
        self.assertTrue(has_build_metadata("1.2.3-rc1+build.123"))

    def test_returns_false_when_not_present(self):
        self.assertFalse(has_build_metadata("1.2.3"))
        self.assertFalse(has_build_metadata("2.0.0"))
        self.assertFalse(has_build_metadata("1.2.3-rc1"))
        self.assertFalse(has_build_metadata(""))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            has_build_metadata(123)  # type: ignore[arg-type]


class TestHasPrerelease(unittest.TestCase):
    def test_returns_true_when_present(self):
        self.assertTrue(has_prerelease("1.2.3-rc1"))
        self.assertTrue(has_prerelease("1.0.0-alpha.1"))
        self.assertTrue(has_prerelease("1.2.3-rc1+build.123"))

    def test_returns_false_when_not_present(self):
        self.assertFalse(has_prerelease("1.2.3"))
        self.assertFalse(has_prerelease("2.0.0"))
        self.assertFalse(has_prerelease("1.2.3+build.123"))
        self.assertFalse(has_prerelease(""))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            has_prerelease(123)  # type: ignore[arg-type]


class TestIsRelease(unittest.TestCase):
    def test_returns_true_when_no_prerelease(self):
        self.assertTrue(is_release("1.2.3"))
        self.assertTrue(is_release("2.0.0"))
        self.assertTrue(is_release("1.2.3+build.123"))

    def test_returns_false_when_prerelease_present(self):
        self.assertFalse(is_release("1.2.3-rc1"))
        self.assertFalse(is_release("1.0.0-alpha.1"))
        self.assertFalse(is_release("1.2.3-rc1+build.123"))
        self.assertFalse(is_release(""))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_release(123)  # type: ignore[arg-type]


class TestHasMetadata(unittest.TestCase):
    def test_returns_true_when_present(self):
        self.assertTrue(has_metadata("1.2.3-rc1"))
        self.assertTrue(has_metadata("1.0.0+build.123"))
        self.assertTrue(has_metadata("1.2.3-rc1+build.123"))

    def test_returns_false_when_not_present(self):
        self.assertFalse(has_metadata("1.2.3"))
        self.assertFalse(has_metadata("2.0.0"))
        self.assertFalse(has_metadata(""))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            has_metadata(123)  # type: ignore[arg-type]


class TestStripPrerelease(unittest.TestCase):
    def test_strips_prerelease(self):
        self.assertEqual(strip_prerelease("1.2.3-rc1"), "1.2.3")
        self.assertEqual(strip_prerelease("1.0.0-alpha.1"), "1.0.0")

    def test_no_prerelease_returns_original(self):
        self.assertEqual(strip_prerelease("1.2.3"), "1.2.3")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            strip_prerelease(123)  # type: ignore[arg-type]

    def test_aliases(self):
        self.assertEqual(strip_prerelease_suffix("1.2.3-rc1"), "1.2.3")
        self.assertEqual(remove_prerelease("1.2.3-rc1"), "1.2.3")


class TestStripBuildMetadata(unittest.TestCase):
    def test_strips_build(self):
        self.assertEqual(strip_build_metadata("1.2.3+20130313144700"), "1.2.3")
        self.assertEqual(strip_build_metadata("1.0.0+build.123"), "1.0.0")

    def test_no_build_returns_original(self):
        self.assertEqual(strip_build_metadata("1.2.3"), "1.2.3")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            strip_build_metadata(123)  # type: ignore[arg-type]

    def test_aliases(self):
        self.assertEqual(strip_build("1.2.3+beta"), "1.2.3")
        self.assertEqual(remove_build_metadata("1.2.3+beta"), "1.2.3")


class TestStripMetadata(unittest.TestCase):
    def test_strips_both(self):
        self.assertEqual(strip_metadata("1.2.3-rc1+build.123"), "1.2.3")

    def test_strips_prerelease_only(self):
        self.assertEqual(strip_metadata("1.2.3-rc1"), "1.2.3")

    def test_strips_build_only(self):
        self.assertEqual(strip_metadata("1.2.3+build.123"), "1.2.3")

    def test_no_metadata_returns_original(self):
        self.assertEqual(strip_metadata("1.2.3"), "1.2.3")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            strip_metadata(123)  # type: ignore[arg-type]


class TestIsVersionAtLeast(unittest.TestCase):
    def test_greater(self):
        self.assertTrue(is_version_at_least("1.2.3", "1.2.0"))

    def test_equal(self):
        self.assertTrue(is_version_at_least("1.2.3", "1.2.3"))

    def test_less(self):
        self.assertFalse(is_version_at_least("1.2.3", "1.3.0"))

    def test_shorter_minimum_is_greater(self):
        # 1.3.0 > 1.3 because (1, 3, 0) > (1, 3)
        self.assertFalse(is_version_at_least("1.3", "1.3.0"))

    def test_alias(self):
        self.assertTrue(at_least("2.0.0", "1.9.9"))
        self.assertFalse(at_least("0.9.0", "1.0.0"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_version_at_least("1.0.0", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_version_at_least(1, "1.0.0")  # type: ignore[arg-type]

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            is_version_at_least("1.x", "1.0.0")


class TestIsVersionAtMost(unittest.TestCase):
    def test_less(self):
        self.assertTrue(is_version_at_most("1.2.3", "1.3.0"))

    def test_equal(self):
        self.assertTrue(is_version_at_most("1.2.3", "1.2.3"))

    def test_greater(self):
        self.assertFalse(is_version_at_most("1.2.3", "1.2.0"))

    def test_shorter_maximum_is_greater(self):
        self.assertFalse(is_version_at_most("1.3.0", "1.3"))

    def test_alias(self):
        self.assertTrue(at_most("1.0.0", "2.0.0"))
        self.assertFalse(at_most("2.0.0", "1.0.0"))

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            is_version_at_most("1.0.0", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_version_at_most(1, "1.0.0")  # type: ignore[arg-type]

    def test_invalid_version_raises(self):
        with self.assertRaises(ValueError):
            is_version_at_most("1.x", "1.0.0")


class TestIsVersionBetween(unittest.TestCase):
    def test_between_inclusive(self):
        self.assertTrue(is_version_between("1.2.5", "1.2.0", "1.3.0"))
        self.assertTrue(is_version_between("1.2.0", "1.2.0", "1.3.0"))
        self.assertTrue(is_version_between("1.3.0", "1.2.0", "1.3.0"))
        self.assertFalse(is_version_between("1.1.9", "1.2.0", "1.3.0"))
        self.assertFalse(is_version_between("1.3.1", "1.2.0", "1.3.0"))

    def test_between_exclusive(self):
        self.assertTrue(is_version_between("1.2.5", "1.2.0", "1.3.0", inclusive=False))
        self.assertFalse(is_version_between("1.2.0", "1.2.0", "1.3.0", inclusive=False))
        self.assertFalse(is_version_between("1.3.0", "1.2.0", "1.3.0", inclusive=False))

    def test_aliases(self):
        self.assertTrue(between("1.0.0", "1.0.0", "2.0.0"))
        self.assertTrue(is_between("1.5.0", "1.0.0", "2.0.0"))
        self.assertFalse(is_between("0.9.0", "1.0.0", "2.0.0"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_version_between(123, "1.0.0", "2.0.0")
        with self.assertRaises(TypeError):
            is_version_between("1.0.0", 123, "2.0.0")
        with self.assertRaises(TypeError):
            is_version_between("1.0.0", "1.0.0", 123)
        with self.assertRaises(TypeError):
            is_version_between("1.0.0", "1.0.0", "2.0.0", inclusive="yes")

    def test_invalid_version(self):
        with self.assertRaises(ValueError):
            is_version_between("bad", "1.0.0", "2.0.0")
        with self.assertRaises(ValueError):
            is_version_between("1.0.0", "bad", "2.0.0")
        with self.assertRaises(ValueError):
            is_version_between("1.0.0", "1.0.0", "bad")


class TestVersionUtilsAliases(unittest.TestCase):
    def test_parse_version_alias(self):
        self.assertEqual(parse_version_alias("1.2.3"), parse_version("1.2.3"))

    def test_greater_than(self):
        self.assertTrue(greater_than("2.0.0", "1.0.0"))
        self.assertFalse(greater_than("1.0.0", "2.0.0"))

    def test_less_than(self):
        self.assertTrue(less_than("1.0.0", "2.0.0"))
        self.assertFalse(less_than("2.0.0", "1.0.0"))

    def test_equal_to(self):
        self.assertTrue(equal_to("1.0.0", "1.0.0"))
        self.assertFalse(equal_to("1.0.0", "2.0.0"))

    def test_increment_major(self):
        self.assertEqual(increment_major("1.2.3"), "2.0.0")

    def test_increment_minor(self):
        self.assertEqual(increment_minor("1.2.3"), "1.3.0")

    def test_increment_patch(self):
        self.assertEqual(increment_patch("1.2.3"), "1.2.4")


class TestCountComponents(unittest.TestCase):
    """Tests for the ``count_components`` helper."""

    def test_three_components(self):
        self.assertEqual(count_components("1.2.3"), 3)

    def test_single_component(self):
        self.assertEqual(count_components("5"), 1)

    def test_two_components(self):
        self.assertEqual(count_components("2.0"), 2)

    def test_four_components(self):
        self.assertEqual(count_components("1.2.3.4"), 4)

    def test_empty_string(self):
        self.assertEqual(count_components(""), 0)

    def test_prerelease_suffix_part_of_last_component(self):
        self.assertEqual(count_components("1.2.3-rc1"), 3)

    def test_build_metadata_counts_as_component(self):
        self.assertEqual(count_components("1.2.3+build.123"), 4)

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            count_components(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_components(None)  # type: ignore[arg-type]


class TestRemainingVersionAliases(unittest.TestCase):
    """Coverage for the aliases that were not exercised before this audit:
    ``bump``, ``dec``, ``decrement``, ``major``, ``minor``, ``parse``,
    ``patch``, and ``to_tuple``."""

    def test_parse_alias_matches_parse_version(self):
        self.assertEqual(parse("1.2.3"), parse_version("1.2.3"))
        self.assertEqual(parse("v2.0.0"), parse_version("2.0.0"))
        self.assertEqual(parse("10"), parse_version("10"))

    def test_parse_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            parse(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            parse(None)  # type: ignore[arg-type]

    def test_parse_alias_rejects_invalid(self):
        with self.assertRaises(ValueError):
            parse("1.2.a")

    def test_to_tuple_alias_matches_version_to_tuple(self):
        self.assertEqual(to_tuple("1.2.3"), version_to_tuple("1.2.3"))
        self.assertEqual(to_tuple("5"), (5,))
        self.assertEqual(to_tuple("v3.2.1"), (3, 2, 1))

    def test_to_tuple_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            to_tuple(1)  # type: ignore[arg-type]

    def test_bump_alias_matches_bump_version(self):
        self.assertEqual(bump("1.2.3"), bump_version("1.2.3"))
        self.assertEqual(bump("1.2.3"), "1.2.4")
        self.assertEqual(bump("1.2.3", "major"), "2.0.0")
        self.assertEqual(bump("1.2.3", "minor"), "1.3.0")

    def test_bump_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            bump(1)  # type: ignore[arg-type]

    def test_bump_alias_rejects_invalid_part(self):
        with self.assertRaises(ValueError):
            bump("1.2.3", "build")

    def test_decrement_alias_matches_decrement_version(self):
        self.assertEqual(decrement("1.2.3"), decrement_version("1.2.3"))
        self.assertEqual(decrement("1.2.3"), "1.2.2")
        self.assertEqual(decrement("1.2.3", "major"), "0.0.0")
        self.assertEqual(decrement("1.2.3", "minor"), "1.1.0")

    def test_decrement_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            decrement(1)  # type: ignore[arg-type]

    def test_decrement_alias_rejects_invalid_part(self):
        with self.assertRaises(ValueError):
            decrement("1.2.3", "build")

    def test_dec_alias_matches_decrement(self):
        self.assertEqual(dec("1.2.3"), decrement("1.2.3"))
        self.assertEqual(dec("1.2.3"), "1.2.2")

    def test_dec_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            dec(1)  # type: ignore[arg-type]

    def test_major_alias_matches_get_major_version(self):
        self.assertEqual(major("1.2.3"), get_major_version("1.2.3"))
        self.assertEqual(major("5"), 5)
        self.assertEqual(major("v9.0.0"), 9)

    def test_major_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            major(1)  # type: ignore[arg-type]

    def test_minor_alias_matches_get_minor_version(self):
        self.assertEqual(minor("1.2.3"), get_minor_version("1.2.3"))
        self.assertEqual(minor("1"), 0)
        self.assertEqual(minor("v2.5.0"), 5)

    def test_minor_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            minor(1)  # type: ignore[arg-type]

    def test_patch_alias_matches_get_patch_version(self):
        self.assertEqual(patch("1.2.3"), get_patch_version("1.2.3"))
        self.assertEqual(patch("1.2"), 0)
        self.assertEqual(patch("v3.2.9"), 9)

    def test_patch_alias_rejects_non_string(self):
        with self.assertRaises(TypeError):
            patch(1)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
