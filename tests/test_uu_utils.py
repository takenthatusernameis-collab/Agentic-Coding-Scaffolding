"""Tests for uu_utils."""

from __future__ import annotations

import io
import unittest

import uu_utils


class TestUuUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in uu_utils.__all__:
            self.assertTrue(hasattr(uu_utils, name))

    def test_encode_decode_roundtrip(self) -> None:
        inp = io.BytesIO(b"hello world\n")
        out = io.BytesIO()
        uu_utils.encode(inp, out)
        encoded = out.getvalue()
        self.assertIn(b"begin", encoded)
        inp2 = io.BytesIO(encoded)
        out2 = io.BytesIO()
        uu_utils.decode(inp2, out2)
        self.assertEqual(out2.getvalue(), b"hello world\n")

    def test_error_class(self) -> None:
        self.assertTrue(issubclass(uu_utils.Error, Exception))

    def test_encode_file_and_decode_file_roundtrip(self) -> None:
        encoded = io.BytesIO()
        uu_utils.encode_file(io.BytesIO(b"file body\n"), encoded, name="test.txt")
        data = encoded.getvalue()
        self.assertIn(b"begin", data)

        decoded = io.BytesIO()
        uu_utils.decode_file(io.BytesIO(data), decoded)
        self.assertEqual(decoded.getvalue(), b"file body\n")


if __name__ == "__main__":
    unittest.main()
