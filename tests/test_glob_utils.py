import os
import tempfile
import unittest

from glob_utils import escape, glob_pattern, has_magic, iglob


class TestGlobUtils(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        for name in ("a.txt", "b.py", "c.txt"):
            open(os.path.join(self.d, name), "w").close()

    def test_glob_pattern(self):
        res = sorted(glob_pattern(os.path.join(self.d, "*.txt")))
        self.assertEqual(len(res), 2)

    def test_iglob(self):
        res = sorted(iglob(os.path.join(self.d, "*.py")))
        self.assertEqual(res, [os.path.join(self.d, "b.py")])

    def test_escape(self):
        self.assertEqual(escape("a*b.txt"), "a[*]b.txt")

    def test_has_magic(self):
        self.assertTrue(has_magic("*.txt"))
        self.assertFalse(has_magic("foo.txt"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            glob_pattern(123)
        with self.assertRaises(TypeError):
            iglob(5)
        with self.assertRaises(TypeError):
            escape(1)
        with self.assertRaises(TypeError):
            has_magic(2)


if __name__ == "__main__":
    unittest.main()
