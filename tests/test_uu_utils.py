import io
import os
import tempfile
import unittest
import warnings

from uu_utils import uu_decode, uu_encode


class TestUuUtils(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", DeprecationWarning)
        self.tmp = tempfile.mkdtemp()

    def test_encode_decode_roundtrip(self):
        data = b"hello world\n"
        src = os.path.join(self.tmp, "out.uu")
        uu_encode(data, src)
        self.assertTrue(os.path.exists(src))
        dec = uu_decode(src)
        self.assertEqual(dec, data)

    def test_encode_type_error(self):
        with self.assertRaises(TypeError):
            uu_encode("x", os.path.join(self.tmp, "a.uu"))

    def test_decode_type_error(self):
        with self.assertRaises(TypeError):
            uu_decode(123)

    def test_decode_to_file(self):
        data = b"abc"
        src = os.path.join(self.tmp, "out.uu")
        dst = os.path.join(self.tmp, "out.bin")
        uu_encode(data, src)
        result = uu_decode(src, dst)
        self.assertEqual(result, data)
        with open(dst, "rb") as f:
            self.assertEqual(f.read(), data)


if __name__ == "__main__":
    unittest.main()