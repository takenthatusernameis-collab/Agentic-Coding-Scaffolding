import unittest

from numbers_utils import (
    Complex,
    Integral,
    Number,
    Rational,
    Real,
    is_abundant_number,
    is_almost_perfect_number,
    is_armstrong_number,
    is_automorphic_number,
    is_complex,
    is_coprime,
    is_deficient_number,
    is_disarium_number,
    is_duck_number,
    is_happy_number,
    is_harshad_number,
    is_integral,
    is_kaprekar_number,
    is_neon_number,
    is_number,
    is_palindromic_number,
    is_pandigital_number,
    is_perfect_number,
    is_perfect_power,
    is_polydivisible_number,
    is_pronic_number,
    is_rational,
    is_real,
    is_repdigit_number,
    is_spy_number,
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


class TestIsComplex(unittest.TestCase):
    def test_complex_numbers(self):
        self.assertTrue(is_complex(5))
        self.assertTrue(is_complex(1.5))
        self.assertTrue(is_complex(2 + 3j))
        self.assertFalse(is_complex("x"))
        self.assertFalse(is_complex(None))

    def test_complex_subclass(self):
        self.assertTrue(is_complex(True))
        self.assertFalse(is_complex([1, 2]))


class TestIsReal(unittest.TestCase):
    def test_real_numbers(self):
        self.assertTrue(is_real(5))
        self.assertTrue(is_real(1.5))
        self.assertTrue(is_real(True))
        self.assertFalse(is_real(2 + 3j))
        self.assertFalse(is_real("x"))
        self.assertFalse(is_real(None))

    def test_real_negative_and_zero(self):
        self.assertTrue(is_real(0))
        self.assertTrue(is_real(-3))


class TestIsRational(unittest.TestCase):
    def test_rational_numbers(self):
        self.assertTrue(is_rational(5))
        self.assertTrue(is_rational(True))
        self.assertFalse(is_rational(1.5))
        self.assertFalse(is_rational(2 + 3j))
        self.assertFalse(is_rational("x"))
        self.assertFalse(is_rational(None))

    def test_rational_zero_and_negative(self):
        self.assertTrue(is_rational(0))
        self.assertTrue(is_rational(-7))


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


class TestIsAlmostPerfectNumber(unittest.TestCase):
    def test_known_almost_perfect_numbers(self):
        for value in (1, 2, 4, 8, 16, 32, 64, 128, 256):
            self.assertTrue(is_almost_perfect_number(value), value)

    def test_non_almost_perfect_numbers(self):
        for value in (3, 5, 6, 7, 9, 10, 12, 15, 20, 28, 100):
            self.assertFalse(is_almost_perfect_number(value), value)

    def test_below_one(self):
        self.assertFalse(is_almost_perfect_number(0))
        self.assertFalse(is_almost_perfect_number(-1))
        self.assertFalse(is_almost_perfect_number(-16))

    def test_type_error(self):
        for value in (1.5, "2", None, True, [2]):
            with self.assertRaises(TypeError):
                is_almost_perfect_number(value)




class TestIsDuckNumber(unittest.TestCase):
    def test_duck_numbers(self):
        for value in (101, 203, 100, 10):
            self.assertTrue(is_duck_number(value), value)

    def test_non_duck_numbers(self):
        for value in (123, 0, 1, 9):
            self.assertFalse(is_duck_number(value), value)

    def test_type_error(self):
        for value in (1.5, "101", None, [0, 1], True):
            with self.assertRaises(TypeError):
                is_duck_number(value)


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
        for value in (
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20, 21, 24, 27, 30, 36, 40, 42, 45, 48, 50, 54,
            60, 63, 70, 72, 80, 81, 84, 90, 100,
        ):
            self.assertTrue(is_harshad_number(value), value)

    def test_non_harshad_numbers(self):
        for value in (
            11, 13, 14, 15, 16, 17, 19, 22, 23, 25, 26, 28, 29, 31, 32, 33, 34, 35, 37, 38, 39, 41,
            43, 44, 46, 47, 49, 51, 52, 53, 55, 56, 57, 58, 59, 61, 62, 64, 65, 66, 67, 68, 69, 71,
            73, 74, 75, 76, 77, 78, 79, 82, 83, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98,
            99,
        ):
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
        for value in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474, 54748,
                     92727, 93084):
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


