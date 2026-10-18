"""Tests for prime_utils module."""

import unittest

from prime_utils import next_prime, nth_prime, previous_prime, prime_factors, primes_up_to


class TestPrimeFactors(unittest.TestCase):
    def test_small_composite(self) -> None:
        self.assertEqual(prime_factors(12), [2, 2, 3])

    def test_prime_itself(self) -> None:
        self.assertEqual(prime_factors(17), [17])

    def test_power_of_two(self) -> None:
        self.assertEqual(prime_factors(16), [2, 2, 2, 2])

    def test_large(self) -> None:
        self.assertEqual(prime_factors(100), [2, 2, 5, 5])

    def test_product_matches(self) -> None:
        from math import prod

        for n in range(2, 200):
            self.assertEqual(prod(prime_factors(n)), n)

    def test_less_than_two_raises(self) -> None:
        with self.assertRaises(ValueError):
            prime_factors(1)
        with self.assertRaises(ValueError):
            prime_factors(0)
        with self.assertRaises(ValueError):
            prime_factors(-5)


class TestNthPrime(unittest.TestCase):
    def test_first(self) -> None:
        self.assertEqual(nth_prime(1), 2)

    def test_sixth(self) -> None:
        self.assertEqual(nth_prime(6), 13)

    def test_tenth(self) -> None:
        self.assertEqual(nth_prime(10), 29)

    def test_less_than_one_raises(self) -> None:
        with self.assertRaises(ValueError):
            nth_prime(0)
        with self.assertRaises(ValueError):
            nth_prime(-3)


class TestPrimesUpTo(unittest.TestCase):
    def test_below_two(self) -> None:
        self.assertEqual(primes_up_to(0), [])
        self.assertEqual(primes_up_to(1), [])

    def test_ten(self) -> None:
        self.assertEqual(primes_up_to(10), [2, 3, 5, 7])

    def test_twenty(self) -> None:
        self.assertEqual(primes_up_to(20), [2, 3, 5, 7, 11, 13, 17, 19])


class TestNextPrime(unittest.TestCase):
    def test_after_one(self) -> None:
        self.assertEqual(next_prime(1), 2)

    def test_after_seven(self) -> None:
        self.assertEqual(next_prime(7), 11)

    def test_after_prime(self) -> None:
        self.assertEqual(next_prime(13), 17)


class TestPreviousPrime(unittest.TestCase):
    def test_before_three(self) -> None:
        self.assertEqual(previous_prime(3), 2)

    def test_before_eleven(self) -> None:
        self.assertEqual(previous_prime(11), 7)

    def test_before_two_raises(self) -> None:
        with self.assertRaises(ValueError):
            previous_prime(2)
        with self.assertRaises(ValueError):
            previous_prime(1)


if __name__ == "__main__":
    unittest.main()
