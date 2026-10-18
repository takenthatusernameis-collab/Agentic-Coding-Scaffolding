"""Unit tests for hash_utils module."""

import tempfile
import unittest
from pathlib import Path

from hash_utils import (
    crc32,
    hash_file,
    md5,
    sha1,
    sha256,
    sha512,
)


class TestMD5(unittest.TestCase):
    def test_md5_string(self):
        result = md5("hello")
        self.assertEqual(result, "5d41402abc4b2a76b9719d911017c592")

    def test_md5_bytes(self):
        result = md5(b"hello")
        self.assertEqual(result, "5d41402abc4b2a76b9719d911017c592")

    def test_md5_empty_string(self):
        result = md5("")
        self.assertEqual(result, "d41d8cd98f00b204e9800998ecf8427e")

    def test_md5_type_error(self):
        with self.assertRaises(TypeError):
            md5(123)  # type: ignore[arg-type]


class TestSHA1(unittest.TestCase):
    def test_sha1_string(self):
        result = sha1("hello")
        self.assertEqual(result, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")

    def test_sha1_bytes(self):
        result = sha1(b"hello")
        self.assertEqual(result, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")

    def test_sha1_empty(self):
        result = sha1("")
        self.assertEqual(result, "da39a3ee5e6b4b0d3255bfef95601890afd80709")

    def test_sha1_type_error(self):
        with self.assertRaises(TypeError):
            sha1(123)  # type: ignore[arg-type]


class TestSHA256(unittest.TestCase):
    def test_sha256_string(self):
        result = sha256("hello")
        self.assertEqual(
            result,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_sha256_bytes(self):
        result = sha256(b"hello")
        self.assertEqual(
            result,
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_sha256_type_error(self):
        with self.assertRaises(TypeError):
            sha256({})  # type: ignore[arg-type]


class TestSHA512(unittest.TestCase):
    def test_sha512_string(self):
        result = sha512("hello")
        self.assertTrue(
            result.startswith(
                "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043"
            )
        )

    def test_sha512_type_error(self):
        with self.assertRaises(TypeError):
            sha512(None)  # type: ignore[arg-type]


class TestCRC32(unittest.TestCase):
    def test_crc32_string(self):
        result = crc32("hello")
        self.assertEqual(result, 0x3610A686)

    def test_crc32_bytes(self):
        result = crc32(b"hello")
        self.assertEqual(result, 0x3610A686)

    def test_crc32_type_error(self):
        with self.assertRaises(TypeError):
            crc32([1, 2, 3])  # type: ignore[arg-type]


class TestHashFile(unittest.TestCase):
    def test_hash_file_sha256(self):
        content = "hello world"
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write(content)
            temp_path = f.name

        try:
            result = hash_file(temp_path)
            expected = sha256(content)
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()

    def test_hash_file_md5(self):
        content = "test data"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = hash_file(temp_path, algorithm="md5")
            expected = md5(content)
            self.assertEqual(result, expected)
        finally:
            Path(temp_path).unlink()

    def test_hash_file_with_bytes_path(self):
        content = "test"
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(content)
            temp_path = f.name.encode("utf-8")

        try:
            result = hash_file(temp_path, algorithm="sha1")
            expected = sha1(content)
            self.assertEqual(result, expected)
        finally:
            Path(f.name).unlink()

    def test_hash_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            hash_file("/non/existent/file.txt")

    def test_hash_file_unsupported_algorithm(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("data")
            temp_path = f.name

        try:
            with self.assertRaises(ValueError):
                hash_file(temp_path, algorithm="invalid")
        finally:
            Path(temp_path).unlink()

    def test_hash_file_type_error(self):
        with self.assertRaises(TypeError):
            hash_file(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
