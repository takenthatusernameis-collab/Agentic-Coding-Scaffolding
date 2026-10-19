"""Tests for tokenize_utils module."""

import codecs
import io
import tempfile
import unittest
from pathlib import Path

import tokenize_utils


class TestTokenizeSource(unittest.TestCase):
    """Verify tokenizing of in-memory sources."""

    def test_tokenize_source_returns_tokens(self):
        tokens = tokenize_utils.tokenize_source("x = 1\n")
        self.assertTrue(tokens)
        self.assertTrue(all(isinstance(tok, tokenize_utils.TokenInfo) for tok in tokens))

    def test_tokenize_source_reports_names_and_values(self):
        tokens = tokenize_utils.tokenize_source("x = 1\n")
        strings = [tok.string for tok in tokens]
        self.assertIn("x", strings)
        self.assertIn("1", strings)
        self.assertIn("=", strings)

    def test_tokenize_source_of_empty_string(self):
        tokens = tokenize_utils.tokenize_source("")
        self.assertTrue(all(tok.string == "" for tok in tokens))

    def test_tokenize_source_requires_string(self):
        with self.assertRaises(TypeError):
            tokenize_utils.tokenize_source(123)  # type: ignore[arg-type]


class TestTokenizeFile(unittest.TestCase):
    """Verify tokenizing of files on disk."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.py"
        self.path.write_text("# -*- coding: utf-8 -*-\nx = 1\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_tokenize_file_returns_tokens(self):
        tokens = tokenize_utils.tokenize_file(self.path)
        self.assertIn("x", [tok.string for tok in tokens])

    def test_tokenize_file_accepts_string_path(self):
        tokens = tokenize_utils.tokenize_file(str(self.path))
        self.assertIn("x", [tok.string for tok in tokens])

    def test_tokenize_file_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            tokenize_utils.tokenize_file(Path(self.tmp.name) / "missing.py")

    def test_tokenize_file_rejects_bad_type(self):
        with self.assertRaises(TypeError):
            tokenize_utils.tokenize_file(42)  # type: ignore[arg-type]


class TestGenerateAndUntokenize(unittest.TestCase):
    """Verify the low level tokenizer helpers."""

    def test_generate_tokens_yields_tokens(self):
        tokens = list(tokenize_utils.generate_tokens(io.StringIO("x = 1\n").readline))
        self.assertTrue(tokens)
        self.assertIn("x", [tok.string for tok in tokens])

    def test_generate_tokens_requires_callable(self):
        with self.assertRaises(TypeError):
            tokenize_utils.generate_tokens("not callable")  # type: ignore[arg-type]

    def test_untokenize_round_trip(self):
        source = "x = 1  # comment\n"
        tokens = tokenize_utils.tokenize_source(source)
        self.assertEqual(tokenize_utils.untokenize(tokens), source)

    def test_untokenize_requires_iterable(self):
        with self.assertRaises(TypeError):
            tokenize_utils.untokenize(5)  # type: ignore[arg-type]


class TestTokenNames(unittest.TestCase):
    """Verify token name lookups."""

    def test_token_name_of_known_type(self):
        self.assertEqual(tokenize_utils.token_name(1), "NAME")
        self.assertEqual(tokenize_utils.token_name(2), "NUMBER")

    def test_token_name_of_unknown_type(self):
        self.assertEqual(tokenize_utils.token_name(-123), "UNKNOWN")

    def test_token_name_requires_int(self):
        with self.assertRaises(TypeError):
            tokenize_utils.token_name("NAME")  # type: ignore[arg-type]

    def test_token_type_lookup(self):
        self.assertEqual(tokenize_utils.token_type("NAME"), 1)
        self.assertEqual(tokenize_utils.token_type("NUMBER"), 2)

    def test_token_type_of_unknown_name(self):
        with self.assertRaises(KeyError):
            tokenize_utils.token_type("NOT_A_TOKEN")

    def test_token_type_requires_string(self):
        with self.assertRaises(TypeError):
            tokenize_utils.token_type(1)  # type: ignore[arg-type]


class TestDetectEncoding(unittest.TestCase):
    """Verify source encoding detection."""

    def test_detect_encoding_defaults_to_utf8(self):
        lines = [b"x = 1\n"]
        encoding, read = tokenize_utils.detect_encoding(iter(lines).__next__)
        self.assertEqual(encoding, "utf-8")
        self.assertEqual(read, [b"x = 1\n"])

    def test_detect_encoding_reads_cookie(self):
        lines = [b"# -*- coding: latin-1 -*-\n", b"x = 1\n"]
        encoding, read = tokenize_utils.detect_encoding(iter(lines).__next__)
        # The standard library normalizes the cookie to the canonical codec name.
        self.assertEqual(codecs.lookup(encoding).name, codecs.lookup("latin-1").name)
        self.assertEqual(read, [b"# -*- coding: latin-1 -*-\n"])

    def test_detect_encoding_of_empty_stream(self):
        encoding, read = tokenize_utils.detect_encoding(iter([]).__next__)
        self.assertEqual(encoding, "utf-8")
        self.assertEqual(read, [])

    def test_detect_encoding_requires_callable(self):
        with self.assertRaises(TypeError):
            tokenize_utils.detect_encoding(None)  # type: ignore[arg-type]


class TestSignificantTokens(unittest.TestCase):
    """Verify token filtering and predicates."""

    def test_significant_tokens_drops_comments_and_blanks(self):
        tokens = tokenize_utils.tokenize_source("x = 1  # comment\n\n")
        significant = tokenize_utils.significant_tokens(tokens)
        names = [tokenize_utils.token_name(tok.type) for tok in significant]
        self.assertNotIn("COMMENT", names)
        self.assertNotIn("NL", names)
        self.assertIn("NAME", names)

    def test_significant_tokens_requires_iterable(self):
        with self.assertRaises(TypeError):
            tokenize_utils.significant_tokens(None)  # type: ignore[arg-type]

    def test_token_predicates(self):
        tokens = tokenize_utils.tokenize_source("import os\nvalue = 'text'\ncount = 2\n")
        by_string = {tok.string: tok for tok in tokens}
        self.assertTrue(tokenize_utils.is_name(by_string["import"]))
        self.assertTrue(tokenize_utils.is_string(by_string["'text'"]))
        self.assertTrue(tokenize_utils.is_number(by_string["2"]))
        self.assertTrue(tokenize_utils.is_keyword(by_string["import"]))
        self.assertFalse(tokenize_utils.is_keyword(by_string["os"]))
        self.assertFalse(tokenize_utils.is_number(by_string["os"]))

    def test_is_comment_detects_comments(self):
        tokens = tokenize_utils.tokenize_source("x = 1  # comment\n")
        comments = [tok for tok in tokens if tokenize_utils.is_comment(tok)]
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].string, "# comment")


if __name__ == "__main__":
    unittest.main()
