"""Tests for aifc_utils."""

from __future__ import annotations

import unittest

import aifc_utils


class TestAifcUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in aifc_utils.__all__:
            self.assertTrue(hasattr(aifc_utils, name))


if __name__ == "__main__":
    unittest.main()
