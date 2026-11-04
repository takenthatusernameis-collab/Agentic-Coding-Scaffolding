import os
import tempfile
import unittest

import dumbdbm_utils


class TestDumbdbmUtils(unittest.TestCase):
    def test_exports(self):
        self.assertTrue(hasattr(dumbdbm_utils, "open"))
        self.assertTrue(hasattr(dumbdbm_utils, "create_dbm"))
        self.assertTrue(callable(dumbdbm_utils.is_available))

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

    def test_bad_types(self):
        with self.assertRaises(TypeError):
            dumbdbm_utils.open(123)


if __name__ == "__main__":
    unittest.main()
