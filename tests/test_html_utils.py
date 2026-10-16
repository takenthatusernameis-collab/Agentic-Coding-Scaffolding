"""Unit tests for html_utils module."""

import unittest

from html_utils import escape_attribute, escape_html, strip_tags, unescape_html


class TestEscapeHtml(unittest.TestCase):
    def test_escape_html_basic(self):
        self.assertEqual(escape_html("<div>"), "&lt;div&gt;")

    def test_escape_html_ampersand(self):
        self.assertEqual(escape_html("Tom & Jerry"), "Tom &amp; Jerry")

    def test_escape_html_quotes(self):
        self.assertEqual(escape_html('He said "hi"'), 'He said &quot;hi&quot;')

    def test_escape_html_none(self):
        self.assertEqual(escape_html(None), "")

    def test_escape_html_empty(self):
        self.assertEqual(escape_html(""), "")

    def test_escape_html_type_error(self):
        with self.assertRaises(TypeError):
            escape_html(123)  # type: ignore[arg-type]


class TestUnescapeHtml(unittest.TestCase):
    def test_unescape_html_named_entities(self):
        self.assertEqual(unescape_html("&lt;div&gt;"), "<div>")
        self.assertEqual(unescape_html("&amp;"), "&")

    def test_unescape_html_numeric_entities(self):
        self.assertEqual(unescape_html("&#60;"), "<")
        self.assertEqual(unescape_html("&#x3c;"), "<")

    def test_unescape_html_plain_text(self):
        self.assertEqual(unescape_html("hello world"), "hello world")

    def test_unescape_html_type_error(self):
        with self.assertRaises(TypeError):
            unescape_html(None)  # type: ignore[arg-type]


class TestStripTags(unittest.TestCase):
    def test_strip_tags_basic(self):
        self.assertEqual(strip_tags("<p>Hello <b>world</b>!</p>"), "Hello world!")

    def test_strip_tags_no_tags(self):
        self.assertEqual(strip_tags("plain text"), "plain text")

    def test_strip_tags_empty(self):
        self.assertEqual(strip_tags(""), "")

    def test_strip_tags_multiline(self):
        self.assertEqual(
            strip_tags("<div>\n  <span>text</span>\n</div>"),
            "\n  text\n",
        )

    def test_strip_tags_type_error(self):
        with self.assertRaises(TypeError):
            strip_tags(["<div>"])  # type: ignore[arg-type]


class TestEscapeAttribute(unittest.TestCase):
    def test_escape_attribute_double_quotes(self):
        self.assertEqual(escape_attribute('a="b"'), 'a=&quot;b&quot;')

    def test_escape_attribute_single_quotes(self):
        self.assertEqual(escape_attribute("it's"), "it&#x27;s")

    def test_escape_attribute_none(self):
        self.assertEqual(escape_attribute(None), "")

    def test_escape_attribute_type_error(self):
        with self.assertRaises(TypeError):
            escape_attribute(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
