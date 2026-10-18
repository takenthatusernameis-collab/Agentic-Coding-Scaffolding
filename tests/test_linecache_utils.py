import os
import tempfile
import unittest

from linecache_utils import checkcache, clearcache, getline, getlines, updatecache


class TestLinecacheUtils(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp()
        with os.fdopen(self.fd, "w") as f:
            f.write("first\nsecond\nthird\n")

    def tearDown(self):
        os.remove(self.path)
        clearcache()

    def test_getline(self):
        self.assertEqual(getline(self.path, 2), "second\n")

    def test_getline_type_error(self):
        with self.assertRaises(TypeError):
            getline(123, 1)

    def test_getlines(self):
        self.assertEqual(getlines(self.path), ["first\n", "second\n", "third\n"])

    def test_getlines_type_error(self):
        with self.assertRaises(TypeError):
            getlines(123)

    def test_checkcache(self):
        checkcache(self.path)

    def test_updatecache(self):
        lines = updatecache(self.path)
        self.assertEqual(lines, ["first\n", "second\n", "third\n"])

    def test_updatecache_type_error(self):
        with self.assertRaises(TypeError):
            updatecache(123)

    def test_clearcache(self):
        clearcache()


if __name__ == "__main__":
    unittest.main()
