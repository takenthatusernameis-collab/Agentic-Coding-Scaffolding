"""Tests for xdrlib_utils."""

from __future__ import annotations

import importlib
import sys
import unittest
from unittest import mock

import xdrlib_utils


class TestXdrlibUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in xdrlib_utils.__all__:
            self.assertTrue(hasattr(xdrlib_utils, name))

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(xdrlib_utils.is_available(), bool)

    def test_error_classes(self) -> None:
        self.assertTrue(issubclass(xdrlib_utils.Error, Exception))
        self.assertTrue(issubclass(xdrlib_utils.ConversionError, xdrlib_utils.Error))

    @unittest.skipUnless(xdrlib_utils.is_available(), "xdrlib is not available")
    def test_packer_unpacker_roundtrip(self) -> None:
        p = xdrlib_utils.Packer()
        p.pack_uint(5)
        data = p.get_buffer()
        u = xdrlib_utils.Unpacker(data)
        self.assertEqual(u.unpack_uint(), 5)


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`xdrlib` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"xdrlib": None}):
                reloaded = importlib.reload(xdrlib_utils)
                assert reloaded.is_available() is False
                assert issubclass(reloaded.Error, Exception)
                assert issubclass(reloaded.ConversionError, reloaded.Error)
                with self.assertRaises(RuntimeError):
                    reloaded.Packer()
                with self.assertRaises(RuntimeError):
                    reloaded.Unpacker(b"")
        finally:
            importlib.reload(xdrlib_utils)
        assert xdrlib_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
