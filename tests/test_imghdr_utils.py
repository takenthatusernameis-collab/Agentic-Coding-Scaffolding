"""Tests for imghdr_utils."""

import unittest

import imghdr_utils

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
JPEG = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00" + b"\x00" * 16
GIF = b"GIF89a" + b"\x00" * 16
BMP = b"BM" + b"\x00" * 16
TIFF = b"II*\x00" + b"\x00" * 16
WEBP = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 8


class _FakeFile:
    """Minimal file-like object exposing read/seek for detect()."""

    def __init__(self, data: bytes) -> None:
        self._data = data

    def read(self, size: int = -1) -> bytes:
        return self._data if size < 0 else self._data[:size]

    def seek(self, offset: int) -> int:
        return offset


class TestExports(unittest.TestCase):
    def test_exports(self) -> None:
        for name in [
            "what",
            "tests",
            "detect",
            "is_available",
            "is_image",
            "matching_formats",
            "read_header",
            "register_test",
            "supported_formats",
            "unregister_test",
        ]:
            self.assertTrue(hasattr(imghdr_utils, name), name)

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(imghdr_utils.is_available(), bool)


@unittest.skipUnless(imghdr_utils.is_available(), "imghdr not available")
class TestDetect(unittest.TestCase):
    def test_detect_png(self) -> None:
        self.assertEqual(imghdr_utils.detect(None, PNG), "png")

    def test_detect_jpeg(self) -> None:
        self.assertEqual(imghdr_utils.detect(None, JPEG), "jpeg")

    def test_detect_gif(self) -> None:
        self.assertEqual(imghdr_utils.detect(None, GIF), "gif")

    def test_detect_bmp(self) -> None:
        self.assertEqual(imghdr_utils.detect(None, BMP), "bmp")

    def test_detect_tiff(self) -> None:
        self.assertEqual(imghdr_utils.detect(None, TIFF), "tiff")

    def test_detect_webp(self) -> None:
        self.assertEqual(imghdr_utils.detect(None, WEBP), "webp")

    def test_detect_unknown_returns_none(self) -> None:
        self.assertIsNone(imghdr_utils.detect(None, b"not an image"))

    def test_detect_reads_from_file_object(self) -> None:
        self.assertEqual(imghdr_utils.detect(_FakeFile(PNG)), "png")

    def test_detect_file_object_without_read(self) -> None:
        self.assertIsNone(imghdr_utils.detect(object(), b"not an image"))


@unittest.skipUnless(imghdr_utils.is_available(), "imghdr not available")
class TestPredicates(unittest.TestCase):
    def test_is_image_true(self) -> None:
        self.assertTrue(imghdr_utils.is_image(None, PNG))

    def test_is_image_false(self) -> None:
        self.assertFalse(imghdr_utils.is_image(None, b"not an image"))

    def test_matching_formats_hit(self) -> None:
        self.assertEqual(imghdr_utils.matching_formats(None, PNG), ["png"])

    def test_matching_formats_miss(self) -> None:
        self.assertEqual(imghdr_utils.matching_formats(None, b"not an image"), [])

    def test_read_header_returns_bytes(self) -> None:
        self.assertEqual(imghdr_utils.read_header(None, PNG), PNG)

    def test_supported_formats_contains_common(self) -> None:
        formats = imghdr_utils.supported_formats()
        self.assertIsInstance(formats, list)
        for name in ("jpeg", "png", "gif"):
            self.assertIn(name, formats)

    def test_register_and_unregister_are_noops(self) -> None:
        # The wrappers accept arbitrary args and intentionally return None.
        imghdr_utils.register_test(id(PNG), lambda *a: None)
        imghdr_utils.unregister_test(id(PNG))


if __name__ == "__main__":
    unittest.main()
