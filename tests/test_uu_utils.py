"""Tests for uu_utils."""

from __future__ import annotations

import importlib
import io
import sys
import unittest
from unittest import mock

import uu_utils


class TestUuUtils(unittest.TestCase):
    def test_exports(self) -> None:
        for name in uu_utils.__all__:
            self.assertTrue(hasattr(uu_utils, name))

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(uu_utils.is_available(), bool)

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

    def test_encode_backtick_parameter_not_ignored_on_fallback(self) -> None:
        """Test that backtick parameter is passed even when fallback is used."""
        if not uu_utils.is_available():
            self.skipTest("uu module not available")

        inp = io.BytesIO(b"test\n")
        out = io.BytesIO()

        call_args = []

        def mock_encode(*args, **kwargs):
            call_args.append((args, kwargs))
            if len(call_args) == 1:
                # First call fails with TypeError (simulating unsupported kwarg)
                raise TypeError("unexpected keyword argument 'backtick'")
            # Second call succeeds
            return None

        with mock.patch.object(uu_utils._uu, "encode", side_effect=mock_encode):
            uu_utils.encode(inp, out, backtick=True)
            self.assertEqual(len(call_args), 2)
            # Verify second call - backtick is keyword-only so can't be passed positionally
            # in older Python versions. The fallback correctly omits it.
            # But the first call should have attempted to pass it.
            self.assertIn("backtick", call_args[0][1])
            self.assertTrue(call_args[0][1]["backtick"])

    def test_decode_quiet_parameter_not_ignored_on_fallback(self) -> None:
        """Test that quiet parameter is passed even when fallback is used."""
        if not uu_utils.is_available():
            self.skipTest("uu module not available")

        # Create encoded data first
        inp = io.BytesIO(b"test\n")
        encoded = io.BytesIO()
        uu_utils.encode(inp, encoded)
        encoded_data = encoded.getvalue()

        out = io.BytesIO()

        call_args = []

        def mock_decode(*args, **kwargs):
            call_args.append((args, kwargs))
            if len(call_args) == 1:
                # First call fails with TypeError (simulating unsupported kwarg)
                raise TypeError("unexpected keyword argument 'quiet'")
            # Second call succeeds
            return None

        with mock.patch.object(uu_utils._uu, "decode", side_effect=mock_decode):
            uu_utils.decode(io.BytesIO(encoded_data), out, quiet=1)
            self.assertEqual(len(call_args), 2)
            # Verify second call includes quiet parameter (positionally as 4th arg)
            self.assertEqual(len(call_args[1][0]), 4)  # in_file, out_file, mode, quiet
            self.assertTrue(call_args[1][0][3])  # quiet=True


class TestUnavailableModule(unittest.TestCase):
    """Verify the Python 3.13+ path where :mod:`uu` no longer ships."""

    def test_unavailable_branch(self) -> None:
        try:
            with mock.patch.dict(sys.modules, {"uu": None}):
                reloaded = importlib.reload(uu_utils)
                assert reloaded.is_available() is False
                assert issubclass(reloaded.Error, Exception)
                with self.assertRaises(RuntimeError):
                    reloaded.encode(io.BytesIO(b"x"), io.BytesIO())
                with self.assertRaises(RuntimeError):
                    reloaded.decode(io.BytesIO(b""), io.BytesIO())
                with self.assertRaises(RuntimeError):
                    reloaded.encode_file(io.BytesIO(b"x"), io.BytesIO())
                with self.assertRaises(RuntimeError):
                    reloaded.decode_file(io.BytesIO(b""), io.BytesIO())
        finally:
            importlib.reload(uu_utils)
        assert uu_utils.is_available() is True


if __name__ == "__main__":
    unittest.main()
