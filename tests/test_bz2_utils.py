"""Tests for bz2_utils."""

import os
import tempfile

from bz2_utils import (
    bz2_compress,
    bz2_decompress,
    bz2_open,
    bz2_read,
    bz2_write,
)


def test_bz2_compress_decompress_roundtrip():
    data = b"hello world" * 10
    compressed = bz2_compress(data)
    assert bz2_decompress(compressed) == data


def test_bz2_write_read_roundtrip():
    data = b"hello world" * 10
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "test.bz2")
        bz2_write(path, data)
        assert bz2_read(path) == data


def test_bz2_open():
    data = b"hello world"
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "test.bz2")
        with bz2_open(path, "wb") as f:
            f.write(data)
        with bz2_open(path, "rb") as f:
            assert f.read() == data
