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


class TestEdgeCases(unittest.TestCase):
    def test_whitespace_stripped(self):
        parsed = parse_semver("  1.2.3-alpha+build  ")
        self.assertEqual(str(parsed), "1.2.3-alpha+build")

    def test_whitespace_only_rejected(self):
        for invalid in ["   ", "\t", "\n", " \t\n "]:
            with self.assertRaises(ValueError):
                parse_semver(invalid)
        self.assertFalse(is_valid_semver("   "))

    def test_empty_prerelease_or_build_markers_rejected(self):
        for invalid in ["1.0.0-", "1.0.0+", "1.0.0-alpha+", "1.0.0-+build"]:
            with self.assertRaises(ValueError):
                parse_semver(invalid)

    def test_numeric_prerelease_leading_zeroes_rejected(self):
        for invalid in ["1.0.0-01", "1.0.0-alpha.01", "1.0.0-00", "1.0.0-1.02"]:
            with self.assertRaises(ValueError):
                parse_semver(invalid)
            self.assertFalse(is_valid_semver(invalid))
        # Single zero is valid
        self.assertEqual(parse_semver("1.0.0-0").prerelease, "0")
        self.assertTrue(is_valid_semver("1.0.0-alpha.0"))

    def test_build_metadata_ignored_for_precedence(self):
        self.assertEqual(compare_semver("1.0.0+build1", "1.0.0+build2"), 0)
        self.assertFalse(parse_semver("1.0.0+build1") < parse_semver("1.0.0+build2"))
        self.assertFalse(parse_semver("1.0.0+build1") > parse_semver("1.0.0+build2"))
        self.assertEqual(parse_semver("1.0.0+build1"), parse_semver("1.0.0+build2"))
        self.assertEqual(compare_semver("1.0.0", "1.0.0+bbb"), 0)

    def test_build_metadata_ignored_for_equality_and_hash(self):
        a = SemanticVersion(1, 0, 0, build="a")
        b = SemanticVersion(1, 0, 0, build="b")
        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        self.assertEqual(str(a), "1.0.0+a")
        self.assertEqual(str(b), "1.0.0+b")

    def test_build_metadata_preserved_in_string(self):
        self.assertEqual(str(parse_semver("1.0.0+build1")), "1.0.0+build1")
        self.assertNotEqual(str(parse_semver("1.0.0+build1")), str(parse_semver("1.0.0+build2")))

    def test_bump_strips_prerelease_and_build(self):
        self.assertEqual(bump_major("1.2.3-alpha+build"), "2.0.0")
        self.assertEqual(bump_minor("1.2.3-alpha.1"), "1.3.0")
        self.assertEqual(bump_patch("1.2.3+build.7"), "1.2.4")

    def test_is_valid_semver_non_string(self):
        self.assertFalse(is_valid_semver(True))
        self.assertFalse(is_valid_semver(False))
        self.assertFalse(is_valid_semver(None))
        self.assertFalse(is_valid_semver(123))
        self.assertFalse(is_valid_semver(["1.0.0"]))

    def test_semantic_version_rejects_bool_components(self):
        with self.assertRaises(TypeError):
            SemanticVersion(True, 0, 0)
        with self.assertRaises(TypeError):
            SemanticVersion(1, False, 0)
        with self.assertRaises(TypeError):
            SemanticVersion(1, 0, True)

    def test_semantic_version_rejects_non_int_components(self):
        with self.assertRaises(TypeError):
            SemanticVersion("1", 0, 0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            SemanticVersion(1, 2.0, 0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            SemanticVersion(1, 0, None)  # type: ignore[arg-type]

    def test_semantic_version_rejects_negative_components(self):
        with self.assertRaises(ValueError):
            SemanticVersion(-1, 0, 0)
        with self.assertRaises(ValueError):
            SemanticVersion(0, -1, 0)
        with self.assertRaises(ValueError):
            SemanticVersion(0, 0, -1)

    def test_semantic_version_rejects_non_string_metadata(self):
        with self.assertRaises(TypeError):
            SemanticVersion(1, 0, 0, prerelease=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            SemanticVersion(1, 0, 0, build=object())  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            SemanticVersion(1, 0, 0, prerelease=True)  # type: ignore[arg-type]

    def test_semantic_version_accepts_none_metadata(self):
        v = SemanticVersion(1, 0, 0, prerelease=None, build=None)
        self.assertIsNone(v.prerelease)
        self.assertIsNone(v.build)

    def test_compare_semver_rejects_non_string(self):
        with self.assertRaises(ValueError):
            compare_semver("1.0.0", True)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compare_semver(None, "1.0.0")  # type: ignore[arg-type]

    def test_bump_rejects_non_string(self):
        for fn in (bump_major, bump_minor, bump_patch):
            with self.assertRaises(ValueError):
                fn(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

class TestSemanticVersionIdentifierValidation(unittest.TestCase):
    def test_rejects_empty_prerelease_identifier(self):
        for bad in ("", ".", "a..b", ".a", "a.", "alpha..1"):
            with self.assertRaises(ValueError):
                SemanticVersion(1, 0, 0, prerelease=bad)

    def test_rejects_empty_build_identifier(self):
        for bad in ("", ".", "a..b", ".a", "a.", "build..1"):
            with self.assertRaises(ValueError):
                SemanticVersion(1, 0, 0, build=bad)

    def test_rejects_numeric_prerelease_leading_zeroes(self):
        for bad in ("01", "alpha.01", "00", "1.02"):
            with self.assertRaises(ValueError):
                SemanticVersion(1, 0, 0, prerelease=bad)

    def test_accepts_valid_identifiers(self):
        v = SemanticVersion(1, 0, 0, prerelease="alpha.1.0", build="build.123.sha")
        self.assertEqual(str(v), "1.0.0-alpha.1.0+build.123.sha")

    def test_compare_semver_rejects_bool_true(self):
        with self.assertRaises(ValueError):
            compare_semver(True, "1.0.0")  # type: ignore[arg-type]
