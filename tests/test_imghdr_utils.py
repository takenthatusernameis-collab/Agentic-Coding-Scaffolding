"""Tests for imghdr_utils."""

import io
import tempfile
import unittest
from pathlib import Path

from imghdr_utils import what, tests


class TestWhat(unittest.TestCase):
    def test_png(self):
        data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 24
        self.assertEqual(what(io.BytesIO(data)), "png")

    def test_jpeg(self):
        data = b"\xff\xd8\xff\xdb" + b"\x00" * 28
        self.assertEqual(what(io.BytesIO(data)), "jpeg")

    def test_unknown(self):
        self.assertIsNone(what(io.BytesIO(b"hello world" + b"\x00" * 22)))

    def test_file_path(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.png"
            p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 24)
            self.assertEqual(what(str(p)), "png")

    def test_tests_list(self):
        self.assertTrue(len(tests) > 0)


if __name__ == "__main__":
    unittest.main()
