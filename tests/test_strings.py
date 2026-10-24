"""Tests for strings module."""

import unittest

from strings import (
    camel_to_snake,
    capitalize_words,
    char_count,
    count_consonants,
    count_vowels,
    is_anagram,
    is_blank,
    is_palindrome,
    levenshtein_distance,
    remove_whitespace,
    reverse_string,
    slugify,
    snake_to_camel,
    title_case,
    truncate,
    word_count,
)


class TestReverseString(unittest.TestCase):
    def test_reverse_basic(self):
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_reverse_empty(self):
        self.assertEqual(reverse_string(""), "")

    def test_reverse_single_char(self):
        self.assertEqual(reverse_string("a"), "a")

    def test_reverse_palindrome(self):
        self.assertEqual(reverse_string("racecar"), "racecar")

    def test_reverse_with_spaces(self):
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")

    def test_reverse_rejects_non_string(self):
        with self.assertRaises(TypeError):
            reverse_string(123)  # type: ignore[arg-type]


class TestIsPalindrome(unittest.TestCase):
    def test_palindrome_odd(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_palindrome_even(self):
        self.assertTrue(is_palindrome("abba"))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_case_insensitive(self):
        self.assertTrue(is_palindrome("RaceCar"))

    def test_ignores_non_alphanumeric(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))

    def test_empty_is_palindrome(self):
        self.assertTrue(is_palindrome(""))

    def test_single_char_is_palindrome(self):
        self.assertTrue(is_palindrome("a"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_palindrome(None)  # type: ignore[arg-type]


class TestCountVowels(unittest.TestCase):
    def test_count_basic(self):
        self.assertEqual(count_vowels("hello"), 2)

    def test_count_no_vowels(self):
        self.assertEqual(count_vowels("rhythm"), 0)

    def test_count_case_insensitive(self):
        self.assertEqual(count_vowels("AEIOU"), 5)

    def test_count_empty(self):
        self.assertEqual(count_vowels(""), 0)

    def test_count_all_vowels(self):
        self.assertEqual(count_vowels("aeiou"), 5)

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            count_vowels(42)  # type: ignore[arg-type]


class TestCountConsonants(unittest.TestCase):
    def test_count_basic(self):
        self.assertEqual(count_consonants("hello"), 3)

    def test_count_no_consonants(self):
        self.assertEqual(count_consonants("aeiou"), 0)

    def test_count_all_consonants(self):
        self.assertEqual(count_consonants("rhythm"), 6)

    def test_count_ignores_non_alpha(self):
        self.assertEqual(count_consonants("hello world"), 7)

    def test_count_empty(self):
        self.assertEqual(count_consonants(""), 0)

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            count_consonants(None)  # type: ignore[arg-type]


class TestIsAnagram(unittest.TestCase):
    def test_anagram_basic(self):
        self.assertTrue(is_anagram("listen", "silent"))

    def test_not_anagram(self):
        self.assertFalse(is_anagram("hello", "world"))

    def test_anagram_with_spaces(self):
        self.assertTrue(is_anagram("The Eyes", "They See"))

    def test_anagram_case_insensitive(self):
        self.assertTrue(is_anagram("LISTEN", "silent"))

    def test_anagram_empty_strings(self):
        self.assertTrue(is_anagram("", ""))

    def test_rejects_non_string_first(self):
        with self.assertRaises(TypeError):
            is_anagram(123, "abc")  # type: ignore[arg-type]

    def test_rejects_non_string_second(self):
        with self.assertRaises(TypeError):
            is_anagram("abc", 123)  # type: ignore[arg-type]


class TestCapitalizeWords(unittest.TestCase):
    def test_capitalize_basic(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")

    def test_capitalize_multiple(self):
        self.assertEqual(capitalize_words("python programming"), "Python Programming")

    def test_capitalize_empty(self):
        self.assertEqual(capitalize_words(""), "")

    def test_capitalize_single_word(self):
        self.assertEqual(capitalize_words("python"), "Python")

    def test_capitalize_preserves_extra_spaces(self):
        # split(" ") preserves consecutive spaces as empty words
        self.assertEqual(capitalize_words("a  b"), "A  B")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            capitalize_words(123)  # type: ignore[arg-type]


class TestTruncate(unittest.TestCase):
    def test_truncate_basic(self):
        self.assertEqual(truncate("hello world", 8), "hello...")

    def test_truncate_no_truncation(self):
        self.assertEqual(truncate("hi", 8), "hi")

    def test_truncate_custom_suffix(self):
        self.assertEqual(truncate("hello world", 8, suffix=".."), "hello ..")

    def test_truncate_exact_length(self):
        self.assertEqual(truncate("hello", 5), "hello")

    def test_truncate_suffix_equals_length(self):
        self.assertEqual(truncate("hello world", 3, suffix="..."), "...")
        self.assertEqual(truncate("hello world", 3, suffix=".."), "h..")

    def test_truncate_zero_length(self):
        self.assertEqual(truncate("hello", 0), "")

    def test_truncate_negative_length_raises(self):
        with self.assertRaises(ValueError):
            truncate("hello", -1)

    def test_truncate_suffix_longer_than_length_raises(self):
        with self.assertRaises(ValueError):
            truncate("hello", 2, suffix="...")

    def test_truncate_rejects_non_string(self):
        with self.assertRaises(TypeError):
            truncate(123, 5)  # type: ignore[arg-type]

    def test_truncate_rejects_non_string_suffix(self):
        with self.assertRaises(TypeError):
            truncate("hello", 5, suffix=123)  # type: ignore[arg-type]

    def test_truncate_rejects_non_int_length(self):
        with self.assertRaises(TypeError):
            truncate("hello", "five")  # type: ignore[arg-type]

    def test_truncate_rejects_bool_length(self):
        with self.assertRaises(TypeError):
            truncate("hello", True)


class TestLevenshteinDistance(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)

    def test_empty_first(self):
        self.assertEqual(levenshtein_distance("", "abc"), 3)

    def test_empty_second(self):
        self.assertEqual(levenshtein_distance("abc", ""), 3)

    def test_both_empty(self):
        self.assertEqual(levenshtein_distance("", ""), 0)

    def test_identical(self):
        self.assertEqual(levenshtein_distance("abc", "abc"), 0)

    def test_single_substitution(self):
        self.assertEqual(levenshtein_distance("cat", "car"), 1)

    def test_single_insertion(self):
        self.assertEqual(levenshtein_distance("cat", "cats"), 1)

    def test_single_deletion(self):
        self.assertEqual(levenshtein_distance("cats", "cat"), 1)

    def test_rejects_non_string_first(self):
        with self.assertRaises(TypeError):
            levenshtein_distance(123, "abc")  # type: ignore[arg-type]

    def test_rejects_non_string_second(self):
        with self.assertRaises(TypeError):
            levenshtein_distance("abc", 123)  # type: ignore[arg-type]


class TestTitleCase(unittest.TestCase):
    def test_title_case_basic(self):
        self.assertEqual(title_case("hello world"), "Hello World")

    def test_title_case_multiple(self):
        self.assertEqual(title_case("the quick brown fox"), "The Quick Brown Fox")

    def test_title_case_empty(self):
        self.assertEqual(title_case(""), "")

    def test_title_case_single_word(self):
        self.assertEqual(title_case("hello"), "Hello")

    def test_title_case_rejects_non_string(self):
        with self.assertRaises(TypeError):
            title_case(123)  # type: ignore[arg-type]


class TestCamelToSnake(unittest.TestCase):
    def test_camel_to_snake_basic(self):
        self.assertEqual(camel_to_snake("helloWorld"), "hello_world")

    def test_camel_to_snake_multiple_caps(self):
        self.assertEqual(camel_to_snake("getHTTPResponse"), "get_http_response")

    def test_camel_to_snake_already_snake(self):
        self.assertEqual(camel_to_snake("hello_world"), "hello_world")

    def test_camel_to_snake_rejects_non_string(self):
        with self.assertRaises(TypeError):
            camel_to_snake(None)  # type: ignore[arg-type]


class TestSnakeToCamel(unittest.TestCase):
    def test_snake_to_camel_basic(self):
        self.assertEqual(snake_to_camel("hello_world"), "helloWorld")

    def test_snake_to_camel_capitalize_first(self):
        self.assertEqual(snake_to_camel("hello_world", capitalize_first=True), "HelloWorld")

    def test_snake_to_camel_single_word(self):
        self.assertEqual(snake_to_camel("hello"), "hello")

    def test_snake_to_camel_rejects_non_string(self):
        with self.assertRaises(TypeError):
            snake_to_camel(123)  # type: ignore[arg-type]

    def test_snake_to_camel_rejects_non_bool(self):
        with self.assertRaises(TypeError):
            snake_to_camel("hello_world", capitalize_first="true")  # type: ignore[arg-type]


class TestSlugify(unittest.TestCase):
    def test_slugify_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_slugify_with_special_chars(self):
        self.assertEqual(slugify("Hello, World!"), "hello-world")

    def test_slugify_multiple_spaces(self):
        self.assertEqual(slugify("hello   world"), "hello-world")

    def test_slugify_leading_trailing(self):
        self.assertEqual(slugify("  hello world  "), "hello-world")

    def test_slugify_empty(self):
        self.assertEqual(slugify(""), "")

    def test_slugify_rejects_non_string(self):
        with self.assertRaises(TypeError):
            slugify(123)  # type: ignore[arg-type]


class TestRemoveWhitespace(unittest.TestCase):
    def test_remove_whitespace_basic(self):
        self.assertEqual(remove_whitespace("hello world"), "helloworld")

    def test_remove_whitespace_tabs_newlines(self):
        self.assertEqual(remove_whitespace("hello\n\tworld"), "helloworld")

    def test_remove_whitespace_empty(self):
        self.assertEqual(remove_whitespace(""), "")

    def test_remove_whitespace_rejects_non_string(self):
        with self.assertRaises(TypeError):
            remove_whitespace(None)  # type: ignore[arg-type]


class TestWordCount(unittest.TestCase):
    def test_word_count_basic(self):
        self.assertEqual(word_count("hello world"), 2)

    def test_word_count_multiple_spaces(self):
        self.assertEqual(word_count("hello   world"), 2)

    def test_word_count_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_word_count_whitespace_only(self):
        self.assertEqual(word_count("   "), 0)

    def test_word_count_single_word(self):
        self.assertEqual(word_count("hello"), 1)

    def test_word_count_rejects_non_string(self):
        with self.assertRaises(TypeError):
            word_count(123)  # type: ignore[arg-type]


class TestCharCount(unittest.TestCase):
    def test_char_count_basic(self):
        self.assertEqual(char_count("hello"), 5)

    def test_char_count_with_spaces(self):
        self.assertEqual(char_count("hello world"), 11)

    def test_char_count_empty(self):
        self.assertEqual(char_count(""), 0)

    def test_char_count_rejects_non_string(self):
        with self.assertRaises(TypeError):
            char_count([])  # type: ignore[arg-type]


class TestIsBlank(unittest.TestCase):
    def test_is_blank_empty(self):
        self.assertTrue(is_blank(""))

    def test_is_blank_whitespace(self):
        self.assertTrue(is_blank("   "))
        self.assertTrue(is_blank("\t\n"))

    def test_is_blank_not_blank(self):
        self.assertFalse(is_blank("hello"))
        self.assertFalse(is_blank(" hello "))

    def test_is_blank_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_blank(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
