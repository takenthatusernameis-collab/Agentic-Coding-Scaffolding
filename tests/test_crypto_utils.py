"""Tests for crypto_utils module."""

import unittest

from crypto_utils import base64_decode, base64_encode, generate_token, hash_string


class TestHashString(unittest.TestCase):
    def test_sha256_default(self) -> None:
        result = hash_string("hello")
        self.assertEqual(len(result), 64)
        self.assertEqual(
            result,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_md5(self) -> None:
        result = hash_string("hello", algorithm="md5")
        self.assertEqual(len(result), 32)
        self.assertEqual(
            result,
            "5d41402abc4b2a76b9719d911017c592",
        )

    def test_sha1(self) -> None:
        result = hash_string("hello", algorithm="sha1")
        self.assertEqual(len(result), 40)

    def test_sha512(self) -> None:
        result = hash_string("hello", algorithm="sha512")
        self.assertEqual(len(result), 128)

    def test_uppercase_algorithm(self) -> None:
        result = hash_string("hello", algorithm="SHA256")
        self.assertEqual(len(result), 64)

    def test_invalid_algorithm(self) -> None:
        with self.assertRaises(ValueError):
            hash_string("hello", algorithm="not-a-real-algo")

    def test_non_string_value(self) -> None:
        with self.assertRaises(TypeError):
            hash_string(123)  # type: ignore[arg-type]

    def test_empty_string(self) -> None:
        result = hash_string("")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)

    def test_different_inputs_different_hashes(self) -> None:
        self.assertNotEqual(hash_string("hello"), hash_string("world"))


class TestGenerateToken(unittest.TestCase):
    def test_default_length(self) -> None:
        token = generate_token()
        self.assertEqual(len(token), 64)

    def test_custom_length(self) -> None:
        token = generate_token(16)
        self.assertEqual(len(token), 32)

    def test_length_one(self) -> None:
        token = generate_token(1)
        self.assertEqual(len(token), 2)

    def test_uniqueness(self) -> None:
        tokens = {generate_token(16) for _ in range(100)}
        self.assertEqual(len(tokens), 100)

    def test_zero_length_raises(self) -> None:
        with self.assertRaises(ValueError):
            generate_token(0)

    def test_negative_length_raises(self) -> None:
        with self.assertRaises(ValueError):
            generate_token(-1)

    def test_non_integer_length_raises(self) -> None:
        with self.assertRaises(TypeError):
            generate_token("16")  # type: ignore[arg-type]

    def test_boolean_length_raises(self) -> None:
        with self.assertRaises(TypeError):
            generate_token(True)

    def test_hex_characters_only(self) -> None:
        token = generate_token(16)
        self.assertTrue(all(c in "0123456789abcdef" for c in token))


class TestBase64Encode(unittest.TestCase):
    def test_encode_hello(self) -> None:
        self.assertEqual(base64_encode("hello"), "aGVsbG8=")

    def test_encode_empty(self) -> None:
        self.assertEqual(base64_encode(""), "")

    def test_encode_unicode(self) -> None:
        encoded = base64_encode("héllo")
        self.assertEqual(base64_decode(encoded), "héllo")

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            base64_encode(123)  # type: ignore[arg-type]

    def test_roundtrip(self) -> None:
        original = "The quick brown fox jumps over the lazy dog"
        self.assertEqual(base64_decode(base64_encode(original)), original)


class TestBase64Decode(unittest.TestCase):
    def test_decode_hello(self) -> None:
        self.assertEqual(base64_decode("aGVsbG8="), "hello")

    def test_decode_empty(self) -> None:
        self.assertEqual(base64_decode(""), "")

    def test_invalid_base64_raises(self) -> None:
        with self.assertRaises(ValueError):
            base64_decode("!!!not-base64!!!")

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            base64_decode(123)  # type: ignore[arg-type]

    def test_unpadded_input_raises(self) -> None:
        with self.assertRaises(ValueError):
            base64_decode("aGVsbG8")


if __name__ == "__main__":
    unittest.main()
