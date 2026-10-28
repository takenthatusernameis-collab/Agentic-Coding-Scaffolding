"""Tests for strings module."""

import unittest

from strings import (
    camel_to_snake,
    capitalize_words,
    center,
    char_count,
    char_frequency,
    chunk_string,
    common_prefix,
    common_suffix,
    contains_all,
    contains_any,
    count_consonants,
    count_letters,
    count_occurrences,
    count_vowels,
    count_words,
    drop,
    ends_with,
    first_n,
    initials,
    is_alpha,
    is_alphanumeric,
    is_anagram,
    is_ascii,
    is_blank,
    is_digit,
    is_hex,
    is_identifier,
    is_integer,
    is_lower,
    is_palindrome,
    is_pangram,
    is_printable,
    is_rotation,
    is_space,
    is_subsequence,
    is_title,
    is_upper,
    is_whitespace,
    join_lines,
    last_n,
    levenshtein_distance,
    lstrip_chars,
    normalize_whitespace,
    pad_left,
    pad_right,
    partition,
    remove_blank_lines,
    remove_consonants,
    remove_digits,
    remove_punctuation,
    remove_vowels,
    remove_whitespace,
    replace_many,
    reverse_string,
    reverse_words,
    rpartition,
    rstrip_chars,
    slugify,
    snake_to_camel,
    split_lines,
    starts_with,
    strip_chars,
    strip_html,
    strip_non_ascii,
    swap_case,
    take,
    title_case,
    truncate,
    truncate_bytes,
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




class TestNormalizeWhitespace(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(normalize_whitespace("a  b\t\nc"), "a b c")

    def test_empty(self):
        self.assertEqual(normalize_whitespace(""), "")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            normalize_whitespace(123)  # type: ignore[arg-type]


class TestIsUpper(unittest.TestCase):
    def test_upper(self):
        self.assertTrue(is_upper("HELLO"))
        self.assertTrue(is_upper("HELLO123"))

    def test_mixed(self):
        self.assertFalse(is_upper("Hello"))
        self.assertFalse(is_upper("hello"))

    def test_no_alpha(self):
        self.assertFalse(is_upper("123!"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_upper(123)  # type: ignore[arg-type]


class TestIsLower(unittest.TestCase):
    def test_lower(self):
        self.assertTrue(is_lower("hello"))
        self.assertTrue(is_lower("hello123"))

    def test_mixed(self):
        self.assertFalse(is_lower("Hello"))
        self.assertFalse(is_lower("HELLO"))

    def test_no_alpha(self):
        self.assertFalse(is_lower("123!"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_lower(123)  # type: ignore[arg-type]


class TestIsTitle(unittest.TestCase):
    def test_title(self):
        self.assertTrue(is_title("Hello World"))
        self.assertTrue(is_title("This Is A Title"))

    def test_mixed(self):
        self.assertFalse(is_title("hello world"))
        self.assertFalse(is_title("HELLO WORLD"))
        self.assertFalse(is_title("Hello world"))

    def test_no_alpha(self):
        self.assertFalse(is_title("123!"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_title(123)  # type: ignore[arg-type]


class TestIsAlpha(unittest.TestCase):
    def test_alpha(self):
        self.assertTrue(is_alpha("hello"))
        self.assertTrue(is_alpha("HelloWorld"))

    def test_not_alpha_with_space(self):
        self.assertFalse(is_alpha("hello world"))

    def test_not_alpha_with_digit(self):
        self.assertFalse(is_alpha("hello123"))

    def test_not_alpha_empty(self):
        self.assertFalse(is_alpha(""))

    def test_not_alpha_single_symbol(self):
        self.assertFalse(is_alpha("!"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_alpha(123)  # type: ignore[arg-type]


class TestIsAlphanumeric(unittest.TestCase):
    def test_alphanumeric(self):
        self.assertTrue(is_alphanumeric("hello123"))
        self.assertTrue(is_alphanumeric("Hello"))
        self.assertTrue(is_alphanumeric("123"))

    def test_not_alphanumeric_with_space(self):
        self.assertFalse(is_alphanumeric("hello world"))

    def test_not_alphanumeric_with_symbol(self):
        self.assertFalse(is_alphanumeric("hello!"))
        self.assertFalse(is_alphanumeric("test_123"))

    def test_not_alphanumeric_empty(self):
        self.assertFalse(is_alphanumeric(""))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_alphanumeric(123)  # type: ignore[arg-type]


class TestIsDigit(unittest.TestCase):
    def test_digit(self):
        self.assertTrue(is_digit("123"))
        self.assertTrue(is_digit("0"))

    def test_not_digit_with_sign(self):
        self.assertFalse(is_digit("-1"))
        self.assertFalse(is_digit("+1"))

    def test_not_digit_with_decimal(self):
        self.assertFalse(is_digit("12.3"))

    def test_not_digit_with_letters(self):
        self.assertFalse(is_digit("123a"))

    def test_not_digit_empty(self):
        self.assertFalse(is_digit(""))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_digit(123)  # type: ignore[arg-type]


class TestIsHex(unittest.TestCase):
    def test_hex_lowercase(self):
        self.assertTrue(is_hex("1a2f"))
        self.assertTrue(is_hex("deadbeef"))

    def test_hex_uppercase(self):
        self.assertTrue(is_hex("1A2F"))
        self.assertTrue(is_hex("DEADBEEF"))

    def test_hex_mixed_case(self):
        self.assertTrue(is_hex("DeAdBeEf"))
        self.assertTrue(is_hex("0123456789AbCdEf"))

    def test_hex_digits_only(self):
        self.assertTrue(is_hex("0"))
        self.assertTrue(is_hex("000"))
        self.assertTrue(is_hex("ff"))

    def test_not_hex_with_invalid_char(self):
        self.assertFalse(is_hex("1g3"))
        self.assertFalse(is_hex("xyz"))
        self.assertFalse(is_hex("hello"))

    def test_not_hex_with_sign(self):
        self.assertFalse(is_hex("-1a"))
        self.assertFalse(is_hex("+1a"))

    def test_not_hex_with_decimal(self):
        self.assertFalse(is_hex("1.2f"))

    def test_not_hex_empty(self):
        self.assertFalse(is_hex(""))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_hex(123)  # type: ignore[arg-type]


class TestIsInteger(unittest.TestCase):
    def test_integer(self):
        self.assertTrue(is_integer("123"))
        self.assertTrue(is_integer("-123"))
        self.assertTrue(is_integer("+123"))
        self.assertTrue(is_integer("0"))

    def test_not_integer_with_decimal(self):
        self.assertFalse(is_integer("12.3"))

    def test_not_integer_with_letters(self):
        self.assertFalse(is_integer("123a"))

    def test_not_integer_empty(self):
        self.assertFalse(is_integer(""))

    def test_not_integer_just_sign(self):
        self.assertFalse(is_integer("-"))
        self.assertFalse(is_integer("+"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            is_integer(123)  # type: ignore[arg-type]


class TestIsAscii(unittest.TestCase):
    def test_ascii(self) -> None:
        self.assertTrue(is_ascii("hello"))
        self.assertTrue(is_ascii("HelloWorld"))
        self.assertTrue(is_ascii("123"))
        self.assertTrue(is_ascii("Hello, World!"))

    def test_not_ascii(self) -> None:
        self.assertFalse(is_ascii("héllo"))
        self.assertFalse(is_ascii("日本語"))
        self.assertFalse(is_ascii("naïve"))

    def test_not_ascii_empty(self) -> None:
        self.assertFalse(is_ascii(""))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_ascii(123)  # type: ignore[arg-type]


class TestIsWhitespace(unittest.TestCase):
    def test_whitespace(self) -> None:
        self.assertTrue(is_whitespace("   "))
        self.assertTrue(is_whitespace("\t"))
        self.assertTrue(is_whitespace("\n"))
        self.assertTrue(is_whitespace(" \t\n"))
        self.assertTrue(is_space("   "))

    def test_not_whitespace(self) -> None:
        self.assertFalse(is_whitespace("hello"))
        self.assertFalse(is_whitespace("a b"))

    def test_empty(self) -> None:
        self.assertFalse(is_whitespace(""))
        self.assertFalse(is_space(""))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_whitespace(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_space(None)  # type: ignore[arg-type]


class TestIsPrintable(unittest.TestCase):
    def test_printable(self) -> None:
        self.assertTrue(is_printable("hello"))
        self.assertTrue(is_printable("Hello World!"))

    def test_not_printable(self) -> None:
        self.assertFalse(is_printable("\t"))
        self.assertFalse(is_printable("\n"))

    def test_empty(self) -> None:
        self.assertFalse(is_printable(""))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_printable(123)  # type: ignore[arg-type]


class TestIsIdentifier(unittest.TestCase):
    def test_identifier(self) -> None:
        self.assertTrue(is_identifier("hello"))
        self.assertTrue(is_identifier("_hello"))
        self.assertTrue(is_identifier("hello123"))
        self.assertTrue(is_identifier("_123"))

    def test_not_identifier(self) -> None:
        self.assertFalse(is_identifier("123hello"))
        self.assertFalse(is_identifier("hello-world"))
        self.assertFalse(is_identifier("hello world"))
        self.assertFalse(is_identifier(""))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_identifier(123)  # type: ignore[arg-type]


class TestIsPangram(unittest.TestCase):
    def test_pangram(self) -> None:
        self.assertTrue(is_pangram("The quick brown fox jumps over the lazy dog"))
        self.assertTrue(is_pangram("Pack my box with five dozen liquor jugs"))

    def test_pangram_case_insensitive(self) -> None:
        self.assertTrue(is_pangram("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"))
        self.assertTrue(is_pangram("the quick brown fox jumps over the lazy dog"))

    def test_not_pangram_missing_letters(self) -> None:
        self.assertFalse(is_pangram("Hello world"))
        self.assertFalse(is_pangram("abcdefghijklmnopqrstuvwxy"))
        self.assertFalse(is_pangram(""))

    def test_pangram_ignores_non_alphabetic(self) -> None:
        self.assertTrue(is_pangram("The quick brown fox jumps over the lazy dog!"))
        self.assertTrue(is_pangram("The1quick2brown3fox4jumps5over6the7lazy8dog9"))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_pangram(123)  # type: ignore[arg-type]


class TestIsSubsequence(unittest.TestCase):
    def test_subsequence_present(self) -> None:
        self.assertTrue(is_subsequence("abc", "aebdc"))
        self.assertTrue(is_subsequence("ace", "abcde"))
        self.assertTrue(is_subsequence("abc", "abc"))
        self.assertTrue(is_subsequence("a", "a"))

    def test_subsequence_not_present(self) -> None:
        self.assertFalse(is_subsequence("abc", "acb"))
        self.assertFalse(is_subsequence("abc", "ab"))
        self.assertFalse(is_subsequence("abc", "def"))
        self.assertFalse(is_subsequence("abcd", "abc"))

    def test_empty_needle_is_subsequence(self) -> None:
        self.assertTrue(is_subsequence("", "anything"))
        self.assertTrue(is_subsequence("", ""))

    def test_empty_haystack(self) -> None:
        self.assertFalse(is_subsequence("a", ""))
        self.assertTrue(is_subsequence("", ""))

    def test_case_sensitive(self) -> None:
        self.assertFalse(is_subsequence("ABC", "abc"))
        self.assertFalse(is_subsequence("abc", "ABC"))
        self.assertTrue(is_subsequence("abc", "aXbYc"))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_subsequence("abc", 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_subsequence(123, "abc")  # type: ignore[arg-type]


class TestIsRotation(unittest.TestCase):
    def test_rotation_true(self) -> None:
        self.assertTrue(is_rotation("abcde", "cdeab"))
        self.assertTrue(is_rotation("abcde", "deabc"))
        self.assertTrue(is_rotation("abcde", "eabcd"))
        self.assertTrue(is_rotation("abcde", "bcdea"))
        self.assertTrue(is_rotation("abcde", "abcde"))

    def test_rotation_false(self) -> None:
        self.assertFalse(is_rotation("abcde", "abced"))
        self.assertFalse(is_rotation("abcde", "abcda"))
        self.assertFalse(is_rotation("abc", "abcd"))
        self.assertFalse(is_rotation("abcd", "abc"))
        self.assertFalse(is_rotation("hello", "world"))

    def test_rotation_empty(self) -> None:
        self.assertTrue(is_rotation("", ""))
        self.assertTrue(is_rotation("a", "a"))
        self.assertFalse(is_rotation("a", ""))
        self.assertFalse(is_rotation("", "a"))

    def test_rotation_case_sensitive(self) -> None:
        self.assertFalse(is_rotation("Abcde", "abcde"))
        self.assertFalse(is_rotation("abcde", "Abcde"))

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            is_rotation(123, "abcde")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_rotation("abcde", 123)  # type: ignore[arg-type]


class TestSwapCase(unittest.TestCase):
    def test_swap(self):
        self.assertEqual(swap_case("Hello World"), "hELLO wORLD")

    def test_empty(self):
        self.assertEqual(swap_case(""), "")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            swap_case(123)  # type: ignore[arg-type]


class TestCountOccurrences(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_occurrences("hello hello", "hello"), 2)
        self.assertEqual(count_occurrences("aaa", "aa"), 1)

    def test_empty_substring(self):
        with self.assertRaises(ValueError):
            count_occurrences("hello", "")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            count_occurrences(123, "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_occurrences("a", 123)  # type: ignore[arg-type]


class TestStartsWith(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(starts_with("hello", "he"))
        self.assertFalse(starts_with("hello", "hi"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            starts_with(123, "he")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            starts_with("hello", 123)  # type: ignore[arg-type]


class TestEndsWith(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(ends_with("hello", "lo"))
        self.assertFalse(ends_with("hello", "hi"))

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            ends_with(123, "lo")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ends_with("hello", 123)  # type: ignore[arg-type]


class TestPadLeft(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(pad_left("hi", 5), "   hi")
        self.assertEqual(pad_left("hi", 5, "0"), "000hi")

    def test_no_pad(self):
        self.assertEqual(pad_left("hello", 3), "hello")

    def test_fillchar_must_be_single(self):
        with self.assertRaises(ValueError):
            pad_left("hi", 5, "00")

    def test_rejects_invalid(self):
        with self.assertRaises(TypeError):
            pad_left(123, 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pad_left("hi", "5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pad_left("hi", 5, 0)  # type: ignore[arg-type]


class TestPadRight(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(pad_right("hi", 5), "hi   ")
        self.assertEqual(pad_right("hi", 5, "0"), "hi000")

    def test_fillchar_must_be_single(self):
        with self.assertRaises(ValueError):
            pad_right("hi", 5, "00")

    def test_rejects_invalid(self):
        with self.assertRaises(TypeError):
            pad_right(123, 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pad_right("hi", "5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pad_right("hi", 5, 0)  # type: ignore[arg-type]


class TestCenter(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(center("hi", 6), "  hi  ")
        self.assertEqual(center("hi", 6, "*"), "**hi**")

    def test_fillchar_must_be_single(self):
        with self.assertRaises(ValueError):
            center("hi", 6, "**")

    def test_rejects_invalid(self):
        with self.assertRaises(TypeError):
            center(123, 6)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            center("hi", "6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            center("hi", 6, 0)  # type: ignore[arg-type]


class TestStripChars(unittest.TestCase):
    def test_lstrip(self):
        self.assertEqual(lstrip_chars("xxxhello", "x"), "hello")

    def test_rstrip(self):
        self.assertEqual(rstrip_chars("helloxxx", "x"), "hello")

    def test_strip(self):
        self.assertEqual(strip_chars("xxxhelloxxx", "x"), "hello")

    def test_rejects_invalid(self):
        with self.assertRaises(TypeError):
            lstrip_chars(123, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            rstrip_chars("hi", 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            strip_chars(123, "x")  # type: ignore[arg-type]


class TestReverseWords(unittest.TestCase):
    def test_reverse_words_basic(self):
        self.assertEqual(reverse_words("hello world"), "world hello")

    def test_reverse_words_empty(self):
        self.assertEqual(reverse_words(""), "")

    def test_reverse_words_single(self):
        self.assertEqual(reverse_words("hello"), "hello")

    def test_reverse_words_rejects_non_string(self):
        with self.assertRaises(TypeError):
            reverse_words(123)  # type: ignore[arg-type]


class TestCommonPrefix(unittest.TestCase):
    def test_common_prefix_basic(self):
        self.assertEqual(common_prefix("interstellar", "internet"), "inter")

    def test_common_prefix_identical(self):
        self.assertEqual(common_prefix("hello", "hello"), "hello")

    def test_common_prefix_no_match(self):
        self.assertEqual(common_prefix("hello", "world"), "")

    def test_common_prefix_one_empty(self):
        self.assertEqual(common_prefix("", "abc"), "")
        self.assertEqual(common_prefix("abc", ""), "")

    def test_common_prefix_both_empty(self):
        self.assertEqual(common_prefix("", ""), "")

    def test_common_prefix_same_first_char(self):
        self.assertEqual(common_prefix("abc", "abd"), "ab")

    def test_common_prefix_rejects_non_string_first(self):
        with self.assertRaises(TypeError):
            common_prefix(123, "abc")  # type: ignore[arg-type]

    def test_common_prefix_rejects_non_string_second(self):
        with self.assertRaises(TypeError):
            common_prefix("abc", 123)  # type: ignore[arg-type]


class TestCommonSuffix(unittest.TestCase):
    def test_common_suffix_basic(self):
        self.assertEqual(common_suffix("running", "walking"), "ing")

    def test_common_suffix_identical(self):
        self.assertEqual(common_suffix("hello", "hello"), "hello")

    def test_common_suffix_no_match(self):
        self.assertEqual(common_suffix("hello", "world"), "")

    def test_common_suffix_one_empty(self):
        self.assertEqual(common_suffix("", "abc"), "")
        self.assertEqual(common_suffix("abc", ""), "")

    def test_common_suffix_both_empty(self):
        self.assertEqual(common_suffix("", ""), "")

    def test_common_suffix_same_last_chars(self):
        self.assertEqual(common_suffix("jumping", "running"), "ing")

    def test_common_suffix_rejects_non_string_first(self):
        with self.assertRaises(TypeError):
            common_suffix(123, "abc")  # type: ignore[arg-type]

    def test_common_suffix_rejects_non_string_second(self):
        with self.assertRaises(TypeError):
            common_suffix("abc", 123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestNewHelpers(unittest.TestCase):
    def test_char_frequency(self):

        self.assertEqual(char_frequency("aab"), {"a": 2, "b": 1})

    def test_first_last_take_drop(self):
        from strings import drop, first_n, last_n

        self.assertEqual(first_n("hello", 3), "hel")
        self.assertEqual(take("hello", 2), "he")
        self.assertEqual(last_n("hello", 2), "lo")
        self.assertEqual(drop("hello", 2), "llo")
        self.assertEqual(drop("hello", 0), "hello")
        self.assertEqual(drop("hello", 5), "")

    def test_drop_non_str_raises_type_error(self):
        from strings import drop

        with self.assertRaises(TypeError):
            drop(123, 2)  # type: ignore[arg-type]

    def test_drop_non_int_n_raises_type_error(self):
        from strings import drop

        with self.assertRaises(TypeError):
            drop("hello", "2")

    def test_drop_negative_n_raises_value_error(self):
        from strings import drop

        with self.assertRaises(ValueError):
            drop("hello", -1)

    def test_between(self):
        from strings import between

        self.assertEqual(between("<tag>hello</tag>", "<tag>", "</tag>"), "hello")

    def test_contains_any_all(self):
        from strings import contains_all

        self.assertTrue(contains_any("hello", ["x", "he"]))
        self.assertFalse(contains_any("hello", ["x", "y"]))
        self.assertTrue(contains_all("hello world", ["hello", "world"]))
        self.assertFalse(contains_all("hello", ["hello", "world"]))

    def test_count_words(self):

        self.assertEqual(count_words("hello world"), 2)

    def test_remove_punctuation(self):

        self.assertEqual(remove_punctuation("hello, world!"), "hello world")

    def test_remove_consonants(self):
        self.assertEqual(remove_consonants("hello"), "eo")
        self.assertEqual(remove_consonants("HELLO"), "EO")
        self.assertEqual(remove_consonants("a1b2"), "a12")

    def test_remove_vowels(self):
        self.assertEqual(remove_vowels("hello"), "hll")
        self.assertEqual(remove_vowels("a1e2"), "12")

    def test_remove_digits(self):

        self.assertEqual(remove_digits("a1b2c3"), "abc")
        self.assertEqual(remove_digits("no digits"), "no digits")

    def test_is_palindrome(self):
        from strings import is_palindrome

        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertFalse(is_palindrome("hello"))
        self.assertTrue(is_palindrome("Madam", ignore_case=True))
        self.assertTrue(is_palindrome("12321"))

    def test_is_palindrome_ignore_spaces_false(self):
        from strings import is_palindrome

        self.assertTrue(is_palindrome("a b a", ignore_spaces=False))

    def test_is_palindrome_rejects_non_string(self):
        from strings import is_palindrome

        with self.assertRaises(TypeError):
            is_palindrome(123)  # type: ignore[arg-type]

    def test_reverse_words(self):
        from strings import reverse_words

        self.assertEqual(reverse_words("hello world"), "world hello")
        self.assertEqual(reverse_words("one"), "one")

    def test_reverse_words_rejects_non_string(self):
        from strings import reverse_words

        with self.assertRaises(TypeError):
            reverse_words(123)  # type: ignore[arg-type]

    def test_truncate(self):
        from strings import truncate

        self.assertEqual(truncate("hello world", 5), "he...")
        self.assertEqual(truncate("hello", 10), "hello")
        self.assertEqual(truncate("hello world", 3), "...")
        self.assertEqual(truncate("hello world", 8, suffix="!!"), "hello !!")

    def test_truncate_rejects_non_string(self):
        from strings import truncate

        with self.assertRaises(TypeError):
            truncate(123, 5)  # type: ignore[arg-type]

    def test_truncate_rejects_non_int_length(self):
        from strings import truncate

        with self.assertRaises(TypeError):
            truncate("hello", "5")  # type: ignore[arg-type]

    def test_truncate_negative_length_raises(self):
        from strings import truncate

        with self.assertRaises(ValueError):
            truncate("hello", -1)


class TestRemoveBlankLines(unittest.TestCase):
    def test_basic(self):

        self.assertEqual(remove_blank_lines("a\n\nb\n\nc"), "a\nb\nc")

    def test_no_blanks(self):

        self.assertEqual(remove_blank_lines("a\nb"), "a\nb")

    def test_all_blank(self):

        self.assertEqual(remove_blank_lines("\n\n"), "")

    def test_non_str_raises(self):

        with self.assertRaises(TypeError):
            remove_blank_lines(123)


class TestPartition(unittest.TestCase):
    def test_partition_basic(self):

        self.assertEqual(partition("hello/world", "/"), ("hello", "/", "world"))

    def test_partition_not_found(self):

        self.assertEqual(partition("hello", "/"), ("hello", "", ""))

    def test_partition_empty_separator_raises(self):

        with self.assertRaises(ValueError):
            partition("hello", "")

    def test_partition_rejects_non_string(self):

        with self.assertRaises(TypeError):
            partition(123, "/")
        with self.assertRaises(TypeError):
            partition("hello", 123)  # type: ignore[arg-type]


class TestRPartition(unittest.TestCase):
    def test_rpartition_basic(self):

        self.assertEqual(rpartition("a/b/c", "/"), ("a/b", "/", "c"))

    def test_rpartition_not_found(self):

        self.assertEqual(rpartition("hello", "/"), ("", "", "hello"))

    def test_rpartition_empty_separator_raises(self):

        with self.assertRaises(ValueError):
            rpartition("hello", "")

    def test_rpartition_rejects_non_string(self):

        with self.assertRaises(TypeError):
            rpartition(123, "/")
        with self.assertRaises(TypeError):
            rpartition("hello", 123)  # type: ignore[arg-type]


class TestSplitLines(unittest.TestCase):
    def test_split_lines_basic(self):

        self.assertEqual(split_lines("a\nb\nc"), ["a", "b", "c"])

    def test_split_lines_keepends(self):
        from strings import split_lines

        self.assertEqual(split_lines("a\nb", keepends=True), ["a\n", "b"])

    def test_split_lines_empty(self):
        from strings import split_lines

        self.assertEqual(split_lines(""), [])

    def test_split_lines_keepends_non_bool_raises(self):
        from strings import split_lines

        with self.assertRaises(TypeError):
            split_lines("a\nb", keepends="true")  # type: ignore[arg-type]

    def test_split_lines_rejects_non_string(self):
        from strings import split_lines

        with self.assertRaises(TypeError):
            split_lines(123)  # type: ignore[arg-type]


class TestJoinLines(unittest.TestCase):
    def test_join_lines_basic(self):
        from strings import join_lines

        self.assertEqual(join_lines(["a", "b"], "\n"), "a\nb")

    def test_join_lines_default_sep(self):
        from strings import join_lines

        self.assertEqual(join_lines(["a", "b"]), "a\nb")

    def test_join_lines_non_list_raises(self):
        from strings import join_lines

        with self.assertRaises(TypeError):
            join_lines("ab")  # type: ignore[arg-type]

    def test_join_lines_bad_element_raises(self):
        from strings import join_lines

        with self.assertRaises(TypeError):
            join_lines(["a", 123])  # type: ignore[arg-type]

    def test_join_lines_sep_non_string_raises(self):

        with self.assertRaises(TypeError):
            join_lines(["a"], 123)  # type: ignore[arg-type]


class TestReplaceMany(unittest.TestCase):
    def test_replace_many_basic(self):
        from strings import replace_many

        self.assertEqual(replace_many("hello world", {"hello": "hi", "world": "there"}), "hi there")

    def test_replace_many_non_dict_raises(self):
        from strings import replace_many

        with self.assertRaises(TypeError):
            replace_many("hi", [])  # type: ignore[arg-type]

    def test_replace_many_bad_key_or_value_raises(self):
        from strings import replace_many

        with self.assertRaises(TypeError):
            replace_many("hi", {123: "x"})  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            replace_many("hi", {"x": 123})  # type: ignore[arg-type]

    def test_replace_many_rejects_non_string(self):

        with self.assertRaises(TypeError):
            replace_many(123, {"a": "b"})  # type: ignore[arg-type]


class TestStripHtml(unittest.TestCase):
    def test_strip_html_basic(self):

        self.assertEqual(strip_html("<p>hello</p>"), "hello")

    def test_strip_html_nested(self):

        self.assertEqual(strip_html("<div><b>hi</b></div>"), "hi")

    def test_strip_html_no_tags(self):

        self.assertEqual(strip_html("hello"), "hello")

    def test_strip_html_rejects_non_string(self):

        with self.assertRaises(TypeError):
            strip_html(123)  # type: ignore[arg-type]


class TestBetween(unittest.TestCase):
    def test_between_basic(self):
        from strings import between

        self.assertEqual(between("hello [world]", "[", "]"), "world")

    def test_between_start_not_found(self):
        from strings import between

        self.assertEqual(between("hello", "x", "]"), "")

    def test_between_end_not_found(self):
        from strings import between

        self.assertEqual(between("hello [world", "[", "]"), "")

    def test_between_rejects_non_string(self):
        from strings import between

        with self.assertRaises(TypeError):
            between(123, "[", "]")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            between("hello", 123, "]")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            between("hello", "[", 123)  # type: ignore[arg-type]


class TestContainsAnyAll(unittest.TestCase):
    def test_contains_any_basic(self):

        self.assertTrue(contains_any("hello", ["x", "he"]))
        self.assertFalse(contains_any("hello", ["x", "y"]))

    def test_contains_all_basic(self):

        self.assertTrue(contains_all("hello world", ["hello", "world"]))
        self.assertFalse(contains_all("hello world", ["hello", "foo"]))

    def test_contains_any_all_non_list_raises(self):
        from strings import contains_all

        with self.assertRaises(TypeError):
            contains_any("hi", "h")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains_all("hi", "h")  # type: ignore[arg-type]

    def test_contains_any_all_bad_elements_raise(self):
        from strings import contains_all

        with self.assertRaises(TypeError):
            contains_any("hi", [123])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains_all("hi", [123])  # type: ignore[arg-type]

    def test_contains_any_all_rejects_non_string(self):
        from strings import contains_all

        with self.assertRaises(TypeError):
            contains_any(123, ["a"])  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            contains_all(123, ["a"])  # type: ignore[arg-type]


class TestCharFrequency(unittest.TestCase):
    def test_char_frequency_basic(self):

        self.assertEqual(char_frequency("aba"), {"a": 2, "b": 1})

    def test_char_frequency_empty(self):

        self.assertEqual(char_frequency(""), {})

    def test_char_frequency_rejects_non_string(self):

        with self.assertRaises(TypeError):
            char_frequency(123)  # type: ignore[arg-type]


class TestChunkString(unittest.TestCase):
    def test_basic(self):
        from strings import chunk_string

        self.assertEqual(chunk_string("abcdef", 2), ["ab", "cd", "ef"])
        self.assertEqual(chunk_string("hello", 3), ["hel", "lo"])

    def test_empty_string(self):
        from strings import chunk_string

        self.assertEqual(chunk_string("", 5), [])

    def test_size_larger_than_string(self):
        from strings import chunk_string

        self.assertEqual(chunk_string("abc", 10), ["abc"])

    def test_size_one(self):
        from strings import chunk_string

        self.assertEqual(chunk_string("abc", 1), ["a", "b", "c"])

    def test_invalid_size(self):
        from strings import chunk_string

        with self.assertRaises(ValueError):
            chunk_string("abc", 0)
        with self.assertRaises(ValueError):
            chunk_string("abc", -1)

    def test_non_str_raises(self):
        from strings import chunk_string

        with self.assertRaises(TypeError):
            chunk_string(123, 2)

    def test_non_int_size_raises(self):
        from strings import chunk_string

        with self.assertRaises(TypeError):
            chunk_string("abc", 2.5)
        with self.assertRaises(TypeError):
            chunk_string("abc", True)  # type: ignore[arg-type]



class TestInitials(unittest.TestCase):
    def test_basic(self):
        from strings import initials

        self.assertEqual(initials("foo bar baz"), "FBB")

    def test_separator(self):
        from strings import initials

        self.assertEqual(initials("foo bar", separator="."), "F.B")

    def test_empty(self):
        from strings import initials

        self.assertEqual(initials(""), "")

    def test_non_str_raises(self):
        from strings import initials

        with self.assertRaises(TypeError):
            initials(123)  # type: ignore[arg-type]

    def test_non_str_separator_raises(self):
        from strings import initials

        with self.assertRaises(TypeError):
            initials("foo bar", separator=5)  # type: ignore[arg-type]


class TestStringsBoundaryCases(unittest.TestCase):
    """Boundary case tests for string utilities."""

    # Empty string edge cases
    def test_is_palindrome_empty_is_true(self):
        self.assertTrue(is_palindrome(""))

    def test_reverse_empty(self):
        self.assertEqual(reverse_string(""), "")

    def test_capitalize_words_empty(self):
        self.assertEqual(capitalize_words(""), "")

    def test_title_case_empty(self):
        self.assertEqual(title_case(""), "")

    def test_truncate_empty(self):
        self.assertEqual(truncate("", 5), "")

    def test_slugify_empty(self):
        self.assertEqual(slugify(""), "")

    def test_remove_whitespace_empty(self):
        self.assertEqual(remove_whitespace(""), "")

    def test_normalize_whitespace_empty(self):
        self.assertEqual(normalize_whitespace(""), "")

    def test_swap_case_empty(self):
        self.assertEqual(swap_case(""), "")

    def test_reverse_words_empty(self):
        self.assertEqual(reverse_words(""), "")

    def test_is_blank_empty(self):
        self.assertTrue(is_blank(""))

    def test_is_blank_whitespace_only_spaces(self):
        self.assertTrue(is_blank("   "))

    def test_is_blank_whitespace_only_tabs(self):
        self.assertTrue(is_blank("\t"))

    def test_is_blank_whitespace_only_newlines(self):
        self.assertTrue(is_blank("\n"))

    def test_is_blank_whitespace_mixed(self):
        self.assertTrue(is_blank(" \t\n\r"))

    def test_is_blank_with_content(self):
        self.assertFalse(is_blank("hello"))

    # Single character
    def test_single_char_is_palindrome(self):
        self.assertTrue(is_palindrome("a"))
        self.assertTrue(is_palindrome("Z"))

    def test_is_alpha_single_char(self):
        self.assertTrue(is_alpha("a"))
        self.assertFalse(is_alpha("1"))

    def test_is_alphanumeric_single_char(self):
        self.assertTrue(is_alphanumeric("a"))
        self.assertTrue(is_alphanumeric("5"))

    def test_is_digit_single_zero(self):
        self.assertTrue(is_digit("0"))

    def test_is_hex_single_digit(self):
        self.assertTrue(is_hex("a"))
        self.assertTrue(is_hex("F"))
        self.assertTrue(is_hex("5"))

    # Whitespace only
    def test_word_count_whitespace_only_spaces(self):
        self.assertEqual(word_count("   "), 0)

    def test_word_count_whitespace_only_tabs(self):
        self.assertEqual(word_count("\t\t"), 0)

    def test_word_count_whitespace_only_newlines(self):
        self.assertEqual(word_count("\n\n"), 0)

    def test_count_vowels_whitespace_only(self):
        self.assertEqual(count_vowels("   "), 0)

    def test_count_consonants_whitespace_only(self):
        self.assertEqual(count_consonants("   "), 0)

    # Unicode boundary cases
    def test_is_alpha_unicode_letters(self):
        self.assertTrue(is_alpha("café"))
        self.assertTrue(is_alpha("naïve"))
        self.assertTrue(is_alpha("Москва"))  # Russian

    def test_is_alphanumeric_unicode(self):
        self.assertTrue(is_alphanumeric("café123"))

    def test_is_ascii_unicode_false(self):
        self.assertFalse(is_ascii("café"))
        self.assertFalse(is_ascii("Москва"))

    def test_is_ascii_pure_ascii_true(self):
        self.assertTrue(is_ascii("hello123!"))

    def test_is_pangram_empty_string(self):
        self.assertFalse(is_pangram(""))

    def test_is_identifier_unicode_letters(self):
        # Python identifiers can have unicode letters in some cases,
        # but behavior follows str.isidentifier. Just test that it doesn't crash.
        result = is_identifier("café")
        self.assertIsInstance(result, bool)

    # is_integer edge cases
    def test_is_integer_positive_with_plus(self):
        self.assertTrue(is_integer("+123"))

    def test_is_integer_negative(self):
        self.assertTrue(is_integer("-123"))

    def test_is_integer_empty_after_strip(self):
        self.assertFalse(is_integer("   "))

    def test_is_integer_just_plus(self):
        self.assertFalse(is_integer("+"))

    def test_is_integer_just_minus(self):
        self.assertFalse(is_integer("-"))

    def test_is_integer_with_decimal(self):
        self.assertFalse(is_integer("123.45"))

    # is_palindrome with different params
    def test_is_palindrome_ignore_case_false(self):
        self.assertFalse(is_palindrome("Racecar", ignore_case=False))
        self.assertTrue(is_palindrome("racecar", ignore_case=False))

    def test_is_palindrome_ignore_spaces_false(self):
        # With ignore_spaces False, spaces count as chars
        result = is_palindrome("a b a", ignore_spaces=False)
        # "a b a" vs "a b a" reversed with spaces kept? "a b a" reversed charwise is "a b a"?
        # "a b a" -> chars a, space, b, space, a -> reversed a, space, b, space, a -> same
        self.assertTrue(result)

    def test_is_palindrome_ignore_case_non_bool(self):
        with self.assertRaises(TypeError):
            is_palindrome("test", ignore_case="yes")  # type: ignore[arg-type]

    def test_is_palindrome_ignore_spaces_non_bool(self):
        with self.assertRaises(TypeError):
            is_palindrome("test", ignore_spaces=1)  # type: ignore[arg-type]

    # levenshtein_distance
    def test_levenshtein_distance_empty_strings(self):
        self.assertEqual(levenshtein_distance("", ""), 0)

    def test_levenshtein_distance_one_empty(self):
        self.assertEqual(levenshtein_distance("hello", ""), 5)
        self.assertEqual(levenshtein_distance("", "world"), 5)

    def test_levenshtein_distance_identical(self):
        self.assertEqual(levenshtein_distance("test", "test"), 0)

    # first_n/last_n/drop boundaries
    def test_first_n_zero(self):
        self.assertEqual(first_n("hello", 0), "")

    def test_last_n_zero(self):
        self.assertEqual(last_n("hello", 0), "")

    def test_first_n_all_chars(self):
        self.assertEqual(first_n("hello", 5), "hello")

    def test_first_n_more_than_length(self):
        self.assertEqual(first_n("hi", 10), "hi")

    def test_last_n_more_than_length(self):
        self.assertEqual(last_n("hi", 10), "hi")

    def test_drop_all_chars(self):
        self.assertEqual(drop("hello", 5), "")

    def test_drop_more_than_length(self):
        self.assertEqual(drop("hello", 10), "")

    def test_first_n_negative_raises(self):
        with self.assertRaises(ValueError):
            first_n("hello", -1)

    def test_last_n_negative_raises(self):
        with self.assertRaises(ValueError):
            last_n("hello", -1)

    # count_occurrences edge cases
    def test_count_occurrences_same_string(self):
        self.assertEqual(count_occurrences("hello", "hello"), 1)

    def test_count_occurrences_no_match(self):
        self.assertEqual(count_occurrences("hello", "xyz"), 0)

    # starts_with/ends_with
    def test_starts_with_empty_prefix(self):
        self.assertTrue(starts_with("hello", ""))

    def test_ends_with_empty_suffix(self):
        self.assertTrue(ends_with("hello", ""))

    # chunk_string edge cases
    def test_chunk_string_size_equal_to_length(self):
        self.assertEqual(chunk_string("abc", 3), ["abc"])

    # initials edge cases
    def test_initials_whitespace_only(self):
        self.assertEqual(initials("   "), "")

    def test_initials_multiple_spaces(self):
        self.assertEqual(initials("foo   bar"), "FB")

    # is_printable
    def test_is_printable_empty(self):
        self.assertFalse(is_printable(""))

    def test_is_printable_normal_text(self):
        self.assertTrue(is_printable("hello world!"))

    def test_is_printable_with_tab(self):
        # tab might be considered printable depending, but test current behavior
        result = is_printable("\t")
        self.assertIsInstance(result, bool)


class TestStringsBoundaryAudit(unittest.TestCase):
    def test_empty_string_helpers(self):
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_words(""), "")
        self.assertEqual(count_vowels(""), 0)
        self.assertEqual(count_consonants(""), 0)
        self.assertEqual(word_count(""), 0)
        self.assertEqual(char_count(""), 0)
        self.assertTrue(is_blank(""))
        self.assertEqual(normalize_whitespace(""), "")
        self.assertEqual(remove_whitespace(""), "")
        self.assertEqual(slugify(""), "")
        self.assertEqual(truncate("", 5), "")
        self.assertEqual(first_n("", 3), "")
        self.assertEqual(last_n("", 3), "")
        self.assertEqual(take("", 3), "")
        self.assertEqual(drop("", 3), "")
        self.assertEqual(chunk_string("", 2), [])
        self.assertEqual(initials(""), "")
        self.assertEqual(common_prefix("", ""), "")
        self.assertEqual(common_suffix("", ""), "")

    def test_unicode_basic(self):
        self.assertEqual(reverse_string("café"), "éfac")
        self.assertTrue(is_palindrome("A man a plan a canal Panama".replace(" ", "").lower()))
        self.assertIsInstance(count_vowels("café"), int)

    def test_type_errors(self):
        for name, fn in [("reverse_string", reverse_string)]:
            with self.assertRaises(TypeError):
                fn(123)  # type: ignore[arg-type]


class TestStringsComprehensiveBoundary(unittest.TestCase):
    def test_all_is_alpha_empty_and_cases(self):
        self.assertFalse(is_alpha(""))
        self.assertTrue(is_alpha("abc"))
        self.assertTrue(is_alpha("ABC"))
        self.assertFalse(is_alpha("abc123"))
        self.assertFalse(is_alpha("abc def"))

    def test_all_is_alphanumeric_cases(self):
        self.assertFalse(is_alphanumeric(""))
        self.assertTrue(is_alphanumeric("abc123"))
        self.assertTrue(is_alphanumeric("123"))
        self.assertFalse(is_alphanumeric("abc!"))

    def test_all_is_ascii_cases(self):
        self.assertFalse(is_ascii(""))
        self.assertTrue(is_ascii("hello"))
        self.assertFalse(is_ascii("café"))

    def test_all_is_digit_hex_integer(self):
        self.assertFalse(is_digit(""))
        self.assertTrue(is_digit("123"))
        self.assertFalse(is_digit("12.3"))
        self.assertFalse(is_hex(""))
        self.assertTrue(is_hex("deadBEEF123"))
        self.assertFalse(is_hex("xyz"))
        self.assertFalse(is_integer(""))
        self.assertTrue(is_integer("123"))
        self.assertTrue(is_integer("-123"))
        self.assertTrue(is_integer("+123"))
        self.assertFalse(is_integer("12.3"))

    def test_all_is_whitespace_space_blank(self):
        self.assertFalse(is_whitespace(""))
        self.assertTrue(is_whitespace("   "))
        self.assertTrue(is_whitespace("\t\n\r"))
        self.assertFalse(is_space(""))
        self.assertTrue(is_space("   "))
        self.assertTrue(is_space("\t"))
        self.assertTrue(is_blank(""))
        self.assertTrue(is_blank(" \t\n"))
        self.assertFalse(is_blank("x"))

    def test_all_is_title_upper_lower(self):
        self.assertFalse(is_title(""))
        self.assertTrue(is_title("Hello World"))
        self.assertFalse(is_title("hello World"))
        self.assertFalse(is_upper(""))
        self.assertTrue(is_upper("HELLO"))
        self.assertFalse(is_upper("Hello"))
        self.assertFalse(is_lower(""))
        self.assertTrue(is_lower("hello"))
        self.assertFalse(is_lower("Hello"))

    def test_is_identifier_cases(self):
        self.assertFalse(is_identifier(""))
        self.assertTrue(is_identifier("foo"))
        self.assertTrue(is_identifier("_foo"))
        self.assertTrue(is_identifier("foo123"))
        self.assertFalse(is_identifier("123foo"))
        self.assertFalse(is_identifier("foo-bar"))

    def test_is_pangram_cases(self):
        self.assertFalse(is_pangram(""))
        self.assertTrue(is_pangram("The quick brown fox jumps over the lazy dog"))

    def test_is_printable_cases(self):
        self.assertFalse(is_printable(""))
        self.assertTrue(is_printable("hello world!"))

    def test_is_subsequence_edges(self):
        self.assertTrue(is_subsequence("", "abc"))
        self.assertTrue(is_subsequence("ac", "abc"))
        self.assertFalse(is_subsequence("ca", "abc"))
        self.assertTrue(is_subsequence("abc", "abc"))

    def test_is_anagram_case_insensitive_ignore_spaces(self):
        self.assertTrue(is_anagram("Dormitory", "dirty room"))
        self.assertFalse(is_anagram("abc", "ab"))

    def test_levenshtein_edges(self):
        self.assertEqual(levenshtein_distance("", ""), 0)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", "abc"), 0)

    def test_truncate_edges(self):
        self.assertEqual(truncate("", 5), "")
        self.assertEqual(truncate("hello", 10), "hello")
        self.assertEqual(truncate("hello world", 8), "hello...")
        self.assertEqual(truncate("hello world", 5, "..."), "he...")

    def test_truncate_type_errors(self):
        with self.assertRaises(TypeError):
            truncate(123, 5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            truncate("hi", "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            truncate("hi", 5, 123)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            truncate("hi", -1)

    def test_is_palindrome_type_and_cases(self):
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))
        with self.assertRaises(TypeError):
            is_palindrome("test", ignore_case="yes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_palindrome("test", ignore_spaces=1)  # type: ignore[arg-type]

    def test_chunk_string_edges(self):
        self.assertEqual(chunk_string("", 2), [])
        self.assertEqual(chunk_string("abc", 3), ["abc"])
        self.assertEqual(chunk_string("abcd", 2), ["ab", "cd"])
        with self.assertRaises(ValueError):
            chunk_string("abc", 0)
        with self.assertRaises(ValueError):
            chunk_string("abc", -1)
        with self.assertRaises(TypeError):
            chunk_string(123, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            chunk_string("abc", "x")  # type: ignore[arg-type]

    def test_initials_edges(self):
        self.assertEqual(initials(""), "")
        self.assertEqual(initials("   "), "")
        self.assertEqual(initials("foo   bar"), "FB")
        self.assertEqual(initials("John Doe Smith"), "JDS")
        self.assertEqual(initials("John Doe", separator="."), "J.D")

    def test_common_prefix_suffix_edges(self):
        self.assertEqual(common_prefix("", ""), "")
        self.assertEqual(common_prefix("abc", "abx"), "ab")
        self.assertEqual(common_suffix("", ""), "")
        self.assertEqual(common_suffix("hello", "bello"), "ello")

    def test_count_words_char_count_edges(self):
        self.assertEqual(word_count(""), 0)
        self.assertEqual(word_count("   "), 0)
        self.assertEqual(word_count("hello world"), 2)
        self.assertEqual(char_count(""), 0)
        self.assertEqual(char_count("abc"), 3)

    def test_slugify_edges(self):
        self.assertEqual(slugify(""), "")
        self.assertEqual(slugify("Hello World!"), "hello-world")

    def test_remove_blank_lines_edges(self):
        self.assertEqual(remove_blank_lines("a\n\nb"), "a\nb")
        self.assertEqual(remove_blank_lines("\n\n"), "")

    def test_starts_ends_with_empty(self):
        self.assertTrue(starts_with("hello", ""))
        self.assertTrue(ends_with("hello", ""))

    def test_between_edges(self):
        from strings import between
        self.assertEqual(between("hello[world]test", "[", "]"), "world")

    def test_contains_any_all_edges(self):
        self.assertTrue(contains_any("hello", ["x", "he"]))
        self.assertFalse(contains_any("hello", ["x", "y"]))
        self.assertTrue(contains_all("hello", ["he", "lo"]))
        self.assertFalse(contains_all("hello", ["he", "x"]))

    def test_type_errors_comprehensive(self):
        string_funcs = [
            reverse_string,
            reverse_words,
            count_vowels,
            count_consonants,
    count_letters,
            word_count,
            char_count,
            is_blank,
            normalize_whitespace,
            remove_whitespace,
            slugify,
            is_alpha,
            is_alphanumeric,
            is_ascii,
            is_digit,
            is_hex,
            is_integer,
            is_whitespace,
            is_space,
            is_title,
            is_upper,
            is_lower,
            is_subsequence,
            is_anagram,
            capitalize_words,
            title_case,
            snake_to_camel,
            camel_to_snake,
            swap_case,
            remove_punctuation,
            remove_digits,
            strip_non_ascii,
            truncate_bytes,
            count_occurrences,
            starts_with,
            ends_with,
            lstrip_chars,
            rstrip_chars,
            strip_chars,
            split_lines,
            replace_many,
            strip_html,
            char_frequency,
            first_n,
            last_n,
            drop,
            take,
        ]
        for fn in string_funcs:
            try:
                fn(123)  # type: ignore[arg-type]
                self.fail(f"{fn.__name__} should raise TypeError")
            except TypeError:
                pass

    def test_levenshtein_type_errors(self):
        with self.assertRaises(TypeError):
            levenshtein_distance(123, "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            levenshtein_distance("a", 123)  # type: ignore[arg-type]

    def test_is_subsequence_type_errors(self):
        with self.assertRaises(TypeError):
            is_subsequence(123, "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_subsequence("a", 123)  # type: ignore[arg-type]

    def test_is_anagram_type_errors(self):
        with self.assertRaises(TypeError):
            is_anagram(123, "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_anagram("a", 123)  # type: ignore[arg-type]

    def test_unicode_multibyte(self):
        self.assertEqual(reverse_string("你好世界"), "界世好你")
        self.assertIsInstance(count_vowels("café"), int)
        self.assertFalse(is_ascii("café"))
        self.assertEqual(slugify("café & crème"), "café-crème")

    def test_strip_non_ascii(self):
        self.assertEqual(strip_non_ascii("hello"), "hello")
        self.assertEqual(strip_non_ascii("héllo"), "hllo")
        self.assertEqual(strip_non_ascii("你好"), "")

    def test_truncate_bytes(self):
        self.assertEqual(truncate_bytes("hello", 10), "hello")
        self.assertEqual(truncate_bytes("héllo", 4, encoding="utf-8"), "hél")
        self.assertEqual(truncate_bytes("hello", 0), "")


class TestCountLetters(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_letters("abc123"), 3)
        self.assertEqual(count_letters(""), 0)
        self.assertEqual(count_letters("ABC"), 3)
    def test_type_error(self):
        with self.assertRaises(TypeError):
            count_letters(123)  # type: ignore[arg-type]
