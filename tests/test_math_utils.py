"""Tests for math_utils module."""

import unittest

from math_utils import clamp, factorial, fibonacci, gcd, is_prime, lcm


class TestFactorial(unittest.TestCase):
    def test_factorial_zero(self) -> None:
        self.assertEqual(factorial(0), 1)

    def test_factorial_positive(self) -> None:
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(1), 1)

    def test_factorial_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            factorial(-1)


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_zero(self) -> None:
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_one(self) -> None:
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_sequence(self) -> None:
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)

    def test_fibonacci_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            fibonacci(-1)


class TestGCD(unittest.TestCase):
    def test_gcd_basic(self) -> None:
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_coprime(self) -> None:
        self.assertEqual(gcd(17, 13), 1)

    def test_gcd_same(self) -> None:
        self.assertEqual(gcd(5, 5), 5)


class TestLCM(unittest.TestCase):
    def test_lcm_basic(self) -> None:
        self.assertEqual(lcm(4, 6), 12)

    def test_lcm_coprime(self) -> None:
        self.assertEqual(lcm(3, 5), 15)

    def test_lcm_zero(self) -> None:
        self.assertEqual(lcm(0, 5), 0)


class TestIsPrime(unittest.TestCase):
    def test_prime_numbers(self) -> None:
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(17))

    def test_non_prime_numbers(self) -> None:
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(9))
        self.assertFalse(is_prime(15))

    def test_prime_edge_cases(self) -> None:
        self.assertRaises(ValueError, is_prime, 1)
        self.assertRaises(ValueError, is_prime, 0)
        self.assertRaises(ValueError, is_prime, -7)


class TestClamp(unittest.TestCase):
    def test_clamp_inside_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_below_range(self) -> None:
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_clamp_above_range(self) -> None:
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_clamp_invalid_range(self) -> None:
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


if __name__ == "__main__":
    unittest.main()