class TestIsHappyNumber(unittest.TestCase):
    def test_known_happy_numbers(self):
        for value in (1, 7, 10, 13, 19, 23, 28, 31, 32, 44):
            self.assertTrue(is_happy_number(value), value)

    def test_non_happy_numbers(self):
        for value in (2, 3, 4, 5, 6, 8, 9, 11, 12, 14, 15, 16, 17, 18, 20):
            self.assertFalse(is_happy_number(value), value)

    def test_zero_is_happy(self):
        self.assertTrue(is_happy_number(0))

    def test_negative_numbers(self):
        for value in (-1, -7, -19):
            self.assertFalse(is_happy_number(value))

    def test_type_error(self):
        for value in (1.5, "7", None, True, [7]):
            with self.assertRaises(TypeError):
                is_happy_number(value)


class TestIsPronicNumber(unittest.TestCase):
    def test_known_pronic_numbers(self):
        for value in (2, 6, 12, 20, 30, 42, 56, 72):
            self.assertTrue(is_pronic_number(value), value)

    def test_non_pronic_numbers(self):
        for value in (1, 3, 4, 5, 7, 8, 9, 10, 11):
            self.assertFalse(is_pronic_number(value), value)

    def test_zero_and_negatives(self):
        self.assertFalse(is_pronic_number(0))
        for value in (-2, -1):
            self.assertFalse(is_pronic_number(value))

    def test_type_error(self):
        for value in (1.5, "2", None, True, [2]):
            with self.assertRaises(TypeError):
                is_pronic_number(value)


class TestIsPolydivisibleNumber(unittest.TestCase):
    def test_known_polydivisible_numbers(self):
        for value in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 102, 123, 1236, 12360):
            self.assertTrue(is_polydivisible_number(value), value)

    def test_non_polydivisible_numbers(self):
        for value in (11, 13, 15, 17, 19, 100, 124, 1234, 12345):
            self.assertFalse(is_polydivisible_number(value), value)

    def test_negatives(self):
        for value in (-1, -12, -123):
            self.assertFalse(is_polydivisible_number(value))

    def test_type_error(self):
        for value in (1.5, "12", None, True, [12]):
            with self.assertRaises(TypeError):
                is_polydivisible_number(value)


class TestIsSpyNumber(unittest.TestCase):

    def test_known_spy_numbers(self):
        for value in (1, 2, 3, 4, 5, 6, 7, 8, 9, 22, 123, 132, 213, 231, 312, 321, 1124):
            self.assertTrue(is_spy_number(value), value)

    def test_non_spy_numbers(self):
        for value in (10, 11, 12, 14, 15, 100, 1234):
            self.assertFalse(is_spy_number(value), value)

    def test_below_one(self):
        for value in (0, -1, -22):
            self.assertFalse(is_spy_number(value), value)

    def test_type_error(self):
        for value in (1.5, "22", None, True, [22]):
            with self.assertRaises(TypeError):
                is_spy_number(value)


class TestIsRepdigitNumber(unittest.TestCase):
    def test_known_repdigits(self):
        for value in (0, 5, 9, 11, 22, 33, 55, 66, 77, 88, 99, 111, 222, 555, 666, 777, 888, 999):
            self.assertTrue(is_repdigit_number(value), value)

    def test_non_repdigits(self):
        for value in (12, 10, 123, 121, 112, 102):
            self.assertFalse(is_repdigit_number(value), value)

    def test_negatives(self):
        for value in (-1, -5, -11):
            self.assertFalse(is_repdigit_number(value), value)

    def test_type_error(self):
        for value in (1.5, "11", None, True, [11]):
            with self.assertRaises(TypeError):
                is_repdigit_number(value)


