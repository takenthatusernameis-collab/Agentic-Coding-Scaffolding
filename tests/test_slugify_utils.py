"""Tests for slugify_utils."""

import unittest

from slugify_utils import deslugify, is_slug, slugify, slugify_many, truncate_slug


class TestSlugify(unittest.TestCase):
    def test_slugify_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_slugify_accents(self):
        self.assertEqual(slugify("Cafe Resume"), "cafe-resume")

    def test_slugify_custom_separator(self):
        self.assertEqual(slugify("Hello World", "_"), "hello_world")

    def test_slugify_invalid_text(self):
        with self.assertRaises(TypeError):
            slugify(123)  # type: ignore[arg-type]

    def test_slugify_empty_separator(self):
        with self.assertRaises(ValueError):
            slugify("Hello World", "")

    def test_slugify_strips_leading_trailing_separators(self):
        self.assertEqual(slugify(" -- Hello World -- "), "hello-world")

    def test_slugify_separator_chars_in_word_not_stripped(self):
        # separator="ab" should not strip "ab" from end of word "cab"
        self.assertEqual(slugify("hello world cab", "ab"), "helloabworldabcab")

    def test_slugify_multi_char_separator_preserves_word_boundaries(self):
        # Multi-char separator should work correctly
        self.assertEqual(slugify("foo bar baz", "--"), "foo--bar--baz")


class TestIsSlug(unittest.TestCase):
    def test_is_slug(self):
        self.assertTrue(is_slug("hello-world"))

    def test_not_is_slug(self):
        self.assertFalse(is_slug("Hello World"))

    def test_empty_is_not_slug(self):
        self.assertFalse(is_slug(""))

    def test_is_slug_invalid_text(self):
        with self.assertRaises(TypeError):
            is_slug(123)  # type: ignore[arg-type]

    def test_is_slug_custom_separator(self):
        self.assertTrue(is_slug("hello_world", "_"))
        self.assertFalse(is_slug("hello-world", "_"))

    def test_is_slug_rejects_trailing_separator(self):
        self.assertFalse(is_slug("hello-world-", "-"))
        self.assertFalse(is_slug("helloabworldab", "ab"))

    def test_is_slug_rejects_leading_separator(self):
        self.assertFalse(is_slug("-hello-world", "-"))
        self.assertFalse(is_slug("abhelloabworld", "ab"))

    def test_is_slug_rejects_double_separator(self):
        self.assertFalse(is_slug("hello--world", "-"))
        self.assertFalse(is_slug("helloababworld", "ab"))

    def test_is_slug_rejects_uppercase(self):
        self.assertFalse(is_slug("Hello-world", "-"))
        self.assertFalse(is_slug("hello-World", "-"))

    def test_is_slug_alphanumeric_separator_valid(self):
        self.assertTrue(is_slug("helloabworld", "ab"))
        self.assertTrue(is_slug("foosepbar", "sep"))


class TestDeslugify(unittest.TestCase):
    def test_deslugify(self):
        self.assertEqual(deslugify("hello-world"), "Hello World")

    def test_deslugify_custom_separator(self):
        self.assertEqual(deslugify("hello_world", "_"), "Hello World")

    def test_deslugify_invalid(self):
        with self.assertRaises(TypeError):
            deslugify(123)  # type: ignore[arg-type]

    def test_deslugify_empty_separator(self):
        with self.assertRaises(ValueError):
            deslugify("hello-world", "")


class TestTruncateSlug(unittest.TestCase):
    def test_truncate_slug_no_truncation(self):
        self.assertEqual(truncate_slug("hello-world", 100), "hello-world")

    def test_truncate_slug_basic(self):
        self.assertEqual(truncate_slug("hello-world-foo-bar", 12), "hello...")

    def test_truncate_slug_hard_cut(self):
        self.assertEqual(truncate_slug("abcdefghij", 5), "ab...")

    def test_truncate_slug_invalid_text(self):
        with self.assertRaises(TypeError):
            truncate_slug(123, 5)  # type: ignore[arg-type]

    def test_truncate_slug_invalid_max_length(self):
        with self.assertRaises(ValueError):
            truncate_slug("abc", -1)

    def test_truncate_slug_bool_max_length_rejected(self):
        with self.assertRaises(TypeError):
            truncate_slug("abc", True)  # type: ignore[arg-type]

    def test_truncate_slug_max_length_zero(self):
        self.assertEqual(truncate_slug("hello", 0), "")

    def test_truncate_slug_custom_ellipsis(self):
        self.assertEqual(
            truncate_slug("hello-world-foo-bar", 12, ellipsis=".."),
            "hello..",
        )

    def test_truncate_slug_multi_char_separator(self):
        slug = "foo--bar--baz--qux"
        self.assertEqual(truncate_slug(slug, 12, separator="--"), "foo--bar...")

    def test_truncate_slug_separator_chars_in_word_not_stripped(self):
        # separator="ab" should not strip "ab" from end of word when truncating
        slug = "helloabworldabcab"  # from slugify("hello world cab", "ab")
        # Truncate to include "cab" but before next separator
        self.assertEqual(truncate_slug(slug, 20, separator="ab"), "helloabworldabcab")


class TestSlugifyMany(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            slugify_many(["Hello World", "Foo Bar"]),
            ["hello-world", "foo-bar"],
        )

    def test_accepts_tuple(self):
        self.assertEqual(
            slugify_many(("Hello World", "Foo Bar")),
            ["hello-world", "foo-bar"],
        )

    def test_accepts_generator(self):
        self.assertEqual(
            slugify_many(iter(["Hello World", "Foo Bar"])),
            ["hello-world", "foo-bar"],
        )

    def test_accepts_set(self):
        # Order is not guaranteed for a set, so compare as a set.
        self.assertEqual(
            set(slugify_many({"Hello World", "Foo Bar"})),
            {"hello-world", "foo-bar"},
        )

    def test_rejects_string(self):
        with self.assertRaises(TypeError):
            slugify_many("nope")

    def test_rejects_non_iterable(self):
        with self.assertRaises(TypeError):
            slugify_many(123)  # type: ignore[arg-type]

    def test_rejects_non_string_items(self):
        with self.assertRaises(TypeError):
            slugify_many(["ok", 5])  # type: ignore[list-item]

    def test_rejects_empty_separator(self):
        with self.assertRaises(ValueError):
            slugify_many(["Hello World"], "")


if __name__ == "__main__":
    unittest.main()
