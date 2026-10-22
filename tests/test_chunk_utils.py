"""Tests for chunk_utils."""

import io
import struct
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import chunk_utils

HAVE_CHUNK = chunk_utils.is_available()


def make_chunk(name, payload, bigendian=True, inclheader=False):
    """Build the bytes of a single chunk with the given name and payload."""
    strflag = ">" if bigendian else "<"
    size = len(payload) + (8 if inclheader else 0)
    return name + struct.pack(strflag + "L", size) + payload


#: A stream that holds fewer than eight bytes cannot be opened as a chunk.
SHORT = b"ab"


class TestAvailability(unittest.TestCase):
    """The wrapper reports whether the interpreter ships the module."""

    def test_is_available_matches_the_import(self):
        self.assertEqual(chunk_utils.is_available(), HAVE_CHUNK)

    def test_helpers_raise_when_the_module_is_missing(self):
        with mock.patch.object(chunk_utils, "_chunk", None):
            self.assertFalse(chunk_utils.is_available())
            with self.assertRaises(RuntimeError):
                chunk_utils.open_chunk(io.BytesIO(make_chunk(b"TEXT", b"data")))
            with self.assertRaises(RuntimeError):
                chunk_utils.read_chunk(io.BytesIO(make_chunk(b"TEXT", b"data")))


class TestReadChunk(unittest.TestCase):
    """The wrapper reads the payload of a chunk in one call."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_payload_of_a_chunk_is_returned(self):
        data = make_chunk(b"TEXT", b"hello world")
        self.assertEqual(chunk_utils.read_chunk(io.BytesIO(data)), b"hello world")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_byte_stream_is_accepted(self):
        data = make_chunk(b"FORM", b"\x00\x01\x02\x03")
        self.assertEqual(chunk_utils.read_chunk(io.BytesIO(data)), b"\x00\x01\x02\x03")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_stream_position_is_restored(self):
        data = make_chunk(b"TEXT", b"payload")
        stream = io.BytesIO(b"prefix" + data + b"suffix")
        stream.read(6)
        position = stream.tell()
        self.assertEqual(chunk_utils.read_chunk(stream), b"payload")
        self.assertEqual(stream.tell(), position)

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            path.write_bytes(make_chunk(b"TEXT", b"from file"))
            self.assertEqual(chunk_utils.read_chunk(str(path)), b"from file")
            self.assertEqual(chunk_utils.read_chunk(path), b"from file")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_little_endian_chunk_is_read(self):
        data = make_chunk(b"TEXT", b"little", bigendian=False)
        self.assertEqual(
            chunk_utils.read_chunk(io.BytesIO(data), bigendian=False), b"little"
        )

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_chunk_with_an_odd_payload_is_read(self):
        data = make_chunk(b"TEXT", b"odd")
        self.assertEqual(
            chunk_utils.read_chunk(io.BytesIO(data), align=True), b"odd"
        )

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(42)
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(b"\x00\x00\x00\x00\x00\x00\x00\x00")

    def test_an_unsupported_flag_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"data"))
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(stream, bigendian=1)
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(stream, align="yes")
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(stream, inclheader=None)


class TestOpenChunk(unittest.TestCase):
    """The wrapper opens a chunk and exposes its name and size."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_name_and_the_size_of_a_chunk_are_reported(self):
        data = make_chunk(b"FORM", b"payload data")
        chunk = chunk_utils.open_chunk(io.BytesIO(data))
        self.assertEqual(chunk.getname(), b"FORM")
        self.assertEqual(chunk.getsize(), len(b"payload data"))
        self.assertEqual(chunk.read(), b"payload data")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_skip_moves_to_the_end_of_the_chunk(self):
        data = make_chunk(b"TEXT", b"skip me")
        stream = io.BytesIO(data)
        chunk = chunk_utils.open_chunk(stream, align=False)
        chunk.skip()
        self.assertEqual(stream.tell(), len(data))

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_chunk_can_be_closed(self):
        data = make_chunk(b"TEXT", b"close me")
        chunk = chunk_utils.open_chunk(io.BytesIO(data))
        chunk.close()
        self.assertTrue(chunk.closed)

    def test_an_unsupported_stream_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(42)
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(b"not a stream")

    def test_an_unsupported_flag_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"data"))
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(stream, bigendian=0)
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(stream, align="no")
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(stream, inclheader=1)


if __name__ == "__main__":
    unittest.main()
