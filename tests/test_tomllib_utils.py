"""Tests for tomllib_utils module."""

import os
import tempfile
import unittest

from tomllib_utils import is_valid_toml, load_toml_string, read_toml


class TestTomllibUtils(unittest.TestCase):
    def test_read_toml_basic(self) -> None:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".toml") as f:
            path = f.name
            f.write(b'title = "example"\nvalue = 42\n')

        try:
            data = read_toml(path)
            self.assertEqual(data, {"title": "example", "value": 42})
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_toml_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_toml("/nonexistent/path.toml")

    def test_load_toml_string(self) -> None:
        data = load_toml_string('a = 1\nb = "two"')
        self.assertEqual(data, {"a": 1, "b": "two"})

    def test_is_valid_toml_true(self) -> None:
        self.assertTrue(is_valid_toml('key = "val"'))

    def test_is_valid_toml_false(self) -> None:
        self.assertFalse(is_valid_toml("key ="))
