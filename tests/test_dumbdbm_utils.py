import os
import tempfile
import unittest
from unittest.mock import MagicMock

import dumbdbm_utils


class TestDumbdbmUtils(unittest.TestCase):
    def test_exports(self):
        self.assertTrue(hasattr(dumbdbm_utils, "open"))
        self.assertTrue(hasattr(dumbdbm_utils, "create_dbm"))
        self.assertTrue(callable(dumbdbm_utils.is_available))
        for name in ["get", "set", "delete", "keys", "items", "values", "clear", "update", "close"]:
            self.assertTrue(hasattr(dumbdbm_utils, name), name)

    def test_is_available(self):
        self.assertTrue(dumbdbm_utils.is_available())

    def test_open_and_write(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            db = dumbdbm_utils.create_dbm(path)
            db[b"key"] = b"value"
            self.assertEqual(db[b"key"], b"value")
            db.close()
        finally:
            for ext in ["", ".dat", ".dir", ".bak"]:
                try:
                    os.unlink(path + ext)
                except FileNotFoundError:
                    pass

    def test_helpers(self):
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            db = dumbdbm_utils.create_dbm(path)
            dumbdbm_utils.set(db, b"a", b"1")
            self.assertEqual(dumbdbm_utils.get(db, b"a"), b"1")
            self.assertEqual(dumbdbm_utils.get(db, b"missing", b"default"), b"default")
            self.assertIn(b"a", dumbdbm_utils.keys(db))
            dumbdbm_utils.update(db, {b"b": b"2"}, c=b"3")
            self.assertEqual(dumbdbm_utils.get(db, b"b"), b"2")
            self.assertEqual(dumbdbm_utils.get(db, b"c"), b"3")
            self.assertTrue(len(dumbdbm_utils.items(db)) >= 2)
            self.assertTrue(len(dumbdbm_utils.values(db)) >= 2)
            dumbdbm_utils.delete(db, b"a")
            self.assertNotIn(b"a", dumbdbm_utils.keys(db))
            dumbdbm_utils.clear(db)
            self.assertEqual(dumbdbm_utils.keys(db), [])
            dumbdbm_utils.close(db)
        finally:
            for ext in ["", ".dat", ".dir", ".bak"]:
                try:
                    os.unlink(path + ext)
                except FileNotFoundError:
                    pass

    def test_bad_types(self):
        with self.assertRaises(TypeError):
            dumbdbm_utils.open(123)

    def test_open_dbm_alias_and_error(self):
        self.assertIs(dumbdbm_utils.open_dbm, dumbdbm_utils.open)
        self.assertIs(dumbdbm_utils.error, dumbdbm_utils.dumbdbm.error)
        fd, path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        try:
            db = dumbdbm_utils.open_dbm(path, "c")
            dumbdbm_utils.set(db, b"k", b"v")
            self.assertEqual(dumbdbm_utils.get(db, b"k"), b"v")
            dumbdbm_utils.close(db)
        finally:
            for ext in ["", ".dat", ".dir", ".bak"]:
                try:
                    os.unlink(path + ext)
                except FileNotFoundError:
                    pass

    def test_keys_propagates_exception(self):
        """keys() should propagate exceptions from the underlying database."""
        mock_db = MagicMock()
        mock_db.keys.side_effect = RuntimeError("database corrupted")
        with self.assertRaises(RuntimeError):
            dumbdbm_utils.keys(mock_db)

    def test_items_propagates_exception(self):
        """items() should propagate exceptions from the underlying database."""
        mock_db = MagicMock()
        mock_db.items.side_effect = RuntimeError("database corrupted")
        with self.assertRaises(RuntimeError):
            dumbdbm_utils.items(mock_db)

    def test_values_propagates_exception(self):
        """values() should propagate exceptions from the underlying database."""
        mock_db = MagicMock()
        mock_db.values.side_effect = RuntimeError("database corrupted")
        with self.assertRaises(RuntimeError):
            dumbdbm_utils.values(mock_db)

    def test_clear_propagates_exception(self):
        """clear() should propagate exceptions from the underlying database."""
        mock_db = MagicMock()
        mock_db.keys.return_value = [b"key1"]
        mock_db.__delitem__.side_effect = RuntimeError("database corrupted")
        with self.assertRaises(RuntimeError):
            dumbdbm_utils.clear(mock_db)

    def test_set_requires_bytes(self):
        """set() should require bytes for key and value."""
        mock_db = MagicMock()
        with self.assertRaises(TypeError):
            dumbdbm_utils.set(mock_db, "key", b"value")
        with self.assertRaises(TypeError):
            dumbdbm_utils.set(mock_db, b"key", "value")
        with self.assertRaises(TypeError):
            dumbdbm_utils.set(mock_db, "key", "value")

    def test_get_requires_bytes_key(self):
        """get() should require bytes for key."""
        mock_db = MagicMock()
        with self.assertRaises(TypeError):
            dumbdbm_utils.get(mock_db, "key")

    def test_delete_requires_bytes_key(self):
        """delete() should require bytes for key."""
        mock_db = MagicMock()
        with self.assertRaises(TypeError):
            dumbdbm_utils.delete(mock_db, "key")

    def test_update_requires_bytes(self):
        """update() should require bytes for keys and values."""
        mock_db = MagicMock()
        with self.assertRaises(TypeError):
            dumbdbm_utils.update(mock_db, {"key": b"value"})
        with self.assertRaises(TypeError):
            dumbdbm_utils.update(mock_db, {b"key": "value"})
        with self.assertRaises(TypeError):
            dumbdbm_utils.update(mock_db, key="value")
        with self.assertRaises(TypeError):
            dumbdbm_utils.update(mock_db, key=b"value", other="value")


if __name__ == "__main__":
    unittest.main()
