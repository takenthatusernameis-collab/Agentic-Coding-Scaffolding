"""Tests for tomllib_utils module."""

import os
import tempfile
import tomllib
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

    def test_load_toml_string_invalid_toml_raises_tomldecodeerror(self) -> None:
        """``load_toml_string`` propagates ``tomllib.TOMLDecodeError`` for invalid TOML.

        This is a genuine stdlib delegation leak (not an input-validation gap),
        documented in ``Raises:`` with ``# audit-ignore: TOMLDecodeError``.
        """
        with self.assertRaises(tomllib.TOMLDecodeError):
            load_toml_string("key =")

    def test_is_valid_toml_true(self) -> None:
        self.assertTrue(is_valid_toml('key = "val"'))

    def test_is_valid_toml_false(self) -> None:
        self.assertFalse(is_valid_toml("key ="))

    def test_is_valid_toml_rejects_non_string(self) -> None:
        """``is_valid_toml`` treats non-string input as invalid TOML.

        The predicate returns ``bool`` (like ``duration_utils.is_valid_duration``)
        rather than raising, so a non-string is simply not valid TOML. Passing
        an ``int`` previously fell through to ``tomllib.loads``, whose first
        operation is ``s.replace(...)`` and which surfaced an
        ``AttributeError`` instead of a clean ``False``.
        """
        self.assertFalse(is_valid_toml(123))  # type: ignore[arg-type]
        self.assertFalse(is_valid_toml(None))  # type: ignore[arg-type]
        self.assertFalse(is_valid_toml(["a", "b"]))  # type: ignore[arg-type]
