"""Tests for sndhdr_utils."""

import importlib
import sys
import unittest
from unittest import mock

import sndhdr_utils


def test_exports():
    for name in ["what", "whathdr", "tests", "is_available"]:
        assert hasattr(sndhdr_utils, name)


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`sndhdr` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"sndhdr": None}):
                reloaded = importlib.reload(sndhdr_utils)
                assert reloaded.is_available() is False
                with self.assertRaises(RuntimeError):
                    reloaded.what("dummy")
                with self.assertRaises(RuntimeError):
                    reloaded.whathdr("dummy")
                assert reloaded.tests == []
        finally:
            importlib.reload(sndhdr_utils)
        assert sndhdr_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
