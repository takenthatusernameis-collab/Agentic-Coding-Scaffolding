import errno
import unittest

from errno_utils import errno_code, errno_name, errorcode, is_errno, strerror


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

    def test_errno_code(self):
        self.assertEqual(errno_code("EEXIST"), errno.EEXIST)
        self.assertIsNone(errno_code("NOT_A_REAL_ERRNO"))

    def test_errno_name(self):
        self.assertEqual(errno_name(errno.EEXIST), "EEXIST")

    def test_errno_name_unknown(self):
        self.assertIsNone(errno_name(999999))

    def test_errno_name_type_error(self):
        with self.assertRaises(TypeError):
            errno_name("EEXIST")


if __name__ == "__main__":
    unittest.main()
