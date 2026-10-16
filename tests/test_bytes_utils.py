import unittest

from bytes_utils import from_hex, to_hex


class TestBytesUtils(unittest.TestCase):
    def test_to_hex(self):
        self.assertEqual(to_hex(b"abc"), "616263")

    def test_from_hex(self):
        self.assertEqual(from_hex("616263"), b"abc")

    def test_to_hex_type_error(self):
        with self.assertRaises(TypeError):
            to_hex("abc")

    def test_from_hex_type_error(self):
        with self.assertRaises(TypeError):
            from_hex(123)


if __name__ == "__main__":
    unittest.main()
