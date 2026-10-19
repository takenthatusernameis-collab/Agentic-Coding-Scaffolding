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
