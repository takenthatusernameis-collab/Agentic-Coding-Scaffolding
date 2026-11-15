"""Tests for html_entities_utils module."""

import html
import unittest

from html_entities_utils import (
    escape,
    is_available,
    name2codepoint,
    unescape,
)


class TestHTMLEntitiesUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertTrue(is_available())

    def test_name2codepoint_has_amp(self):
        self.assertIn("amp", name2codepoint)

    def test_escape_basic(self):
        self.assertEqual(escape("<div>"), "&lt;div&gt;")

    def test_escape_quotes(self):
        self.assertEqual(escape('"hello"'), "&quot;hello&quot;")

    def test_escape_ampersand(self):
        self.assertEqual(escape("a & b"), "a &amp; b")

    def test_escape_quote_false_keeps_quotes(self):
        self.assertEqual(escape('a "quoted" value', quote=False), 'a "quoted" value')
        self.assertEqual(escape("it's", quote=False), "it's")

    def test_escape_quote_false_still_escapes_markup(self):
        self.assertEqual(escape("<b> & 'x'</b>", quote=False), "&lt;b&gt; &amp; 'x'&lt;/b&gt;")

    def test_escape_matches_stdlib_for_both_quote_modes(self):
        for text in ('<a href="x">\'y\' & z</a>', "plain", "&amp;"):
            self.assertEqual(escape(text, quote=True), html.escape(text, quote=True))
            self.assertEqual(escape(text, quote=False), html.escape(text, quote=False))

    def test_escape_rejects_non_string(self):
        with self.assertRaises(TypeError):
            escape(123)

    def test_escape_rejects_non_bool_quote(self):
        with self.assertRaises(TypeError):
            escape("<b>", quote="yes")  # type: ignore[arg-type]

    def test_unescape_basic(self):
        self.assertEqual(unescape("&lt;div&gt;"), "<div>")

    def test_unescape_amp(self):
        self.assertEqual(unescape("a &amp; b"), "a & b")

    def test_unescape_rejects_non_string(self):
        with self.assertRaises(TypeError):
            unescape(123)


if __name__ == "__main__":
    unittest.main()
