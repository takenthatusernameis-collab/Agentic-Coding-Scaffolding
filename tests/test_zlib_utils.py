"""Tests for zlib_utils."""

from zlib_utils import (
    zlib_adler32,
    zlib_compress,
    zlib_compressobj,
    zlib_crc32,
    zlib_decompress,
    zlib_decompressobj,
)


def test_zlib_compress_decompress_roundtrip():
    data = b"hello world" * 10
    compressed = zlib_compress(data)
    assert zlib_decompress(compressed) == data


def test_zlib_compressobj_decompressobj_roundtrip():
    data = b"hello world" * 10
    co = zlib_compressobj()
    compressed = co.compress(data) + co.flush()
    do = zlib_decompressobj()
    assert do.decompress(compressed) == data


def test_zlib_crc32():
    assert zlib_crc32(b"hello") == 907060870


def test_zlib_adler32():
    assert zlib_adler32(b"hello") == 103547413
