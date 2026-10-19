"""Tests for shelve_utils."""

import os
import shutil
import tempfile
import unittest

from shelve_utils import (
    close,
    contains,
    delete,
    get,
    is_shelf,
    keys,
    open_shelf,
    set_value,
    sync,
)


class TestShelveUtils(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.path = os.path.join(self.tmp, "shelf")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_open_shelf_creates_database(self):
        shelf = open_shelf(self.path)
        try:
            self.assertTrue(is_shelf(shelf))
            self.assertTrue(os.path.exists(self.path) or len(os.listdir(self.tmp)) > 0)
        finally:
            close(shelf)

    def test_open_shelf_rejects_non_string_filename(self):
        with self.assertRaises(TypeError):
            open_shelf(123)

    def test_open_shelf_rejects_invalid_flag(self):
        with self.assertRaises(ValueError):
            open_shelf(self.path, flag="x")

    def test_open_shelf_accepts_explicit_protocol(self):
        shelf = open_shelf(self.path, protocol=2)
        try:
            set_value(shelf, "a", 1)
            self.assertEqual(get(shelf, "a"), 1)
        finally:
            close(shelf)

    def test_set_value_and_get(self):
        shelf = open_shelf(self.path)
        try:
            set_value(shelf, "name", "kilo")
            set_value(shelf, "count", 3)
            self.assertEqual(get(shelf, "name"), "kilo")
            self.assertEqual(get(shelf, "count"), 3)
        finally:
            close(shelf)

    def test_get_returns_default_for_missing_key(self):
        shelf = open_shelf(self.path)
        try:
            self.assertIsNone(get(shelf, "missing"))
            self.assertEqual(get(shelf, "missing", "fallback"), "fallback")
        finally:
            close(shelf)

    def test_get_rejects_non_string_key(self):
        shelf = open_shelf(self.path)
        try:
            with self.assertRaises(TypeError):
                get(shelf, 1)
        finally:
            close(shelf)

    def test_set_value_rejects_non_string_key(self):
        shelf = open_shelf(self.path)
        try:
            with self.assertRaises(TypeError):
                set_value(shelf, 1, "value")
        finally:
            close(shelf)

    def test_keys_lists_stored_keys(self):
        shelf = open_shelf(self.path)
        try:
            set_value(shelf, "a", 1)
            set_value(shelf, "b", 2)
            self.assertEqual(sorted(keys(shelf)), ["a", "b"])
        finally:
            close(shelf)

    def test_contains_reports_membership(self):
        shelf = open_shelf(self.path)
        try:
            set_value(shelf, "present", 1)
            self.assertTrue(contains(shelf, "present"))
            self.assertFalse(contains(shelf, "absent"))
        finally:
            close(shelf)

    def test_contains_rejects_non_string_key(self):
        shelf = open_shelf(self.path)
        try:
            with self.assertRaises(TypeError):
                contains(shelf, 1)
        finally:
            close(shelf)

    def test_delete_removes_key(self):
        shelf = open_shelf(self.path)
        try:
            set_value(shelf, "gone", 1)
            delete(shelf, "gone")
            self.assertFalse(contains(shelf, "gone"))
        finally:
            close(shelf)

    def test_delete_missing_key_raises_key_error(self):
        shelf = open_shelf(self.path)
        try:
            with self.assertRaises(KeyError):
                delete(shelf, "nope")
        finally:
            close(shelf)

    def test_delete_rejects_non_string_key(self):
        shelf = open_shelf(self.path)
        try:
            with self.assertRaises(TypeError):
                delete(shelf, 1)
        finally:
            close(shelf)

    def test_values_persist_across_sessions(self):
        shelf = open_shelf(self.path)
        try:
            set_value(shelf, "persisted", [1, 2, 3])
        finally:
            close(shelf)

        shelf = open_shelf(self.path)
        try:
            self.assertEqual(get(shelf, "persisted"), [1, 2, 3])
        finally:
            close(shelf)

    def test_sync_with_writeback(self):
        shelf = open_shelf(self.path, writeback=True)
        try:
            set_value(shelf, "cached", "value")
            sync(shelf)
            self.assertEqual(get(shelf, "cached"), "value")
        finally:
            close(shelf)

    def test_sync_rejects_object_without_sync(self):
        with self.assertRaises(AttributeError):
            sync(object())

    def test_close_rejects_object_without_close(self):
        with self.assertRaises(AttributeError):
            close(object())

    def test_is_shelf_rejects_other_objects(self):
        self.assertFalse(is_shelf({}))
        self.assertFalse(is_shelf(None))


if __name__ == "__main__":
    unittest.main()
