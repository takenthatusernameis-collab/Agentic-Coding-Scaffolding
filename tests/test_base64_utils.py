"""Unit tests for base64_utils module."""

import unittest

from base64_utils import (
    base64_decode,
    base64_decode_bytes,
    base64_encode,
    base64_encode_bytes,
    hex_decode,
    hex_encode,
    is_valid_base64,
    is_valid_hex,
)


class TestBase64Encode(unittest.TestCase):
    def test_base64_encode_string(self):
        self.assertEqual(base64_encode("hello"), "aGVsbG8=")

    def test_base64_encode_bytes(self):
        self.assertEqual(base64_encode(b"hello"), "aGVsbG8=")

    def test_base64_encode_empty(self):
        self.assertEqual(base64_encode(""), "")

    def test_base64_encode_urlsafe(self):
        self.assertEqual(base64_encode("hello", urlsafe=True), "aGVsbG8=")

    def test_base64_encode_type_error(self):
        with self.assertRaises(TypeError):
            base64_encode(123)  # type: ignore[arg-type]


class TestBase64Decode(unittest.TestCase):
    def test_base64_decode_basic(self):
        self.assertEqual(base64_decode("aGVsbG8="), "hello")

    def test_base64_decode_roundtrip(self):
        self.assertEqual(base64_decode(base64_encode("hello")), "hello")

    def test_base64_decode_invalid(self):
        with self.assertRaises(ValueError):
            base64_decode("not valid base64!!!")

    def test_base64_decode_type_error(self):
        with self.assertRaises(TypeError):
            base64_decode(123)  # type: ignore[arg-type]


class TestBase64EncodeBytes(unittest.TestCase):
    def test_base64_encode_bytes_basic(self):
        self.assertEqual(base64_encode_bytes("hello"), b"aGVsbG8=")

    def test_base64_encode_bytes_type_error(self):
        with self.assertRaises(TypeError):
            base64_encode_bytes(123)  # type: ignore[arg-type]


class TestBase64DecodeBytes(unittest.TestCase):
    def test_base64_decode_bytes_basic(self):
        self.assertEqual(base64_decode_bytes("aGVsbG8="), b"hello")

    def test_base64_decode_bytes_roundtrip(self):
        self.assertEqual(base64_decode_bytes(base64_encode("hello")), b"hello")

    def test_base64_decode_bytes_invalid(self):
        with self.assertRaises(ValueError):
            base64_decode_bytes("not valid base64!!!")

    def test_base64_decode_bytes_type_error(self):
        with self.assertRaises(TypeError):
            base64_decode_bytes(123)  # type: ignore[arg-type]


class TestHexEncode(unittest.TestCase):
    def test_hex_encode_string(self):
        self.assertEqual(hex_encode("hello"), "68656c6c6f")

    def test_hex_encode_bytes(self):
        self.assertEqual(hex_encode(b"hello"), "68656c6c6f")

    def test_hex_encode_empty(self):
        self.assertEqual(hex_encode(""), "")

    def test_hex_encode_type_error(self):
        with self.assertRaises(TypeError):
            hex_encode(123)  # type: ignore[arg-type]


class TestHexDecode(unittest.TestCase):
    def test_hex_decode_basic(self):
        self.assertEqual(hex_decode("68656c6c6f"), "hello")

    def test_hex_decode_roundtrip(self):
        self.assertEqual(hex_decode(hex_encode("hello")), "hello")

    def test_hex_decode_invalid(self):
        with self.assertRaises(ValueError):
            hex_decode("zzzz")

    def test_hex_decode_type_error(self):
        with self.assertRaises(TypeError):
            hex_decode(123)  # type: ignore[arg-type]


class TestIsValidBase64(unittest.TestCase):
    def test_is_valid_base64_true(self):
        self.assertTrue(is_valid_base64("aGVsbG8="))

    def test_is_valid_base64_false(self):
        self.assertFalse(is_valid_base64("not valid base64!!!"))

    def test_is_valid_base64_type_error_returns_false(self):
        self.assertFalse(is_valid_base64(123))  # type: ignore[arg-type]


class TestIsValidHex(unittest.TestCase):
    def test_is_valid_hex_true(self):
        self.assertTrue(is_valid_hex("68656c6c6f"))

    def test_is_valid_hex_false(self):
        self.assertFalse(is_valid_hex("zzzz"))

    def test_is_valid_hex_type_error_returns_false(self):
        self.assertFalse(is_valid_hex(123))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
