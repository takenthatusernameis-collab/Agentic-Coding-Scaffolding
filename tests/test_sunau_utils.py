"""Tests for sunau_utils."""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
import unittest
from unittest import mock

import sunau_utils


class TestSunauUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in sunau_utils.__all__:
            self.assertTrue(hasattr(sunau_utils, name))

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(sunau_utils.is_available(), bool)

    def test_error_is_an_exception_class(self) -> None:
        self.assertTrue(isinstance(sunau_utils.Error, type))
        self.assertTrue(issubclass(sunau_utils.Error, Exception))

    def test_open_is_callable(self) -> None:
        self.assertTrue(callable(sunau_utils.open))

    @unittest.skipUnless(sunau_utils.is_available(), "sunau is not available")
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


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`sunau` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"sunau": None}):
                reloaded = importlib.reload(sunau_utils)
                assert reloaded.is_available() is False
                assert issubclass(reloaded.Error, Exception)
                with self.assertRaises(RuntimeError):
                    reloaded.open("sample.au", "rb")
        finally:
            importlib.reload(sunau_utils)
        assert sunau_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
