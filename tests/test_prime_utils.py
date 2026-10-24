"""Tests for prime_utils module."""

import unittest

from prime_utils import is_coprime, nth_prime, prime_factors, primes_up_to


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


if __name__ == "__main__":
    unittest.main()
