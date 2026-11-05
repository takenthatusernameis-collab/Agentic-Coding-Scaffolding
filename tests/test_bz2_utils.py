"""Tests for bz2_utils."""

import os
import tempfile
import unittest
from pathlib import Path

from bz2_utils import (
    bz2_compress,
    bz2_decompress,
    bz2_open,
    bz2_read,
    bz2_write,
)


class TestBz2Utils(unittest.TestCase):

    def test_bz2_compress_decompress_roundtrip(self):
        data = b"hello world" * 10
        compressed = bz2_compress(data)
        assert bz2_decompress(compressed) == data


    def test_bz2_compress_empty_data(self):
        compressed = bz2_compress(b"")
        assert bz2_decompress(compressed) == b""


    def test_bz2_compress_single_byte(self):
        data = b"x"
        compressed = bz2_compress(data)
        assert bz2_decompress(compressed) == data


    def test_bz2_compress_compresslevel_roundtrip(self):
        data = b"abcde" * 1000
        for level in (1, 5, 9):
            compressed = bz2_compress(data, compresslevel=level)
            assert bz2_decompress(compressed) == data


    def test_bz2_decompress_invalid_data_raises(self):
        with self.assertRaises(Exception):
            bz2_decompress(b"not valid bz2 data")


    def test_bz2_decompress_non_bytes_raises(self):
        with self.assertRaises(TypeError):
            bz2_decompress("not bytes")  # type: ignore[arg-type]


    def test_bz2_compress_non_bytes_raises(self):
        with self.assertRaises(TypeError):
            bz2_compress("not bytes")  # type: ignore[arg-type]


    def test_bz2_compress_negative_level_raises(self):
        with self.assertRaises(ValueError):
            bz2_compress(b"data", compresslevel=-1)


    def test_bz2_compress_level_too_high_raises(self):
        with self.assertRaises(ValueError):
            bz2_compress(b"data", compresslevel=10)


    def test_bz2_write_read_roundtrip(self):
        data = b"hello world" * 10
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.bz2")
            bz2_write(path, data)
            assert bz2_read(path) == data


    def test_bz2_write_empty_data(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "empty.bz2")
            bz2_write(path, b"")
            assert bz2_read(path) == b""


    def test_bz2_write_overwrites_existing(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "over.bz2")
            bz2_write(path, b"first")
            bz2_write(path, b"second")
            assert bz2_read(path) == b"second"


    def test_bz2_write_with_compresslevel(self):
        data = b"compress me" * 50
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "level.bz2")
            bz2_write(path, data, compresslevel=1)
            assert bz2_read(path) == data


    def test_bz2_read_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "missing.bz2")
            with self.assertRaises(FileNotFoundError):
                bz2_read(path)


    def test_bz2_read_directory_raises(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(IsADirectoryError):
                bz2_read(d)


    def test_bz2_open_write_read(self):
        data = b"hello world"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test.bz2")
            with bz2_open(path, "wb") as f:
                f.write(data)
            with bz2_open(path, "rb") as f:
                assert f.read() == data


    def test_bz2_open_text_mode(self):
        data = "hello world\n" * 5
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "text.bz2")
            with bz2_open(path, "wt") as f:
                f.write(data)
            with bz2_open(path, "rt") as f:
                assert f.read() == data


    def test_bz2_open_with_compresslevel(self):
        data = b"compress me" * 50
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "level.bz2")
            with bz2_open(path, "wb", compresslevel=1) as f:
                f.write(data)
            with bz2_open(path, "rb") as f:
                assert f.read() == data


    def test_bz2_open_pathlib_path(self):
        data = b"pathlib path"
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "pl.bz2"
            with bz2_open(str(path), "wb") as f:
                f.write(data)
            with bz2_open(str(path), "rb") as f:
                assert f.read() == data


    def test_bz2_roundtrip_large(self):
        data = bytes(range(256)) * 100
        compressed = bz2_compress(data)
        assert bz2_decompress(compressed) == data


    def test_bz2_open_default_mode_is_binary_read(self):
        data = b"default mode"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "default.bz2")
            bz2_write(path, data)
            with bz2_open(path) as f:
                assert f.read() == data


    def test_bz2_compress_idempotent(self):
        data = b"same data" * 5
        assert bz2_compress(data) == bz2_compress(data)


if __name__ == "__main__":
    unittest.main()
