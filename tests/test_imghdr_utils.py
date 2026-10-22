"""Tests for imghdr_utils."""

import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import imghdr_utils

HAVE_IMGHDR = imghdr_utils.is_available()

#: The headers of the formats the standard library recognizes.
HEADERS = {
    "png": b"\x89PNG\r\n\x1a\n" + b"\x00" * 24,
    "jpeg": b"\xff\xd8\xff\xdb" + b"\x00" * 28,
    "gif": b"GIF89a" + b"\x00" * 26,
    "tiff": b"MM\x00\x2a" + b"\x00" * 28,
    "rgb": b"\x01\xda" + b"\x00" * 30,
    "pbm": b"P1 4 4" + b"\x00" * 26,
    "pgm": b"P2 4 4" + b"\x00" * 26,
    "ppm": b"P3 4 4" + b"\x00" * 26,
    "rast": b"\x59\xa6\x6a\x95" + b"\x00" * 28,
    "xbm": b"#define x_width 4" + b"\x00" * 16,
    "bmp": b"BM" + b"\x00" * 30,
    "webp": b"RIFF" + b"\x00" * 4 + b"WEBP" + b"\x00" * 20,
    "exr": b"\x76\x2f\x31\x01" + b"\x00" * 28,
}

#: Bytes that no format of the standard library recognizes.
UNKNOWN = b"hello world" + b"\x00" * 21


class TestAvailability(unittest.TestCase):
    """The wrapper reports whether the interpreter ships the module."""

    def test_is_available_matches_the_import(self):
        self.assertEqual(imghdr_utils.is_available(), HAVE_IMGHDR)

    def test_helpers_raise_when_the_module_is_missing(self):
        with mock.patch.object(imghdr_utils, "_imghdr", None):
            self.assertFalse(imghdr_utils.is_available())
            with self.assertRaises(RuntimeError):
                imghdr_utils.what(io.BytesIO(HEADERS["png"]))
            with self.assertRaises(RuntimeError):
                imghdr_utils.detect(HEADERS["png"])
            with self.assertRaises(RuntimeError):
                imghdr_utils.supported_formats()


class TestWhat(unittest.TestCase):
    """The wrapper recognizes the formats of the standard library."""

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_every_format_is_recognized(self):
        for name, header in HEADERS.items():
            with self.subTest(format=name):
                self.assertEqual(imghdr_utils.what(io.BytesIO(header)), name)

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_unknown_data_is_not_an_image(self):
        self.assertIsNone(imghdr_utils.what(io.BytesIO(UNKNOWN)))

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_a_path_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"
            path.write_bytes(HEADERS["png"])
            self.assertEqual(imghdr_utils.what(str(path)), "png")
            self.assertEqual(imghdr_utils.what(path), "png")

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_stream_position_is_restored(self):
        stream = io.BytesIO(HEADERS["png"])
        self.assertEqual(imghdr_utils.what(stream), "png")
        self.assertEqual(stream.tell(), 0)

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_header_is_read_from_the_current_position(self):
        stream = io.BytesIO(b"skip" + HEADERS["png"])
        stream.read(4)
        self.assertEqual(imghdr_utils.what(stream), "png")
        self.assertEqual(stream.tell(), 4)

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_an_explicit_header_is_used(self):
        self.assertEqual(imghdr_utils.what("unused.png", h=HEADERS["gif"]), "gif")

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.what(42)
        with self.assertRaises(TypeError):
            imghdr_utils.what(b"\x89PNG")

    def test_an_unsupported_header_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.what("image.png", h="not bytes")


class TestDetect(unittest.TestCase):
    """The wrapper recognizes a header without a file."""

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_every_format_is_recognized(self):
        for name, header in HEADERS.items():
            with self.subTest(format=name):
                self.assertEqual(imghdr_utils.detect(header), name)

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_unknown_data_matches_nothing(self):
        self.assertIsNone(imghdr_utils.detect(UNKNOWN))
        self.assertEqual(imghdr_utils.matching_formats(UNKNOWN), [])

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_a_bytearray_is_accepted(self):
        self.assertEqual(imghdr_utils.detect(bytearray(HEADERS["png"])), "png")

    def test_unsupported_data_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.detect("not bytes")
        with self.assertRaises(TypeError):
            imghdr_utils.matching_formats(None)


