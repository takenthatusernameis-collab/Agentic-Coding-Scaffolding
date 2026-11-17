import os
import tempfile
import unittest

from filecmp_utils import cmp_directories, cmp_files, same_file


class TestFilecmpUtils(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.a = os.path.join(self.d, "a.txt")
        self.b = os.path.join(self.d, "b.txt")
        with open(self.a, "w") as f:
            f.write("hello")
        with open(self.b, "w") as f:
            f.write("hello")

    def test_cmp_files_equal(self):
        self.assertTrue(cmp_files(self.a, self.b))

    def test_cmp_files_not_equal(self):
        with open(self.b, "w") as f:
            f.write("world")
        self.assertFalse(cmp_files(self.a, self.b))

    def test_cmp_files_type_error(self):
        with self.assertRaises(TypeError):
            cmp_files(123, self.b)

    def test_cmp_directories(self):
        d1 = os.path.join(self.d, "d1")
        d2 = os.path.join(self.d, "d2")
        os.makedirs(d1)
        os.makedirs(d2)
        with open(os.path.join(d1, "x.txt"), "w") as f:
            f.write("x")
        with open(os.path.join(d2, "x.txt"), "w") as f:
            f.write("x")
        result = cmp_directories(d1, d2)
        self.assertEqual(result.left_only, [])
        self.assertEqual(result.right_only, [])
        self.assertEqual(result.diff_files, [])

    def _make_pair(self, content_a, content_b):
        d1 = os.path.join(self.d, "s1")
        d2 = os.path.join(self.d, "s2")
        os.makedirs(d1, exist_ok=True)
        os.makedirs(d2, exist_ok=True)
        a = os.path.join(d1, "x.txt")
        b = os.path.join(d2, "x.txt")
        with open(a, "w") as f:
            f.write(content_a)
        with open(b, "w") as f:
            f.write(content_b)
        os.utime(a, (1000000, 1000000))
        os.utime(b, (1000000, 1000000))
        return d1, d2

    def test_cmp_directories_shallow_ignores_content_difference(self):
        d1, d2 = self._make_pair("aaaa", "bbbb")
        result = cmp_directories(d1, d2, shallow=True)
        self.assertEqual(result.same_files, ["x.txt"])
        self.assertEqual(result.diff_files, [])

    def test_cmp_directories_deep_detects_content_difference(self):
        d1, d2 = self._make_pair("aaaa", "bbbb")
        result = cmp_directories(d1, d2, shallow=False)
        self.assertEqual(result.same_files, [])
        self.assertEqual(result.diff_files, ["x.txt"])

    def test_cmp_directories_deep_detects_nested_content_difference(self):
        d1, d2 = self._make_pair("aaaa", "bbbb")
        sub1 = os.path.join(d1, "sub")
        sub2 = os.path.join(d2, "sub")
        os.makedirs(sub1)
        os.makedirs(sub2)
        a = os.path.join(sub1, "y.txt")
        b = os.path.join(sub2, "y.txt")
        with open(a, "w") as f:
            f.write("cccc")
        with open(b, "w") as f:
            f.write("dddd")
        os.utime(a, (1000000, 1000000))
        os.utime(b, (1000000, 1000000))

        result = cmp_directories(d1, d2, shallow=False)
        self.assertEqual(result.subdirs["sub"].diff_files, ["y.txt"])

    def test_cmp_directories_type_error(self):
        with self.assertRaises(TypeError):
            cmp_directories(1, 2)

    def test_same_file(self):
        self.assertTrue(same_file(self.a, self.a))

    def test_same_file_different(self):
        self.assertFalse(same_file(self.a, self.b))

    def test_same_file_type_error(self):
        with self.assertRaises(TypeError):
            same_file(1, 2)


if __name__ == "__main__":
    unittest.main()
