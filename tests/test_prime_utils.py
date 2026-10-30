"""Tests for prime_utils module."""

import unittest

from prime_utils import (
    coprime,
    distinct_prime_factors,
    is_abundant_number,
    is_automorphic,
    is_chen_prime,
    is_circular_prime,
    is_composite,
    is_coprime,
    is_cousin_prime,
    is_deficient_number,
    is_emirp,
    is_mersenne_prime,
    is_palindromic_prime,
    is_perfect_number,
    is_perfect_square,
    is_power_of_two,
    is_prime,
    is_prime_power,
    is_pythagorean_prime,
    is_safe_prime,
    is_semiprime,
    is_sexy_prime,
    is_sophie_germain_prime,
    is_squarefree,
    is_twin_prime,
    is_wilson_prime,
    largest_prime_factor,
    next_prime,
    nth_prime,
    prev_prime,
    prime_count,
    prime_factors,
    prime_gap,
    primes_up_to,
    primorial,
    radical,
    sum_of_proper_divisors,
    total_prime_factors,
)


class TestPrimesUpTo(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(primes_up_to(10), [2, 3, 5, 7])

    def test_below_two(self):
        self.assertEqual(primes_up_to(0), [])
        self.assertEqual(primes_up_to(1), [])
        self.assertEqual(primes_up_to(-5), [])

    def test_two(self):
        self.assertEqual(primes_up_to(2), [2])

    def test_inclusive(self):
        self.assertEqual(primes_up_to(13), [2, 3, 5, 7, 11, 13])

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            primes_up_to(10.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            primes_up_to("10")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            primes_up_to(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            primes_up_to(True)  # type: ignore[arg-type]


class TestIsPrime(unittest.TestCase):
    def test_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(97))
        self.assertTrue(is_prime(101))

    def test_not_prime(self):
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(15))
        self.assertFalse(is_prime(100))

    def test_negative(self):
        self.assertFalse(is_prime(-1))
        self.assertFalse(is_prime(-7))
        self.assertFalse(is_prime(-2))

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_prime(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime("2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime(True)  # type: ignore[arg-type]


class TestNthPrime(unittest.TestCase):
    def test_first(self):
        self.assertEqual(nth_prime(1), 2)

    def test_tenth(self):
        self.assertEqual(nth_prime(10), 29)

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            nth_prime(0)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            nth_prime(-3)

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            nth_prime(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nth_prime("1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nth_prime(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nth_prime(True)  # type: ignore[arg-type]


class TestPrimeFactors(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(prime_factors(12), [2, 2, 3])

    def test_prime(self):
        self.assertEqual(prime_factors(17), [17])

    def test_power_of_two(self):
        self.assertEqual(prime_factors(16), [2, 2, 2, 2])

    def test_large(self):
        self.assertEqual(prime_factors(100), [2, 2, 5, 5])

    def test_below_two_raises(self):
        with self.assertRaises(ValueError):
            prime_factors(1)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            prime_factors(-7)

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            prime_factors(10.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prime_factors("10")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prime_factors(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prime_factors(True)  # type: ignore[arg-type]


class TestIsCoprime(unittest.TestCase):
    def test_coprime(self):
        self.assertTrue(is_coprime(8, 9))

    def test_not_coprime(self):
        self.assertFalse(is_coprime(8, 12))

    def test_same_value(self):
        self.assertTrue(is_coprime(1, 1))
        self.assertFalse(is_coprime(5, 5))

    def test_negative(self):
        self.assertTrue(is_coprime(-8, 9))

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_coprime(8.5, 9)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(8, "9")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(None, 9)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(8, True)  # type: ignore[arg-type]


class TestIsCircularPrime(unittest.TestCase):
    def test_true_cases(self):
        for n in [2, 3, 5, 7, 11, 13, 17, 37, 79, 113, 197]:
            self.assertTrue(is_circular_prime(n))

    def test_false_cases(self):
        for n in [23, 29, 41, 101, 19, 0, 1, 4]:
            self.assertFalse(is_circular_prime(n))

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_circular_prime(13.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_circular_prime("13")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_circular_prime(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_circular_prime(True)  # type: ignore[arg-type]


class TestNextPrime(unittest.TestCase):
    def test_exact_prime(self):
        self.assertEqual(next_prime(7), 7)

    def test_between(self):
        self.assertEqual(next_prime(8), 11)
        self.assertEqual(next_prime(10), 11)

    def test_small(self):
        self.assertEqual(next_prime(0), 2)
        self.assertEqual(next_prime(1), 2)
        self.assertEqual(next_prime(2), 2)

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            next_prime(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            next_prime(True)  # type: ignore[arg-type]


class TestPrevPrime(unittest.TestCase):
    def test_exact_prime(self):
        self.assertEqual(prev_prime(7), 7)

    def test_between(self):
        self.assertEqual(prev_prime(10), 7)
        self.assertEqual(prev_prime(8), 7)

    def test_two(self):
        self.assertEqual(prev_prime(2), 2)

    def test_below_raises(self):
        with self.assertRaises(ValueError):
            prev_prime(1)

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            prev_prime(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prev_prime(True)  # type: ignore[arg-type]


class TestIsComposite(unittest.TestCase):
    """Tests for is_composite function."""

    def test_composites(self):
        self.assertTrue(is_composite(4))
        self.assertTrue(is_composite(6))
        self.assertTrue(is_composite(8))
        self.assertTrue(is_composite(9))
        self.assertTrue(is_composite(10))
        self.assertTrue(is_composite(15))
        self.assertTrue(is_composite(121))

    def test_primes(self):
        self.assertFalse(is_composite(2))
        self.assertFalse(is_composite(3))
        self.assertFalse(is_composite(5))
        self.assertFalse(is_composite(101))

    def test_neither(self):
        self.assertFalse(is_composite(0))
        self.assertFalse(is_composite(1))
        self.assertFalse(is_composite(-1))
        self.assertFalse(is_composite(-4))
        self.assertFalse(is_composite(-9))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_composite(4.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_composite("9")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_composite(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_composite(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_composite(False)  # type: ignore[arg-type]


class TestIsPerfectSquare(unittest.TestCase):
    def test_zero(self):
        self.assertTrue(is_perfect_square(0))

    def test_small_squares(self):
        self.assertTrue(is_perfect_square(1))
        self.assertTrue(is_perfect_square(4))
        self.assertTrue(is_perfect_square(9))
        self.assertTrue(is_perfect_square(16))
        self.assertTrue(is_perfect_square(25))
        self.assertTrue(is_perfect_square(100))

    def test_large_square(self):
        self.assertTrue(is_perfect_square(10000))
        self.assertTrue(is_perfect_square(1000000))

    def test_non_square(self):
        self.assertFalse(is_perfect_square(2))
        self.assertFalse(is_perfect_square(3))
        self.assertFalse(is_perfect_square(5))
        self.assertFalse(is_perfect_square(8))
        self.assertFalse(is_perfect_square(15))

    def test_negative(self):
        self.assertFalse(is_perfect_square(-1))
        self.assertFalse(is_perfect_square(-4))
        self.assertFalse(is_perfect_square(-100))

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_perfect_square(2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_perfect_square("4")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_perfect_square(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_perfect_square(True)  # type: ignore[arg-type]


class TestIsPowerOfTwo(unittest.TestCase):
    def test_powers_of_two(self):
        self.assertTrue(is_power_of_two(1))  # 2^0
        self.assertTrue(is_power_of_two(2))  # 2^1
        self.assertTrue(is_power_of_two(4))  # 2^2
        self.assertTrue(is_power_of_two(8))  # 2^3
        self.assertTrue(is_power_of_two(16))  # 2^4
        self.assertTrue(is_power_of_two(32))  # 2^5
        self.assertTrue(is_power_of_two(64))  # 2^6
        self.assertTrue(is_power_of_two(1024))  # 2^10
        self.assertTrue(is_power_of_two(1 << 20))

    def test_not_power_of_two(self):
        self.assertFalse(is_power_of_two(0))
        self.assertFalse(is_power_of_two(3))
        self.assertFalse(is_power_of_two(5))
        self.assertFalse(is_power_of_two(6))
        self.assertFalse(is_power_of_two(12))
        self.assertFalse(is_power_of_two(15))
        self.assertFalse(is_power_of_two(100))

    def test_negative(self):
        self.assertFalse(is_power_of_two(-1))
        self.assertFalse(is_power_of_two(-2))
        self.assertFalse(is_power_of_two(-8))

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_power_of_two(2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_power_of_two("4")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_power_of_two(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_power_of_two(True)  # type: ignore[arg-type]


class TestIsSemiprime(unittest.TestCase):
    def test_semiprimes(self):
        self.assertTrue(is_semiprime(4))
        self.assertTrue(is_semiprime(6))
        self.assertTrue(is_semiprime(9))
        self.assertTrue(is_semiprime(10))
        self.assertTrue(is_semiprime(15))

    def test_primes_not_semiprime(self):
        self.assertFalse(is_semiprime(2))
        self.assertFalse(is_semiprime(3))
        self.assertFalse(is_semiprime(5))
        self.assertFalse(is_semiprime(101))

    def test_other_not_semiprime(self):
        self.assertFalse(is_semiprime(0))
        self.assertFalse(is_semiprime(1))
        self.assertFalse(is_semiprime(2))
        self.assertFalse(is_semiprime(3))
        self.assertFalse(is_semiprime(16))  # 2^4, four factors
        self.assertFalse(is_semiprime(-6))

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_semiprime(6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_semiprime("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_semiprime(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_semiprime(True)


class TestSquarefree(unittest.TestCase):
    def test_squarefree_numbers(self):
        self.assertTrue(is_squarefree(1))
        self.assertTrue(is_squarefree(2))
        self.assertTrue(is_squarefree(3))
        self.assertTrue(is_squarefree(6))
        self.assertTrue(is_squarefree(10))
        self.assertTrue(is_squarefree(30))

    def test_not_squarefree(self):
        self.assertFalse(is_squarefree(4))
        self.assertFalse(is_squarefree(8))
        self.assertFalse(is_squarefree(9))
        self.assertFalse(is_squarefree(12))
        self.assertFalse(is_squarefree(16))
        self.assertFalse(is_squarefree(0))
        self.assertFalse(is_squarefree(18))

    def test_negative(self):
        self.assertTrue(is_squarefree(-6))
        self.assertFalse(is_squarefree(-8))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_squarefree(6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_squarefree("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_squarefree(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_squarefree(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestIsPrimePower(unittest.TestCase):
    def test_primes_are_prime_powers(self):
        self.assertTrue(is_prime_power(2))
        self.assertTrue(is_prime_power(3))
        self.assertTrue(is_prime_power(5))
        self.assertTrue(is_prime_power(101))

    def test_prime_powers(self):
        self.assertTrue(is_prime_power(4))  # 2^2
        self.assertTrue(is_prime_power(8))  # 2^3
        self.assertTrue(is_prime_power(9))  # 3^2
        self.assertTrue(is_prime_power(16))  # 2^4
        self.assertTrue(is_prime_power(25))  # 5^2
        self.assertTrue(is_prime_power(27))  # 3^3
        self.assertTrue(is_prime_power(2**6))  # 64

    def test_non_prime_powers(self):
        self.assertFalse(is_prime_power(1))
        self.assertFalse(is_prime_power(6))  # 2*3
        self.assertFalse(is_prime_power(10))
        self.assertFalse(is_prime_power(12))
        self.assertFalse(is_prime_power(18))
        self.assertFalse(is_prime_power(36))  # 6^2 but base not prime

    def test_negative_numbers(self):
        self.assertFalse(is_prime_power(-4))
        self.assertFalse(is_prime_power(-2))

    def test_zero(self):
        self.assertFalse(is_prime_power(0))

    def test_non_int_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_prime_power(2.0)
        with self.assertRaises(TypeError):
            is_prime_power("4")
        with self.assertRaises(TypeError):
            is_prime_power(None)


class TestIsSophieGermainPrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [2, 3, 5, 11, 23, 29, 41, 53, 83, 89]:
            self.assertTrue(is_sophie_germain_prime(p))

    def test_false_cases(self):
        for n in [7, 13, 17, 19, 0, 1, 4, 6]:
            self.assertFalse(is_sophie_germain_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_sophie_germain_prime(2.0)


class TestIsEmirp(unittest.TestCase):
    def test_true_cases(self):
        for p in [13, 17, 31, 37, 71, 73, 79, 97]:
            self.assertTrue(is_emirp(p))

    def test_false_cases(self):
        for n in [2, 3, 5, 7, 11, 101, 0, 1, 4, 22]:
            self.assertFalse(is_emirp(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_emirp(13.0)


class TestIsTwinPrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [3, 5, 7, 11, 17, 29, 41]:
            self.assertTrue(is_twin_prime(p))

    def test_false_cases(self):
        for n in [2, 23, 0, 1, 4, 8]:
            self.assertFalse(is_twin_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_twin_prime(3.0)


class TestIsPalindromicPrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [2, 3, 5, 7, 11, 101, 131, 151, 181, 191]:
            self.assertTrue(is_palindromic_prime(p))

    def test_false_cases(self):
        for n in [13, 17, 103, 0, 1, 4, 22]:
            self.assertFalse(is_palindromic_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_palindromic_prime(11.0)


class TestIsMersennePrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [3, 7, 31, 127]:
            self.assertTrue(is_mersenne_prime(p))

    def test_false_cases(self):
        for n in [1, 5, 23, 31 * 2, 0, 2, 127 * 3]:
            self.assertFalse(is_mersenne_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_mersenne_prime(3.0)


class TestIsSafePrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [5, 7, 11, 23, 47, 59, 83, 107]:
            self.assertTrue(is_safe_prime(p))

    def test_false_cases(self):
        for n in [2, 3, 13, 17, 0, 1, 4, 6]:
            self.assertFalse(is_safe_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_safe_prime(5.0)


class TestIsChenPrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]:
            self.assertTrue(is_chen_prime(p))

    def test_false_cases(self):
        for n in [43, 4, 6, 0, 1, -3]:
            self.assertFalse(is_chen_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_chen_prime(5.0)
        with self.assertRaises(TypeError):
            is_chen_prime("5")
        with self.assertRaises(TypeError):
            is_chen_prime(True)


class TestSumOfProperDivisors(unittest.TestCase):
    def test_basic_cases(self):
        self.assertEqual(sum_of_proper_divisors(1), 0)
        self.assertEqual(sum_of_proper_divisors(6), 1 + 2 + 3)
        self.assertEqual(sum_of_proper_divisors(28), 1 + 2 + 4 + 7 + 14)
        self.assertEqual(sum_of_proper_divisors(12), 1 + 2 + 3 + 4 + 6)
        self.assertEqual(sum_of_proper_divisors(0), 0)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            sum_of_proper_divisors(6.0)
        with self.assertRaises(TypeError):
            sum_of_proper_divisors(None)


class TestAliquotSum(unittest.TestCase):
    def test_alias(self):
        from prime_utils import aliquot_sum

        self.assertEqual(aliquot_sum(6), sum_of_proper_divisors(6))


class TestIsPerfectNumber(unittest.TestCase):
    def test_true_cases(self):
        for n in [6, 28, 496]:
            self.assertTrue(is_perfect_number(n))

    def test_false_cases(self):
        for n in [1, 2, 4, 12, 0, -6]:
            self.assertFalse(is_perfect_number(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_perfect_number(6.0)


class TestIsAbundantNumber(unittest.TestCase):
    def test_true_cases(self):
        for n in [12, 18, 20, 24]:
            self.assertTrue(is_abundant_number(n))

    def test_false_cases(self):
        for n in [1, 2, 6, 28, 0]:
            self.assertFalse(is_abundant_number(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_abundant_number(12.0)


class TestIsDeficientNumber(unittest.TestCase):
    def test_true_cases(self):
        for n in [1, 2, 3, 4, 5, 7, 8, 9, 10]:
            self.assertTrue(is_deficient_number(n))

    def test_false_cases(self):
        for n in [0, 12, 18, 20, 24]:
            self.assertFalse(is_deficient_number(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_deficient_number(2.0)


class TestIsCousinPrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [3, 7, 13, 19, 37, 43]:
            self.assertTrue(is_cousin_prime(p))

    def test_false_cases(self):
        for n in [2, 0, 1, 4, 8]:
            self.assertFalse(is_cousin_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_cousin_prime(3.0)


class TestIsSexyPrime(unittest.TestCase):
    def test_true_cases(self):
        for p in [5, 7, 11, 13, 17, 23, 31, 37]:
            self.assertTrue(is_sexy_prime(p))

    def test_false_cases(self):
        for n in [2, 3, 0, 1, 4, 127, 139, 149]:
            self.assertFalse(is_sexy_prime(n))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_sexy_prime(5.0)


class TestPrimeUtilsBoundary(unittest.TestCase):
    def test_is_prime_boundaries(self):
        self.assertFalse(is_prime(-100))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(1))
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(999983))

    def test_prime_factors_one_raises(self):
        with self.assertRaises(ValueError):
            prime_factors(1)
        with self.assertRaises(ValueError):
            prime_factors(0)
        with self.assertRaises(ValueError):
            prime_factors(-5)

    def test_nth_prime_large(self):
        self.assertEqual(nth_prime(100), 541)

    def test_next_prev_prime_boundaries(self):
        self.assertEqual(next_prime(-5), 2)
        self.assertEqual(next_prime(0), 2)
        self.assertEqual(next_prime(1), 2)
        with self.assertRaises(ValueError):
            prev_prime(1)
        self.assertEqual(prev_prime(2), 2)

    def test_sum_proper_divisors_negative(self):
        self.assertIsInstance(sum_of_proper_divisors(-6), int)

    def test_is_prime_power_large(self):
        self.assertTrue(is_prime_power(2**20))
        self.assertFalse(is_prime_power(2**20 + 1))

    def test_prime_count_large(self):
        self.assertEqual(prime_count(1000), 168)

    def test_type_errors_boundary(self):
        for fn in (is_prime, is_composite, primes_up_to):
            with self.assertRaises(TypeError):
                fn(None)  # type: ignore[arg-type]


class TestPrimeCount(unittest.TestCase):
    def test_below_two_returns_zero(self):
        self.assertEqual(prime_count(-100), 0)
        self.assertEqual(prime_count(0), 0)
        self.assertEqual(prime_count(1), 0)

    def test_small_values(self):
        self.assertEqual(prime_count(2), 1)
        self.assertEqual(prime_count(3), 2)
        self.assertEqual(prime_count(4), 2)
        self.assertEqual(prime_count(5), 3)
        self.assertEqual(prime_count(10), 4)

    def test_known_values(self):
        self.assertEqual(prime_count(10), 4)
        self.assertEqual(prime_count(20), 8)
        self.assertEqual(prime_count(100), 25)
        self.assertEqual(prime_count(1000), 168)

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            prime_count(10.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prime_count("10")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prime_count(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            prime_count(True)  # type: ignore[arg-type]


class TestPrimeGap(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(prime_gap(14), 3)  # 17 - 14
        self.assertEqual(prime_gap(10), 1)  # 11 - 10

    def test_prime_input(self):
        self.assertEqual(prime_gap(7), 4)  # 11 - 7
        self.assertEqual(prime_gap(2), 1)  # 3 - 2
        self.assertEqual(prime_gap(3), 2)  # 5 - 3
        self.assertEqual(prime_gap(5), 2)  # 7 - 5

    def test_large(self):
        # 89 is prime, so the gap is measured to the next prime after 89
        # (i.e. next_prime(90) - 89 = 97 - 89 = 8).
        self.assertEqual(prime_gap(89), 8)
        self.assertEqual(prime_gap(90), 7)  # 97 - 90

    def test_type_error(self):
        with self.assertRaises(TypeError):
            prime_gap(5.0)
        with self.assertRaises(TypeError):
            prime_gap("5")
        with self.assertRaises(TypeError):
            prime_gap(None)
        with self.assertRaises(TypeError):
            prime_gap(True)


class TestPrimeClassificationNegatives(unittest.TestCase):
    """Prime-classification helpers must reject negatives, not classify them."""

    def test_is_twin_prime_negative(self):
        self.assertFalse(is_twin_prime(-5))
        self.assertFalse(is_twin_prime(-3))

    def test_is_cousin_prime_negative(self):
        self.assertFalse(is_cousin_prime(-7))
        self.assertFalse(is_cousin_prime(-3))

    def test_is_sexy_prime_negative(self):
        self.assertFalse(is_sexy_prime(-11))
        self.assertFalse(is_sexy_prime(-5))

    def test_is_palindromic_prime_negative(self):
        self.assertFalse(is_palindromic_prime(-11))
        self.assertFalse(is_palindromic_prime(-101))

    def test_is_mersenne_prime_negative(self):
        self.assertFalse(is_mersenne_prime(-7))
        self.assertFalse(is_mersenne_prime(-31))

    def test_is_safe_prime_negative(self):
        self.assertFalse(is_safe_prime(-5))
        self.assertFalse(is_safe_prime(-11))

    def test_is_sophie_germain_prime_negative(self):
        self.assertFalse(is_sophie_germain_prime(-5))
        self.assertFalse(is_sophie_germain_prime(-2))

    def test_is_emirp_negative(self):
        self.assertFalse(is_emirp(-13))
        self.assertFalse(is_emirp(-17))

    def test_is_circular_prime_negative(self):
        self.assertFalse(is_circular_prime(-7))
        self.assertFalse(is_circular_prime(-197))


class TestSumOfProperDivisorsEdge(unittest.TestCase):
    def test_negative_inputs(self):
        self.assertEqual(sum_of_proper_divisors(-1), 0)
        self.assertEqual(sum_of_proper_divisors(-6), 0)
        self.assertEqual(sum_of_proper_divisors(-28), 0)

    def test_two(self):
        self.assertEqual(sum_of_proper_divisors(2), 1)

    def test_prime(self):
        self.assertEqual(sum_of_proper_divisors(13), 1)


class TestIsPrimePowerLarge(unittest.TestCase):
    def test_large_power_of_two(self):
        self.assertTrue(is_prime_power(2**31))
        self.assertTrue(is_prime_power(2**62))

    def test_large_non_power(self):
        self.assertFalse(is_prime_power(2**31 + 1))
        self.assertFalse(is_prime_power(2**62 + 1))

    def test_large_prime_power_of_odd_prime(self):
        self.assertTrue(is_prime_power(3**20))
        self.assertFalse(is_prime_power(3**20 + 1))


class TestIsSquarefreeEdge(unittest.TestCase):
    def test_negative_squarefree(self):
        self.assertTrue(is_squarefree(-1))
        self.assertTrue(is_squarefree(-2))
        self.assertTrue(is_squarefree(-30))

    def test_negative_not_squarefree(self):
        self.assertFalse(is_squarefree(-4))
        self.assertFalse(is_squarefree(-12))

    def test_zero(self):
        self.assertFalse(is_squarefree(0))


class TestIsSemiprimeEdge(unittest.TestCase):
    def test_small_non_semiprime(self):
        self.assertFalse(is_semiprime(0))
        self.assertFalse(is_semiprime(1))
        self.assertFalse(is_semiprime(2))
        self.assertFalse(is_semiprime(3))

    def test_negative(self):
        self.assertFalse(is_semiprime(-6))
        self.assertFalse(is_semiprime(-10))


class TestIsPerfectSquareEdge(unittest.TestCase):
    def test_zero_is_square(self):
        self.assertTrue(is_perfect_square(0))

    def test_negative_not_square(self):
        self.assertFalse(is_perfect_square(-1))
        self.assertFalse(is_perfect_square(-4))


class TestNextPrevPrimeEdge(unittest.TestCase):
    def test_next_prime_negative(self):
        self.assertEqual(next_prime(-5), 2)
        self.assertEqual(next_prime(-1), 2)

    def test_next_prime_even(self):
        self.assertEqual(next_prime(4), 5)
        self.assertEqual(next_prime(6), 7)

    def test_prev_prime_two(self):
        self.assertEqual(prev_prime(2), 2)

    def test_prev_prime_three(self):
        self.assertEqual(prev_prime(3), 3)

    def test_prev_prime_even(self):
        self.assertEqual(prev_prime(10), 7)
        self.assertEqual(prev_prime(8), 7)


class TestPrimesUpToEdge(unittest.TestCase):
    def test_two(self):
        self.assertEqual(primes_up_to(2), [2])

    def test_three(self):
        self.assertEqual(primes_up_to(3), [2, 3])

    def test_below_two(self):
        self.assertEqual(primes_up_to(0), [])
        self.assertEqual(primes_up_to(1), [])
        self.assertEqual(primes_up_to(-5), [])


class TestIsCoprimeEdge(unittest.TestCase):
    def test_with_zero(self):
        self.assertTrue(is_coprime(0, 1))
        self.assertFalse(is_coprime(0, 5))

    def test_negative(self):
        self.assertTrue(is_coprime(-8, 9))
        self.assertFalse(is_coprime(-6, 9))


class TestIsPerfectAbundantDeficientEdge(unittest.TestCase):
    def test_perfect_number_496(self):
        self.assertTrue(is_perfect_number(496))

    def test_abundant_number_edge(self):
        self.assertTrue(is_abundant_number(945))

    def test_deficient_primes(self):
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
            self.assertTrue(is_deficient_number(p))

    def test_negative_not_classified(self):
        self.assertFalse(is_perfect_number(-6))
        self.assertFalse(is_abundant_number(-12))


class TestIsPythagoreanPrime(unittest.TestCase):
    def test_pythagorean_primes(self):
        for p in [5, 13, 17, 41, 101]:
            self.assertTrue(is_pythagorean_prime(p))

    def test_non_pythagorean(self):
        for p in [2, 3, 7, 11, 19]:
            self.assertFalse(is_pythagorean_prime(p))

    def test_composite(self):
        self.assertFalse(is_pythagorean_prime(25))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_pythagorean_prime(5.0)


class TestCoprimeAlias(unittest.TestCase):
    def test_coprime_alias_equals_is_coprime(self):
        self.assertEqual(coprime(8, 9), is_coprime(8, 9))
        self.assertEqual(coprime(14, 15), True)
        self.assertEqual(coprime(14, 21), False)

    def test_coprime_alias_type_error(self):
        with self.assertRaises(TypeError):
            coprime(1.0, 2)


class TestRadical(unittest.TestCase):
    def test_radical_one(self):
        self.assertEqual(radical(1), 1)

    def test_radical_primes(self):
        for p in [2, 3, 5, 7, 11]:
            self.assertEqual(radical(p), p)

    def test_radical_prime_power(self):
        self.assertEqual(radical(8), 2)
        self.assertEqual(radical(16), 2)

    def test_radical_multiple_primes(self):

        self.assertEqual(radical(12), 6)
        self.assertEqual(radical(18), 6)
        self.assertEqual(radical(30), 30)

    def test_radical_with_repeats(self):
        self.assertEqual(radical(60), 30)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            radical(4.0)
        with self.assertRaises(TypeError):
            radical(True)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            radical(0)
        with self.assertRaises(ValueError):
            radical(-6)


class TestPrimorial(unittest.TestCase):
    def test_primorial_small(self):
        self.assertEqual(primorial(0), 1)
        self.assertEqual(primorial(1), 1)
        self.assertEqual(primorial(2), 2)
        self.assertEqual(primorial(3), 6)
        self.assertEqual(primorial(5), 30)
        self.assertEqual(primorial(7), 210)

    def test_primorial_composite_upper_bound(self):
        self.assertEqual(primorial(4), 6)
        self.assertEqual(primorial(10), 210)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            primorial(5.0)
        with self.assertRaises(TypeError):
            primorial(True)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            primorial(-1)
        with self.assertRaises(ValueError):
            primorial(-10)


if __name__ == "__main__":
    unittest.main()


class TestTotalPrimeFactors(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(total_prime_factors(1), 0)
        self.assertEqual(total_prime_factors(2), 1)
        self.assertEqual(total_prime_factors(12), 3)
        self.assertEqual(total_prime_factors(30), 3)

    def test_prime_power(self):
        self.assertEqual(total_prime_factors(8), 3)
        self.assertEqual(total_prime_factors(27), 3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            total_prime_factors(5.0)
        with self.assertRaises(TypeError):
            total_prime_factors(True)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            total_prime_factors(0)
        with self.assertRaises(ValueError):
            total_prime_factors(-1)


class TestDistinctPrimeFactors(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(distinct_prime_factors(1), 0)
        self.assertEqual(distinct_prime_factors(2), 1)
        self.assertEqual(distinct_prime_factors(12), 2)
        self.assertEqual(distinct_prime_factors(30), 3)

    def test_prime_power(self):
        self.assertEqual(distinct_prime_factors(8), 1)
        self.assertEqual(distinct_prime_factors(27), 1)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            distinct_prime_factors(5.0)
        with self.assertRaises(TypeError):
            distinct_prime_factors(True)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            distinct_prime_factors(0)
        with self.assertRaises(ValueError):
            distinct_prime_factors(-1)


class TestLargestPrimeFactor(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(largest_prime_factor(12), 3)
        self.assertEqual(largest_prime_factor(2), 2)
        self.assertEqual(largest_prime_factor(17), 17)
        self.assertEqual(largest_prime_factor(30), 5)

    def test_prime_power(self):
        self.assertEqual(largest_prime_factor(8), 2)
        self.assertEqual(largest_prime_factor(27), 3)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            largest_prime_factor(5.0)
        with self.assertRaises(TypeError):
            largest_prime_factor(True)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            largest_prime_factor(0)
        with self.assertRaises(ValueError):
            largest_prime_factor(-1)
        with self.assertRaises(ValueError):
            largest_prime_factor(1)


class TestIsAutomorphic(unittest.TestCase):
    def test_small_automorphic(self):
        self.assertTrue(is_automorphic(0))
        self.assertTrue(is_automorphic(1))
        self.assertTrue(is_automorphic(5))
        self.assertTrue(is_automorphic(6))

    def test_multi_digit_automorphic(self):
        self.assertTrue(is_automorphic(25))
        self.assertTrue(is_automorphic(76))
        self.assertTrue(is_automorphic(376))
        self.assertTrue(is_automorphic(625))
        self.assertTrue(is_automorphic(9376))

    def test_non_automorphic(self):
        self.assertFalse(is_automorphic(2))
        self.assertFalse(is_automorphic(7))
        self.assertFalse(is_automorphic(10))
        self.assertFalse(is_automorphic(100))
        self.assertFalse(is_automorphic(123))

    def test_negative(self):
        self.assertFalse(is_automorphic(-5))
        self.assertFalse(is_automorphic(-25))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_automorphic(5.0)
        with self.assertRaises(TypeError):
            is_automorphic("5")
        with self.assertRaises(TypeError):
            is_automorphic(True)


class TestIsWilsonPrime(unittest.TestCase):
    def test_known_wilson_primes(self):
        for p in [5, 13, 563]:
            self.assertTrue(is_wilson_prime(p), p)

    def test_non_wilson_primes(self):
        for p in [2, 3, 7, 11, 17, 19, 23, 29, 31]:
            self.assertFalse(is_wilson_prime(p), p)

    def test_composite_is_not_wilson_prime(self):
        for n in [1, 4, 6, 8, 9, 10, 12, 14, 15]:
            self.assertFalse(is_wilson_prime(n), n)

    def test_negative_is_not_wilson_prime(self):
        for n in [-5, -13, -563]:
            self.assertFalse(is_wilson_prime(n), n)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_wilson_prime(5.0)
        with self.assertRaises(TypeError):
            is_wilson_prime("5")
        with self.assertRaises(TypeError):
            is_wilson_prime(True)
        with self.assertRaises(TypeError):
            is_wilson_prime(None)


if __name__ == "__main__":
    unittest.main()
