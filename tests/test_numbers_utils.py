import unittest

from numbers_utils import (
    Complex,
    Integral,
    Number,
    Rational,
    Real,
    is_abundant_number,
    is_deficient_number,
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


class TestIsAbundantNumber(unittest.TestCase):
    def test_known_abundant_numbers(self):
        for value in (
            12, 18, 20, 24, 30, 36, 40, 42, 48, 54, 56, 60, 66, 70, 72,
            78, 80, 84, 88, 90, 96, 100,
        ):
            self.assertTrue(is_abundant_number(value), value)

    def test_non_abundant_numbers(self):
        for value in (
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19,
            21, 22, 23, 25, 26, 27, 28, 29,
        ):
            self.assertFalse(is_abundant_number(value), value)

    def test_below_two(self):
        self.assertFalse(is_abundant_number(1))
        self.assertFalse(is_abundant_number(0))
        self.assertFalse(is_abundant_number(-12))

    def test_type_error(self):
        for value in (1.5, "12", None, True, [12]):
            with self.assertRaises(TypeError):
                is_abundant_number(value)


class TestIsDeficientNumber(unittest.TestCase):
    def test_known_deficient_numbers(self):
        for value in (1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19):
            self.assertTrue(is_deficient_number(value), value)

    def test_non_deficient_numbers(self):
        for value in (6, 12, 18, 20, 24, 28, 496, 8128):
            self.assertFalse(is_deficient_number(value), value)

    def test_below_one(self):
        self.assertFalse(is_deficient_number(0))
        self.assertFalse(is_deficient_number(-1))
        self.assertFalse(is_deficient_number(-6))

    def test_type_error(self):
        for value in (1.5, "1", None, True, [1]):
            with self.assertRaises(TypeError):
                is_deficient_number(value)
