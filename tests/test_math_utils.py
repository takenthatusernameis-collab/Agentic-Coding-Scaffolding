"""Tests for math_utils module."""

import unittest

from math_utils import clamp, factorial, fibonacci, gcd, is_even, is_prime, lcm


class TestFactorial(unittest.TestCase):
    def test_factorial_zero(self) -> None:
        self.assertEqual(factorial(0), 1)

    def test_factorial_positive(self) -> None:
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)

    def test_factorial_large(self) -> None:
        self.assertEqual(factorial(10), 3628800)
        self.assertEqual(factorial(20), 2432902008176640000)

    def test_factorial_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_factorial_non_int_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            factorial(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            factorial("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            factorial(True)  # type: ignore[arg-type]


class TestFibonacci(unittest.TestCase):
    def test_fibonacci_zero(self) -> None:
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_one(self) -> None:
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_sequence(self) -> None:
        self.assertEqual(fibonacci(2), 1)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(6), 8)
        self.assertEqual(fibonacci(10), 55)

    def test_fibonacci_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_fibonacci_non_int_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            fibonacci(1.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            fibonacci("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            fibonacci(False)  # type: ignore[arg-type]


class TestGCD(unittest.TestCase):
    def test_gcd_basic(self) -> None:
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_coprime(self) -> None:
        self.assertEqual(gcd(17, 13), 1)

    def test_gcd_same(self) -> None:
        self.assertEqual(gcd(5, 5), 5)

    def test_gcd_with_zero(self) -> None:
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(5, 0), 5)
        self.assertEqual(gcd(0, 0), 0)

    def test_gcd_negative(self) -> None:
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)

    def test_gcd_non_int_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            gcd(1.5, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            gcd("48", 18)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            gcd(48, True)  # type: ignore[arg-type]


class TestLCM(unittest.TestCase):
    def test_lcm_basic(self) -> None:
        self.assertEqual(lcm(4, 6), 12)

    def test_lcm_coprime(self) -> None:
        self.assertEqual(lcm(3, 5), 15)

    def test_lcm_zero(self) -> None:
        self.assertEqual(lcm(0, 5), 0)
        self.assertEqual(lcm(5, 0), 0)
        self.assertEqual(lcm(0, 0), 0)

    def test_lcm_negative(self) -> None:
        self.assertEqual(lcm(-4, 6), 12)
        self.assertEqual(lcm(4, -6), 12)

    def test_lcm_non_int_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            lcm(1.5, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lcm("4", 6)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lcm(4, False)  # type: ignore[arg-type]


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
        with self.assertRaises(ValueError):
            is_prime(1)
        with self.assertRaises(ValueError):
            is_prime(0)
        with self.assertRaises(ValueError):
            is_prime(-7)

    def test_prime_large(self) -> None:
        self.assertTrue(is_prime(9999991))
        self.assertFalse(is_prime(9999993))

    def test_prime_non_int_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_prime(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime(True)  # type: ignore[arg-type]


class TestClamp(unittest.TestCase):
    def test_clamp_inside_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_below_range(self) -> None:
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_clamp_above_range(self) -> None:
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_clamp_at_boundaries(self) -> None:
        self.assertEqual(clamp(0, 0, 10), 0)
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_clamp_floats(self) -> None:
        self.assertAlmostEqual(clamp(2.5, 0.0, 1.0), 1.0)
        self.assertAlmostEqual(clamp(-0.5, 0.0, 1.0), 0.0)
        self.assertAlmostEqual(clamp(0.5, 0.0, 1.0), 0.5)

    def test_clamp_invalid_range(self) -> None:
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)

    def test_clamp_non_number_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            clamp("5", 0, 10)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp(5, "0", 10)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp(5, 0, "10")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp(True, 0, 10)  # type: ignore[arg-type]


class TestIsEven(unittest.TestCase):
    def test_even_ints(self) -> None:
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(-4))

    def test_odd_ints(self) -> None:
        self.assertFalse(is_even(1))
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(-3))

    def test_non_int_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_even(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even("2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
