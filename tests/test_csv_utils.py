"""Tests for csv_utils module."""

import os
import tempfile
import unittest

from csv_utils import (
    append_csv_row,
    read_csv,
    read_csv_as_lists,
    write_csv,
    write_csv_from_lists,
)


class TestReadWriteCSV(unittest.TestCase):
    def test_read_write_csv_dicts(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            rows = [
                {"name": "Alice", "age": "30"},
                {"name": "Bob", "age": "25"},
            ]
            write_csv(path, rows)
            loaded = read_csv(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[0]["name"], "Alice")
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_write_csv_empty_rows(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            os.unlink(path)
            write_csv(path, [])
            self.assertFalse(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_write_csv_empty_rows_with_fieldnames_writes_header(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            # remove the temp file so we can verify write_csv creates it
            os.unlink(path)
            write_csv(path, [], fieldnames=["a", "b"])
            self.assertTrue(os.path.exists(path))
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read(), "a,b\n")
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_write_csv_lists(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            rows = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
            write_csv_from_lists(path, rows)
            loaded = read_csv_as_lists(path)
            self.assertEqual(loaded, rows)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_read_csv_with_custom_delimiter(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("name;age\nAlice;30\n")
            loaded = read_csv(path, delimiter=";")
            self.assertEqual(loaded[0]["name"], "Alice")
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_append_csv_row(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            append_csv_row(path, {"name": "Alice", "age": "30"})
            append_csv_row(path, {"name": "Bob", "age": "25"})
            loaded = read_csv(path)
            self.assertEqual(len(loaded), 2)
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_append_csv_row_respects_delimiter(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            path = f.name

        try:
            write_csv(path, [{"name": "Alice", "age": "30"}], delimiter=";")
            append_csv_row(
                path,
                {"name": "Bob", "age": "25"},
                fieldnames=["name", "age"],
                delimiter=";",
            )
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Alice;30", content)
            self.assertIn("Bob;25", content)
            self.assertNotIn("Bob,25", content)
            loaded = read_csv(path, delimiter=";")
            self.assertEqual(len(loaded), 2)
            self.assertEqual(loaded[1], {"name": "Bob", "age": "25"})
        finally:
            if os.path.exists(path):
                os.unlink(path)
