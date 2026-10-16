"""Tests for fractions_utils."""

import unittest

from fractions_utils import (
    abs_value,
    add,
    compare,
    denominator,
    divide,
    from_float,
    is_integer,
    is_negative,
    is_positive,
    is_zero,
    multiply,
    negate,
    numerator,
    power,
    subtract,
    to_float,
    to_fraction,
)


class TestToFraction(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(to_fraction("1/3"), to_fraction("1/3"))
        self.assertEqual(str(to_fraction("1/3")), "1/3")

    def test_from_int(self):
        self.assertEqual(to_fraction(3), to_fraction("3"))

    def test_from_float(self):
        self.assertEqual(to_fraction(0.5), to_fraction("1/2"))

    def test_from_fraction_passthrough(self):
        from fractions import Fraction

        value = Fraction(2, 3)
        self.assertIs(to_fraction(value), value)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            to_fraction(None)
        with self.assertRaises(TypeError):
            to_fraction([1, 2])
        with self.assertRaises(TypeError):
            to_fraction(True)

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            to_fraction("not-a-number")
        with self.assertRaises(ValueError):
            to_fraction("")


class TestAddSubtractMultiply(unittest.TestCase):
    def test_add_exact(self):
        self.assertEqual(add("1/10", "2/10"), to_fraction("3/10"))
        self.assertEqual(add("1/3", "1/3"), to_fraction("2/3"))

    def test_subtract(self):
        self.assertEqual(subtract("5", "2"), to_fraction("3"))
        self.assertEqual(subtract("1/2", "1/4"), to_fraction("1/4"))

    def test_multiply(self):
        self.assertEqual(multiply("1/2", "2/3"), to_fraction("1/3"))
        self.assertEqual(multiply(-2, "3/4"), to_fraction("-3/2"))


class TestDivide(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide("1/2", "1/4"), to_fraction("2"))
        self.assertEqual(divide(6, "1/3"), to_fraction("18"))

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(5, 0)


class TestPower(unittest.TestCase):
    def test_power(self):
        self.assertEqual(power("1/2", 2), to_fraction("1/4"))
        self.assertEqual(power(2, 3), to_fraction("8"))
        self.assertEqual(power("2/3", -1), to_fraction("3/2"))


class TestCompare(unittest.TestCase):
    def test_compare(self):
        self.assertEqual(compare("1/2", "1/3"), 1)
        self.assertEqual(compare("1/3", "1/2"), -1)
        self.assertEqual(compare("1/2", "1/2"), 0)


class TestAbsNegate(unittest.TestCase):
    def test_abs_value(self):
        self.assertEqual(abs_value("-3/4"), to_fraction("3/4"))
        self.assertEqual(abs_value("3/4"), to_fraction("3/4"))

    def test_negate(self):
        self.assertEqual(negate("3/4"), to_fraction("-3/4"))
        self.assertEqual(negate("-3/4"), to_fraction("3/4"))


class TestPredicates(unittest.TestCase):
    def test_is_positive(self):
        self.assertTrue(is_positive("1/2"))
        self.assertFalse(is_positive("-1/2"))
        self.assertFalse(is_positive(0))

    def test_is_negative(self):
        self.assertTrue(is_negative("-1/2"))
        self.assertFalse(is_negative("1/2"))
        self.assertFalse(is_negative(0))

    def test_is_zero(self):
        self.assertTrue(is_zero(0))
        self.assertTrue(is_zero("0/5"))
        self.assertFalse(is_zero("1/2"))

    def test_is_integer(self):
        self.assertTrue(is_integer(3))
        self.assertTrue(is_integer("6/2"))
        self.assertFalse(is_integer("1/2"))


class TestNumeratorDenominator(unittest.TestCase):
    def test_numerator_denominator(self):
        self.assertEqual(numerator("6/8"), 3)
        self.assertEqual(denominator("6/8"), 4)
        self.assertEqual(numerator("-3/4"), -3)
        self.assertEqual(denominator("-3/4"), 4)


class TestFloatConversion(unittest.TestCase):
    def test_to_float(self):
        self.assertEqual(to_float("1/2"), 0.5)
        self.assertEqual(to_float("1/3"), 1 / 3)

    def test_from_float(self):
        self.assertEqual(from_float(0.5), to_fraction("1/2"))


if __name__ == "__main__":
    unittest.main()
