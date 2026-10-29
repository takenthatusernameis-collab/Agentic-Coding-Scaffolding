"""Tests for xdrlib_utils."""

from __future__ import annotations

import unittest

import xdrlib_utils


class TestXdrlibUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in xdrlib_utils.__all__:
            self.assertTrue(hasattr(xdrlib_utils, name))

    def test_packer_unpacker_roundtrip(self) -> None:
        p = xdrlib_utils.Packer()
        p.pack_uint(5)
        data = p.get_buffer()
        u = xdrlib_utils.Unpacker(data)
        self.assertEqual(u.unpack_uint(), 5)


if __name__ == "__main__":
    unittest.main()
