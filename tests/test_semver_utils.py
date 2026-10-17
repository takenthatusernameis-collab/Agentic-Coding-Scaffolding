import unittest

from semver_utils import (
    SemanticVersion,
    bump_major,
    bump_minor,
    bump_patch,
    compare_semver,
    is_valid_semver,
    parse_semver,
)


class TestParseSemver(unittest.TestCase):
    def test_valid_versions(self):
        self.assertEqual(str(parse_semver("1.0.0")), "1.0.0")
        self.assertEqual(str(parse_semver("2.10.3")), "2.10.3")
        self.assertEqual(str(parse_semver("1.0.0-alpha")), "1.0.0-alpha")
        self.assertEqual(str(parse_semver("1.0.0-alpha.1")), "1.0.0-alpha.1")
        self.assertEqual(str(parse_semver("1.0.0+build.123")), "1.0.0+build.123")
        self.assertEqual(
            str(parse_semver("1.0.0-beta+exp.sha.5114f85")),
            "1.0.0-beta+exp.sha.5114f85",
        )

    def test_parsed_fields(self):
        parsed = parse_semver("1.2.3")
        self.assertEqual(parsed.major, 1)
        self.assertEqual(parsed.minor, 2)
        self.assertEqual(parsed.patch, 3)
        self.assertIsNone(parsed.prerelease)
        self.assertIsNone(parsed.build)

    def test_prerelease_and_build_fields(self):
        parsed = parse_semver("1.0.0-alpha.1+build.5")
        self.assertEqual(parsed.prerelease, "alpha.1")
        self.assertEqual(parsed.build, "build.5")
        self.assertTrue(parsed.is_prerelease())

    def test_no_prerelease(self):
        parsed = parse_semver("1.0.0")
        self.assertFalse(parsed.is_prerelease())

    def test_invalid_versions(self):
        for invalid in ["", "1.2", "1.2.3.4", "v1.2.3", "1.02.3", "01.0.0", "abc", "1.2.3-"]:
            with self.assertRaises(ValueError):
                parse_semver(invalid)

    def test_non_string_input(self):
        with self.assertRaises(ValueError):
            parse_semver(123)  # type: ignore[arg-type]


class TestCompareSemver(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(compare_semver("1.0.0", "1.0.0"), 0)

    def test_less_than(self):
        self.assertEqual(compare_semver("1.0.0", "2.0.0"), -1)
        self.assertEqual(compare_semver("1.0.0", "1.1.0"), -1)
        self.assertEqual(compare_semver("1.0.0", "1.0.1"), -1)

    def test_greater_than(self):
        self.assertEqual(compare_semver("2.0.0", "1.0.0"), 1)
        self.assertEqual(compare_semver("1.1.0", "1.0.0"), 1)
        self.assertEqual(compare_semver("1.0.1", "1.0.0"), 1)

    def test_prerelease_lower_than_release(self):
        self.assertEqual(compare_semver("1.0.0-alpha", "1.0.0"), -1)
        self.assertEqual(compare_semver("1.0.0", "1.0.0-alpha"), 1)

    def test_prerelease_comparison(self):
        self.assertEqual(compare_semver("1.0.0-alpha", "1.0.0-alpha.1"), -1)
        self.assertEqual(compare_semver("1.0.0-alpha.1", "1.0.0-alpha.beta"), -1)
        self.assertEqual(compare_semver("1.0.0-alpha.1", "1.0.0-alpha.1"), 0)
        self.assertEqual(compare_semver("1.0.0-1", "1.0.0-alpha"), -1)  # numeric < alpha


class TestBump(unittest.TestCase):
    def test_bump_major(self):
        self.assertEqual(bump_major("1.2.3"), "2.0.0")
        self.assertEqual(bump_major("0.9.0"), "1.0.0")

    def test_bump_minor(self):
        self.assertEqual(bump_minor("1.2.3"), "1.3.0")
        self.assertEqual(bump_minor("1.0.9"), "1.1.0")

    def test_bump_patch(self):
        self.assertEqual(bump_patch("1.2.3"), "1.2.4")
        self.assertEqual(bump_patch("1.2.9"), "1.2.10")


class TestIsValidSemver(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_valid_semver("1.0.0"))
        self.assertTrue(is_valid_semver("2.0.0-rc.1+build"))

    def test_invalid(self):
        self.assertFalse(is_valid_semver("not-a-version"))
        self.assertFalse(is_valid_semver("1.2"))
        self.assertFalse(is_valid_semver(""))


class TestSemanticVersionOrdering(unittest.TestCase):
    def test_operators(self):
        self.assertTrue(SemanticVersion(1, 0, 0) < SemanticVersion(2, 0, 0))
        self.assertTrue(SemanticVersion(2, 0, 0) > SemanticVersion(1, 0, 0))
        self.assertTrue(SemanticVersion(1, 0, 0) <= SemanticVersion(1, 0, 0))
        self.assertTrue(SemanticVersion(1, 0, 0) >= SemanticVersion(1, 0, 0))
        self.assertFalse(SemanticVersion(1, 0, 0) < SemanticVersion(1, 0, 0))


if __name__ == "__main__":
    unittest.main()
