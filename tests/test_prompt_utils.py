"""Unit tests for prompt_utils module."""

import unittest

from prompt_utils import (
    clean_prompt,
    estimate_token_count,
    extract_keywords,
    format_prompt_template,
    truncate_prompt,
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


if __name__ == "__main__":
    unittest.main()
