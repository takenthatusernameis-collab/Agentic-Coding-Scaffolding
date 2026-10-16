"""Tests for markdown_utils module."""

import unittest

from markdown_utils import (
    count_words,
    extract_code_blocks,
    heading_level,
    is_heading,
    strip_markdown,
)


class TestExtractCodeBlocks(unittest.TestCase):
    def test_extracts_single_block(self) -> None:
        text = "intro\n```python\nprint('hi')\n```\noutro"
        self.assertEqual(extract_code_blocks(text), ["print('hi')"])

    def test_extracts_multiple_blocks(self) -> None:
        text = "```js\na()\n```\n\n```py\nb()\n```"
        self.assertEqual(extract_code_blocks(text), ["a()", "b()"])

    def test_no_blocks(self) -> None:
        self.assertEqual(extract_code_blocks("no code here"), [])

    def test_language_tag_optional(self) -> None:
        text = "```\nplain\n```"
        self.assertEqual(extract_code_blocks(text), ["plain"])


class TestStripMarkdown(unittest.TestCase):
    def test_strips_bold(self) -> None:
        self.assertEqual(strip_markdown("this is **bold** text"), "this is bold text")

    def test_strips_italic(self) -> None:
        self.assertEqual(strip_markdown("this is *italic* text"), "this is italic text")

    def test_strips_inline_code(self) -> None:
        self.assertEqual(strip_markdown("use `foo()` here"), "use foo() here")

    def test_strips_heading(self) -> None:
        self.assertEqual(strip_markdown("# Title"), "Title")

    def test_strips_link(self) -> None:
        self.assertEqual(strip_markdown("[label](http://example.com)"), "label")

    def test_strips_blockquote(self) -> None:
        self.assertEqual(strip_markdown("> quoted"), "quoted")


class TestCountWords(unittest.TestCase):
    def test_counts_words(self) -> None:
        self.assertEqual(count_words("hello world foo"), 3)

    def test_empty(self) -> None:
        self.assertEqual(count_words(""), 0)


class TestHeading(unittest.TestCase):
    def test_is_heading(self) -> None:
        self.assertTrue(is_heading("# Title"))
        self.assertTrue(is_heading("## Sub"))
        self.assertFalse(is_heading("not heading"))

    def test_heading_level(self) -> None:
        self.assertEqual(heading_level("# Title"), 1)
        self.assertEqual(heading_level("### Deep"), 3)
        self.assertEqual(heading_level("not heading"), 0)
