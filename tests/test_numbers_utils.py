import unittest

from numbers_utils import (
    Complex,
    Integral,
    Number,
    Rational,
    Real,
    is_integral,
    is_number,
    is_perfect_number,
)


class TestNumbersUtils(unittest.TestCase):
    def test_is_number(self):
        self.assertTrue(is_number(5))
        self.assertTrue(is_number(1.5))
        self.assertTrue(is_number(2 + 3j))
        self.assertFalse(is_number("x"))

    def test_is_integral(self):
        self.assertTrue(is_integral(5))
        self.assertTrue(is_integral(True))
        self.assertFalse(is_integral(1.5))
        self.assertFalse(is_integral("x"))

    def test_classes(self):
        self.assertTrue(issubclass(int, Integral))
        self.assertTrue(issubclass(float, Real))
        self.assertTrue(issubclass(complex, Number))
        self.assertTrue(issubclass(int, Rational))
        self.assertTrue(issubclass(complex, Complex))


class TestIsPerfectNumber(unittest.TestCase):
    def test_known_perfect_numbers(self):
        for value in (6, 28, 496, 8128, 33550336):
            self.assertTrue(is_perfect_number(value), value)

    def test_non_perfect_numbers(self):
        for value in (1, 2, 3, 4, 5, 7, 8, 9, 10, 12, 27, 29):
            self.assertFalse(is_perfect_number(value), value)

    def test_large_perfect_number(self):
        self.assertTrue(is_perfect_number(8589869056))

    def test_below_two(self):
        self.assertFalse(is_perfect_number(1))
        self.assertFalse(is_perfect_number(0))
        self.assertFalse(is_perfect_number(-6))

    def test_type_error(self):
        for value in (1.5, "6", None, True, [6]):
            with self.assertRaises(TypeError):
                is_perfect_number(value)


if __name__ == "__main__":
    unittest.main()
