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

    def test_add_subtract_multiply(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(5, 2), 3)
        self.assertEqual(multiply(2, 3), 6)

    def test_divide_power_modulo(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(modulo(10, 3), 1)

    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-1, 0, 10), 0)
        self.assertEqual(clamp(11, 0, 10), 10)

    def test_between(self):
        self.assertTrue(between(5, 0, 10))
        self.assertTrue(between(0, 0, 10))
        self.assertFalse(between(0, 0, 10, inclusive=False))


if __name__ == "__main__":
    unittest.main()
