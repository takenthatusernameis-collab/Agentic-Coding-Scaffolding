import unittest

from getopt_utils import GetoptError, getopt, gnu_getopt


class TestGetoptUtils(unittest.TestCase):
    def test_getopt(self):
        opts, args = getopt(["-a", "val", "pos"], "a:", ["alpha="])
        self.assertEqual(opts, [("-a", "val")])
        self.assertEqual(args, ["pos"])

    def test_getopt_long(self):
        opts, args = getopt(["--alpha", "val"], "", ["alpha="])
        self.assertEqual(opts, [("--alpha", "val")])
        self.assertEqual(args, [])

    def test_getopt_type_error_args(self):
        with self.assertRaises(TypeError):
            getopt("bad", "a:")

    def test_getopt_type_error_shortopts(self):
        with self.assertRaises(TypeError):
            getopt(["-a"], 123)

    def test_gnu_getopt(self):
        opts, args = gnu_getopt(["pos", "-a", "val"], "a:")
        self.assertEqual(opts, [("-a", "val")])
        self.assertEqual(args, ["pos"])

    def test_gnu_getopt_type_error(self):
        with self.assertRaises(TypeError):
            gnu_getopt("bad", "a:")

    def test_getopt_error(self):
        with self.assertRaises(GetoptError):
            getopt(["-z"], "a:")


if __name__ == "__main__":
    unittest.main()
