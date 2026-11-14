"""Tests for sunau_utils."""

from __future__ import annotations

import os
import tempfile
import unittest

import sunau_utils


class TestSunauUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in sunau_utils.__all__:
            self.assertTrue(hasattr(sunau_utils, name))

    def test_error_is_an_exception_class(self) -> None:
        self.assertTrue(isinstance(sunau_utils.Error, type))
        self.assertTrue(issubclass(sunau_utils.Error, Exception))

    def test_open_is_callable(self) -> None:
        self.assertTrue(callable(sunau_utils.open))

    def test_open_round_trip(self) -> None:
        frames = bytes(range(256))
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "sample.au")
            with sunau_utils.open(path, "wb") as writer:
                writer.setnchannels(1)
                writer.setsampwidth(2)
                writer.setframerate(8000)
                writer.writeframes(frames)
            with sunau_utils.open(path, "rb") as reader:
                self.assertEqual(reader.getnchannels(), 1)
                self.assertEqual(reader.getsampwidth(), 2)
                self.assertEqual(reader.getframerate(), 8000)
                data = reader.readframes(reader.getnframes())
                self.assertIsNotNone(data)
                assert data is not None
                self.assertEqual(len(data), len(frames))


if __name__ == "__main__":
    unittest.main()
