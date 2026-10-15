"""Tests for json_utils module."""

import json
import os
import tempfile
import unittest

from json_utils import (
    dump_json_string,
    is_valid_json,
    load_json_string,
    pretty_print_json,
    read_json,
    write_json,
)


class TestReadWriteJson(unittest.TestCase):
    def test_read_write_json_basic(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            path = f.name

        try:
            data = {"name": "test", "value": 42}
            write_json(path, data)
            loaded = read_json(path)
            self.assertEqual(data, loaded)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_json_file_not_found(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_json("/nonexistent/path.json")

    def test_write_json_with_indent(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            path = f.name

        try:
            data = {"a": 1, "b": 2}
            write_json(path, data, indent=2)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("  ", content)  # indentation
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_write_json_overwrite(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            path = f.name

        try:
            write_json(path, {"a": 1})
            write_json(path, {"b": 2})
            loaded = read_json(path)
            self.assertEqual({"b": 2}, loaded)
        finally:
            if os.path.exists(path):
                os.unlink(path)


class TestJsonStrings(unittest.TestCase):
    def test_load_json_string(self) -> None:
        s = '{"key": "value", "num": 123}'
        result = load_json_string(s)
        self.assertEqual(result, {"key": "value", "num": 123})

    def test_load_json_string_invalid(self) -> None:
        with self.assertRaises(json.JSONDecodeError):
            load_json_string("{invalid json}")

    def test_dump_json_string(self) -> None:
        data = {"key": "value", "num": 123}
        result = dump_json_string(data)
        # Should be valid JSON
        self.assertTrue(is_valid_json(result))
        self.assertEqual(load_json_string(result), data)

    def test_dump_json_string_compact(self) -> None:
        data = {"a": 1, "b": 2}
        result = dump_json_string(data, indent=0)
        self.assertTrue(is_valid_json(result))

    def test_dump_json_string_ensure_ascii(self) -> None:
        data = {"text": "café"}
        result = dump_json_string(data, ensure_ascii=True)
        self.assertTrue(is_valid_json(result))


class TestIsValidJson(unittest.TestCase):
    def test_is_valid_json_true(self) -> None:
        self.assertTrue(is_valid_json('{"a": 1}'))
        self.assertTrue(is_valid_json("[]"))
        self.assertTrue(is_valid_json('"string"'))
        self.assertTrue(is_valid_json("123"))
        self.assertTrue(is_valid_json("true"))
        self.assertTrue(is_valid_json("null"))

    def test_is_valid_json_false(self) -> None:
        self.assertFalse(is_valid_json("{"))
        self.assertFalse(is_valid_json("}"))
        self.assertFalse(is_valid_json("{'a': 1}"))  # single quotes
        self.assertFalse(is_valid_json("undefined"))
        self.assertFalse(is_valid_json(""))
        self.assertFalse(is_valid_json(None))  # type: ignore[arg-type]


class TestPrettyPrintJson(unittest.TestCase):
    def test_pretty_print_json_basic(self) -> None:
        data = {"a": 1, "b": [2, 3]}
        result = pretty_print_json(data)
        self.assertTrue(is_valid_json(result))
        self.assertIn("\n", result)  # formatted

    def test_pretty_print_json_custom_indent(self) -> None:
        data = {"a": 1}
        result = pretty_print_json(data, indent=2)
        self.assertTrue(is_valid_json(result))
