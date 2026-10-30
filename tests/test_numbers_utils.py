import unittest

from numbers_utils import (
    Complex,
    Integral,
    Number,
    Rational,
    Real,
    is_abundant_number,
    is_armstrong_number,
    is_automorphic_number,
    is_deficient_number,
    is_harshad_number,
    is_integral,
    is_neon_number,
    is_number,
    is_perfect_number,
    is_strong_number,
    proper_divisors,
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


class TestProperDivisors(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(proper_divisors(1), [])
        self.assertEqual(proper_divisors(6), [1, 2, 3])
        self.assertEqual(proper_divisors(28), [1, 2, 4, 7, 14])
        self.assertEqual(proper_divisors(12), [1, 2, 3, 4, 6])

    def test_type_error(self):
        for value in (1.5, "6", None, True, [6]):
            with self.assertRaises(TypeError):
                proper_divisors(value)

    def test_value_error(self):
        for value in (0, -1, -6):
            with self.assertRaises(ValueError):
                proper_divisors(value)


class TestIsStrongNumber(unittest.TestCase):
    def test_known_strong_numbers(self):
        for value in (1, 2, 145, 40585):
            self.assertTrue(is_strong_number(value), value)

    def test_non_strong_numbers(self):
        for value in (0, 3, 4, 5, 6, 7, 8, 10, 123, 144):
            self.assertFalse(is_strong_number(value), value)

    def test_below_one(self):
        self.assertFalse(is_strong_number(0))
        self.assertFalse(is_strong_number(-1))
        self.assertFalse(is_strong_number(-145))

    def test_type_error(self):
        for value in (1.5, "1", None, True, [1]):
            with self.assertRaises(TypeError):
                is_strong_number(value)


class TestIsHarshadNumber(unittest.TestCase):
    def test_known_harshad_numbers(self):
        for value in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20, 21, 24, 27, 30, 36, 40, 42, 45, 48, 50, 54, 60, 63, 70, 72, 80, 81, 84, 90, 100):
            self.assertTrue(is_harshad_number(value), value)

    def test_non_harshad_numbers(self):
        for value in (11, 13, 14, 15, 16, 17, 19, 22, 23, 25, 26, 28, 29, 31, 32, 33, 34, 35, 37, 38, 39, 41, 43, 44, 46, 47, 49, 51, 52, 53, 55, 56, 57, 58, 59, 61, 62, 64, 65, 66, 67, 68, 69, 71, 73, 74, 75, 76, 77, 78, 79, 82, 83, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99):
            self.assertFalse(is_harshad_number(value), value)

    def test_zero(self):
        self.assertTrue(is_harshad_number(0))

    def test_negative_harshad(self):
        self.assertTrue(is_harshad_number(-18))
        self.assertTrue(is_harshad_number(-21))

    def test_type_error(self):
        for value in (1.5, "18", None, True, [18]):
            with self.assertRaises(TypeError):
                is_harshad_number(value)


class TestIsNeonNumber(unittest.TestCase):
    def test_known_neon_numbers(self):
        for value in (0, 1, 9):
            self.assertTrue(is_neon_number(value), value)

    def test_non_neon_numbers(self):
        for value in (2, 3, 4, 5, 6, 7, 8, 10, 45, 100, 123):
            self.assertFalse(is_neon_number(value), value)

    def test_below_zero(self):
        self.assertFalse(is_neon_number(-1))
        self.assertFalse(is_neon_number(-9))

    def test_type_error(self):
        for value in (1.5, "9", None, True, [9]):
            with self.assertRaises(TypeError):
                is_neon_number(value)


class TestIsArmstrongNumber(unittest.TestCase):
    def test_known_armstrong_numbers(self):
        for value in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474, 54748, 92727, 93084):
            self.assertTrue(is_armstrong_number(value), value)

    def test_non_armstrong_numbers(self):
        for value in (10, 12, 123, 145, 200, 300, 1000):
            self.assertFalse(is_armstrong_number(value), value)

    def test_below_zero(self):
        self.assertFalse(is_armstrong_number(-153))
        self.assertFalse(is_armstrong_number(-1))

    def test_type_error(self):
        for value in (1.5, "153", None, True, [153]):
            with self.assertRaises(TypeError):
                is_armstrong_number(value)


class TestIsAutomorphicNumber(unittest.TestCase):
    def test_known_automorphic_numbers(self):
        for value in (0, 1, 5, 6, 25, 76, 376, 625, 9376, 90625, 109376):
            self.assertTrue(is_automorphic_number(value), value)

    def test_non_automorphic_numbers(self):
        for value in (2, 3, 4, 7, 8, 9, 10, 11, 12, 24, 26, 75, 77, 375, 377, 624, 626):
            self.assertFalse(is_automorphic_number(value), value)

    def test_below_zero(self):
        self.assertFalse(is_automorphic_number(-5))
        self.assertFalse(is_automorphic_number(-1))

    def test_type_error(self):
        for value in (1.5, "5", None, True, [5]):
            with self.assertRaises(TypeError):
                is_automorphic_number(value)


if __name__ == "__main__":
    unittest.main()
