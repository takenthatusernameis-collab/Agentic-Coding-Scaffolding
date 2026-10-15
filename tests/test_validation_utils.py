"""Tests for validation_utils module."""

import re
import unittest

from validation_utils import (
    is_alphanumeric,
    is_boolean_string,
    is_email,
    is_integer,
    is_none_or_empty,
    is_numeric,
    is_valid_hostname,
    matches_regex,
    max_length,
    min_length,
)


class TestIsEmail(unittest.TestCase):
    def test_valid_emails(self):
        self.assertTrue(is_email("test@example.com"))
        self.assertTrue(is_email("user.name@domain.org"))
        self.assertTrue(is_email("user+tag@example.co.uk"))
        self.assertTrue(is_email("user123@domain123.com"))

    def test_invalid_emails(self):
        self.assertFalse(is_email(None))
        self.assertFalse(is_email(""))
        self.assertFalse(is_email("   "))
        self.assertFalse(is_email(123))
        self.assertFalse(is_email("invalid"))
        self.assertFalse(is_email("invalid@"))
        self.assertFalse(is_email("@example.com"))
        self.assertFalse(is_email("test@"))
        self.assertFalse(is_email("test.example.com"))
        self.assertFalse(is_email("test@ex@ample.com"))
        self.assertFalse(is_email("test@.com"))

    def test_whitespace_handling(self):
        self.assertTrue(is_email("  test@example.com  "))


class TestIsNumeric(unittest.TestCase):
    def test_numeric_values(self):
        self.assertTrue(is_numeric(123))
        self.assertTrue(is_numeric(123.45))
        self.assertTrue(is_numeric(0))
        self.assertTrue(is_numeric(-10))
        self.assertTrue(is_numeric("-10"))
        self.assertTrue(is_numeric("123.45"))
        self.assertTrue(is_numeric("0.0"))
        self.assertTrue(is_numeric("+10"))

    def test_non_numeric_values(self):
        self.assertFalse(is_numeric(None))
        self.assertFalse(is_numeric(""))
        self.assertFalse(is_numeric("abc"))
        self.assertFalse(is_numeric("12a3"))
        self.assertFalse(is_numeric(True))
        self.assertFalse(is_numeric(False))
        self.assertFalse(is_numeric([]))
        self.assertFalse(is_numeric({}))


class TestIsInteger(unittest.TestCase):
    def test_integer_values(self):
        self.assertTrue(is_integer(123))
        self.assertTrue(is_integer(0))
        self.assertTrue(is_integer(-10))
        self.assertTrue(is_integer("123"))
        self.assertTrue(is_integer("-10"))
        self.assertTrue(is_integer("+10"))
        self.assertTrue(is_integer(10.0))

    def test_non_integer_values(self):
        self.assertFalse(is_integer(None))
        self.assertFalse(is_integer(""))
        self.assertFalse(is_integer("123.45"))
        self.assertFalse(is_integer(123.45))
        self.assertFalse(is_integer(True))
        self.assertFalse(is_integer(False))
        self.assertFalse(is_integer("abc"))


class TestIsAlphanumeric(unittest.TestCase):
    def test_alphanumeric_values(self):
        self.assertTrue(is_alphanumeric("abc123"))
        self.assertTrue(is_alphanumeric("ABC123"))
        self.assertTrue(is_alphanumeric("123"))
        self.assertTrue(is_alphanumeric("abc"))

    def test_non_alphanumeric_values(self):
        self.assertFalse(is_alphanumeric(None))
        self.assertFalse(is_alphanumeric(""))
        self.assertFalse(is_alphanumeric("abc 123"))
        self.assertFalse(is_alphanumeric("abc-123"))
        self.assertFalse(is_alphanumeric("abc_123"))
        self.assertFalse(is_alphanumeric("abc.123"))
        self.assertFalse(is_alphanumeric(123))
        self.assertFalse(is_alphanumeric(True))


class TestIsBooleanString(unittest.TestCase):
    def test_boolean_strings(self):
        self.assertTrue(is_boolean_string("true"))
        self.assertTrue(is_boolean_string("false"))
        self.assertTrue(is_boolean_string("TRUE"))
        self.assertTrue(is_boolean_string("False"))
        self.assertTrue(is_boolean_string("1"))
        self.assertTrue(is_boolean_string("0"))

    def test_non_boolean_strings(self):
        self.assertFalse(is_boolean_string(None))
        self.assertFalse(is_boolean_string(""))
        self.assertFalse(is_boolean_string(1))
        self.assertFalse(is_boolean_string(True))
        self.assertFalse(is_boolean_string("yes"))
        self.assertFalse(is_boolean_string("no"))
        self.assertFalse(is_boolean_string("t"))
        self.assertFalse(is_boolean_string("f"))


