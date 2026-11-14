"""Tests for spwd_utils."""

import importlib
import sys
import unittest
from unittest import mock

import spwd_utils


def test_exports():
    for name in ["getspnam", "getspall", "is_available"]:
        assert hasattr(spwd_utils, name)


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`spwd` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"spwd": None}):
                reloaded = importlib.reload(spwd_utils)
                assert reloaded.is_available() is False
                with self.assertRaises(RuntimeError):
                    reloaded.getspnam("dummy")
                with self.assertRaises(RuntimeError):
                    reloaded.getspall()
        finally:
            importlib.reload(spwd_utils)
        assert spwd_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