class TestIsPalindromicNumber(unittest.TestCase):
    def test_known_palindromes(self):
        for value in (0, 1, 2, 9, 11, 22, 121, 1221, 12321):
            self.assertTrue(is_palindromic_number(value), value)

    def test_non_palindromes(self):
        for value in (10, 12, 102, 123, 89):
            self.assertFalse(is_palindromic_number(value), value)

    def test_negatives(self):
        for value in (-1, -11):
            with self.assertRaises(ValueError):
                is_palindromic_number(value)

    def test_type_error(self):
        for value in (1.5, "121", None, True, [121]):
            with self.assertRaises(TypeError):
                is_palindromic_number(value)


class TestIsCoprime(unittest.TestCase):
    def test_coprime_pairs(self):
        for a, b in ((2, 3), (3, 4), (8, 9), (1, 100), (14, 15)):
            self.assertTrue(is_coprime(a, b), (a, b))

    def test_not_coprime(self):
        for a, b in ((2, 4), (6, 9), (4, 2), (0, 5)):
            self.assertFalse(is_coprime(a, b), (a, b))

    def test_type_error(self):
        for value in (1.5, "2", None, [2]):
            with self.assertRaises(TypeError):
                is_coprime(value, 3)
            with self.assertRaises(TypeError):
                is_coprime(3, value)
        with self.assertRaises(TypeError):
            is_coprime(True, 3)
        with self.assertRaises(TypeError):
            is_coprime(3, True)


class TestIsPerfectPower(unittest.TestCase):
    def test_known_perfect_powers(self):
        for value in (4, 8, 9, 16, 25, 27, 32, 36, 49, 64, 81, 100, 121, 125, 128):
            self.assertTrue(is_perfect_power(value), value)

    def test_not_perfect_powers(self):
        for value in (2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20):
            self.assertFalse(is_perfect_power(value), value)

    def test_one_and_below(self):
        self.assertFalse(is_perfect_power(1))
        self.assertFalse(is_perfect_power(0))
        self.assertFalse(is_perfect_power(-8))

    def test_type_error(self):
        for value in (1.5, "4", None, True, [4]):
            with self.assertRaises(TypeError):
                is_perfect_power(value)


class TestIsPandigitalNumber(unittest.TestCase):
    def test_known_pandigitals_base10(self):
        for value in (1023456789, 1234567890, 9876543210, 1023456798):
            self.assertTrue(is_pandigital_number(value), value)

    def test_non_pandigitals_base10(self):
        for value in (123456789, 987654321, 12345, 112233, 12345678, 123456798, 0, 1, 9):
            self.assertFalse(is_pandigital_number(value), value)

    def test_negatives(self):
        for value in (-1, -1023456789):
            self.assertFalse(is_pandigital_number(value), value)

    def test_other_bases(self):
        # base 2: 0b10 == 2 uses both 0 and 1
        self.assertTrue(is_pandigital_number(2, base=2))
        self.assertFalse(is_pandigital_number(1, base=2))
        # base 4: 0x1023 in base 4 == 75 decimal uses 0,1,2,3
        self.assertTrue(is_pandigital_number(75, base=4))
        self.assertFalse(is_pandigital_number(74, base=4))
        # base 16: 0x1023456789abcdef == 1162849439785405935 decimal
        self.assertTrue(is_pandigital_number(1162849439785405935, base=16))
        self.assertFalse(is_pandigital_number(1162849439785405934, base=16))

    def test_default_base(self):
        self.assertTrue(is_pandigital_number(1023456789))
        self.assertFalse(is_pandigital_number(12345))

    def test_type_errors(self):
        for value in (1.5, "1023456789", None, [0, 1]):
            with self.assertRaises(TypeError):
                is_pandigital_number(value)
        with self.assertRaises(TypeError):
            is_pandigital_number(1023456789, base=10.0)
        with self.assertRaises(TypeError):
            is_pandigital_number(1023456789, base=True)

    def test_value_error_bad_base(self):
        for base in (1, 0, -1, 37, 100):
            with self.assertRaises(ValueError):
                is_pandigital_number(1023456789, base=base)


if __name__ == "__main__":
    unittest.main()
