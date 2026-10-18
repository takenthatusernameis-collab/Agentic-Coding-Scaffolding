"""Tests for lzma_utils."""

import os
import tempfile

from lzma_utils import (
    lzma_compress,
    lzma_decompress,
    lzma_open,
    lzma_read,
    lzma_write,
)


def test_lzma_compress_decompress_roundtrip():
    data = b"hello world" * 10
    compressed = lzma_compress(data)
    assert lzma_decompress(compressed) == data


def test_lzma_write_read_roundtrip():
    data = b"hello world" * 10
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "test.xz")
        lzma_write(path, data)
        assert lzma_read(path) == data


def test_lzma_open():
    data = b"hello world"
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "test.xz")
        with lzma_open(path, "wb") as f:
            f.write(data)
        with lzma_open(path, "rb") as f:
            assert f.read() == data