class TestIsNoneOrEmpty(unittest.TestCase):
    def test_none_or_empty_values(self):
        self.assertTrue(is_none_or_empty(None))
        self.assertTrue(is_none_or_empty(""))
        self.assertTrue(is_none_or_empty([]))
        self.assertTrue(is_none_or_empty({}))
        self.assertTrue(is_none_or_empty(set()))
        self.assertTrue(is_none_or_empty(()))

    def test_non_empty_values(self):
        self.assertFalse(is_none_or_empty("test"))
        self.assertFalse(is_none_or_empty(123))
        self.assertFalse(is_none_or_empty([1, 2]))
        self.assertFalse(is_none_or_empty({"a": 1}))
        self.assertFalse(is_none_or_empty({1}))
        self.assertFalse(is_none_or_empty((1,)))
        self.assertFalse(is_none_or_empty(0))
        self.assertFalse(is_none_or_empty(False))


class TestMinLength(unittest.TestCase):
    def test_min_length_valid(self):
        self.assertTrue(min_length("test", 2))
        self.assertTrue(min_length("test", 4))
        self.assertTrue(min_length([1, 2, 3], 2))
        self.assertTrue(min_length({"a": 1}, 1))
        self.assertTrue(min_length("", 0))
        self.assertTrue(min_length("a", 0))

    def test_min_length_invalid(self):
        self.assertFalse(min_length("test", 5))
        self.assertFalse(min_length([1, 2], 5))

    def test_min_length_errors(self):
        with self.assertRaises(ValueError):
            min_length("test", -1)
        with self.assertRaises(ValueError):
            min_length("test", "4")


class TestMaxLength(unittest.TestCase):
    def test_max_length_valid(self):
        self.assertTrue(max_length("test", 5))
        self.assertTrue(max_length("test", 4))
        self.assertTrue(max_length([1, 2], 3))
        self.assertTrue(max_length("", 0))
        self.assertTrue(max_length("", 5))

    def test_max_length_invalid(self):
        self.assertFalse(max_length("test", 2))
        self.assertFalse(max_length([1, 2, 3, 4], 2))

    def test_max_length_errors(self):
        with self.assertRaises(ValueError):
            max_length("test", -1)
        with self.assertRaises(ValueError):
            max_length("test", "4")


class TestMatchesRegex(unittest.TestCase):
    def test_matches_regex_string(self):
        self.assertTrue(matches_regex("test", r"^test$"))
        self.assertTrue(matches_regex("abc123", r"^[a-z]+\d+$"))
        self.assertTrue(matches_regex("Hello", r"hello", re.IGNORECASE))

    def test_matches_regex_pattern(self):
        pattern = re.compile(r"^test$")
        self.assertTrue(matches_regex("test", pattern))
        self.assertFalse(matches_regex("other", pattern))

    def test_matches_regex_errors(self):
        with self.assertRaises(TypeError):
            matches_regex(123, r"test")
        with self.assertRaises(TypeError):
            matches_regex("test", 123)
        with self.assertRaises(ValueError):
            matches_regex("test", r"[invalid")


class TestIsValidHostname(unittest.TestCase):
    def test_valid_hostnames(self):
        self.assertTrue(is_valid_hostname("example.com"))
        self.assertTrue(is_valid_hostname("sub.example.com"))
        self.assertTrue(is_valid_hostname("localhost"))
        self.assertTrue(is_valid_hostname("192.168.1.1"))
        self.assertTrue(is_valid_hostname("test-domain.com"))
        self.assertTrue(is_valid_hostname("a.b.c.d"))

    def test_invalid_hostnames(self):
        self.assertFalse(is_valid_hostname(None))
        self.assertFalse(is_valid_hostname(""))
        self.assertFalse(is_valid_hostname("   "))
        self.assertFalse(is_valid_hostname("-example.com"))
        self.assertFalse(is_valid_hostname("example-.com"))
        self.assertFalse(is_valid_hostname("ex..ample.com"))
        self.assertFalse(is_valid_hostname("." * 254))  # too long
        self.assertFalse(is_valid_hostname("a" * 64 + ".com"))  # label too long
        self.assertFalse(is_valid_hostname("example.com."))
        self.assertFalse(is_valid_hostname("example.com.."))


if __name__ == "__main__":
    unittest.main()
