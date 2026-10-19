import errno
import unittest

from errno_utils import errorcode, is_errno, strerror


class TestErrnoUtils(unittest.TestCase):
    def test_errorcode(self):
        self.assertEqual(errorcode(errno.EEXIST), "EEXIST")

    def test_errorcode_unknown(self):
        self.assertIsNone(errorcode(999999))

    def test_strerror(self):
        self.assertIn("exist", strerror(errno.EEXIST).lower())

    def test_is_errno(self):
        self.assertTrue(is_errno(errno.EEXIST, "EEXIST"))
        self.assertFalse(is_errno(errno.EEXIST, "ENOENT"))


if __name__ == "__main__":
    unittest.main()
