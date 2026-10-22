"""Tests for chunk_utils."""

import io
import struct
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import chunk_utils

HAVE_CHUNK = chunk_utils.is_available()


def make_chunk(name, payload, bigendian=True, align=True, inclheader=False):
    """Build the bytes of a single chunk with the given name and payload."""
    prefix = ">" if bigendian else "<"
    size = len(payload) + (8 if inclheader else 0)
    body = name + struct.pack(prefix + "L", size) + payload
    if align and len(payload) % 2:
        body += b"\x00"
    return body


#: A stream that holds fewer than eight bytes cannot be opened as a chunk.
SHORT = b"ab"


class TestAvailability(unittest.TestCase):
    """The wrapper reports whether the interpreter ships the module."""

    def test_is_available_matches_the_import(self):
        self.assertEqual(chunk_utils.is_available(), HAVE_CHUNK)

    def test_the_readers_raise_when_the_module_is_missing(self):
        with mock.patch.object(chunk_utils, "_chunk", None):
            self.assertFalse(chunk_utils.is_available())
            with self.assertRaises(RuntimeError):
                chunk_utils.open_chunk(io.BytesIO(make_chunk(b"TEXT", b"data")))
            with self.assertRaises(RuntimeError):
                chunk_utils.read_chunk(io.BytesIO(make_chunk(b"TEXT", b"data")))
            with self.assertRaises(RuntimeError):
                chunk_utils.peek_chunk(io.BytesIO(make_chunk(b"TEXT", b"data")))
            with self.assertRaises(RuntimeError):
                chunk_utils.skip_chunk(io.BytesIO(make_chunk(b"TEXT", b"data")))
            with self.assertRaises(RuntimeError):
                chunk_utils.iter_chunks(io.BytesIO(make_chunk(b"TEXT", b"data")))
            with self.assertRaises(RuntimeError):
                chunk_utils.read_chunks(io.BytesIO(make_chunk(b"TEXT", b"data")))

    def test_the_writers_keep_working_when_the_module_is_missing(self):
        with mock.patch.object(chunk_utils, "_chunk", None):
            self.assertEqual(chunk_utils.chunk_name(b"TEXT"), "TEXT")
            self.assertEqual(
                chunk_utils.build_chunk(b"TEXT", b"data"),
                make_chunk(b"TEXT", b"data"),
            )
            stream = io.BytesIO()
            written = chunk_utils.write_chunk(stream, b"TEXT", b"data")
            self.assertEqual(written, len(make_chunk(b"TEXT", b"data")))


class TestChunkName(unittest.TestCase):
    """The wrapper decodes the identifier of a chunk."""

    def test_bytes_are_decoded(self):
        self.assertEqual(chunk_utils.chunk_name(b"FORM"), "FORM")

    def test_text_is_accepted(self):
        self.assertEqual(chunk_utils.chunk_name("FORM"), "FORM")

    def test_every_byte_maps_to_one_character(self):
        self.assertEqual(chunk_utils.chunk_name(b"\x00\xffA "), "\x00ÿA ")

    def test_a_name_of_the_wrong_length_is_rejected(self):
        with self.assertRaises(ValueError):
            chunk_utils.chunk_name(b"TEX")
        with self.assertRaises(ValueError):
            chunk_utils.chunk_name("TEX")

    def test_a_name_that_is_not_ascii_is_rejected(self):
        with self.assertRaises(ValueError):
            chunk_utils.chunk_name("TÉXT")

    def test_an_unsupported_name_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.chunk_name(42)


class TestBuildChunk(unittest.TestCase):
    """The wrapper builds the bytes of a chunk."""

    def test_the_bytes_of_a_chunk_are_built(self):
        self.assertEqual(
            chunk_utils.build_chunk(b"TEXT", b"hello"),
            b"TEXT" + struct.pack(">L", 5) + b"hello" + b"\x00",
        )

    def test_an_even_payload_is_not_padded(self):
        self.assertEqual(
            chunk_utils.build_chunk(b"TEXT", b"hello!"),
            b"TEXT" + struct.pack(">L", 6) + b"hello!",
        )

    def test_the_padding_can_be_left_out(self):
        self.assertEqual(
            chunk_utils.build_chunk(b"TEXT", b"hello", align=False),
            b"TEXT" + struct.pack(">L", 5) + b"hello",
        )

    def test_a_little_endian_size_is_written(self):
        self.assertEqual(
            chunk_utils.build_chunk(b"TEXT", b"hello", bigendian=False),
            b"TEXT" + struct.pack("<L", 5) + b"hello" + b"\x00",
        )

    def test_the_size_can_include_the_header(self):
        self.assertEqual(
            chunk_utils.build_chunk(b"TEXT", b"hello", inclheader=True),
            b"TEXT" + struct.pack(">L", 13) + b"hello" + b"\x00",
        )

    def test_text_is_accepted_as_the_identifier(self):
        self.assertEqual(
            chunk_utils.build_chunk("TEXT", b"hello"),
            chunk_utils.build_chunk(b"TEXT", b"hello"),
        )

    def test_a_bytearray_is_accepted_as_the_payload(self):
        self.assertEqual(
            chunk_utils.build_chunk(b"TEXT", bytearray(b"hello")),
            chunk_utils.build_chunk(b"TEXT", b"hello"),
        )

    def test_an_unsupported_payload_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.build_chunk(b"TEXT", "hello")

    def test_an_unsupported_identifier_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.build_chunk(42, b"hello")

    def test_an_unsupported_flag_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.build_chunk(b"TEXT", b"hello", bigendian=1)
        with self.assertRaises(TypeError):
            chunk_utils.build_chunk(b"TEXT", b"hello", align="yes")
        with self.assertRaises(TypeError):
            chunk_utils.build_chunk(b"TEXT", b"hello", inclheader=None)


