"""Tests for string_utils module."""

import unittest

from string_utils import (
    camel_to_snake,
    indent_text,
    pluralize,
    remove_blank_lines,
    remove_extra_whitespace,
    slugify,
    snake_to_camel,
    title_case,
    truncate,
    truncate_words,
    wrap_text,
)


class TestSlugify(unittest.TestCase):
    def test_basic_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_multiple_spaces(self):
        self.assertEqual(slugify("  Python   is   Great!  "), "python-is-great")

    def test_underscores(self):
        self.assertEqual(slugify("foo_bar_baz"), "foo-bar-baz")

    def test_already_slug(self):
        self.assertEqual(slugify("already-a-slug"), "already-a-slug")

    def test_empty(self):
        self.assertEqual(slugify(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            slugify(123)


class TestCamelToSnake(unittest.TestCase):
    def test_camel_case(self):
        self.assertEqual(camel_to_snake("helloWorld"), "hello_world")

    def test_pascal_case(self):
        self.assertEqual(camel_to_snake("HelloWorld"), "hello_world")

    def test_acronym(self):
        self.assertEqual(camel_to_snake("XMLParser"), "xml_parser")

    def test_already_snake(self):
        self.assertEqual(camel_to_snake("already_snake"), "already_snake")

    def test_hyphens(self):
        self.assertEqual(camel_to_snake("hello-world"), "hello_world")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            camel_to_snake(None)


class TestSnakeToCamel(unittest.TestCase):
    def test_snake_case(self):
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")

    def test_acronym(self):
        self.assertEqual(snake_to_camel("xml_parser"), "xmlParser")

    def test_already_camel(self):
        self.assertEqual(snake_to_camel("alreadyCamel"), "alreadyCamel")

    def test_empty(self):
        self.assertEqual(snake_to_camel(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            snake_to_camel(42)


class TestPluralize(unittest.TestCase):
    def test_regular(self):
        self.assertEqual(pluralize("cat"), "cats")

    def test_count_one(self):
        self.assertEqual(pluralize("cat", 1), "cat")

    def test_count_two(self):
        self.assertEqual(pluralize("cat", 2), "cats")

    def test_s_x_z(self):
        self.assertEqual(pluralize("bus"), "buses")
        self.assertEqual(pluralize("box"), "boxes")
        self.assertEqual(pluralize("buzz"), "buzzes")

    def test_ch_sh(self):
        self.assertEqual(pluralize("church"), "churches")
        self.assertEqual(pluralize("brush"), "brushes")

    def test_consonant_y(self):
        self.assertEqual(pluralize("baby"), "babies")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            pluralize(1)


class TestTruncate(unittest.TestCase):
    def test_truncate_with_suffix(self):
        self.assertEqual(truncate("Hello, world!", 5), "He...")

    def test_no_truncation(self):
        self.assertEqual(truncate("Hi", 10), "Hi")

    def test_empty_suffix(self):
        self.assertEqual(truncate("Hello, world!", 8, suffix=""), "Hello, w")

    def test_shorter_than_suffix(self):
        # Text fits within length, so it is returned unchanged even though the
        # suffix alone would not fit.
        self.assertEqual(truncate("hi", 2, suffix="..."), "hi")

    def test_negative_length(self):
        with self.assertRaises(ValueError):
            truncate("hello", -1)

    def test_non_string(self):
        with self.assertRaises(TypeError):
            truncate(123, 5)


class TestWrapText(unittest.TestCase):
    def test_wrap(self):
        self.assertEqual(wrap_text("hello world", 5), "hello\nworld")

    def test_default_width(self):
        result = wrap_text("a b c d e f g h i j k l m n o p")
        self.assertLessEqual(max(len(line) for line in result.split("\n")), 70)

    def test_non_string(self):
        with self.assertRaises(TypeError):
            wrap_text(None)

    def test_non_positive_width(self):
        with self.assertRaises(ValueError):
            wrap_text("hello", 0)
        with self.assertRaises(ValueError):
            wrap_text("hello", -3)


class TestIndentText(unittest.TestCase):
    def test_indent(self):
        self.assertEqual(indent_text("line1\nline2", "  "), "  line1\n  line2")

    def test_default_prefix(self):
        result = indent_text("a\nb")
        self.assertEqual(result, "    a\n    b")

    def test_empty_string(self):
        self.assertEqual(indent_text("", "  "), "  ")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            indent_text(123)


class TestRemoveExtraWhitespace(unittest.TestCase):
    def test_collapse_spaces(self):
        self.assertEqual(remove_extra_whitespace("  hello   world  "), "hello world")

    def test_tabs_and_newlines(self):
        self.assertEqual(remove_extra_whitespace("a\n\tb"), "a b")

    def test_empty(self):
        self.assertEqual(remove_extra_whitespace(""), "")

    def test_non_string(self):
        with self.assertRaises(TypeError):
            remove_extra_whitespace(7)


class TestRemoveBlankLines(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(remove_blank_lines("a\n\nb\n\n\nc"), "a\nb\nc")

    def test_no_blanks(self):
        self.assertEqual(remove_blank_lines("a\nb\nc"), "a\nb\nc")

    def test_empty(self):
        self.assertEqual(remove_blank_lines(""), "")

    def test_whitespace_only_lines(self):
        self.assertEqual(remove_blank_lines("a\n   \n\tb\n"), "a\n\tb")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            remove_blank_lines(123)  # type: ignore[arg-type]


class TestTruncateWords(unittest.TestCase):
    def test_truncate_with_default_suffix(self):
        self.assertEqual(truncate_words("the quick brown fox", 2), "the quick...")

    def test_custom_suffix(self):
        self.assertEqual(truncate_words("the quick brown fox", 1, suffix="…"), "the…")

    def test_no_truncation(self):
        self.assertEqual(truncate_words("hi", 5), "hi")

    def test_exact_word_count(self):
        self.assertEqual(truncate_words("hi there", 2), "hi there")

    def test_empty_text(self):
        self.assertEqual(truncate_words("", 3), "")

    def test_max_words_zero(self):
        self.assertEqual(truncate_words("hi there", 0), "...")

    def test_collapses_extra_whitespace(self):
        self.assertEqual(truncate_words("  the   quick\tbrown  ", 2), "the quick...")

    def test_single_word_kept_when_max_one(self):
        self.assertEqual(truncate_words("hello", 1), "hello")

    def test_negative_max_words(self):
        with self.assertRaises(ValueError):
            truncate_words("hello", -1)

    def test_boolean_max_words_raises(self):
        with self.assertRaises(TypeError):
            truncate_words("hello", True)  # type: ignore[arg-type]

    def test_non_string_text(self):
        with self.assertRaises(TypeError):
            truncate_words(123, 2)  # type: ignore[arg-type]

    def test_non_string_suffix(self):
        with self.assertRaises(TypeError):
            truncate_words("hello world", 1, suffix=5)  # type: ignore[arg-type]


class TestTitleCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(title_case("hello world"), "Hello World")

    def test_small_words_lowercase(self):
        self.assertEqual(title_case("the quick brown fox"), "The Quick Brown Fox")

    def test_small_words_middle(self):
        self.assertEqual(title_case("war and peace"), "War and Peace")

    def test_first_and_last_capitalized(self):
        self.assertEqual(title_case("the man"), "The Man")

    def test_empty(self):
        self.assertEqual(title_case(""), "")

    def test_custom_small_words(self):
        self.assertEqual(
            title_case("hello world of python", small_words=["of"]),
            "Hello World of Python",
        )

    def test_non_string(self):
        with self.assertRaises(TypeError):
            title_case(True)


if __name__ == "__main__":
    unittest.main()
