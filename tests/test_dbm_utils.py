"""Tests for dbm_utils module."""

import dbm
import tempfile
import unittest
from pathlib import Path

import dbm_utils


class TestOpenDatabase(unittest.TestCase):
    """Verify opening and closing databases."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.db"

    def tearDown(self):
        self.tmp.cleanup()

    def test_open_database_creates_and_persists(self):
        database = dbm_utils.open_database(self.path)
        try:
            database[b"key"] = b"value"
        finally:
            dbm_utils.close(database)
        reopened = dbm_utils.open_database(self.path, flag="r")
        try:
            self.assertEqual(reopened[b"key"], b"value")
        finally:
            dbm_utils.close(reopened)

    def test_open_database_read_only(self):
        database = dbm_utils.open_database(self.path, flag="c")
        database[b"a"] = b"1"
        dbm_utils.close(database)
        read_only = dbm_utils.open_database(self.path, flag="r")
        try:
            self.assertEqual(read_only[b"a"], b"1")
        finally:
            dbm_utils.close(read_only)

    def test_open_database_new_empty(self):
        database = dbm_utils.open_database(self.path, flag="c")
        database[b"existing"] = b"data"
        dbm_utils.close(database)
        fresh = dbm_utils.open_database(self.path, flag="n")
        try:
            self.assertEqual(list(fresh.keys()), [])
        finally:
            dbm_utils.close(fresh)

    def test_open_database_requires_path(self):
        with self.assertRaises(TypeError):
            dbm_utils.open_database(42)  # type: ignore[arg-type]

    def test_open_database_accepts_string_path(self):
        database = dbm_utils.open_database(str(self.path))
        dbm_utils.close(database)
        self.assertTrue(self.path.exists())

    def test_open_database_rejects_bad_flag(self):
        with self.assertRaises(TypeError):
            dbm_utils.open_database(self.path, flag="x")  # type: ignore[arg-type]

    def test_close_requires_close_method(self):
        with self.assertRaises(AttributeError):
            dbm_utils.close(object())


class TestRecordOperations(unittest.TestCase):
    """Verify read, write, delete, and key listing."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.db"

    def tearDown(self):
        self.tmp.cleanup()

    def _open(self, flag="c"):
        return dbm_utils.open_database(self.path, flag=flag)

    def test_write_and_read_record(self):
        database = self._open()
        try:
            dbm_utils.write_record(database, b"alpha", b"one")
            self.assertEqual(dbm_utils.read_record(database, b"alpha"), b"one")
            self.assertIsNone(dbm_utils.read_record(database, b"missing"))
        finally:
            dbm_utils.close(database)

    def test_write_record_requires_bytes(self):
        database = self._open()
        try:
            with self.assertRaises(TypeError):
                dbm_utils.write_record(database, "alpha", b"one")  # type: ignore[arg-type]
            with self.assertRaises(TypeError):
                dbm_utils.write_record(database, b"alpha", "one")  # type: ignore[arg-type]
        finally:
            dbm_utils.close(database)

    def test_delete_record(self):
        database = self._open()
        try:
            dbm_utils.write_record(database, b"temp", b"gone")
            self.assertTrue(dbm_utils.has_key(database, b"temp"))
            dbm_utils.delete_record(database, b"temp")
            self.assertFalse(dbm_utils.has_key(database, b"temp"))
            self.assertIsNone(dbm_utils.read_record(database, b"temp"))
        finally:
            dbm_utils.close(database)

    def test_delete_record_requires_bytes(self):
        database = self._open()
        try:
            with self.assertRaises(TypeError):
                dbm_utils.delete_record(database, "temp")  # type: ignore[arg-type]
        finally:
            dbm_utils.close(database)

    def test_delete_record_missing_key_raises(self):
        database = self._open()
        try:
            with self.assertRaises(KeyError):
                dbm_utils.delete_record(database, b"absent")
        finally:
            dbm_utils.close(database)

    def test_has_key(self):
        database = self._open()
        try:
            self.assertFalse(dbm_utils.has_key(database, b"anything"))
            dbm_utils.write_record(database, b"present", b"yes")
            self.assertTrue(dbm_utils.has_key(database, b"present"))
        finally:
            dbm_utils.close(database)

    def test_has_key_requires_bytes(self):
        database = self._open()
        try:
            with self.assertRaises(TypeError):
                dbm_utils.has_key(database, "present")  # type: ignore[arg-type]
        finally:
            dbm_utils.close(database)

    def test_list_keys(self):
        database = self._open()
        try:
            self.assertEqual(dbm_utils.list_keys(database), [])
            dbm_utils.write_record(database, b"b", b"2")
            dbm_utils.write_record(database, b"a", b"1")
            self.assertEqual(sorted(dbm_utils.list_keys(database)), [b"a", b"b"])
        finally:
            dbm_utils.close(database)

    def test_sync_database(self):
        database = self._open()
        try:
            dbm_utils.write_record(database, b"sync", b"me")
            dbm_utils.sync_database(database)
            self.assertEqual(dbm_utils.read_record(database, b"sync"), b"me")
        finally:
            dbm_utils.close(database)

    def test_sync_database_requires_sync_method(self):
        with self.assertRaises(AttributeError):
            dbm_utils.sync_database(object())


class TestDatabaseInspection(unittest.TestCase):
    """Verify flag validation, backend detection, and error exposure."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.db"

    def tearDown(self):
        self.tmp.cleanup()

    def test_is_valid_flag(self):
        self.assertTrue(dbm_utils.is_valid_flag("r"))
        self.assertTrue(dbm_utils.is_valid_flag("w"))
        self.assertTrue(dbm_utils.is_valid_flag("c"))
        self.assertTrue(dbm_utils.is_valid_flag("n"))
        self.assertFalse(dbm_utils.is_valid_flag("x"))
        self.assertFalse(dbm_utils.is_valid_flag(None))
        self.assertFalse(dbm_utils.is_valid_flag(1))

    def test_available_backends_include_dumb(self):
        self.assertIn("dbm.dumb", dbm_utils.available_backends())

    def test_which_database_existing_file(self):
        database = dbm_utils.open_database(self.path, flag="c")
        dbm_utils.close(database)
        self.assertIsNotNone(dbm_utils.which_database(self.path))

    def test_which_database_missing_file(self):
        missing = Path(self.tmp.name) / "nope.db"
        self.assertFalse(missing.exists())
        self.assertIsNone(dbm_utils.which_database(missing))

    def test_dbm_error_is_dbm_error(self):
        self.assertIs(dbm_utils.dbm_error, dbm.error)


class TestContextManager(unittest.TestCase):
    """Verify databases can be used as context managers."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sample.db"

    def tearDown(self):
        self.tmp.cleanup()

    def test_database_supports_context_manager(self):
        with dbm_utils.open_database(self.path) as database:
            dbm_utils.write_record(database, b"ctx", b"ok")
        with dbm_utils.open_database(self.path, flag="r") as database:
            self.assertEqual(database[b"ctx"], b"ok")


if __name__ == "__main__":
    unittest.main()
