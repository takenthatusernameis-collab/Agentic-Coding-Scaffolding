"""Tests for string_utils module."""

import unittest

from string_utils import (
    camel_to_snake,
    dedent_text,
    indent_text,
    is_isogram,
    pluralize,
    remove_blank_lines,
    remove_extra_whitespace,
    slugify,
    snake_to_camel,
    title_case,
    truncate,
    truncate_words,
    wrap_text,
    wrap_words,
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

    def test_whitespace_only(self):
        self.assertEqual(slugify("   "), "")

    def test_unicode_characters(self):
        self.assertEqual(slugify("café & naïve"), "café-naïve")

    def test_consecutive_hyphens(self):
        self.assertEqual(slugify("hello---world"), "hello-world")

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

    def test_non_string_text(self):
        with self.assertRaises(TypeError):
            truncate(123, 5)  # type: ignore[arg-type]

    def test_non_string_suffix(self):
        with self.assertRaises(TypeError):
            truncate("hello", 5, suffix=123)  # type: ignore[arg-type]

    def test_empty_string(self):
        self.assertEqual(truncate("", 5), "")

    def test_single_char(self):
        self.assertEqual(truncate("a", 1), "a")
        self.assertEqual(truncate("a", 0, suffix="..."), "")

    def test_length_less_than_suffix_truncation_case(self):
        # When text needs truncation and length < len(suffix)
        self.assertEqual(truncate("hello", 2, suffix="..."), "..")


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


class TestWrapWords(unittest.TestCase):
    def test_default_width(self):
        text = "a b c d e f g h i j k l m n o p"
        result = wrap_words(text)
        self.assertLessEqual(max(len(line) for line in result.split("\n")), 70)

    def test_custom_width(self):
        self.assertEqual(wrap_words("hello world", 5), "hello\nworld")

    def test_long_word_break(self):
        self.assertEqual(wrap_words("abcdefghij", 4), "abcd\nefgh\nij")

    def test_no_break(self):
        self.assertEqual(wrap_words("abcdefghij", 4, False), "abcdefghij")

    def test_empty_string(self):
        self.assertEqual(wrap_words(""), "")

    def test_single_word(self):
        self.assertEqual(wrap_words("hello", 10), "hello")

    def test_type_error_text(self):
        with self.assertRaises(TypeError):
            wrap_words(123)  # type: ignore[arg-type]

    def test_type_error_width(self):
        with self.assertRaises(TypeError):
            wrap_words("hello", True)  # type: ignore[arg-type]

    def test_value_error_width(self):
        with self.assertRaises(ValueError):
            wrap_words("hello", 0)

    def test_type_error_break_flag(self):
        with self.assertRaises(TypeError):
            wrap_words("hello", 5, "yes")  # type: ignore[arg-type]


class TestSlugifyBoundary(unittest.TestCase):
    def test_very_long_string(self):
        text = "a " * 5000
        result = slugify(text)
        self.assertTrue(result)
        self.assertRegex(result, r"^[a-z0-9-]+$")

    def test_only_punctuation(self):
        self.assertEqual(slugify("!@#$%^&*()"), "")

    def test_slashes_and_dots(self):
        self.assertEqual(slugify("a/b.c d"), "abc-d")

    def test_no_leading_trailing_or_consecutive_hyphens(self):
        result = slugify("  Hello   World  ")
        self.assertFalse(result.startswith("-"))
        self.assertFalse(result.endswith("-"))
        self.assertNotIn("--", result)

    def test_unicode_slug_preserved(self):
        self.assertEqual(slugify("café & naïve"), "café-naïve")

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    slugify(value)  # type: ignore[arg-type]


class TestCamelToSnakeBoundary(unittest.TestCase):
    def test_consecutive_underscores(self):
        self.assertEqual(camel_to_snake("hello__world"), "hello__world")

    def test_leading_and_trailing_underscores(self):
        self.assertEqual(camel_to_snake("_hello_world_"), "_hello_world_")

    def test_single_char(self):
        self.assertEqual(camel_to_snake("a"), "a")
        self.assertEqual(camel_to_snake("A"), "a")

    def test_very_long_string(self):
        text = "A" + "b" * 10000
        self.assertEqual(camel_to_snake(text), "a" + "b" * 10000)

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    camel_to_snake(value)  # type: ignore[arg-type]


class TestSnakeToCamelBoundary(unittest.TestCase):
    def test_consecutive_underscores(self):
        self.assertEqual(snake_to_camel("hello__world"), "helloWorld")

    def test_leading_and_trailing_underscores(self):
        self.assertEqual(snake_to_camel("_hello_world_"), "HelloWorld")

    def test_single_char(self):
        self.assertEqual(snake_to_camel("a"), "a")

    def test_very_long_string(self):
        text = "a_" + "b" * 10000
        self.assertEqual(snake_to_camel(text), "a" + "B" + "b" * 9999)

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    snake_to_camel(value)  # type: ignore[arg-type]


class TestPluralizeBoundary(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(pluralize(""), "s")

    def test_single_char(self):
        self.assertEqual(pluralize("a"), "as")

    def test_unicode_word(self):
        self.assertEqual(pluralize("café"), "cafés")

    def test_count_zero_returns_plural(self):
        self.assertEqual(pluralize("cat", 0), "cats")

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    pluralize(value)  # type: ignore[arg-type]


class TestTruncateBoundary(unittest.TestCase):
    def test_length_zero_with_empty_suffix(self):
        self.assertEqual(truncate("hello", 0, suffix=""), "")

    def test_length_zero_with_nonempty_suffix(self):
        self.assertEqual(truncate("hello", 0), "")

    def test_very_long_suffix(self):
        self.assertEqual(truncate("hello", 10, suffix="x" * 100), "hello")

    def test_length_equals_text_length(self):
        self.assertEqual(truncate("hello", 5), "hello")

    def test_unicode_text(self):
        self.assertEqual(truncate("café au lait", 7), "café...")

    def test_non_string_types(self):
        with self.assertRaises(TypeError):
            truncate(None, 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            truncate("hello", 5, suffix=None)  # type: ignore[arg-type]


class TestWrapTextBoundary(unittest.TestCase):
    def test_width_one(self):
        self.assertEqual(wrap_text("a b c", 1), "a\nb\nc")

    def test_whitespace_only(self):
        self.assertEqual(wrap_text("   ", 5), "")

    def test_very_long_text(self):
        text = "word " * 1000
        result = wrap_text(text, 10)
        self.assertLessEqual(max(len(line) for line in result.split("\n")), 10)

    def test_unicode_text(self):
        self.assertEqual(wrap_text("café naïve", 5), "café\nnaïve")


class TestWrapWordsBoundary(unittest.TestCase):
    def test_width_one(self):
        self.assertEqual(wrap_words("a b c", 1), "a\nb\nc")

    def test_word_exactly_width(self):
        self.assertEqual(wrap_words("abcd efgh", 4), "abcd\nefgh")

    def test_whitespace_only(self):
        self.assertEqual(wrap_words("   \t  ", 5), "")

    def test_single_char_words(self):
        self.assertEqual(wrap_words("a b c d e", 3), "a b\nc d\ne")

    def test_very_long_text(self):
        text = "word " * 1000
        result = wrap_words(text, 10)
        self.assertLessEqual(max(len(line) for line in result.split("\n")), 10)

    def test_width_equals_text_length(self):
        self.assertEqual(wrap_words("hello world", 11), "hello world")


class TestIndentTextBoundary(unittest.TestCase):
    def test_empty_prefix(self):
        self.assertEqual(indent_text("a\nb", ""), "a\nb")

    def test_very_long_prefix(self):
        self.assertEqual(indent_text("a", "-" * 100), "-" * 100 + "a")

    def test_single_line(self):
        self.assertEqual(indent_text("hello", "  "), "  hello")

    def test_non_string_types(self):
        with self.assertRaises(TypeError):
            indent_text(None, "  ")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            indent_text("a", None)  # type: ignore[arg-type]


class TestRemoveExtraWhitespaceBoundary(unittest.TestCase):
    def test_unicode_whitespace(self):
        self.assertEqual(remove_extra_whitespace("a\u00a0b"), "a b")

    def test_very_long_string(self):
        text = "a   b" * 10000
        self.assertEqual(remove_extra_whitespace(text), "a b" * 10000)

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    remove_extra_whitespace(value)  # type: ignore[arg-type]


class TestRemoveBlankLinesBoundary(unittest.TestCase):
    def test_all_blank_lines(self):
        self.assertEqual(remove_blank_lines("\n\n   \n\t\n"), "")

    def test_very_long_text(self):
        text = "\n".join(["line"] * 1000 + [""] * 1000)
        result = remove_blank_lines(text)
        self.assertEqual(result.count("line"), 1000)

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    remove_blank_lines(value)  # type: ignore[arg-type]


class TestTitleCaseBoundary(unittest.TestCase):
    def test_whitespace_only(self):
        self.assertEqual(title_case("   "), "   ")

    def test_single_char(self):
        self.assertEqual(title_case("a"), "A")

    def test_unicode_text(self):
        self.assertEqual(title_case("café au lait"), "Café Au Lait")

    def test_very_long_text(self):
        text = "word " * 10000
        result = title_case(text)
        self.assertEqual(result.count("Word"), 10000)

    def test_all_small_words(self):
        self.assertEqual(
            title_case("the and of", small_words=["the", "and", "of"]),
            "The and Of",
        )

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    title_case(value)  # type: ignore[arg-type]


class TestSlugifyCrossCheck(unittest.TestCase):
    def test_ascii_slug_invariant(self):
        for text in (
            "Hello World",
            "a/b.c d",
            "   ",
            "!@#$",
            "XMLParser2",
            "already-a-slug",
        ):
            result = slugify(text)
            self.assertRegex(result, r"^[a-z0-9-]*$")
            self.assertFalse(result.startswith("-"))
            self.assertFalse(result.endswith("-"))
            self.assertNotIn("--", result)

    def test_unicode_slug_no_bad_hyphens(self):
        result = slugify("café & naïve")
        self.assertEqual(result, "café-naïve")
        self.assertFalse(result.startswith("-"))
        self.assertFalse(result.endswith("-"))
        self.assertNotIn("--", result)


class TestStringUtilsBoundary(unittest.TestCase):
    def test_wrap_words_width_one_break(self):
        self.assertEqual(wrap_words("abc", 1), "a\nb\nc")
        self.assertEqual(wrap_words("a b c", 1), "a\nb\nc")

    def test_wrap_words_width_one_no_break(self):
        self.assertEqual(wrap_words("abc", 1, False), "abc")

    def test_wrap_words_multiple_spaces(self):
        self.assertEqual(wrap_words("hello   world", 5), "hello\nworld")

    def test_wrap_words_tabs(self):
        self.assertEqual(wrap_words("hello\tworld", 5), "hello\nworld")

    def test_wrap_words_whitespace_only(self):
        self.assertEqual(wrap_words("   \t\n  ", 10), "")

    def test_wrap_words_very_long_string(self):
        text = "word " * 2000
        result = wrap_words(text.rstrip(), 10)
        lines = result.split("\n")
        self.assertTrue(all(len(line) <= 10 for line in lines))

    def test_is_isogram_whitespace_only_all_blank(self):
        self.assertTrue(is_isogram("   "))
        self.assertTrue(is_isogram("\t\n\r"))

    def test_is_isogram_unicode_mixed_case(self):
        self.assertTrue(is_isogram("Subdermatoglyphic"))
        self.assertTrue(is_isogram("uncopyrightable"))

    def test_is_isogram_very_long_isogram(self):
        text = "abcdefghijklmnopqrstuvwxyz"
        self.assertTrue(is_isogram(text))
        text2 = "abcdefghijklmnopqrstuvwxyz" * 2  # has repeats
        self.assertFalse(is_isogram(text2))

    def test_is_isogram_punctuation_heavy(self):
        self.assertTrue(is_isogram("a.b,c!d?e;f:g"))
        self.assertFalse(is_isogram("a.b,a!c?d;e:f"))
    def test_lines_respect_width(self):
        text = "The quick brown fox jumps over the lazy dog"
        for width in (1, 5, 10, 20, 70):
            result = wrap_words(text, width)
            for line in result.split("\n"):
                self.assertLessEqual(len(line), width)

    def test_words_preserved_in_order(self):
        text = "one two three four five"
        result = wrap_words(text, 10, break_long_words=False)
        words = result.replace("\n", " ").split()
        self.assertEqual(words, ["one", "two", "three", "four", "five"])


class TestTitleCaseCrossCheck(unittest.TestCase):
    def test_first_and_last_capitalized(self):
        result = title_case("the quick brown fox")
        self.assertEqual(result[0], "T")
        self.assertTrue(result.endswith("Fox"))

    def test_small_words_lowercased_in_middle(self):
        result = title_case("war and peace")
        self.assertIn("and", result)


class TestPluralizeCrossCheck(unittest.TestCase):
    def test_count_one_returns_input(self):
        for word in ("cat", "bus", "baby", "church", "café"):
            self.assertEqual(pluralize(word, 1), word)


class TestIsIsogram(unittest.TestCase):
    def test_isogram(self):
        self.assertTrue(is_isogram("abc"))
        self.assertTrue(is_isogram("abcdefghijklmnopqrstuvwxyz"))
        self.assertTrue(is_isogram("Emily Jung Schwartzkopf"))

    def test_not_isogram(self):
        self.assertFalse(is_isogram("hello"))
        self.assertFalse(is_isogram("bookkeeper"))
        self.assertFalse(is_isogram("aabbcc"))

    def test_case_insensitive(self):
        self.assertFalse(is_isogram("Hh"))
        self.assertFalse(is_isogram("Aa"))
        self.assertTrue(is_isogram("AbC"))

    def test_empty_string(self):
        self.assertTrue(is_isogram(""))

    def test_single_char(self):
        self.assertTrue(is_isogram("a"))
        self.assertTrue(is_isogram("Z"))

    def test_ignores_non_letters(self):
        self.assertTrue(is_isogram("a-b-c"))
        self.assertTrue(is_isogram("a1b2c3"))
        self.assertTrue(is_isogram("a b c"))

    def test_unicode_letters(self):
        self.assertTrue(is_isogram("café"))
        self.assertFalse(is_isogram("caféfé"))

    def test_whitespace_only(self):
        self.assertTrue(is_isogram("   "))
        self.assertTrue(is_isogram("\t\n"))

    def test_non_string(self):
        with self.assertRaises(TypeError):
            is_isogram(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_isogram(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_isogram(["a"])  # type: ignore[arg-type]

    def test_very_long_string(self):
        text = "".join(chr(97 + i % 26) for i in range(1000))
        self.assertFalse(is_isogram(text))


class TestDedentText(unittest.TestCase):
    def test_basic_dedent(self):
        self.assertEqual(dedent_text("    hello\n      world"), "hello\n  world")

    def test_blank_lines_untouched(self):
        self.assertEqual(
            dedent_text("\n    hello\n\n    world\n"),
            "\nhello\n\nworld\n",
        )

    def test_no_indent(self):
        self.assertEqual(dedent_text("no indent"), "no indent")

    def test_empty_string(self):
        self.assertEqual(dedent_text(""), "")

    def test_tabs_count_as_four(self):
        # The common indent is 2 (from "  world"); the leading tab on the
        # first line counts as 4, so it is fully consumed by the 2-space strip.
        self.assertEqual(dedent_text("\thello\n  world"), "hello\nworld")

    def test_single_line(self):
        self.assertEqual(dedent_text("    hello"), "hello")

    def test_uneven_indent_keeps_relative(self):
        self.assertEqual(
            dedent_text("  a\n    b\n      c"),
            "a\n  b\n    c",
        )

    def test_invariant_round_trip(self):
        text = "line one\nline two\nline three"
        indented = indent_text(text, "    ")
        self.assertEqual(dedent_text(indented), text)

    def test_non_string_types(self):
        for value in (None, 123, 3.14, ["a"], {"a": 1}):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    dedent_text(value)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
