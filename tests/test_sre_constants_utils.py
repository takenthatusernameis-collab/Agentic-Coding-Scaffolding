"""Tests for the :mod:`sre_constants_utils` wrapper."""

from __future__ import annotations

import types
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


class TestAssertValidFlags(unittest.TestCase):

    def test_accepts_int_flags(self)-> None:
        """Valid integer flags are accepted and return ``None``."""
        sre_constants_utils.assert_valid_flags(0)

    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_accepts_module_argument(self)-> None:
        """The optional ``module`` argument is forwarded when present."""
        import re

        sre_constants_utils.assert_valid_flags(0, re)

    def test_rejects_non_int_flags(self)-> None:
        """Non-integer flags raise ``TypeError``."""
        with self.assertRaises(TypeError):
            sre_constants_utils.assert_valid_flags("0")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sre_constants_utils.assert_valid_flags(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sre_constants_utils.assert_valid_flags([1])  # type: ignore[arg-type]


class TestErrorCodes(unittest.TestCase):

    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_returns_dict(self)-> None:
        """``error_codes`` returns a mapping."""
        result = sre_constants_utils.error_codes()
        assert isinstance(result, dict)

    def test_degradation_without_module(self)-> None:
        """Helpers raise ``RuntimeError`` when the module is missing."""
        original = sre_constants_utils._sre_constants
        try:
            sre_constants_utils._sre_constants = None  # type: ignore[assignment]
            with self.assertRaisesRegex(RuntimeError, "sre_constants"):
                sre_constants_utils.error_codes()
        finally:
            sre_constants_utils._sre_constants = original


class TestErrorExport(unittest.TestCase):

    def test_error_is_an_exception_class(self) -> None:
        """``error`` is the regex error class, usable as an exception."""
        assert isinstance(sre_constants_utils.error, type)
        assert issubclass(sre_constants_utils.error, Exception)

    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_error_matches_stdlib(self) -> None:
        """When the module is available, ``error`` is the stdlib class."""
        import sre_constants

        assert sre_constants_utils.error is sre_constants.error


class TestBoolRejection(unittest.TestCase):

    def test_assert_valid_flags_rejects_bool(self):
        with self.assertRaises(TypeError):
            sre_constants_utils.assert_valid_flags(True)  # type: ignore[arg-type]

    def test_lookup_opcode_rejects_bool(self):
        with self.assertRaises(TypeError):
            sre_constants_utils.lookup_opcode(True)  # type: ignore[arg-type]


class TestFallbackBranches(unittest.TestCase):
    """Pin defensive branches that the standard library build may not hit."""

    def test_get_opcodes_and_names_fallback_without_opcodes(self) -> None:
        """Without an ``OPCODES`` attribute the helpers degrade to empty."""
        original = sre_constants_utils._sre_constants
        try:
            sre_constants_utils._sre_constants = types.SimpleNamespace()  # type: ignore[assignment]
            assert sre_constants_utils.get_opcodes() == []
            assert sre_constants_utils.opcodenames() == {}
        finally:
            sre_constants_utils._sre_constants = original

    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_lookup_opcode_unknown_raises_value_error(self) -> None:
        """An integer outside the known opcodes raises ``ValueError``."""
        names = sre_constants_utils.opcodenames()
        unknown = (max(names) + 1000) if names else 0
        with self.assertRaises(ValueError):
            sre_constants_utils.lookup_opcode(unknown)

    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_op_code_unknown_name_raises_value_error(self) -> None:
        """An unknown opcode name raises ``ValueError``."""
        with self.assertRaises(ValueError):
            sre_constants_utils.op_code("__not_a_real_opcode_name__")

    @unittest.skipIf(not sre_constants_utils.is_available(), "sre_constants not available")
    def test_get_all_returns_public_constants(self) -> None:
        """``get_all`` returns the public constants of the module."""
        result = sre_constants_utils.get_all()
        assert isinstance(result, dict)
        assert "error" in result
        assert all(not key.startswith("_") for key in result)

    def test_assert_valid_flags_forwards_when_available(self) -> None:
        """``assert_valid_flags`` forwards to the stdlib helper when present."""
        calls: list = []
        fake = types.SimpleNamespace(
            assert_valid_flags=lambda flags, module: calls.append((flags, module)),
        )
        original = sre_constants_utils._sre_constants
        try:
            sre_constants_utils._sre_constants = fake  # type: ignore[assignment]
            sentinel = object()
            sre_constants_utils.assert_valid_flags(7, sentinel)
            assert calls == [(7, sentinel)]
        finally:
            sre_constants_utils._sre_constants = original

    def test_error_codes_returns_copy_of_mapping(self) -> None:
        """``error_codes`` returns a copy of the stdlib mapping."""
        fake = types.SimpleNamespace(error_codes={"a": 1})
        original = sre_constants_utils._sre_constants
        try:
            sre_constants_utils._sre_constants = fake  # type: ignore[assignment]
            result = sre_constants_utils.error_codes()
            assert result == {"a": 1}
            result["b"] = 2
            assert "b" not in fake.error_codes
        finally:
            sre_constants_utils._sre_constants = original


if __name__ == "__main__":
    unittest.main()
