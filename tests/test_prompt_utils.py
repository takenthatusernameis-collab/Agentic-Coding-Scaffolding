"""Unit tests for prompt_utils module."""

import unittest

from prompt_utils import (
    clean_prompt,
    collapse_blank_lines,
    count_blank_lines,
    count_characters,
    count_consonants,
    count_digits,
    count_leading_newlines,
    count_letters,
    count_lines,
    count_non_blank_lines,
    count_non_whitespace_characters,
    count_paragraphs,
    count_placeholders,
    count_sentences,
    count_trailing_newlines,
    count_unique_words,
    count_vowels,
    count_whitespace_characters,
    count_words,
    dedent_lines,
    ensure_leading_newline,
    ensure_surrounded_by_newlines,
    ensure_trailing_newline,
    estimate_token_count,
    extract_keywords,
    extract_placeholders,
    first_line,
    format_prompt_template,
    has_placeholders,
    indent_lines,
    last_line,
    lstrip_lines,
    normalize_line_endings,
    remove_blank_lines,
    reverse_lines,
    rstrip_lines,
    strip_blank_lines,
    strip_leading_newlines,
    strip_lines,
    strip_trailing_newlines,
    truncate_lines,
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


class TestIndentLines(unittest.TestCase):
    def test_basic(self):
        result = indent_lines("a\nb\nc")
        self.assertEqual(result, "    a\n    b\n    c")

    def test_custom_prefix(self):
        result = indent_lines("a\nb", prefix="> ")
        self.assertEqual(result, "> a\n> b")

    def test_skip_blank_default_off(self):
        result = indent_lines("a\n\nb")
        self.assertEqual(result, "    a\n    \n    b")

    def test_skip_blank_true(self):
        result = indent_lines("a\n\nb", skip_blank=True)
        self.assertEqual(result, "    a\n\n    b")

    def test_empty(self):
        self.assertEqual(indent_lines(""), "")

    def test_rejects_non_str_text(self):
        with self.assertRaises(TypeError):
            indent_lines(123)  # type: ignore[arg-type]

    def test_rejects_non_str_prefix(self):
        with self.assertRaises(TypeError):
            indent_lines("a", prefix=123)  # type: ignore[arg-type]

    def test_rejects_non_bool_skip_blank(self):
        with self.assertRaises(TypeError):
            indent_lines("a", skip_blank="yes")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()

class TestDedentLines(unittest.TestCase):
    def test_basic(self):
        result = dedent_lines("    a\n      b")
        self.assertEqual(result, "a\n  b")

    def test_empty(self):
        self.assertEqual(dedent_lines(""), "")

    def test_no_indent(self):
        self.assertEqual(dedent_lines("hello\nworld"), "hello\nworld")

    def test_skip_blank_lines(self):
        result = dedent_lines("\n    hello\n\n    world\n")
        self.assertEqual(result, "\nhello\n\nworld\n")

    def test_rejects_non_str(self):
        with self.assertRaises(TypeError):
            dedent_lines(123)  # type: ignore[arg-type]


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


class TestRstripLines(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(rstrip_lines("hello   \nworld  \n"), "hello\nworld\n")

    def test_no_trailing(self):
        self.assertEqual(rstrip_lines("no trailing"), "no trailing")

    def test_empty(self):
        self.assertEqual(rstrip_lines(""), "")

    def test_whitespace_only_lines(self):
        self.assertEqual(rstrip_lines("   \n\t\n"), "\n\n")

    def test_mixed_spaces_and_tabs(self):
        self.assertEqual(rstrip_lines("a \t\nb\t "), "a\nb")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            rstrip_lines(123)  # type: ignore[arg-type]


class TestLstripLines(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(lstrip_lines("   hello\n  world\n"), "hello\nworld\n")

    def test_no_leading(self):
        self.assertEqual(lstrip_lines("no leading"), "no leading")

    def test_empty(self):
        self.assertEqual(lstrip_lines(""), "")

    def test_whitespace_only_lines(self):
        self.assertEqual(lstrip_lines("   \n\t\n"), "\n\n")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            lstrip_lines(123)  # type: ignore[arg-type]


class TestStripLines(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(strip_lines("   hello   \n  world  \n"), "hello\nworld\n")

    def test_no_trim(self):
        self.assertEqual(strip_lines("no trim"), "no trim")

    def test_empty(self):
        self.assertEqual(strip_lines(""), "")

    def test_whitespace_only_lines(self):
        self.assertEqual(strip_lines("   \n\t\n"), "\n\n")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            strip_lines(123)  # type: ignore[arg-type]


class TestEnsureLeadingNewline(unittest.TestCase):
    def test_adds_newline(self):
        self.assertEqual(ensure_leading_newline("hello"), "\nhello")

    def test_keeps_existing_newline(self):
        self.assertEqual(ensure_leading_newline("\nhello"), "\nhello")

    def test_empty_string(self):
        self.assertEqual(ensure_leading_newline(""), "")

    def test_multiple_newlines(self):
        self.assertEqual(ensure_leading_newline("\n\nhello"), "\n\nhello")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            ensure_leading_newline(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ensure_leading_newline(None)  # type: ignore[arg-type]


class TestEnsureTrailingNewline(unittest.TestCase):
    def test_adds_newline(self):
        self.assertEqual(ensure_trailing_newline("hello"), "hello\n")

    def test_keeps_existing_newline(self):
        self.assertEqual(ensure_trailing_newline("hello\n"), "hello\n")

    def test_empty_string(self):
        self.assertEqual(ensure_trailing_newline(""), "")

    def test_multiple_newlines(self):
        self.assertEqual(ensure_trailing_newline("hello\n\n"), "hello\n\n")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            ensure_trailing_newline(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ensure_trailing_newline(None)  # type: ignore[arg-type]


class TestEnsureSurroundedByNewlines(unittest.TestCase):
    def test_wraps(self):
        self.assertEqual(ensure_surrounded_by_newlines("hello"), "\nhello\n")

    def test_keeps_existing(self):
        self.assertEqual(ensure_surrounded_by_newlines("\nhello\n"), "\nhello\n")

    def test_empty_string(self):
        self.assertEqual(ensure_surrounded_by_newlines(""), "")

    def test_leading_only(self):
        self.assertEqual(ensure_surrounded_by_newlines("hello\n"), "\nhello\n")

    def test_trailing_only(self):
        self.assertEqual(ensure_surrounded_by_newlines("\nhello"), "\nhello\n")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            ensure_surrounded_by_newlines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ensure_surrounded_by_newlines(None)  # type: ignore[arg-type]


class TestFirstLine(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(first_line("hello\nworld"), "hello")

    def test_single_line(self):
        self.assertEqual(first_line("single"), "single")

    def test_empty(self):
        self.assertEqual(first_line(""), "")

    def test_crlf(self):
        self.assertEqual(first_line("a\r\nb"), "a")

    def test_cr(self):
        self.assertEqual(first_line("a\rb"), "a")

    def test_ends_with_newline(self):
        self.assertEqual(first_line("hello\n"), "hello")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            first_line(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            first_line(None)  # type: ignore[arg-type]


class TestLastLine(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(last_line("hello\nworld"), "world")

    def test_single_line(self):
        self.assertEqual(last_line("single"), "single")

    def test_empty(self):
        self.assertEqual(last_line(""), "")

    def test_crlf(self):
        self.assertEqual(last_line("a\r\nb"), "b")

    def test_cr(self):
        self.assertEqual(last_line("a\rb"), "b")

    def test_ends_with_newline(self):
        self.assertEqual(last_line("hello\n"), "hello")

    def test_trailing_newlines(self):
        self.assertEqual(last_line("hello\n\n"), "")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            last_line(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            last_line(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestCountLines(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_lines(""), 0)

    def test_single(self):
        self.assertEqual(count_lines("hello"), 1)

    def test_multiple(self):
        self.assertEqual(count_lines("hello\nworld"), 2)

    def test_trailing_newline(self):
        self.assertEqual(count_lines("hello\n"), 1)

    def test_crlf(self):
        self.assertEqual(count_lines("a\r\nb"), 2)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_lines(123)  # type: ignore[arg-type]


class TestCountBlankLines(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_blank_lines(""), 0)

    def test_no_blank_lines(self):
        self.assertEqual(count_blank_lines("hello\nworld"), 0)

    def test_blank_line_between(self):
        self.assertEqual(count_blank_lines("hello\n\nworld"), 1)

    def test_whitespace_only_line(self):
        self.assertEqual(count_blank_lines("hello\n   \n\t\nworld"), 2)

    def test_all_blank(self):
        self.assertEqual(count_blank_lines("\n\n"), 2)

    def test_crlf(self):
        self.assertEqual(count_blank_lines("a\r\n\r\nb"), 1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_blank_lines(123)  # type: ignore[arg-type]


class TestCountNonBlankLines(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_non_blank_lines(""), 0)

    def test_single_non_blank(self):
        self.assertEqual(count_non_blank_lines("hello"), 1)

    def test_multiple_non_blank(self):
        self.assertEqual(count_non_blank_lines("hello\nworld"), 2)

    def test_trailing_newline(self):
        self.assertEqual(count_non_blank_lines("hello\n"), 1)

    def test_blank_lines_excluded(self):
        self.assertEqual(count_non_blank_lines("hello\n\nworld"), 2)

    def test_whitespace_only_lines_excluded(self):
        self.assertEqual(count_non_blank_lines("hello\n   \n\t\nworld"), 2)

    def test_all_blank(self):
        self.assertEqual(count_non_blank_lines("\n\n"), 0)

    def test_crlf(self):
        self.assertEqual(count_non_blank_lines("a\r\n\r\nb"), 2)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_non_blank_lines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_non_blank_lines(None)  # type: ignore[arg-type]


class TestCountTrailingNewlines(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_trailing_newlines(""), 0)

    def test_no_trailing_newlines(self):
        self.assertEqual(count_trailing_newlines("hello"), 0)

    def test_single_trailing_newline(self):
        self.assertEqual(count_trailing_newlines("hello\n"), 1)

    def test_multiple_trailing_newlines(self):
        self.assertEqual(count_trailing_newlines("hello\n\n"), 2)

    def test_trailing_newlines_after_content(self):
        self.assertEqual(count_trailing_newlines("a\nb\n\n\n"), 3)

    def test_crlf_counts_one_newline(self):
        self.assertEqual(count_trailing_newlines("hello\r\n"), 1)

    def test_trailing_spaces_not_counted(self):
        self.assertEqual(count_trailing_newlines("hello   \n"), 1)

    def test_only_newlines(self):
        self.assertEqual(count_trailing_newlines("\n\n\n"), 3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_trailing_newlines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_trailing_newlines(None)  # type: ignore[arg-type]


class TestCountLeadingNewlines(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_leading_newlines(""), 0)

    def test_no_leading_newlines(self):
        self.assertEqual(count_leading_newlines("hello"), 0)

    def test_single_leading_newline(self):
        self.assertEqual(count_leading_newlines("\nhello"), 1)

    def test_multiple_leading_newlines(self):
        self.assertEqual(count_leading_newlines("\n\nhello"), 2)

    def test_leading_newlines_before_content(self):
        self.assertEqual(count_leading_newlines("\n\n\na\nb"), 3)

    def test_only_newlines(self):
        self.assertEqual(count_leading_newlines("\n\n\n"), 3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_leading_newlines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_leading_newlines(None)  # type: ignore[arg-type]


class TestCountParagraphs(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_paragraphs(""), 0)

    def test_single_paragraph(self):
        self.assertEqual(count_paragraphs("hello"), 1)

    def test_multiple_lines_one_paragraph(self):
        self.assertEqual(count_paragraphs("hello\nworld"), 1)

    def test_two_paragraphs(self):
        self.assertEqual(count_paragraphs("hello\n\nworld"), 2)

    def test_three_paragraphs(self):
        self.assertEqual(count_paragraphs("a\n\nb\n\nc"), 3)

    def test_multiple_blank_lines_still_one_separator(self):
        self.assertEqual(count_paragraphs("hello\n\n\nworld"), 2)

    def test_trailing_blank_lines_ignored(self):
        self.assertEqual(count_paragraphs("hello\n\n"), 1)
        self.assertEqual(count_paragraphs("hello\n\n\n"), 1)

    def test_all_blank(self):
        self.assertEqual(count_paragraphs("\n\n"), 0)

    def test_crlf(self):
        self.assertEqual(count_paragraphs("a\r\n\r\nb"), 2)

    def test_whitespace_only_separator(self):
        self.assertEqual(count_paragraphs("hello\n   \n\t\nworld"), 2)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_paragraphs(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_paragraphs(None)  # type: ignore[arg-type]


class TestCountWords(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_words(""), 0)

    def test_single_word(self):
        self.assertEqual(count_words("hello"), 1)

    def test_multiple_words(self):
        self.assertEqual(count_words("Hello world"), 2)

    def test_multiple_whitespace(self):
        self.assertEqual(count_words("a   b\tc\n  d"), 4)

    def test_leading_trailing_whitespace(self):
        self.assertEqual(count_words("  hello  "), 1)

    def test_unicode(self):
        self.assertEqual(count_words("héllo wörld"), 2)

    def test_punctuation(self):
        self.assertEqual(count_words("one, two! three?"), 3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_words(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_words(None)  # type: ignore[arg-type]


class TestTruncateLines(unittest.TestCase):
    def test_no_truncation(self):
        self.assertEqual(truncate_lines("a\nb\nc", 5), "a\nb\nc")

    def test_exact_lines(self):
        self.assertEqual(truncate_lines("a\nb\nc", 3), "a\nb\nc")

    def test_truncates(self):
        self.assertEqual(truncate_lines("a\nb\nc\nd", 2), "a\nb...")

    def test_zero_lines(self):
        self.assertEqual(truncate_lines("a\nb", 0), "...")

    def test_zero_lines_default_suffix(self):
        self.assertEqual(truncate_lines("a\nb", 0, suffix="..."), "...")

    def test_custom_suffix(self):
        self.assertEqual(truncate_lines("a\nb\nc\nd", 2, suffix=" <more>"), "a\nb <more>")

    def test_empty_suffix(self):
        self.assertEqual(truncate_lines("a\nb\nc", 1, suffix=""), "a")

    def test_single_line_kept(self):
        self.assertEqual(truncate_lines("only", 1), "only")

    def test_negative_lines(self):
        with self.assertRaises(ValueError):
            truncate_lines("a\nb", -1)

    def test_non_str_text(self):
        with self.assertRaises(TypeError):
            truncate_lines(123, 1)  # type: ignore[arg-type]

    def test_non_int_max_lines(self):
        with self.assertRaises(TypeError):
            truncate_lines("a\nb", "two")  # type: ignore[arg-type]

    def test_non_str_suffix(self):
        with self.assertRaises(TypeError):
            truncate_lines("a\nb", 1, suffix=5)  # type: ignore[arg-type]


class TestNormalizeLineEndings(unittest.TestCase):
    def test_no_change(self):
        self.assertEqual(normalize_line_endings("a\nb\nc"), "a\nb\nc")

    def test_crlf(self):
        self.assertEqual(normalize_line_endings("a\r\nb\r\nc"), "a\nb\nc")

    def test_lone_cr(self):
        self.assertEqual(normalize_line_endings("a\rb\rc"), "a\nb\nc")

    def test_mixed(self):
        self.assertEqual(normalize_line_endings("a\r\nb\rc\nd"), "a\nb\nc\nd")

    def test_empty(self):
        self.assertEqual(normalize_line_endings(""), "")

    def test_only_crlf(self):
        self.assertEqual(normalize_line_endings("\r\n\r\n"), "\n\n")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            normalize_line_endings(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            normalize_line_endings(None)  # type: ignore[arg-type]


class TestCountCharacters(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_characters(""), 0)

    def test_ascii(self):
        self.assertEqual(count_characters("Hello world"), 11)

    def test_whitespace_counted(self):
        self.assertEqual(count_characters("a b"), 3)

    def test_unicode(self):
        self.assertEqual(count_characters("héllo"), 5)
        self.assertEqual(count_characters("🚀"), 1)

    def test_single_character(self):
        self.assertEqual(count_characters("x"), 1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_characters(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_characters(None)  # type: ignore[arg-type]


class TestReverseLines(unittest.TestCase):
    def test_multiple_lines(self):
        self.assertEqual(reverse_lines("a\nb\nc"), "c\nb\na")

    def test_single_line(self):
        self.assertEqual(reverse_lines("single"), "single")

    def test_empty(self):
        self.assertEqual(reverse_lines(""), "")

    def test_preserves_content(self):
        self.assertEqual(reverse_lines("first\nsecond\nthird"), "third\nsecond\nfirst")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            reverse_lines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            reverse_lines(None)  # type: ignore[arg-type]


class TestStripBlankLines(unittest.TestCase):
    def test_outer_blank_lines_removed(self):
        self.assertEqual(strip_blank_lines("\n\nhello\nworld\n\n"), "hello\nworld")

    def test_no_blank_lines(self):
        self.assertEqual(strip_blank_lines("hello"), "hello")

    def test_all_blank(self):
        self.assertEqual(strip_blank_lines("\n\n"), "")

    def test_whitespace_only_lines_are_blank(self):
        self.assertEqual(strip_blank_lines("  \nhello\n\t\n"), "hello")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            strip_blank_lines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            strip_blank_lines(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestCountUniqueWords(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_unique_words(""), 0)

    def test_single_word(self):
        self.assertEqual(count_unique_words("hello"), 1)

    def test_duplicates(self):
        self.assertEqual(count_unique_words("hello world hello"), 2)

    def test_case_sensitive(self):
        self.assertEqual(count_unique_words("Hello hello"), 2)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_unique_words(123)


class TestStripTrailingNewlines(unittest.TestCase):
    def test_removes_trailing_newlines(self):
        self.assertEqual(strip_trailing_newlines("hello\n\n"), "hello")

    def test_no_trailing_newlines(self):
        self.assertEqual(strip_trailing_newlines("hello"), "hello")

    def test_empty(self):
        self.assertEqual(strip_trailing_newlines(""), "")

    def test_only_newlines(self):
        self.assertEqual(strip_trailing_newlines("\n\n\n"), "")

    def test_preserves_other_trailing_whitespace(self):
        self.assertEqual(strip_trailing_newlines("hello \t\n"), "hello \t")

    def test_type_error(self):
        with self.assertRaises(TypeError):
            strip_trailing_newlines(123)  # type: ignore[arg-type]


class TestStripLeadingNewlines(unittest.TestCase):
    def test_removes_leading_newlines(self):
        self.assertEqual(strip_leading_newlines("\n\nhello"), "hello")

    def test_removes_single_leading_newline(self):
        self.assertEqual(strip_leading_newlines("\nhello"), "hello")

    def test_no_leading_newlines(self):
        self.assertEqual(strip_leading_newlines("hello"), "hello")

    def test_empty_string(self):
        self.assertEqual(strip_leading_newlines(""), "")

    def test_only_newlines(self):
        self.assertEqual(strip_leading_newlines("\n\n\n"), "")

    def test_preserves_other_leading_whitespace(self):
        self.assertEqual(strip_leading_newlines("  \thello"), "  \thello")

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            strip_leading_newlines(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            strip_leading_newlines(None)  # type: ignore[arg-type]


class TestCountNonWhitespaceCharacters(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_non_whitespace_characters(""), 0)

    def test_only_whitespace(self):
        self.assertEqual(count_non_whitespace_characters("   \t\n\r"), 0)

    def test_no_whitespace(self):
        self.assertEqual(count_non_whitespace_characters("abc"), 3)

    def test_mixed(self):
        self.assertEqual(count_non_whitespace_characters("Hello world"), 10)

    def test_with_newlines_and_tabs(self):
        self.assertEqual(count_non_whitespace_characters("a b\nc\td"), 4)

    def test_unicode(self):
        self.assertEqual(count_non_whitespace_characters("héllo"), 5)
        self.assertEqual(count_non_whitespace_characters("🚀"), 1)

    def test_single_character(self):
        self.assertEqual(count_non_whitespace_characters("x"), 1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_non_whitespace_characters(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_non_whitespace_characters(None)  # type: ignore[arg-type]


class TestCountWhitespaceCharacters(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_whitespace_characters(""), 0)

    def test_only_whitespace(self):
        self.assertEqual(count_whitespace_characters("   \t\n\r"), 6)

    def test_no_whitespace(self):
        self.assertEqual(count_whitespace_characters("abc"), 0)

    def test_mixed(self):
        self.assertEqual(count_whitespace_characters("Hello world"), 1)

    def test_with_newlines_and_tabs(self):
        self.assertEqual(count_whitespace_characters("a b\nc\td"), 3)

    def test_unicode(self):
        self.assertEqual(count_whitespace_characters("héllo"), 0)

    def test_single_whitespace(self):
        self.assertEqual(count_whitespace_characters(" "), 1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_whitespace_characters(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_whitespace_characters(None)  # type: ignore[arg-type]


class TestCountDigits(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_digits(""), 0)

    def test_no_digits(self):
        self.assertEqual(count_digits("abc def"), 0)

    def test_only_digits(self):
        self.assertEqual(count_digits("123"), 3)

    def test_mixed(self):
        self.assertEqual(count_digits("a1b2c3"), 3)

    def test_leading_zeros(self):
        self.assertEqual(count_digits("007"), 3)

    def test_digits_with_spaces(self):
        self.assertEqual(count_digits("1 2 3"), 3)

    def test_unicode_digits_not_counted(self):
        self.assertEqual(count_digits("٣٤٥"), 0)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_digits(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_digits(None)  # type: ignore[arg-type]
class TestCountLetters(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_letters(""), 0)

    def test_no_letters(self):
        self.assertEqual(count_letters("123 !"), 0)

    def test_only_letters(self):
        self.assertEqual(count_letters("abc"), 3)

    def test_mixed(self):
        self.assertEqual(count_letters("a1b2c3"), 3)

    def test_upper_and_lower(self):
        self.assertEqual(count_letters("AbC"), 3)

    def test_unicode_letters_not_counted(self):
        self.assertEqual(count_letters("αβγ"), 0)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_letters(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_letters(None)  # type: ignore[arg-type]


class TestCountVowels(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_vowels(""), 0)

    def test_no_vowels(self):
        self.assertEqual(count_vowels("xyz"), 0)
        self.assertEqual(count_vowels("bcdfg"), 0)

    def test_only_vowels(self):
        self.assertEqual(count_vowels("aeiou"), 5)
        self.assertEqual(count_vowels("AEIOU"), 5)

    def test_mixed(self):
        self.assertEqual(count_vowels("hello"), 2)
        self.assertEqual(count_vowels("HELLO WORLD"), 3)
        self.assertEqual(count_vowels("a1b2c3"), 1)

    def test_case_insensitive(self):
        self.assertEqual(count_vowels("AeIoU"), 5)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_vowels(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_vowels(None)  # type: ignore[arg-type]


class TestCountConsonants(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(count_consonants(""), 0)

    def test_no_consonants(self):
        self.assertEqual(count_consonants("aeiou"), 0)
        self.assertEqual(count_consonants("AEIOU"), 0)

    def test_only_consonants(self):
        self.assertEqual(count_consonants("bcdfg"), 5)
        self.assertEqual(count_consonants("BCDFG"), 5)

    def test_mixed(self):
        self.assertEqual(count_consonants("hello"), 3)
        self.assertEqual(count_consonants("HELLO WORLD"), 7)
        self.assertEqual(count_consonants("a1b2c3"), 2)

    def test_case_insensitive(self):
        self.assertEqual(count_consonants("BcDfG"), 5)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_consonants(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_consonants(None)  # type: ignore[arg-type]
