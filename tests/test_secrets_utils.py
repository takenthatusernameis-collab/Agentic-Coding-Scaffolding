"""Unit tests for secrets_utils module."""

import unittest

from secrets_utils import (
    choice,
    compare_digest,
    randbelow,
    randbits,
    token_bytes,
    token_hex,
    token_urlsafe,
)


class TestTokenBytes(unittest.TestCase):
    def test_default_length(self):
        result = token_bytes()
        self.assertEqual(len(result), 32)

    def test_custom_length(self):
        result = token_bytes(16)
        self.assertEqual(len(result), 16)

    def test_empty(self):
        self.assertEqual(token_bytes(0), b"")

    def test_unique(self):
        self.assertNotEqual(token_bytes(16), token_bytes(16))

    def test_type_error(self):
        with self.assertRaises(ValueError):
            token_bytes(-1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            token_bytes("16")  # type: ignore[arg-type]


class TestTokenHex(unittest.TestCase):
    def test_default_length(self):
        result = token_hex()
        self.assertGreater(len(result), 0)
        self.assertEqual(len(result) % 2, 0)

    def test_custom_length(self):
        result = token_hex(8)
        self.assertEqual(len(result), 16)

    def test_hex_characters(self):
        result = token_hex(16)
        int(result, 16)  # raises ValueError if not valid hex

    def test_empty(self):
        self.assertEqual(token_hex(0), "")

    def test_unique(self):
        self.assertNotEqual(token_hex(16), token_hex(16))


class TestTokenUrlsafe(unittest.TestCase):
    def test_default_length(self):
        result = token_urlsafe()
        self.assertGreater(len(result), 0)

    def test_custom_length(self):
        result = token_urlsafe(8)
        self.assertGreaterEqual(len(result), 8)

    def test_urlsafe_characters(self):
        result = token_urlsafe(32)
        for char in result:
            self.assertIn(char, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~_")

    def test_empty(self):
        self.assertEqual(token_urlsafe(0), "")

    def test_unique(self):
        self.assertNotEqual(token_urlsafe(16), token_urlsafe(16))


class TestCompareDigest(unittest.TestCase):
    def test_equal_strings(self):
        self.assertTrue(compare_digest("hello", "hello"))

    def test_not_equal_strings(self):
        self.assertFalse(compare_digest("hello", "world"))

    def test_equal_bytes(self):
        self.assertTrue(compare_digest(b"\x00\xff", b"\x00\xff"))

    def test_not_equal_bytes(self):
        self.assertFalse(compare_digest(b"\x00\xff", b"\x00\xfe"))

    def test_mixed_types(self):
        self.assertFalse(compare_digest("hello", b"hello"))
        self.assertFalse(compare_digest(b"hello", "hello"))


class TestRandbelow(unittest.TestCase):
    def test_range(self):
        for _ in range(100):
            value = randbelow(10)
            self.assertGreaterEqual(value, 0)
            self.assertLess(value, 10)

    def test_one(self):
        self.assertEqual(randbelow(1), 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            randbelow(0)
        with self.assertRaises(ValueError):
            randbelow(-1)
        with self.assertRaises(ValueError):
            randbelow(1.5)  # type: ignore[arg-type]


class TestRandbits(unittest.TestCase):
    def test_bits(self):
        for k in (0, 1, 8, 64, 256):
            value = randbits(k)
            self.assertGreaterEqual(value, 0)
            self.assertLess(value, 1 << k)

    def test_zero(self):
        self.assertEqual(randbits(0), 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            randbits(-1)
        with self.assertRaises(ValueError):
            randbits(1.5)  # type: ignore[arg-type]


class TestChoice(unittest.TestCase):
    def test_choice_from_list(self):
        self.assertIn(choice([1, 2, 3]), [1, 2, 3])
        self.assertIn(choice(["a", "b", "c"]), ["a", "b", "c"])

    def test_choice_from_tuple(self):
        self.assertIn(choice(("x", "y")), ("x", "y"))

    def test_empty(self):
        with self.assertRaises(ValueError):
            choice([])  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            choice("")


if __name__ == "__main__":
    unittest.main()