class TestIsImage(unittest.TestCase):
    """The wrapper reports whether a file holds an image."""

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_an_image_is_recognized(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"
            path.write_bytes(HEADERS["png"])
            self.assertTrue(imghdr_utils.is_image(path))
            self.assertTrue(imghdr_utils.is_image(io.BytesIO(HEADERS["png"])))

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_other_data_is_not_an_image(self):
        self.assertFalse(imghdr_utils.is_image(io.BytesIO(UNKNOWN)))

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.is_image(object())


class TestReadHeader(unittest.TestCase):
    """The wrapper reads the header of a file."""

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_default_size_is_used(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "image.png"
            path.write_bytes(HEADERS["png"])
            header = imghdr_utils.read_header(path)
            self.assertEqual(len(header), imghdr_utils.DEFAULT_HEADER_SIZE)
            self.assertEqual(header, HEADERS["png"])

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_a_shorter_header_is_read(self):
        header = imghdr_utils.read_header(io.BytesIO(HEADERS["png"]), 8)
        self.assertEqual(header, HEADERS["png"][:8])

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_stream_position_is_restored(self):
        stream = io.BytesIO(HEADERS["png"])
        stream.read(4)
        position = stream.tell()
        imghdr_utils.read_header(stream)
        self.assertEqual(stream.tell(), position)

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_a_short_file_is_read_entirely(self):
        self.assertEqual(imghdr_utils.read_header(io.BytesIO(b"abc"), 32), b"abc")

    def test_an_invalid_size_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.read_header(io.BytesIO(HEADERS["png"]), "8")
        with self.assertRaises(ValueError):
            imghdr_utils.read_header(io.BytesIO(HEADERS["png"]), 0)

    def test_an_unsupported_file_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.read_header(42)


class TestSupportedFormats(unittest.TestCase):
    """The wrapper lists the formats the interpreter knows."""

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_formats_of_the_standard_library_are_listed(self):
        formats = imghdr_utils.supported_formats()
        for name in HEADERS:
            with self.subTest(format=name):
                self.assertIn(name, formats)

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_list_has_no_duplicates(self):
        formats = imghdr_utils.supported_formats()
        self.assertEqual(len(formats), len(set(formats)))


class TestRegisterTest(unittest.TestCase):
    """The wrapper registers and removes detection functions."""

    def setUp(self):
        self.addCleanup(self._restore)

    def _restore(self):
        if HAVE_IMGHDR:
            imghdr_utils.unregister_test("test_custom")

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_a_custom_function_recognizes_a_format(self):
        def test_custom(header, file):
            if header.startswith(b"CUSTOM"):
                return "custom"
            return None

        name = imghdr_utils.register_test(test_custom)
        self.assertEqual(name, "test_custom")
        self.assertIn("custom", imghdr_utils.supported_formats())
        self.assertEqual(imghdr_utils.detect(b"CUSTOM" + b"\x00" * 26), "custom")

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_a_registered_function_is_removed_again(self):
        def test_custom(header, file):
            return None

        imghdr_utils.register_test(test_custom)
        self.assertTrue(imghdr_utils.unregister_test("test_custom"))
        self.assertNotIn("custom", imghdr_utils.supported_formats())
        self.assertFalse(imghdr_utils.unregister_test("test_custom"))

    @unittest.skipUnless(HAVE_IMGHDR, "the imghdr module is not available")
    def test_the_standard_library_keeps_working(self):
        self.assertEqual(imghdr_utils.detect(HEADERS["png"]), "png")

    def test_an_unsupported_function_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.register_test("not callable")

    def test_a_function_with_the_wrong_signature_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.register_test(lambda header: None)

    def test_an_unsupported_name_is_rejected(self):
        with self.assertRaises(TypeError):
            imghdr_utils.unregister_test(42)


if __name__ == "__main__":
    unittest.main()
