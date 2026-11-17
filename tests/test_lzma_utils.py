"""Tests for lzma_utils."""

import os
import tempfile
import unittest

from lzma_utils import (
    lzma_compress,
    lzma_decompress,
    lzma_open,
    lzma_read,
    lzma_write,
)


class TestLzmaRoundtrips(unittest.TestCase):
    def test_compress_decompress_roundtrip(self):
        data = b"hello world" * 10
        compressed = lzma_compress(data)
        self.assertEqual(lzma_decompress(compressed), data)

    def test_write_read_roundtrip(self):
        data = b"hello world" * 10
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.xz")
            lzma_write(path, data)
            self.assertEqual(lzma_read(path), data)

    def test_open(self):
        data = b"hello world"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.xz")
            with lzma_open(path, "wb") as f:
                f.write(data)
            with lzma_open(path, "rb") as f:
                self.assertEqual(f.read(), data)


class TestLzmaPresetValidation(unittest.TestCase):
    def test_compress_rejects_bool_preset(self):
        with self.assertRaises(TypeError):
            lzma_compress(b"x", preset=True)
        with self.assertRaises(TypeError):
            lzma_compress(b"x", preset=False)

    def test_write_rejects_bool_preset(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.xz")
            with self.assertRaises(TypeError):
                lzma_write(path, b"x", preset=True)
            with self.assertRaises(TypeError):
                lzma_write(path, b"x", preset=False)

    def test_open_rejects_bool_preset(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.xz")
            with self.assertRaises(TypeError):
                lzma_open(path, "wb", preset=True)
            with self.assertRaises(TypeError):
                lzma_open(path, "wb", preset=False)

    def test_open_read_ignores_bool_preset(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.xz")
            with lzma_open(path, "wb") as f:
                f.write(b"hello")
            with lzma_open(path, "rb", preset=True) as f:
                self.assertEqual(f.read(), b"hello")
            with lzma_open(path, "rb", preset=False) as f:
                self.assertEqual(f.read(), b"hello")


if __name__ == "__main__":
    unittest.main()