class TestWriteChunk(unittest.TestCase):
    """The wrapper writes a chunk."""

    def test_a_chunk_is_written_to_a_stream(self):
        stream = io.BytesIO()
        written = chunk_utils.write_chunk(stream, b"TEXT", b"hello")
        self.assertEqual(written, len(make_chunk(b"TEXT", b"hello")))
        self.assertEqual(stream.getvalue(), make_chunk(b"TEXT", b"hello"))

    def test_a_chunk_is_written_to_a_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            written = chunk_utils.write_chunk(str(path), b"TEXT", b"hello")
            self.assertEqual(written, len(make_chunk(b"TEXT", b"hello")))
            self.assertEqual(path.read_bytes(), make_chunk(b"TEXT", b"hello"))

    def test_a_written_chunk_is_read_back(self):
        stream = io.BytesIO()
        chunk_utils.write_chunk(stream, b"TEXT", b"hello")
        stream.seek(0)
        record = chunk_utils.read_chunk(stream)
        self.assertEqual(record.name, b"TEXT")
        self.assertEqual(record.size, 5)
        self.assertEqual(record.data, b"hello")

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.write_chunk(42, b"TEXT", b"hello")

    def test_a_text_stream_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.write_chunk(io.StringIO(), b"TEXT", b"hello")


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
        chunk = chunk_utils.open_chunk(stream)
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

    def test_a_text_stream_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(io.StringIO())

    def test_an_unsupported_flag_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"data"))
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(stream, bigendian=0)
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(stream, align="no")
        with self.assertRaises(TypeError):
            chunk_utils.open_chunk(stream, inclheader=1)


class TestReadChunk(unittest.TestCase):
    """The wrapper reads a chunk in one call."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_record_of_a_chunk_is_returned(self):
        data = make_chunk(b"TEXT", b"hello world")
        record = chunk_utils.read_chunk(io.BytesIO(data))
        self.assertEqual(record.name, b"TEXT")
        self.assertEqual(record.size, 11)
        self.assertEqual(record.data, b"hello world")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_identifier_is_decoded_as_text(self):
        data = make_chunk(b"FORM", b"data")
        record = chunk_utils.read_chunk(io.BytesIO(data))
        self.assertEqual(record.text_name, "FORM")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_byte_stream_is_accepted(self):
        data = make_chunk(b"FORM", b"\x00\x01\x02\x03")
        record = chunk_utils.read_chunk(io.BytesIO(data))
        self.assertEqual(record.data, b"\x00\x01\x02\x03")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            path.write_bytes(make_chunk(b"TEXT", b"from file"))
            self.assertEqual(chunk_utils.read_chunk(str(path)).data, b"from file")
            self.assertEqual(chunk_utils.read_chunk(path).data, b"from file")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_stream_moves_past_the_chunk(self):
        data = make_chunk(b"TEXT", b"payload")
        stream = io.BytesIO(data)
        chunk_utils.read_chunk(stream)
        self.assertEqual(stream.tell(), len(data))

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_little_endian_chunk_is_read(self):
        data = make_chunk(b"TEXT", b"little", bigendian=False)
        record = chunk_utils.read_chunk(io.BytesIO(data), bigendian=False)
        self.assertEqual(record.data, b"little")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_chunk_with_an_odd_payload_is_read(self):
        data = make_chunk(b"TEXT", b"odd")
        record = chunk_utils.read_chunk(io.BytesIO(data))
        self.assertEqual(record.data, b"odd")
        self.assertEqual(record.size, 3)

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_chunk_whose_size_includes_the_header_is_read(self):
        data = make_chunk(b"TEXT", b"odd", inclheader=True)
        record = chunk_utils.read_chunk(io.BytesIO(data), inclheader=True)
        self.assertEqual(record.size, 3)
        self.assertEqual(record.data, b"odd")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_truncated_chunk_reports_the_bytes_it_read(self):
        data = make_chunk(b"TEXT", b"payload")[:-3]
        record = chunk_utils.read_chunk(io.BytesIO(data))
        self.assertEqual(record.size, 7)
        self.assertEqual(record.data, b"paylo")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_short_stream_raises(self):
        with self.assertRaises(EOFError):
            chunk_utils.read_chunk(io.BytesIO(SHORT))

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(42)
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(b"\x00\x00\x00\x00\x00\x00\x00\x00")

    def test_a_text_stream_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(io.StringIO())

    def test_an_unsupported_flag_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"data"))
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(stream, bigendian=1)
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(stream, align="yes")
        with self.assertRaises(TypeError):
            chunk_utils.read_chunk(stream, inclheader=None)


class TestPeekChunk(unittest.TestCase):
    """The wrapper inspects the next chunk without consuming it."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_stream_position_is_restored(self):
        data = make_chunk(b"TEXT", b"payload")
        stream = io.BytesIO(data)
        position = stream.tell()
        record = chunk_utils.peek_chunk(stream)
        self.assertEqual(record.data, b"payload")
        self.assertEqual(stream.tell(), position)

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_chunk_can_be_read_afterwards(self):
        data = make_chunk(b"TEXT", b"payload")
        stream = io.BytesIO(data)
        chunk_utils.peek_chunk(stream)
        self.assertEqual(chunk_utils.read_chunk(stream).data, b"payload")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            path.write_bytes(make_chunk(b"TEXT", b"from file"))
            self.assertEqual(chunk_utils.peek_chunk(path).data, b"from file")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_stream_that_cannot_be_seeked_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"payload"))
        with mock.patch.object(
            stream, "tell", side_effect=io.UnsupportedOperation("tell")
        ):
            with self.assertRaises(ValueError):
                chunk_utils.peek_chunk(stream)

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.peek_chunk(42)

    def test_an_unsupported_flag_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"data"))
        with self.assertRaises(TypeError):
            chunk_utils.peek_chunk(stream, align=1)


