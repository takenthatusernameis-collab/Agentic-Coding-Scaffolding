"""Tests for cgi_utils."""

import importlib
import sys
import unittest
from unittest import mock

import cgi_utils


class TestCgiUtils(unittest.TestCase):
    def test_exports(self):
        assert hasattr(cgi_utils, "FieldStorage")
        assert hasattr(cgi_utils, "MiniFieldStorage")
        assert hasattr(cgi_utils, "escape")
        assert hasattr(cgi_utils, "parse")
        assert hasattr(cgi_utils, "parse_header")
        assert hasattr(cgi_utils, "parse_multipart")
        assert hasattr(cgi_utils, "parse_qs")
        assert hasattr(cgi_utils, "parse_qsl")
        assert hasattr(cgi_utils, "is_available")
        assert cgi_utils.is_available() is True

    def test_escape_quotes_html(self):
        assert cgi_utils.escape("<script>") == "&lt;script&gt;"

    def test_escape_with_quotes(self):
        assert cgi_utils.escape('"x"', True) == "&quot;x&quot;"
        assert cgi_utils.escape('"x"', False) == '"x"'

    def test_escape_coerces_non_strings(self):
        assert cgi_utils.escape(42) == "42"

    def test_parse_qs_and_parse_qsl(self):
        assert cgi_utils.parse_qs("a=1&b=2") == {"a": ["1"], "b": ["2"]}
        assert cgi_utils.parse_qsl("a=1&b=2") == [("a", "1"), ("b", "2")]

    def test_unavailable_branch(self):
        try:
            with mock.patch.dict(sys.modules, {"cgi": None}):
                reloaded = importlib.reload(cgi_utils)
                assert reloaded.is_available() is False
                with self.assertRaises(RuntimeError):
                    reloaded.FieldStorage()
                with self.assertRaises(RuntimeError):
                    reloaded.MiniFieldStorage()
                with self.assertRaises(RuntimeError):
                    reloaded.parse_header("a", "b")
                with self.assertRaises(RuntimeError):
                    reloaded.parse_multipart(b"", {})
                # Pure helpers keep working without the cgi module.
                assert reloaded.escape("<x>") == "&lt;x&gt;"
                assert reloaded.parse_qs("a=1") == {"a": ["1"]}
        finally:
            importlib.reload(cgi_utils)


if __name__ == "__main__":
    unittest.main()
