"""Unit tests for regex_utils module."""

import re
import unittest

from regex_utils import (
    compile_pattern,
    escape_pattern,
    extract_groups,
    find_all,
    is_valid_pattern,
    match_pattern,
    named_groups,
    replace_pattern,
    search_pattern,
    split_pattern,
)


class TestCompilePattern(unittest.TestCase):
    def test_compiles_valid_pattern(self):
        pattern = compile_pattern(r"\d+")
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.findall("a12b34"), ["12", "34"])

    def test_compiles_with_flags(self):
        pattern = compile_pattern(r"hello", flags=re.IGNORECASE)
        self.assertIsNotNone(pattern.search("HELLO"))

    def test_raises_on_invalid_pattern(self):
        with self.assertRaises(ValueError):
            compile_pattern("(")


class TestIsValidPattern(unittest.TestCase):
    def test_valid_pattern(self):
        self.assertTrue(is_valid_pattern(r"\d+"))
        self.assertTrue(is_valid_pattern(r"[a-z]+"))

    def test_invalid_pattern(self):
        self.assertFalse(is_valid_pattern("("))
        self.assertFalse(is_valid_pattern("["))


class TestMatchPattern(unittest.TestCase):
    def test_match_at_start(self):
        match = match_pattern(r"Hello", "Hello world")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), "Hello")

    def test_no_match_at_start(self):
        self.assertIsNone(match_pattern(r"World", "Hello world"))

    def test_match_with_flags(self):
        match = match_pattern(r"hello", "Hello world", flags=re.IGNORECASE)
        self.assertIsNotNone(match)


class TestSearchPattern(unittest.TestCase):
    def test_search_finds_match(self):
        match = search_pattern(r"world", "Hello world")
        self.assertIsNotNone(match)
        self.assertEqual(match.group(), "world")

    def test_search_no_match(self):
        self.assertIsNone(search_pattern(r"zzz", "Hello world"))


class TestFindAll(unittest.TestCase):
    def test_find_all_matches(self):
        self.assertEqual(find_all(r"\d+", "abc123def456"), ["123", "456"])

    def test_find_all_no_matches(self):
        self.assertEqual(find_all(r"\d+", "no numbers here"), [])


class TestReplacePattern(unittest.TestCase):
    def test_replace_whitespace(self):
        self.assertEqual(replace_pattern(r"\s+", "-", "Hello   world"), "Hello-world")

    def test_replace_no_change(self):
        self.assertEqual(replace_pattern(r"zzz", "x", "abc"), "abc")


class TestSplitPattern(unittest.TestCase):
    def test_split_by_comma(self):
        self.assertEqual(split_pattern(r",\s*", "a, b, c"), ["a", "b", "c"])

    def test_split_no_separator(self):
        self.assertEqual(split_pattern(r",", "abc"), ["abc"])


class TestEscapePattern(unittest.TestCase):
    def test_escape_special_chars(self):
        self.assertEqual(escape_pattern("a.b*c?"), r"a\.b\*c\?")

    def test_escape_plain_text(self):
        self.assertEqual(escape_pattern("hello"), "hello")


class TestExtractGroups(unittest.TestCase):
    def test_extract_captured_groups(self):
        self.assertEqual(
            extract_groups(r"(\d+)-(\d+)", "ID 12-34 here"), ("12", "34")
        )

    def test_extract_no_match(self):
        self.assertIsNone(extract_groups(r"\d+", "no digits"))


class TestNamedGroups(unittest.TestCase):
    def test_extract_named_groups(self):
        result = named_groups(r"(?P<year>\d{4})-(?P<month>\d{2})", "2024-01")
        self.assertEqual(result, {"year": "2024", "month": "01"})

    def test_named_groups_no_match(self):
        self.assertIsNone(named_groups(r"\d+", "no digits"))


if __name__ == "__main__":
    unittest.main()
