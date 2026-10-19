"""Tests for zlib_utils."""

import unittest

from zlib_utils import (
    zlib_adler32,
    zlib_compress,
    zlib_compressobj,
    zlib_crc32,
    zlib_decompress,
    zlib_decompressobj,
)


class TestZlibUtils(unittest.TestCase):
    def test_compress_decompress_roundtrip(self):
        data = b"hello world" * 10
        compressed = zlib_compress(data)
        self.assertNotEqual(compressed, data)
        self.assertEqual(zlib_decompress(compressed), data)

    def test_compress_with_level(self):
        data = b"hello world" * 100
        compressed = zlib_compress(data, level=9)
        self.assertEqual(zlib_decompress(compressed), data)

    def test_compressobj_decompressobj_roundtrip(self):
        data = b"hello world" * 10
        co = zlib_compressobj()
        compressed = co.compress(data) + co.flush()
        do = zlib_decompressobj()
        self.assertEqual(do.decompress(compressed), data)

    def test_crc32(self):
        self.assertEqual(zlib_crc32(b"hello"), 907060870)

    def test_adler32(self):
        self.assertEqual(zlib_adler32(b"hello"), 103547413)

    def test_compress_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            zlib_compress("not bytes")  # type: ignore[arg-type]

    def test_decompress_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            zlib_decompress("not bytes")  # type: ignore[arg-type]

    def test_crc32_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            zlib_crc32("not bytes")  # type: ignore[arg-type]

    def test_adler32_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            zlib_adler32("not bytes")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
