"""Tests for aifc_utils."""

from __future__ import annotations

import os
import tempfile
import unittest

import aifc_utils


class TestAifcUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in aifc_utils.__all__:
            self.assertTrue(hasattr(aifc_utils, name))

    def test_error_is_an_exception_class(self) -> None:
        self.assertTrue(isinstance(aifc_utils.Error, type))
        self.assertTrue(issubclass(aifc_utils.Error, Exception))

    def test_open_is_callable(self) -> None:
        self.assertTrue(callable(aifc_utils.open))

    def test_open_round_trip(self) -> None:
        frames = b"\x00\x00\x01\x00\xff\xff"
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "sample.aiff")
            with aifc_utils.open(path, "wb") as writer:
                writer.setnchannels(1)
                writer.setsampwidth(2)
                writer.setframerate(8000)
                writer.setcomptype(b"NONE", b"not compressed")
                writer.writeframes(frames)
            with aifc_utils.open(path, "rb") as reader:
                self.assertEqual(reader.getnchannels(), 1)
                self.assertEqual(reader.getsampwidth(), 2)
                self.assertEqual(reader.getframerate(), 8000)
                self.assertEqual(reader.getcomptype(), b"NONE")
                self.assertEqual(reader.readframes(reader.getnframes()), frames)


if __name__ == "__main__":
    unittest.main()
