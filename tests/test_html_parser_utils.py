"""Tests for html_parser_utils module."""

import unittest

from html_parser_utils import HTMLParser, HTMLStripper, extract_tags, is_available, strip_html_tags


class TestHTMLParserUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertTrue(is_available())

    def test_html_parser_is_importable(self):
        self.assertTrue(issubclass(HTMLParser, object))

    def test_strip_html_tags_basic(self):
        html = "<p>Hello <b>World</b></p>"
        self.assertEqual(strip_html_tags(html), "Hello World")

    def test_strip_html_tags_empty(self):
        self.assertEqual(strip_html_tags(""), "")

    def test_strip_html_tags_no_tags(self):
        self.assertEqual(strip_html_tags("Hello World"), "Hello World")

    def test_strip_html_tags_rejects_non_string(self):
        with self.assertRaises(TypeError):
            strip_html_tags(123)

    def test_html_stripper(self):
        stripper = HTMLStripper()
        stripper.feed("<div>Test</div>")
        stripper.close()
        self.assertEqual(stripper.get_data(), "Test")

    def test_extract_tags_all(self):
        html = '<p class="test">Hello</p>'
        tags = extract_tags(html)
        self.assertTrue(len(tags) > 0)
        self.assertEqual(tags[0]["tag"], "p")

    def test_extract_tags_specific(self):
        html = "<div>A</div><p>B</p>"
        tags = extract_tags(html, tag="p")
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0]["tag"], "p")

    def test_extract_tags_rejects_bad_types(self):
        with self.assertRaises(TypeError):
            extract_tags(123)
        with self.assertRaises(TypeError):
            extract_tags("<p></p>", tag=123)


if __name__ == "__main__":
    unittest.main()
