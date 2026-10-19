"""Unit tests for binascii_utils module."""

import unittest

from binascii_utils import (
    a2b_base64,
    a2b_qp,
    a2b_uu,
    adler32,
    b2a_base64,
    b2a_qp,
    b2a_uu,
    crc32,
    crc_hqx,
    hexlify,
    unhexlify,
)


class TestHexlify(unittest.TestCase):
    def test_hexlify_string(self):
        self.assertEqual(hexlify("hello"), "68656c6c6f")

    def test_hexlify_bytes(self):
        self.assertEqual(hexlify(b"hello"), "68656c6c6f")

    def test_hexlify_empty(self):
        self.assertEqual(hexlify(""), "")

    def test_hexlify_type_error(self):
        with self.assertRaises(TypeError):
            hexlify(123)  # type: ignore[arg-type]


class TestUnhexlify(unittest.TestCase):
    def test_unhexlify_string(self):
        self.assertEqual(unhexlify("68656c6c6f"), b"hello")

    def test_unhexlify_bytes(self):
        self.assertEqual(unhexlify(b"68656c6c6f"), b"hello")

    def test_unhexlify_invalid_hex(self):
        with self.assertRaises(ValueError):
            unhexlify("zz")

    def test_unhexlify_odd_length(self):
        with self.assertRaises(ValueError):
            unhexlify("68656c6")

    def test_unhexlify_type_error(self):
        with self.assertRaises(TypeError):
            unhexlify(123)  # type: ignore[arg-type]


class TestBase64(unittest.TestCase):
    def test_b2a_base64(self):
        self.assertEqual(b2a_base64("hello"), "aGVsbG8=\n")

    def test_a2b_base64(self):
        self.assertEqual(a2b_base64("aGVsbG8=\n"), b"hello")

    def test_base64_roundtrip(self):
        self.assertEqual(a2b_base64(b2a_base64(b"binary data\x00\x01")), b"binary data\x00\x01")

    def test_a2b_base64_type_error(self):
        with self.assertRaises(TypeError):
            a2b_base64(123)  # type: ignore[arg-type]


class TestUU(unittest.TestCase):
    def test_b2a_uu(self):
        self.assertEqual(b2a_uu("hello"), "%:&5L;&\\ \n")

    def test_uu_roundtrip(self):
        self.assertEqual(a2b_uu(b2a_uu(b"hello")), b"hello")

    def test_a2b_uu_type_error(self):
        with self.assertRaises(TypeError):
            a2b_uu(123)  # type: ignore[arg-type]


class TestQuotedPrintable(unittest.TestCase):
    def test_b2a_qp(self):
        self.assertEqual(b2a_qp("hello"), "hello")

    def test_a2b_qp(self):
        self.assertEqual(a2b_qp("hello"), b"hello")

    def test_qp_roundtrip(self):
        self.assertEqual(a2b_qp(b2a_qp(b"abc123")), b"abc123")

    def test_a2b_qp_type_error(self):
        with self.assertRaises(TypeError):
            a2b_qp(123)  # type: ignore[arg-type]


class TestCRC32(unittest.TestCase):
    def test_crc32_string(self):
        self.assertEqual(crc32("hello"), 0x3610A686)

    def test_crc32_bytes(self):
        self.assertEqual(crc32(b"hello"), 0x3610A686)

    def test_crc32_empty(self):
        self.assertEqual(crc32(""), 0)

    def test_crc32_type_error(self):
        with self.assertRaises(TypeError):
            crc32([1, 2, 3])  # type: ignore[arg-type]


class TestAdler32(unittest.TestCase):
    def test_adler32_string(self):
        self.assertEqual(adler32("hello"), 0x062C0215)

    def test_adler32_bytes(self):
        self.assertEqual(adler32(b"hello"), 0x062C0215)

    def test_adler32_empty(self):
        self.assertEqual(adler32(""), 1)

    def test_adler32_type_error(self):
        with self.assertRaises(TypeError):
            adler32(None)  # type: ignore[arg-type]


class TestCRC_HQX(unittest.TestCase):
    def test_crc_hqx_default_value(self):
        self.assertEqual(crc_hqx("hello"), 0xC362)

    def test_crc_hqx_with_initial_value(self):
        self.assertEqual(crc_hqx("hello", 12345), 0x1012)

    def test_crc_hqx_empty(self):
        self.assertEqual(crc_hqx(""), 0)

    def test_crc_hqx_type_error_value(self):
        with self.assertRaises(TypeError):
            crc_hqx("hello", "zero")  # type: ignore[arg-type]

    def test_crc_hqx_type_error_data(self):
        with self.assertRaises(TypeError):
            crc_hqx(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
