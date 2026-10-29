"""Tests for sunau_utils."""

from __future__ import annotations

import unittest

import sunau_utils


class TestSunauUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in sunau_utils.__all__:
            self.assertTrue(hasattr(sunau_utils, name))


if __name__ == "__main__":
    unittest.main()
