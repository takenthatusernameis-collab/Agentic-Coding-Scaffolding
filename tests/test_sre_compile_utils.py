"""Tests for the :mod:`sre_compile_utils` wrapper."""

from __future__ import annotations

import unittest

import sre_compile_utils


class TestSreCompileUtils(unittest.TestCase):

    def test_is_available(self)-> None:
        result = sre_compile_utils.is_available()
        assert isinstance(result, bool)


    @unittest.skipIf(not sre_compile_utils.is_available(), "sre_compile not available")
    def test_compile_pattern(self)-> None:
        code = sre_compile_utils.compile_pattern("abc")
        assert code is not None


    def test_compile_pattern_validates_flags(self)-> None:
        with self.assertRaises(TypeError):
            sre_compile_utils.compile_pattern("abc", "bad")  # type: ignore[arg-type]


    def test_degradation_without_module(self)-> None:
        original = sre_compile_utils._sre_compile
        try:
            sre_compile_utils._sre_compile = None  # type: ignore[assignment]
            with self.assertRaisesRegex(RuntimeError, "sre_compile"):
                sre_compile_utils.compile_pattern("abc")
        finally:
            sre_compile_utils._sre_compile = original


if __name__ == "__main__":
    unittest.main()
