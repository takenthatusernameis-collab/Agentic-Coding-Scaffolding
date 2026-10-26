"""Unit tests for prompt_utils module."""

import unittest

from prompt_utils import (
    clean_prompt,
    collapse_blank_lines,
    count_placeholders,
    count_sentences,
    estimate_token_count,
    extract_keywords,
    extract_placeholders,
    format_prompt_template,
    has_placeholders,
    truncate_prompt,
    truncate_words,
    wrap_prompt,
)


class TestTruncatePrompt(unittest.TestCase):
    def test_truncate_short_text(self):
        result = truncate_prompt("Hello", 10)
        self.assertEqual(result, "Hello")

    def test_truncate_long_text(self):
        result = truncate_prompt("Hello world", 8)
        self.assertEqual(result, "Hello...")

    def test_truncate_with_custom_suffix(self):
        result = truncate_prompt("Hello world", 8, suffix="***")
        self.assertEqual(result, "Hello***")

    def test_truncate_when_suffix_too_long(self):
        result = truncate_prompt("Hello", 2, suffix="...")
        self.assertEqual(result, "He")

    def test_truncate_rejects_non_str_text(self):
        with self.assertRaises(TypeError):
            truncate_prompt(123, 10)  # type: ignore[arg-type]

    def test_truncate_rejects_non_int_max_length(self):
        with self.assertRaises(TypeError):
            truncate_prompt("Hello", 1.5)  # type: ignore[arg-type]

    def test_truncate_rejects_non_str_suffix(self):
        with self.assertRaises(TypeError):
            truncate_prompt("Hello", 10, suffix=5)  # type: ignore[arg-type]

    def test_truncate_rejects_negative_max_length(self):
        with self.assertRaises(ValueError):
            truncate_prompt("Hello", -1)


class TestFormatPromptTemplate(unittest.TestCase):
    def test_format_template(self):
        result = format_prompt_template(
            "Hello {name}, {greeting}!",
            name="Alice",
            greeting="welcome",
        )
        self.assertEqual(result, "Hello Alice, welcome!")

    def test_format_template_multiple(self):
        result = format_prompt_template("{a} {b} {c}", a=1, b=2, c=3)
        self.assertEqual(result, "1 2 3")

    def test_format_template_rejects_non_str(self):
        with self.assertRaises(TypeError):
            format_prompt_template(123)  # type: ignore[arg-type]

    def test_format_template_missing_key(self):
        with self.assertRaises(ValueError):
            format_prompt_template("Hello {name}!")


class TestCleanPrompt(unittest.TestCase):
    def test_clean_whitespace(self):
        result = clean_prompt("Hello   world\n\nTest")
        self.assertEqual(result, "Hello world Test")

    def test_clean_leading_trailing(self):
        result = clean_prompt("   Hello   ")
        self.assertEqual(result, "Hello")

    def test_clean_rejects_non_str(self):
        with self.assertRaises(TypeError):
            clean_prompt(None)  # type: ignore[arg-type]


class TestExtractKeywords(unittest.TestCase):
    def test_extract_keywords_basic(self):
        result = extract_keywords("The quick brown fox jumps over lazy dogs")
        self.assertIn("quick", result)
        self.assertIn("brown", result)
        self.assertIn("jumps", result)

    def test_extract_keywords_min_length(self):
        result = extract_keywords("hi there how are you", min_length=3)
        self.assertNotIn("hi", result)

    def test_extract_keywords_no_duplicates(self):
        result = extract_keywords("test test testing")
        # "test" appears twice, "testing" once - both >=4? "test" is 4 chars, "testing" is 7
        self.assertEqual(result.count("test"), 1)

    def test_extract_keywords_rejects_non_str(self):
        with self.assertRaises(TypeError):
            extract_keywords(123)  # type: ignore[arg-type]

    def test_extract_keywords_rejects_non_int_min_length(self):
        with self.assertRaises(TypeError):
            extract_keywords("hello", min_length=1.5)  # type: ignore[arg-type]

    def test_extract_keywords_rejects_negative_min_length(self):
        with self.assertRaises(ValueError):
            extract_keywords("hello", min_length=-1)


