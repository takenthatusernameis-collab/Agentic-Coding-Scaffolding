"""Unit tests for hmac_utils module."""

import unittest

from hmac_utils import (
    compare_digest,
    hmac_md5,
    hmac_new,
    hmac_sha1,
    hmac_sha256,
    hmac_sha512,
    sign,
    verify,
)


class TestHmacMD5(unittest.TestCase):
    def test_hmac_md5_string(self):
        self.assertEqual(hmac_md5("hello", "key"), "04130747afca4d79e32e87cf2104f087")

    def test_hmac_md5_bytes(self):
        self.assertEqual(hmac_md5(b"hello", b"key"), "04130747afca4d79e32e87cf2104f087")

    def test_hmac_md5_empty(self):
        self.assertEqual(hmac_md5("", "key"), "63530468a04e386459855da0063b6596")

    def test_hmac_md5_type_error(self):
        with self.assertRaises(TypeError):
            hmac_md5(123, "key")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            hmac_md5("hello", 123)  # type: ignore[arg-type]


class TestHmacSHA1(unittest.TestCase):
    def test_hmac_sha1_string(self):
        self.assertEqual(hmac_sha1("hello", "key"), "b34ceac4516ff23a143e61d79d0fa7a4fbe5f266")

    def test_hmac_sha1_bytes(self):
        self.assertEqual(hmac_sha1(b"hello", b"key"), "b34ceac4516ff23a143e61d79d0fa7a4fbe5f266")

    def test_hmac_sha1_type_error(self):
        with self.assertRaises(TypeError):
            hmac_sha1(123, "key")  # type: ignore[arg-type]


class TestHmacSHA256(unittest.TestCase):
    def test_hmac_sha256_string(self):
        self.assertEqual(
            hmac_sha256("hello", "key"),
            "9307b3b915efb5171ff14d8cb55fbcc798c6c0ef1456d66ded1a6aa723a58b7b",
        )

    def test_hmac_sha256_bytes(self):
        self.assertEqual(
            hmac_sha256(b"hello", b"key"),
            "9307b3b915efb5171ff14d8cb55fbcc798c6c0ef1456d66ded1a6aa723a58b7b",
        )

    def test_hmac_sha256_type_error(self):
        with self.assertRaises(TypeError):
            hmac_sha256(123, "key")  # type: ignore[arg-type]


class TestHmacSHA512(unittest.TestCase):
    def test_hmac_sha512_string(self):
        self.assertEqual(
            hmac_sha512("hello", "key"),
            "ff06ab36757777815c008d32c8e14a705b4e7bf310351a06a23b612dc4c7433e"
            "7757d20525a5593b71020ea2ee162d2311b247e9855862b270122419652c0c92",
        )

    def test_hmac_sha512_bytes(self):
        self.assertEqual(
            hmac_sha512(b"hello", b"key"),
            "ff06ab36757777815c008d32c8e14a705b4e7bf310351a06a23b612dc4c7433e"
            "7757d20525a5593b71020ea2ee162d2311b247e9855862b270122419652c0c92",
        )

    def test_hmac_sha512_type_error(self):
        with self.assertRaises(TypeError):
            hmac_sha512(123, "key")  # type: ignore[arg-type]


class TestHmacNew(unittest.TestCase):
    def test_hmac_new_default_algorithm(self):
        self.assertEqual(hmac_new("hello", "key"), hmac_sha256("hello", "key"))

    def test_hmac_new_sha1(self):
        self.assertEqual(hmac_new("hello", "key", "sha1"), hmac_sha1("hello", "key"))

    def test_hmac_new_unsupported_algorithm(self):
        with self.assertRaises(ValueError):
            hmac_new("hello", "key", "sha3")  # type: ignore[arg-type]


class TestSignVerify(unittest.TestCase):
    def test_sign_roundtrip(self):
        signature = sign("hello", "key")
        self.assertTrue(verify("hello", "key", signature))

    def test_sign_default_matches_sha256(self):
        self.assertEqual(sign("hello", "key"), hmac_sha256("hello", "key"))

    def test_verify_wrong_signature(self):
        self.assertFalse(verify("hello", "key", "deadbeef"))

    def test_verify_different_data(self):
        self.assertFalse(verify("hello", "key", sign("world", "key")))

    def test_verify_different_key(self):
        self.assertFalse(verify("hello", "wrong", sign("hello", "key")))


class TestCompareDigest(unittest.TestCase):
    def test_compare_digest_equal(self):
        self.assertTrue(compare_digest("abc", "abc"))

    def test_compare_digest_not_equal(self):
        self.assertFalse(compare_digest("abc", "abd"))

    def test_compare_digest_type_error(self):
        with self.assertRaises(TypeError):
            compare_digest(123, "abc")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            compare_digest("abc", 123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
