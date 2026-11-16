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

    def test_errorcode_rejects_bool(self):
        with self.assertRaises(TypeError):
            errorcode(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            errorcode(False)  # type: ignore[arg-type]

    def test_strerror_rejects_bool(self):
        with self.assertRaises(TypeError):
            strerror(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            strerror(False)  # type: ignore[arg-type]

    def test_is_errno_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_errno(True, "EEXIST")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_errno(False, "EEXIST")  # type: ignore[arg-type]

    def test_errno_name_rejects_bool(self):
        with self.assertRaises(TypeError):
            errno_name(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            errno_name(False)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