class TestWrapPrompt(unittest.TestCase):
    def test_wrap_short_text(self):
        result = wrap_prompt("Hello world", 80)
        self.assertEqual(result, "Hello world")

    def test_wrap_long_text(self):
        result = wrap_prompt("This is a very long line that needs wrapping", 20)
        self.assertIn("\n", result)

    def test_wrap_zero_width(self):
        result = wrap_prompt("Hello", 0)
        self.assertEqual(result, "Hello")

    def test_wrap_rejects_non_str(self):
        with self.assertRaises(TypeError):
            wrap_prompt(123, 80)  # type: ignore[arg-type]

    def test_wrap_rejects_non_int_width(self):
        with self.assertRaises(TypeError):
            wrap_prompt("Hello", 1.5)  # type: ignore[arg-type]

    def test_wrap_rejects_negative_width(self):
        with self.assertRaises(ValueError):
            wrap_prompt("Hello", -1)


class TestEstimateTokenCount(unittest.TestCase):
    def test_estimate_empty(self):
        self.assertEqual(estimate_token_count(""), 0)

    def test_estimate_basic(self):
        result = estimate_token_count("Hello world")  # 11 chars / 4 = ~2-3
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 10)

    def test_estimate_long_text(self):
        text = "This is a longer piece of text for testing token estimation"
        result = estimate_token_count(text)
        self.assertGreater(result, 5)

    def test_estimate_rejects_non_str(self):
        with self.assertRaises(TypeError):
            estimate_token_count(None)  # type: ignore[arg-type]


class TestExtractPlaceholders(unittest.TestCase):
    def test_extract_placeholders_basic(self):
        result = extract_placeholders("Hello {name}, welcome to {place}!")
        self.assertEqual(result, ["name", "place"])

    def test_extract_placeholders_duplicate_names(self):
        result = extract_placeholders("{a} {b} {a} {c}")
        self.assertEqual(result, ["a", "b", "c"])

    def test_extract_placeholders_none(self):
        result = extract_placeholders("No placeholders here")
        self.assertEqual(result, [])

    def test_extract_placeholders_empty(self):
        result = extract_placeholders("")
        self.assertEqual(result, [])

    def test_extract_placeholders_rejects_non_str(self):
        with self.assertRaises(TypeError):
            extract_placeholders(123)  # type: ignore[arg-type]


class TestHasPlaceholders(unittest.TestCase):
    def test_has_placeholders_true(self):
        self.assertTrue(has_placeholders("Hello {name}!"))
        self.assertTrue(has_placeholders("{a} {b} {a}"))

    def test_has_placeholders_false(self):
        self.assertFalse(has_placeholders("No placeholders here"))
        self.assertFalse(has_placeholders(""))
        self.assertFalse(has_placeholders("just text"))

    def test_has_placeholders_matches_count(self):
        self.assertEqual(has_placeholders("Hello {name}, {greeting}!"), True)
        self.assertEqual(has_placeholders("plain"), False)

    def test_has_placeholders_rejects_non_str(self):
        with self.assertRaises(TypeError):
            has_placeholders(123)  # type: ignore[arg-type]


class TestCollapseBlankLines(unittest.TestCase):
    def test_collapses_three(self):
        self.assertEqual(collapse_blank_lines("a\n\n\nb"), "a\n\nb")

    def test_collapses_many(self):
        self.assertEqual(collapse_blank_lines("a\n\n\n\n\nb"), "a\n\nb")

    def test_no_change(self):
        self.assertEqual(collapse_blank_lines("a\nb"), "a\nb")

    def test_empty(self):
        self.assertEqual(collapse_blank_lines(""), "")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            collapse_blank_lines(123)  # type: ignore[arg-type]


class TestCountPlaceholders(unittest.TestCase):
    def test_counts_occurrences(self):
        self.assertEqual(count_placeholders("Hello {name}, {greeting}!"), 2)

    def test_counts_duplicates(self):
        self.assertEqual(count_placeholders("{a} {b} {a}"), 3)

    def test_no_placeholders(self):
        self.assertEqual(count_placeholders("No placeholders"), 0)

    def test_empty(self):
        self.assertEqual(count_placeholders(""), 0)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_placeholders(123)  # type: ignore[arg-type]



class TestCountSentences(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_sentences("Hello world. How are you?"), 2)

    def test_empty(self):
        self.assertEqual(count_sentences(""), 0)

    def test_whitespace(self):
        self.assertEqual(count_sentences("   "), 0)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_sentences(123)  # type: ignore[arg-type]


class TestTruncateWords(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(truncate_words("one two three four", 2), "one two...")

    def test_no_truncation(self):
        self.assertEqual(truncate_words("short text", 5), "short text")

    def test_zero(self):
        self.assertEqual(truncate_words("one two", 0), "...")

    def test_negative(self):
        with self.assertRaises(ValueError):
            truncate_words("a b", -1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            truncate_words(123, 2)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
