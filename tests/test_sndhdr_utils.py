"""Tests for ``sndhdr_utils``."""

from __future__ import annotations

import os
import tempfile
import unittest

from sndhdr_utils import is_available, what, whathdr


class TestSndhdrUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_invalid_filename_type(self):
        with self.assertRaises(TypeError):
            what(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            whathdr(123)  # type: ignore[arg-type]

    def test_what_missing_file(self):
        if not is_available():
            self.skipTest("sndhdr unavailable")
        with self.assertRaises(OSError):
            what("/no/such/file.wav")


if __name__ == "__main__":
    unittest.main()