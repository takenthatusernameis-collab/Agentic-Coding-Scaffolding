import unittest

from numbers_utils import Integral, Number, Real, is_integral, is_number


class TestNumbersUtils(unittest.TestCase):
    def test_is_number(self):
        self.assertTrue(is_number(5))
        self.assertTrue(is_number(1.5))
        self.assertFalse(is_number("x"))

    def test_is_integral(self):
        self.assertTrue(is_integral(5))
        self.assertFalse(is_integral(1.5))

    def test_classes(self):
        self.assertTrue(issubclass(int, Integral))
        self.assertTrue(issubclass(float, Real))
        self.assertTrue(issubclass(complex, Number))


if __name__ == "__main__":
    unittest.main()
