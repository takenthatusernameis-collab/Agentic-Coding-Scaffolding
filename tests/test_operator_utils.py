"""Tests for operator_utils."""

import unittest

from operator_utils import (
    add,
    between,
    clamp,
    divide,
    identity,
    modulo,
    multiply,
    negate,
    power,
    subtract,
)


class TestOperatorUtils(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(identity(5), 5)
        self.assertEqual(identity("x"), "x")

    def test_negate(self):
        self.assertEqual(negate(3), -3)

    def test_negate_rejects_nan(self):
        with self.assertRaises(ValueError):
            negate(float("nan"))
        with self.assertRaises(ValueError):
            negate(float("inf"))
        with self.assertRaises(ValueError):
            negate(float("-inf"))

    def test_negate_rejects_non_number(self):
        with self.assertRaises(TypeError):
            negate("3")
        with self.assertRaises(TypeError):
            negate(True)

    def test_add_subtract_multiply(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(5, 2), 3)
        self.assertEqual(multiply(2, 3), 6)

    def test_add_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                add(bad, 1)
            with self.assertRaises(ValueError):
                add(1, bad)

    def test_subtract_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                subtract(bad, 1)
            with self.assertRaises(ValueError):
                subtract(1, bad)

    def test_multiply_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                multiply(bad, 1)
            with self.assertRaises(ValueError):
                multiply(1, bad)

    def test_divide_power_modulo(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(modulo(10, 3), 1)

    def test_divide_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                divide(bad, 1)
            with self.assertRaises(ValueError):
                divide(1, bad)

    def test_power_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                power(bad, 2)
            with self.assertRaises(ValueError):
                power(2, bad)

    def test_modulo_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                modulo(bad, 3)
            with self.assertRaises(ValueError):
                modulo(10, bad)

    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-1, 0, 10), 0)
        self.assertEqual(clamp(11, 0, 10), 10)

    def test_clamp_rejects_non_finite(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                clamp(bad, 0, 10)
            with self.assertRaises(ValueError):
                clamp(5, bad, 10)
            with self.assertRaises(ValueError):
                clamp(5, 0, bad)

    def test_clamp_rejects_inverted_bounds_and_non_number(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)
        with self.assertRaises(TypeError):
            clamp("5", 0, 10)
        with self.assertRaises(TypeError):
            clamp(5, "0", 10)
        with self.assertRaises(TypeError):
            clamp(5, 0, True)

    def test_between(self):
        self.assertTrue(between(5, 0, 10))
        self.assertTrue(between(0, 0, 10))
        self.assertFalse(between(0, 0, 10, inclusive=False))

    def test_between_rejects_nan_inf(self):
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                between(bad, 0, 10)
            with self.assertRaises(ValueError):
                between(5, bad, 10)
            with self.assertRaises(ValueError):
                between(5, 0, bad)

    def test_between_rejects_inverted_bounds(self):
        with self.assertRaises(ValueError):
            between(5, 10, 0)

    def test_between_rejects_non_number(self):
        with self.assertRaises(TypeError):
            between("5", 0, 10)
        with self.assertRaises(TypeError):
            between(5, "0", 10)
        with self.assertRaises(TypeError):
            between(5, 0, True)


if __name__ == "__main__":
    unittest.main()
