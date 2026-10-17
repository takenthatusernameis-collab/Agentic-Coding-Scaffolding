"""Tests for gzip_utils."""

import os
import tempfile

from gzip_utils import (
    gzip_compress,
    gzip_decompress,
    gzip_open,
    gzip_read,
    gzip_write,
)


def test_gzip_compress_decompress():
    data = b"hello world" * 10
    compressed = gzip_compress(data)
    assert isinstance(compressed, bytes)
    assert gzip_decompress(compressed) == data


def test_gzip_compress_level():
    data = b"hello world" * 10
    c9 = gzip_compress(data, compresslevel=9)
    c1 = gzip_compress(data, compresslevel=1)
    assert gzip_decompress(c9) == data
    assert gzip_decompress(c1) == data


def test_gzip_open():
    data = b"hello"
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        name = tmp.name
    try:
        with gzip_open(name, "wb") as f:
            f.write(data)
        with gzip_open(name, "rb") as f:
            assert f.read() == data
    finally:
        os.remove(name)


def test_gzip_write_read():
    data = b"hello world"
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        name = tmp.name
    try:
        gzip_write(name, data)
        assert gzip_read(name) == data
    finally:
        os.remove(name)
