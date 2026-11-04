import os
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()
