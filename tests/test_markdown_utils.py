"""Tests for markdown_utils module."""

import unittest

from markdown_utils import (
    count_code_blocks,
    count_words,
    extract_code_blocks,
    has_code_blocks,
    has_words,
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


class TestCountCodeBlocks(unittest.TestCase):
    def test_no_blocks(self) -> None:
        self.assertEqual(count_code_blocks("no code"), 0)

    def test_single_block(self) -> None:
        text = "```py\nx = 1\n```"
        self.assertEqual(count_code_blocks(text), 1)

    def test_multiple_blocks(self) -> None:
        text = "```js\na()\n```\n\n```py\nb()\n```"
        self.assertEqual(count_code_blocks(text), 2)

    def test_consistent_with_extract(self) -> None:
        text = "intro\n```python\nprint('hi')\n```\noutro"
        self.assertEqual(count_code_blocks(text), len(extract_code_blocks(text)))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            count_code_blocks(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_code_blocks(123)  # type: ignore[arg-type]


class TestHasCodeBlocks(unittest.TestCase):
    def test_no_blocks(self) -> None:
        self.assertFalse(has_code_blocks("plain text"))

    def test_empty(self) -> None:
        self.assertFalse(has_code_blocks(""))

    def test_single_block(self) -> None:
        self.assertTrue(has_code_blocks("```\na\n```"))

    def test_multiple_blocks(self) -> None:
        text = "```js\na()\n```\n\n```py\nb()\n```"
        self.assertTrue(has_code_blocks(text))

    def test_consistent_with_count(self) -> None:
        text = "```py\nx = 1\n```"
        self.assertEqual(has_code_blocks(text), count_code_blocks(text) > 0)
        self.assertEqual(has_code_blocks("none"), count_code_blocks("none") > 0)

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            has_code_blocks(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_code_blocks(123)  # type: ignore[arg-type]


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


class TestHasWords(unittest.TestCase):
    def test_empty(self) -> None:
        self.assertFalse(has_words(""))

    def test_whitespace_only(self) -> None:
        self.assertFalse(has_words("   "))
        self.assertFalse(has_words("\t\n"))

    def test_single_word(self) -> None:
        self.assertTrue(has_words("hello"))

    def test_multiple_words(self) -> None:
        self.assertTrue(has_words("hello world foo"))

    def test_leading_trailing_whitespace(self) -> None:
        self.assertTrue(has_words("  hello world  "))

    def test_multiple_spaces_between_words(self) -> None:
        self.assertTrue(has_words("a   b   c"))

    def test_unicode(self) -> None:
        self.assertTrue(has_words("héllo wörld"))

    def test_consistent_with_count_words(self) -> None:
        self.assertEqual(has_words("hello world"), count_words("hello world") > 0)
        self.assertEqual(has_words(""), count_words("") > 0)

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            has_words(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            has_words(123)  # type: ignore[arg-type]


class TestHeading(unittest.TestCase):
    def test_is_heading(self) -> None:
        self.assertTrue(is_heading("# Title"))
        self.assertTrue(is_heading("## Sub"))
        self.assertFalse(is_heading("not heading"))

    def test_heading_level(self) -> None:
        self.assertEqual(heading_level("# Title"), 1)
        self.assertEqual(heading_level("### Deep"), 3)
        self.assertEqual(heading_level("not heading"), 0)