class TestIterChunks(unittest.TestCase):
    """The wrapper iterates over the chunks of a file."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_every_chunk_is_yielded(self):
        data = make_chunk(b"TEXT", b"one") + make_chunk(b"FORM", b"two")
        records = list(chunk_utils.iter_chunks(io.BytesIO(data)))
        self.assertEqual([record.name for record in records], [b"TEXT", b"FORM"])
        self.assertEqual([record.data for record in records], [b"one", b"two"])

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            path.write_bytes(make_chunk(b"TEXT", b"one") + make_chunk(b"FORM", b"two"))
            records = list(chunk_utils.iter_chunks(path))
            self.assertEqual(len(records), 2)

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_an_empty_file_yields_no_chunk(self):
        self.assertEqual(list(chunk_utils.iter_chunks(io.BytesIO(b""))), [])

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_arguments_are_validated_before_the_file_is_read(self):
        with self.assertRaises(TypeError):
            chunk_utils.iter_chunks(42)
        with self.assertRaises(TypeError):
            chunk_utils.iter_chunks(io.BytesIO(b""), align=1)

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.iter_chunks(object())


class TestReadChunks(unittest.TestCase):
    """The wrapper returns every chunk of a file as a list."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_every_chunk_is_returned(self):
        data = make_chunk(b"TEXT", b"one") + make_chunk(b"FORM", b"two")
        records = chunk_utils.read_chunks(io.BytesIO(data))
        self.assertEqual(len(records), 2)
        self.assertIsInstance(records, list)

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            path.write_bytes(make_chunk(b"TEXT", b"one"))
            self.assertEqual(len(chunk_utils.read_chunks(path)), 1)

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.read_chunks(42)


class TestSkipChunk(unittest.TestCase):
    """The wrapper skips the payload of a chunk."""

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_the_payload_is_skipped(self):
        data = make_chunk(b"TEXT", b"payload") + make_chunk(b"FORM", b"next")
        stream = io.BytesIO(data)
        skipped = chunk_utils.skip_chunk(stream)
        self.assertEqual(skipped, 7)
        self.assertEqual(chunk_utils.read_chunk(stream).name, b"FORM")

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "chunk.dat"
            path.write_bytes(make_chunk(b"TEXT", b"payload"))
            self.assertEqual(chunk_utils.skip_chunk(path), 7)

    @unittest.skipUnless(HAVE_CHUNK, "the chunk module is not available")
    def test_a_short_stream_raises(self):
        with self.assertRaises(EOFError):
            chunk_utils.skip_chunk(io.BytesIO(SHORT))

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            chunk_utils.skip_chunk(42)

    def test_an_unsupported_flag_is_rejected(self):
        stream = io.BytesIO(make_chunk(b"TEXT", b"data"))
        with self.assertRaises(TypeError):
            chunk_utils.skip_chunk(stream, inclheader="yes")


if __name__ == "__main__":
    unittest.main()
