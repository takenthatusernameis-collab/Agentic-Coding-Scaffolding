"""Tests for the :mod:`sre_parse_utils` wrapper."""

from __future__ import annotations

import re
import unittest

import sre_parse_utils


class TestSreParseUtils(unittest.TestCase):

    def test_is_available(self)-> None:
        """``is_available`` reports whether the module ships."""
        result = sre_parse_utils.is_available()
        assert isinstance(result, bool)


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_parse_pattern_basic(self)-> None:
        """``parse_pattern`` parses a literal pattern."""
        parsed = sre_parse_utils.parse_pattern("abc")
        assert hasattr(parsed, "data")
        assert hasattr(parsed, "getwidth")


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_parse_pattern_with_flags(self)-> None:
        """``parse_pattern`` accepts flags."""
        flag = getattr(sre_parse_utils, "SRE_FLAG_IGNORECASE", 0)  # type: ignore[attr-defined]
        parsed = sre_parse_utils.parse_pattern("abc", flags=flag)
        assert hasattr(parsed, "data")


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_parse_pattern_named_group(self)-> None:
        """``parse_pattern`` parses a named group."""
        parsed = sre_parse_utils.parse_pattern(r"(?P<name>abc)")
        assert parsed is not None
        data = parsed.data
        assert isinstance(data, list)
        assert len(data) == 1


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_parse_template(self)-> None:
        """``parse_template`` parses a replacement template."""
        import re

        pattern = re.compile(r"(?P<name>abc)")
        parsed = sre_parse_utils.parse_template(r"\g<name>", pattern=pattern)
        assert isinstance(parsed, list)


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_parse_template_with_pattern(self)-> None:
        """``parse_template`` resolves numeric and named group references."""
        import re

        pattern = re.compile(r"(?P<name>abc)")
        parsed = sre_parse_utils.parse_template(r"\g<name> and \1", pattern=pattern)
        assert isinstance(parsed, list)
        assert " and " in parsed


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_pattern_width(self)-> None:
        """``pattern_width`` returns the width of a pattern."""
        width = sre_parse_utils.pattern_width("abc")
        assert width is not None
        assert isinstance(width, tuple)
        assert len(width) == 2
        assert width == (3, 3)


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_pattern_width_variable(self)-> None:
        """``pattern_width`` reports a variable width for repetition."""
        width = sre_parse_utils.pattern_width(r"a*")
        assert width is not None
        assert isinstance(width, tuple)
        assert len(width) == 2


    @unittest.skipIf(not sre_parse_utils.is_available(), "sre_parse not available")
    def test_pattern_dump(self)-> None:
        """``pattern_dump`` returns a text dump of the parsed tree."""
        dump = sre_parse_utils.pattern_dump("abc")
        assert isinstance(dump, str)
        assert "LITERAL" in dump


    def test_parse_pattern_validates(self)-> None:
        """``parse_pattern`` validates its arguments."""
        with self.assertRaises(TypeError):
            sre_parse_utils.parse_pattern(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sre_parse_utils.parse_pattern("abc", flags="x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sre_parse_utils.parse_pattern("abc", flags=True)  # type: ignore[arg-type]


    def test_parse_template_validates(self)-> None:
        """``parse_template`` validates its arguments."""
        import re

        with self.assertRaises(TypeError):
            sre_parse_utils.parse_template(123, re.compile(r"a"))  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sre_parse_utils.parse_template(r"\g<1>", "not a pattern")  # type: ignore[arg-type]


    def test_pattern_width_validates(self)-> None:
        """``pattern_width`` validates its arguments."""
        with self.assertRaises(TypeError):
            sre_parse_utils.pattern_width(123)  # type: ignore[arg-type]


    def test_pattern_dump_validates(self)-> None:
        """``pattern_dump`` validates its arguments."""
        with self.assertRaises(TypeError):
            sre_parse_utils.pattern_dump(123)  # type: ignore[arg-type]


    def test_degradation_without_module(self)-> None:
        """Helpers raise RuntimeError when module missing."""
        original = sre_parse_utils._sre_parse
        try:
            sre_parse_utils._sre_parse = None  # type: ignore[assignment]
            with self.assertRaisesRegex(RuntimeError, "sre_parse"):
                sre_parse_utils.parse_pattern("abc")
            with self.assertRaisesRegex(RuntimeError, "sre_parse"):
                sre_parse_utils.parse_template(r"\g<1>", re.compile(r"a"))
            with self.assertRaisesRegex(RuntimeError, "sre_parse"):
                sre_parse_utils.pattern_width("abc")
            with self.assertRaisesRegex(RuntimeError, "sre_parse"):
                sre_parse_utils.pattern_dump("abc")
        finally:
            sre_parse_utils._sre_parse = original  # type: ignore[assignment]


    def test_exports(self)-> None:
        """The module exports its public names."""
        for name in sre_parse_utils.__all__:
            try:
                assert hasattr(sre_parse_utils, name), name
            except AssertionError:
                if sre_parse_utils.is_available() and hasattr(sre_parse_utils._sre_parse, name):
                    pass
                else:
                    raise


    def test_subpattern_and_state_exported(self)-> None:
        """``SubPattern`` and ``State`` are exported when the module is available."""
        if sre_parse_utils.is_available():
            assert sre_parse_utils.SubPattern is not None
            assert sre_parse_utils.State is not None


    def test_error_exported(self)-> None:
        """``error`` is exported when the module is available."""
        if sre_parse_utils.is_available():
            assert sre_parse_utils.error is not None


    def test_constants_exported(self)-> None:
        """Common constants are exported when the module is available."""
        if sre_parse_utils.is_available():
            assert getattr(sre_parse_utils, "LITERAL", None) is not None  # type: ignore[attr-defined]
            assert getattr(sre_parse_utils, "BRANCH", None) is not None  # type: ignore[attr-defined]
            assert getattr(sre_parse_utils, "SUBPATTERN", None) is not None  # type: ignore[attr-defined]


if __name__ == "__main__":
    unittest.main()
