"""Tests for re_utils module."""

import re
import unittest

from re_utils import (
    compile_regex,
    escape,
    find_all,
    find_matches,
    full_match,
    match,
    search,
    split,
    sub,
    subn,
)


class TestFindAll(unittest.TestCase):
    def test_find_all_basic(self):
        result = find_all(r"\d+", "hello 123 world 456")
        self.assertEqual(result, ["123", "456"])

    def test_find_all_with_pattern_object(self):
        pattern = re.compile(r"[a-z]+")
        result = find_all(pattern, "Hello World")
        self.assertEqual(result, ["ello", "orld"])

    def test_find_all_invalid_pattern(self):
        with self.assertRaises(TypeError):
            find_all(123, "text")

    def test_find_all_invalid_text(self):
        with self.assertRaises(TypeError):
            find_all(r"\d+", 123)


class TestFindMatches(unittest.TestCase):
    def test_find_matches_basic(self):
        matches = find_matches(r"\d+", "a1b22c333")
        self.assertEqual(len(matches), 3)
        self.assertEqual([m.group() for m in matches], ["1", "22", "333"])

    def test_find_matches_with_pattern_object(self):
        matches = find_matches(re.compile(r"\w+"), "hello world")
        self.assertEqual(len(matches), 2)


class TestSearch(unittest.TestCase):
    def test_search_found(self):
        result = search(r"world", "hello world")
        self.assertIsInstance(result, re.Match)
        self.assertEqual(result.group(), "world")

    def test_search_not_found(self):
        result = search(r"xyz", "hello world")
        self.assertIsNone(result)


class TestMatch(unittest.TestCase):
    def test_match_at_start(self):
        result = match(r"hello", "hello world")
        self.assertIsInstance(result, re.Match)

    def test_match_not_at_start(self):
        result = match(r"world", "hello world")
        self.assertIsNone(result)


class TestFullMatch(unittest.TestCase):
    def test_full_match(self):
        result = full_match(r"\d+", "12345")
        self.assertIsInstance(result, re.Match)

    def test_full_match_partial(self):
        result = full_match(r"\d+", "123abc")
        self.assertIsNone(result)


class TestSplit(unittest.TestCase):
    def test_split_basic(self):
        result = split(r"\s+", "hello   world\tfoo")
        self.assertEqual(result, ["hello", "world", "foo"])

    def test_split_with_maxsplit(self):
        result = split(r"\s+", "a b c d", maxsplit=2)
        self.assertEqual(result, ["a", "b", "c d"])

    def test_split_invalid_maxsplit(self):
        with self.assertRaises(TypeError):
            split(r"\s+", "a b", maxsplit="2")

    def test_split_bool_maxsplit(self):
        with self.assertRaises(TypeError):
            split(r"\s+", "a b", maxsplit=True)


class TestSub(unittest.TestCase):
    def test_sub_basic(self):
        result = sub(r"\d+", "X", "a1b22c333")
        self.assertEqual(result, "aXbXcX")

    def test_sub_with_count(self):
        result = sub(r"\d+", "X", "a1b22c333", count=2)
        self.assertEqual(result, "aXbXc333")

    def test_sub_with_callable(self):
        result = sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1b2")
        self.assertEqual(result, "a2b4")


class TestSubn(unittest.TestCase):
    def test_subn_basic(self):
        result, count = subn(r"\d+", "X", "a1b22c")
        self.assertEqual(result, "aXbXc")
        self.assertEqual(count, 2)


class TestCompileRegex(unittest.TestCase):
    def test_compile_regex_basic(self):
        pattern = compile_regex(r"\d+")
        self.assertIsInstance(pattern, re.Pattern)

    def test_compile_regex_with_flags(self):
        pattern = compile_regex(r"hello", flags=re.IGNORECASE)
        self.assertTrue(pattern.match("HELLO"))


class TestEscape(unittest.TestCase):
    def test_escape_special_chars(self):
        result = escape("hello.world[test]")
        self.assertEqual(result, r"hello\.world\[test\]")


if __name__ == "__main__":
    unittest.main()
