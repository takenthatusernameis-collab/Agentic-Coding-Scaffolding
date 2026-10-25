"""Tests for prime_utils module."""

import unittest

from prime_utils import is_coprime, is_prime, next_prime, nth_prime, prev_prime, prime_factors, primes_up_to


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


if __name__ == "__main__":
    unittest.main()
