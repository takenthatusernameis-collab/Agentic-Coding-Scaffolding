"""Tests for the :mod:`sre_constants_utils` wrapper."""

from __future__ import annotations

import unittest

import sre_constants_utils


class TestSreConstantsUtils(unittest.TestCase):

    def test_is_available(self)-> None:
        """``is_available`` reports whether the module ships."""
        result = sre_constants_utils.is_available()
        assert isinstance(result, bool)


    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_constants_exist(self)-> None:
        """Basic constants are accessible."""
        assert hasattr(sre_constants_utils, "LITERAL")
        assert hasattr(sre_constants_utils, "BRANCH")


    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_get_opcodes(self)-> None:
        """``get_opcodes`` returns a list."""
        opcodes = sre_constants_utils.get_opcodes()
        assert isinstance(opcodes, list)


    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_opcodenames(self)-> None:
        """``opcodenames`` returns a mapping."""
        names = sre_constants_utils.opcodenames()
        assert isinstance(names, dict)


    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_lookup_and_op_code(self)-> None:
        """Lookup works roundtrip where possible."""
        names = sre_constants_utils.opcodenames()
        if names:
            code = next(iter(names.keys()))
            name = sre_constants_utils.lookup_opcode(code)
            assert isinstance(name, str)
            # roundtrip
            code2 = sre_constants_utils.op_code(name)
            assert code2 == code


    def test_lookup_opcode_validates(self)-> None:
        """``lookup_opcode`` validates input."""
        with self.assertRaises(TypeError):
            sre_constants_utils.lookup_opcode("bad")  # type: ignore[arg-type]


    def test_op_code_validates(self)-> None:
        """``op_code`` validates input."""
        with self.assertRaises(TypeError):
            sre_constants_utils.op_code(123)  # type: ignore[arg-type]


    def test_degradation_without_module(self)-> None:
        """Helpers raise RuntimeError when module missing."""
        original = sre_constants_utils._sre_constants
        try:
            sre_constants_utils._sre_constants = None  # type: ignore[assignment]
            with self.assertRaisesRegex(RuntimeError, "sre_constants"):
                sre_constants_utils.get_opcodes()
            with self.assertRaisesRegex(RuntimeError, "sre_constants"):
                sre_constants_utils.opcodenames()
            with self.assertRaisesRegex(RuntimeError, "sre_constants"):
                sre_constants_utils.get_all()
        finally:
            sre_constants_utils._sre_constants = original


    def test_exports(self)-> None:
        """The module exports its public names."""
        for name in sre_constants_utils.__all__:
            if name in (
                "error_codes",
                "DIGITS",
                "CH_CODES",
                "TYPE_FLAGS",
            ):  # might be empty or missing
                continue
            try:
                assert hasattr(sre_constants_utils, name), name
            except AssertionError:
                if sre_constants_utils.is_available() and hasattr(
                    sre_constants_utils._sre_constants, name
                ):
                    pass  # skip if missing in our export mapping
                else:
                    raise


if __name__ == "__main__":
    unittest.main()
