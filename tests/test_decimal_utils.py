"""Tests for decimal_utils."""

import unittest

from decimal_utils import (
    abs_value,
    add,
    compare,
    divide,
    is_negative,
    is_positive,
    is_zero,
    multiply,
    negate,
    power,
    quantize,
    subtract,
    to_decimal,
)


class TestToDecimal(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(to_decimal("10.5"), to_decimal("10.5"))
        self.assertEqual(str(to_decimal("10.5")), "10.5")

    def test_from_int(self):
        self.assertEqual(to_decimal(3), to_decimal("3"))

    def test_from_float(self):
        self.assertEqual(to_decimal(1.5), to_decimal("1.5"))

    def test_from_decimal_passthrough(self):
        from decimal import Decimal

        value = Decimal("2.75")
        self.assertIs(to_decimal(value), value)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            to_decimal(None)
        with self.assertRaises(TypeError):
            to_decimal([1, 2])
        with self.assertRaises(TypeError):
            to_decimal(True)

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            to_decimal("not-a-number")
        with self.assertRaises(ValueError):
            to_decimal("")


class TestAddSubtractMultiply(unittest.TestCase):
    def test_add_avoids_float_error(self):
        self.assertEqual(add("0.1", "0.2"), to_decimal("0.3"))

    def test_subtract(self):
        self.assertEqual(subtract("5", "2"), to_decimal("3"))

    def test_multiply(self):
        self.assertEqual(multiply("2", "3"), to_decimal("6"))


class TestDivide(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide("10", "2"), to_decimal("5"))

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide("5", "0")


class TestPower(unittest.TestCase):
    def test_power(self):
        self.assertEqual(power("2", "3"), to_decimal("8"))


class TestQuantize(unittest.TestCase):
    def test_quantize(self):
        self.assertEqual(quantize("3.14159", 2), to_decimal("3.14"))
        self.assertEqual(quantize("3.145", 2), to_decimal("3.15"))

    def test_default_places(self):
        self.assertEqual(quantize("3.14159"), to_decimal("3.14"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            quantize("1.5", "2")
        with self.assertRaises(TypeError):
            quantize("1.5", True)

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            quantize("1.5", -1)


class TestCompare(unittest.TestCase):
    def test_compare(self):
        self.assertEqual(compare("1", "2"), -1)
        self.assertEqual(compare("2", "2"), 0)
        self.assertEqual(compare("3", "2"), 1)


class TestAbsNegate(unittest.TestCase):
    def test_abs_value(self):
        self.assertEqual(abs_value("-5"), to_decimal("5"))
        self.assertEqual(abs_value("5"), to_decimal("5"))

    def test_negate(self):
        self.assertEqual(negate("5"), to_decimal("-5"))


class TestPredicates(unittest.TestCase):
    def test_is_positive(self):
        self.assertTrue(is_positive("1"))
        self.assertFalse(is_positive("0"))
        self.assertFalse(is_positive("-1"))

    def test_is_negative(self):
        self.assertTrue(is_negative("-1"))
        self.assertFalse(is_negative("0"))
        self.assertFalse(is_negative("1"))

    def test_is_zero(self):
        self.assertTrue(is_zero("0"))
        self.assertFalse(is_zero("1"))


if __name__ == "__main__":
    unittest.main()
