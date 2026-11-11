import unittest

from numbers_utils import (
    Complex,
    Integral,
    Number,
    Rational,
    Real,
    aliquot_sum,
    is_abundant_number,
    is_almost_perfect_number,
    is_armstrong_number,
    is_automorphic_number,
    is_complex,
    is_coprime,
    is_deficient_number,
    is_disarium_number,
    is_duck_number,
    is_even,
    is_evil_number,
    is_fibonacci_number,
    is_happy_number,
    is_harshad_number,
    is_hexagonal_number,
    is_integral,
    is_kaprekar_number,
    is_narcissistic,
    is_narcissistic_number,
    is_neon_number,
    is_number,
    is_oblong_number,
    is_odd,
    is_odious_number,
    is_palindromic_number,
    is_pandigital_number,
    is_pentagonal_number,
    is_perfect_cube,
    is_perfect_number,
    is_perfect_power,
    is_perfect_square,
    is_polydivisible_number,
    is_power_of,
    is_power_of_two,
    is_pronic_number,
    is_rational,
    is_real,
    is_repdigit_number,
    is_semiperfect_number,
    is_sphenic_number,
    is_spy_number,
    is_squarefree_number,
    is_strong_number,
    is_triangular_number,
    is_ugly_number,
    is_untouchable_number,
    is_weird_number,
    proper_divisors,
    sum_of_divisors,
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


class TestIsPowerOf(unittest.TestCase):
    def test_known_powers(self):
        cases = [
            (1, 2, True),
            (1, 5, True),
            (1, -3, True),
            (8, 2, True),
            (9, 3, True),
            (16, 2, True),
            (27, 3, True),
            (64, 2, True),
            (125, 5, True),
            (1000, 10, True),
            (-8, -2, True),
            (4, -2, True),
            (-4, -2, False),
            (8, -2, False),
            (0, 5, False),
            (0, 0, True),
            (1, 0, True),
            (1, 1, True),
            (2, 1, False),
            (1, -1, True),
            (-1, -1, True),
            (2, -1, False),
            (7, 2, False),
            (6, 2, False),
            (10, 3, False),
            (-27, -3, True),
            (9, -3, True),
            (-9, -3, False),
            (2, 2, True),
            (3, 3, True),
        ]
        for value, base, expected in cases:
            with self.subTest(value=value, base=base):
                self.assertEqual(is_power_of(value, base), expected, (value, base))

    def test_consistency_with_direct_power(self):
        for base in range(-6, 7):
            if base in (0, 1, -1):
                continue
            for k in range(0, 8):
                value = base ** k
                self.assertTrue(is_power_of(value, base), (value, base, k))
            for k in range(1, 6):
                p = base ** k
                for delta in (-1, 1):
                    v = p + delta
                    if v == base ** (k + 1) or v == base ** (k - 1):
                        continue
                    self.assertFalse(is_power_of(v, base), (v, base))

    def test_type_error(self):
        for value in (1.5, "8", None, True, [8]):
            with self.assertRaises(TypeError):
                is_power_of(value, 2)
        for base in (1.5, "2", None, True, [2]):
            with self.assertRaises(TypeError):
                is_power_of(8, base)


if __name__ == "__main__":
    unittest.main()


class TestIsAbundantNumber(unittest.TestCase):
    def test_known_abundant_numbers(self):
        for value in (
            12,
            18,
            20,
            24,
            30,
            36,
            40,
            42,
            48,
            54,
            56,
            60,
            66,
            70,
            72,
            78,
            80,
            84,
            88,
            90,
            96,
            100,
        ):
            self.assertTrue(is_abundant_number(value), value)

    def test_non_abundant_numbers(self):
        for value in (
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            13,
            14,
            15,
            16,
            17,
            19,
            21,
            22,
            23,
            25,
            26,
            27,
            28,
            29,
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


class TestIsFibonacciNumber(unittest.TestCase):
    def test_known_fibonacci_numbers(self):
        for value in (0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144):
            self.assertTrue(is_fibonacci_number(value), value)

    def test_non_fibonacci_numbers(self):
        for value in (4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 22, 100):
            self.assertFalse(is_fibonacci_number(value), value)

    def test_negative(self):
        self.assertFalse(is_fibonacci_number(-1))
        self.assertFalse(is_fibonacci_number(-13))

    def test_type_error(self):
        for value in (1.5, "1", None, True, [1]):
            with self.assertRaises(TypeError):
                is_fibonacci_number(value)


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


class TestAliquotSum(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(aliquot_sum(1), 0)
        self.assertEqual(aliquot_sum(6), 6)
        self.assertEqual(aliquot_sum(28), 28)
        self.assertEqual(aliquot_sum(12), 16)
        self.assertEqual(aliquot_sum(1), sum(proper_divisors(1)))
        self.assertEqual(aliquot_sum(6), sum(proper_divisors(6)))
        self.assertEqual(aliquot_sum(28), sum(proper_divisors(28)))

    def test_perfect_abundant_deficient(self):
        # Perfect numbers have aliquot sum equal to the number itself.
        self.assertEqual(aliquot_sum(6), 6)
        self.assertEqual(aliquot_sum(28), 28)
        # Abundant numbers have aliquot sum greater than the number.
        self.assertGreater(aliquot_sum(12), 12)
        # Deficient numbers have aliquot sum less than the number.
        self.assertLess(aliquot_sum(8), 8)

    def test_type_error(self):
        for value in (1.5, "6", None, True, [6]):
            with self.assertRaises(TypeError):
                aliquot_sum(value)

    def test_value_error(self):
        for value in (0, -1, -6):
            with self.assertRaises(ValueError):
                aliquot_sum(value)


class TestSumOfDivisors(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(sum_of_divisors(1), 1)
        self.assertEqual(sum_of_divisors(6), 12)
        self.assertEqual(sum_of_divisors(28), 56)
        self.assertEqual(sum_of_divisors(12), 28)

    def test_relation_to_aliquot_sum(self):
        for n in (1, 2, 6, 12, 28, 100):
            self.assertEqual(sum_of_divisors(n), aliquot_sum(n) + n)

    def test_type_error(self):
        for value in (1.5, "6", None, True, [6]):
            with self.assertRaises(TypeError):
                sum_of_divisors(value)

    def test_value_error(self):
        for value in (0, -1, -6):
            with self.assertRaises(ValueError):
                sum_of_divisors(value)


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
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            12,
            18,
            20,
            21,
            24,
            27,
            30,
            36,
            40,
            42,
            45,
            48,
            50,
            54,
            60,
            63,
            70,
            72,
            80,
            81,
            84,
            90,
            100,
        ):
            self.assertTrue(is_harshad_number(value), value)

    def test_non_harshad_numbers(self):
        for value in (
            11,
            13,
            14,
            15,
            16,
            17,
            19,
            22,
            23,
            25,
            26,
            28,
            29,
            31,
            32,
            33,
            34,
            35,
            37,
            38,
            39,
            41,
            43,
            44,
            46,
            47,
            49,
            51,
            52,
            53,
            55,
            56,
            57,
            58,
            59,
            61,
            62,
            64,
            65,
            66,
            67,
            68,
            69,
            71,
            73,
            74,
            75,
            76,
            77,
            78,
            79,
            82,
            83,
            85,
            86,
            87,
            88,
            89,
            91,
            92,
            93,
            94,
            95,
            96,
            97,
            98,
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
        for value in (
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            153,
            370,
            371,
            407,
            1634,
            8208,
            9474,
            54748,
            92727,
            93084,
        ):
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
        for value in (
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            12,
            14,
            16,
            18,
            20,
            22,
            24,
            26,
            28,
            36,
            48,
            102,
            123,
            1236,
            12360,
        ):  # noqa: E501
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


class TestIsOdiousNumber(unittest.TestCase):
    def test_known_odious_numbers(self):
        # odious numbers: non-negative ints with an odd number of 1-bits
        for value in (1, 2, 4, 7, 8, 11, 13, 14, 16, 19, 21, 22, 25, 26, 28, 31, 32):
            self.assertTrue(is_odious_number(value), value)

    def test_known_evil_numbers(self):
        # evil numbers have an even number of 1-bits; odious and evil partition N
        for value in (0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30):
            self.assertFalse(is_odious_number(value), value)

    def test_large_odious_number(self):
        # 2**16 - 1 = 65535 = 0b1111111111111111 (16 ones, even -> evil)
        self.assertFalse(is_odious_number(65535))
        # 2**16 + 1 = 65537 = 0b10000000000000001 (2 ones, even -> evil)
        self.assertFalse(is_odious_number(65537))
        # 2**16 + 3 = 65539 = 0b10000000000000011 (3 ones, odd -> odious)
        self.assertTrue(is_odious_number(65539))

    def test_negative_numbers(self):
        for value in (-1, -2, -7):
            self.assertFalse(is_odious_number(value))

    def test_type_error(self):
        for value in (1.5, "2", None, True, [2]):
            with self.assertRaises(TypeError):
                is_odious_number(value)


class TestIsEvilNumber(unittest.TestCase):
    def test_known_evil_numbers(self):
        for value in (0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30):
            self.assertTrue(is_evil_number(value), value)

    def test_known_odious_numbers(self):
        for value in (1, 2, 4, 7, 8, 11, 13, 14, 16, 19, 21, 22, 25, 26, 28, 31, 32):
            self.assertFalse(is_evil_number(value), value)

    def test_large_evil_number(self):
        # 2**16 - 1 = 65535 has 16 ones (even) -> evil
        self.assertTrue(is_evil_number(65535))
        # 2**16 + 3 = 65539 has 3 ones (odd) -> odious
        self.assertFalse(is_evil_number(65539))

    def test_negative_numbers(self):
        for value in (-1, -3, -6):
            self.assertFalse(is_evil_number(value))

    def test_type_error(self):
        for value in (1.5, "3", None, True, [3]):
            with self.assertRaises(TypeError):
                is_evil_number(value)


class TestIsSemiperfectNumber(unittest.TestCase):
    def test_known_semiperfect_numbers(self):
        # numbers that equal the sum of some subset of their proper divisors
        values = (
            6,
            12,
            18,
            20,
            24,
            28,
            30,
            36,
            40,
            42,
            48,
            54,
            56,
            60,
            66,
            72,
            78,
            80,
            84,
            88,
            90,
            96,
            100,
        )
        for value in values:
            self.assertTrue(is_semiperfect_number(value), value)

    def test_perfect_numbers_are_semiperfect(self):
        for value in (6, 28, 496, 8128):
            self.assertTrue(is_semiperfect_number(value), value)

    def test_powers_of_two_are_not_semiperfect(self):
        # powers of two are almost perfect but not semiperfect
        for value in (1, 2, 4, 8, 16, 32, 64, 128):
            self.assertFalse(is_semiperfect_number(value), value)

    def test_primes_and_deficient_numbers(self):
        for value in (2, 3, 4, 5, 7, 9, 11, 13, 17, 19, 23):
            self.assertFalse(is_semiperfect_number(value), value)

    def test_weird_numbers_are_not_semiperfect(self):
        # Weird numbers are abundant but not semiperfect (no subset of proper
        # divisors sums to the number).
        for value in (70, 836, 4030, 5830, 7192, 7912, 9272):
            self.assertFalse(is_semiperfect_number(value), value)

    def test_negative_and_zero(self):
        for value in (0, -1, -12, -100):
            self.assertFalse(is_semiperfect_number(value))

    def test_type_error(self):
        for value in (1.5, "12", None, True, [12]):
            with self.assertRaises(TypeError):
                is_semiperfect_number(value)


class TestIsWeirdNumber(unittest.TestCase):
    def test_known_weird_numbers(self):
        # Weird numbers are abundant but not semiperfect (no subset of proper
        # divisors sums to the number). These are known weird numbers.
        for value in (70, 836, 4030, 5830, 7192, 7912, 9272):
            self.assertTrue(is_weird_number(value), value)

    def test_abundant_but_semiperfect_not_weird(self):
        # 12 is abundant (1+2+3+4+6=16>12) and semiperfect (1+2+3+6=12),
        # so it is not weird. Same for 18 and 20.
        self.assertFalse(is_weird_number(12))
        self.assertFalse(is_weird_number(18))
        self.assertFalse(is_weird_number(20))

    def test_non_abundant_not_weird(self):
        for value in (1, 2, 3, 4, 5, 6, 28, 496):
            self.assertFalse(is_weird_number(value))

    def test_negative_and_zero(self):
        for value in (0, -1, -12, -70):
            self.assertFalse(is_weird_number(value))

    def test_type_error(self):
        for value in (1.5, "70", None, True, [70]):
            with self.assertRaises(TypeError):
                is_weird_number(value)


class TestIsSphenicNumber(unittest.TestCase):
    def test_known_sphenic_numbers(self):
        for value in (
            30, 42, 66, 70, 78, 102, 105, 110, 114, 130, 138, 154, 165, 170, 174,
            182, 186, 190, 195, 222, 230, 231, 238, 246, 255, 258, 266, 273, 282,
            285, 286, 290,
        ):
            self.assertTrue(is_sphenic_number(value), value)

    def test_non_sphenic_numbers(self):
        # prime powers, products of !=3 distinct primes, non-squarefree
        for value in (0, 1, 2, 4, 6, 8, 12, 18, 20, 24, 27, 28, 29, 60, 64, 90, 120, 210):
            self.assertFalse(is_sphenic_number(value), value)

    def test_squareful_with_three_prime_factors_total_count(self):
        # 12 = 2^2*3 has 2 distinct prime factors
        self.assertFalse(is_sphenic_number(12))
        # 60 = 2^2*3*5 not squarefree
        self.assertFalse(is_sphenic_number(60))

    def test_negative_numbers(self):
        for value in (-1, -30, -42):
            self.assertFalse(is_sphenic_number(value))

    def test_type_error(self):
        for value in (1.5, "30", None, True, [30]):
            with self.assertRaises(TypeError):
                is_sphenic_number(value)


class TestAbundance(unittest.TestCase):
    def test_known_values(self):
        from numbers_utils import abundance

        self.assertEqual(abundance(1), -1)
        self.assertEqual(abundance(6), 0)
        self.assertEqual(abundance(28), 0)
        self.assertEqual(abundance(12), 4)
        self.assertEqual(abundance(8), -1)
        self.assertEqual(abundance(7), -6)

    def test_validation(self):
        from numbers_utils import abundance

        with self.assertRaises(TypeError):
            abundance(1.5)
        with self.assertRaises(TypeError):
            abundance(True)
        with self.assertRaises(ValueError):
            abundance(0)
        with self.assertRaises(ValueError):
            abundance(-1)


class TestAreAmicable(unittest.TestCase):
    def test_known_pairs(self):
        from numbers_utils import are_amicable

        self.assertTrue(are_amicable(220, 284))
        self.assertTrue(are_amicable(284, 220))
        self.assertTrue(are_amicable(1184, 1210))

    def test_non_pairs(self):
        from numbers_utils import are_amicable

        self.assertFalse(are_amicable(6, 6))
        self.assertFalse(are_amicable(12, 16))
        self.assertFalse(are_amicable(220, 220))
        self.assertFalse(are_amicable(0, 1))
        self.assertFalse(are_amicable(-220, 284))

    def test_type_error(self):
        from numbers_utils import are_amicable

        with self.assertRaises(TypeError):
            are_amicable(220.0, 284)
        with self.assertRaises(TypeError):
            are_amicable(220, True)
        with self.assertRaises(TypeError):
            are_amicable("220", 284)


class TestIsAmicableNumber(unittest.TestCase):
    def test_known_amicable_numbers(self):
        from numbers_utils import is_amicable_number

        for value in (220, 284, 1184, 1210, 2620, 2924):
            self.assertTrue(is_amicable_number(value), value)

    def test_non_amicable(self):
        from numbers_utils import is_amicable_number

        for value in (1, 2, 6, 28, 496, 12, 100):
            self.assertFalse(is_amicable_number(value), value)

    def test_edge_cases(self):
        from numbers_utils import is_amicable_number

        self.assertFalse(is_amicable_number(0))
        self.assertFalse(is_amicable_number(-220))

    def test_type_error(self):
        from numbers_utils import is_amicable_number

        for value in (1.5, "220", None, True, [220]):
            with self.assertRaises(TypeError):
                is_amicable_number(value)


class TestIsEven(unittest.TestCase):
    def test_even_values(self):

        for value in (0, 2, -2, 100, -100, 2 * 10**6):
            self.assertTrue(is_even(value), value)

    def test_odd_values(self):

        for value in (1, 3, -1, -3, 99, 2 * 10**6 + 1):
            self.assertFalse(is_even(value), value)

    def test_type_error(self):

        for value in (1.5, 2.0, "2", None, True, [2], (2,)):
            with self.assertRaises(TypeError):
                is_even(value)


class TestIsOdd(unittest.TestCase):
    def test_odd_values(self):
        for value in (1, 3, -1, -3, 99, 2 * 10**6 + 1):
            self.assertTrue(is_odd(value), value)

    def test_even_values(self):
        for value in (0, 2, -2, 100, -100, 2 * 10**6):
            self.assertFalse(is_odd(value), value)

    def test_type_error(self):
        for value in (1.5, 2.0, "3", None, True, [3], (3,)):
            with self.assertRaises(TypeError):
                is_odd(value)


class TestIsDisariumNumber(unittest.TestCase):
    def test_known_disarium_numbers(self):
        for value in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 89, 135, 175, 518, 598):
            self.assertTrue(is_disarium_number(value), value)

    def test_non_disarium_numbers(self):
        for value in (10, 11, 12, 13, 14, 15, 20, 100, 136):
            self.assertFalse(is_disarium_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -89, -135):
            self.assertFalse(is_disarium_number(value))

    def test_type_error(self):
        for value in (1.5, "135", None, True, [135]):
            with self.assertRaises(TypeError):
                is_disarium_number(value)


class TestIsKaprekarNumber(unittest.TestCase):
    def test_known_kaprekar_numbers(self):
        for value in (0, 9, 45, 55, 99, 297, 703, 999, 2223):
            self.assertTrue(is_kaprekar_number(value), value)

    def test_non_kaprekar_numbers(self):
        for value in (2, 3, 4, 5, 6, 7, 8, 10, 100, 1000):
            self.assertFalse(is_kaprekar_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -45, -297):
            self.assertFalse(is_kaprekar_number(value))

    def test_type_error(self):
        for value in (1.5, "45", None, True, [45]):
            with self.assertRaises(TypeError):
                is_kaprekar_number(value)


class TestIsPerfectSquare(unittest.TestCase):
    def test_known_perfect_squares(self):
        for value in (0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 10000):
            self.assertTrue(is_perfect_square(value), value)

    def test_non_perfect_squares(self):
        for value in (2, 3, 5, 6, 7, 8, 10, 15, 20, 1000):
            self.assertFalse(is_perfect_square(value), value)

    def test_negative_numbers(self):
        for value in (-1, -4, -16, -100):
            self.assertFalse(is_perfect_square(value))

    def test_type_error(self):
        for value in (1.5, "16", None, True, [16]):
            with self.assertRaises(TypeError):
                is_perfect_square(value)


class TestIsPerfectCube(unittest.TestCase):
    def test_known_perfect_cubes(self):
        for value in (0, 1, 8, 27, 64, 125, 216, 1000):
            self.assertTrue(is_perfect_cube(value), value)

    def test_negative_perfect_cubes(self):
        for value in (-1, -8, -27, -64):
            self.assertTrue(is_perfect_cube(value), value)

    def test_non_perfect_cubes(self):
        for value in (2, 3, 4, 5, 6, 7, 9, 10, 20, 100):
            self.assertFalse(is_perfect_cube(value), value)

    def test_type_error(self):
        for value in (1.5, "27", None, True, [27]):
            with self.assertRaises(TypeError):
                is_perfect_cube(value)


class TestIsPowerOfTwo(unittest.TestCase):
    def test_known_powers_of_two(self):
        for value in (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024, 2 ** 20):
            self.assertTrue(is_power_of_two(value), value)

    def test_non_powers_of_two(self):
        for value in (0, 3, 5, 6, 7, 9, 10, 12, 100, 1000):
            self.assertFalse(is_power_of_two(value), value)

    def test_negative_and_zero(self):
        for value in (0, -1, -2, -4, -16):
            self.assertFalse(is_power_of_two(value))

    def test_type_error(self):
        for value in (1.5, "16", None, True, [16]):
            with self.assertRaises(TypeError):
                is_power_of_two(value)


class TestIsTriangularNumber(unittest.TestCase):
    def test_known_triangular_numbers(self):
        for value in (0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78):
            self.assertTrue(is_triangular_number(value), value)

    def test_non_triangular_numbers(self):
        for value in (2, 4, 5, 7, 8, 9, 11, 12, 20, 100):
            self.assertFalse(is_triangular_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -3, -10):
            self.assertFalse(is_triangular_number(value))

    def test_type_error(self):
        for value in (1.5, "10", None, True, [10]):
            with self.assertRaises(TypeError):
                is_triangular_number(value)


class TestIsPentagonalNumber(unittest.TestCase):
    def test_known_pentagonal_numbers(self):
        for value in (0, 1, 5, 12, 22, 35, 51, 70):
            self.assertTrue(is_pentagonal_number(value), value)

    def test_non_pentagonal_numbers(self):
        for value in (2, 3, 4, 6, 7, 8, 9, 10, 20, 100):
            self.assertFalse(is_pentagonal_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -5, -12):
            self.assertFalse(is_pentagonal_number(value))

    def test_type_error(self):
        for value in (1.5, "12", None, True, [12]):
            with self.assertRaises(TypeError):
                is_pentagonal_number(value)


class TestIsHexagonalNumber(unittest.TestCase):
    def test_known_hexagonal_numbers(self):
        for value in (0, 1, 6, 15, 28, 45, 66, 91):
            self.assertTrue(is_hexagonal_number(value), value)

    def test_non_hexagonal_numbers(self):
        for value in (2, 3, 4, 5, 7, 8, 9, 10, 20, 100):
            self.assertFalse(is_hexagonal_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -6, -15):
            self.assertFalse(is_hexagonal_number(value))

    def test_type_error(self):
        for value in (1.5, "15", None, True, [15]):
            with self.assertRaises(TypeError):
                is_hexagonal_number(value)


class TestIsSquarefreeNumber(unittest.TestCase):
    def test_known_squarefree_numbers(self):
        for value in (
            1,
            2,
            3,
            5,
            6,
            7,
            10,
            11,
            13,
            14,
            15,
            17,
            21,
            22,
            23,
            29,
            30,
        ):
            self.assertTrue(is_squarefree_number(value), value)

    def test_non_squarefree_numbers(self):
        for value in (4, 8, 9, 12, 16, 18, 20, 24, 25, 27, 28, 32, 36, 100):
            self.assertFalse(is_squarefree_number(value), value)

    def test_zero_and_negative(self):
        self.assertFalse(is_squarefree_number(0))
        for value in (-1, -4, -12):
            self.assertFalse(is_squarefree_number(value))

    def test_type_error(self):
        for value in (1.5, "12", None, True, [12]):
            with self.assertRaises(TypeError):
                is_squarefree_number(value)


class TestIsOblongNumber(unittest.TestCase):
    def test_known_oblong_numbers(self):
        for value in (0, 2, 6, 12, 20, 30, 42, 56, 72):
            self.assertTrue(is_oblong_number(value), value)

    def test_non_oblong_numbers(self):
        for value in (1, 3, 4, 5, 7, 8, 9, 10, 11, 100):
            self.assertFalse(is_oblong_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -2, -6):
            self.assertFalse(is_oblong_number(value))

    def test_type_error(self):
        for value in (1.5, "12", None, True, [12]):
            with self.assertRaises(TypeError):
                is_oblong_number(value)


class TestIsUglyNumber(unittest.TestCase):
    def test_known_ugly_numbers(self):
        for value in (
            1,
            2,
            3,
            4,
            5,
            6,
            8,
            9,
            10,
            12,
            15,
            16,
            18,
            20,
            24,
            25,
            27,
            30,
            32,
            36,
            40,
            45,
            48,
            50,
            60,
            64,
            72,
            75,
            80,
            81,
            90,
            96,
            100,
        ):
            self.assertTrue(is_ugly_number(value), value)

    def test_non_ugly_numbers(self):
        for value in (7, 11, 13, 14, 17, 19, 22, 23, 26, 28, 29, 31, 33, 34, 35):
            self.assertFalse(is_ugly_number(value), value)

    def test_zero_and_negative(self):
        self.assertFalse(is_ugly_number(0))
        for value in (-1, -7, -30):
            self.assertFalse(is_ugly_number(value))

    def test_type_error(self):
        for value in (1.5, "30", None, True, [30]):
            with self.assertRaises(TypeError):
                is_ugly_number(value)


class TestIsNarcissisticNumber(unittest.TestCase):
    def test_known_narcissistic_numbers(self):
        for value in (
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            153,
            370,
            371,
            407,
            1634,
            8208,
            9474,
        ):
            self.assertTrue(is_narcissistic_number(value), value)

    def test_non_narcissistic_numbers(self):
        for value in (10, 12, 123, 145, 200, 1000, 9999):
            self.assertFalse(is_narcissistic_number(value), value)

    def test_negative_numbers(self):
        for value in (-1, -153, -370):
            self.assertFalse(is_narcissistic_number(value))

    def test_type_error(self):
        for value in (1.5, "153", None, True, [153]):
            with self.assertRaises(TypeError):
                is_narcissistic_number(value)


class TestIsNarcissisticAlias(unittest.TestCase):
    def test_alias_matches_implementation(self):
        self.assertIs(is_narcissistic, is_narcissistic_number)
        for value in (0, 1, 153, 370, 10, 100):
            self.assertEqual(is_narcissistic(value), is_narcissistic_number(value))

    def test_type_error(self):
        for value in (1.5, "153", None, True, [153]):
            with self.assertRaises(TypeError):
                is_narcissistic(value)


class TestIsUntouchableNumber(unittest.TestCase):
    def test_known_untouchable_numbers(self):
        for value in (2, 5, 52, 88, 120):
            self.assertTrue(is_untouchable_number(value), value)

    def test_non_untouchable_numbers(self):
        for value in (1, 3, 4, 6, 28):
            self.assertFalse(is_untouchable_number(value), value)

    def test_zero_and_negative(self):
        self.assertFalse(is_untouchable_number(0))
        for value in (-1, -2):
            self.assertFalse(is_untouchable_number(value))

    def test_type_error(self):
        for value in (1.5, "2", None, True, [2]):
            with self.assertRaises(TypeError):
                is_untouchable_number(value)


if __name__ == "__main__":
    unittest.main()

