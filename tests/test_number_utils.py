"""Tests for number_utils module."""

import unittest

from number_utils import clamp, format_number, is_integer, percentage, round_to


class TestClamp(unittest.TestCase):
    def test_within_range(self) -> None:
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_below(self) -> None:
        self.assertEqual(clamp(-3, 0, 10), 0)

    def test_above(self) -> None:
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_invalid_range(self) -> None:
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


class TestRoundTo(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(round_to(3.14159), 3)

    def test_places(self) -> None:
        self.assertEqual(round_to(3.14159, 2), 3.14)


class TestIsInteger(unittest.TestCase):
    def test_int(self) -> None:
        self.assertTrue(is_integer(5))

    def test_float_integral(self) -> None:
        self.assertTrue(is_integer(5.0))

    def test_float_non_integral(self) -> None:
        self.assertFalse(is_integer(5.5))


class TestFormatNumber(unittest.TestCase):
    def test_format(self) -> None:
        self.assertEqual(format_number(1234.5, 2), "1,234.50")


class TestPercentage(unittest.TestCase):
    def test_normal(self) -> None:
        self.assertEqual(percentage(1, 4), "25.0%")

    def test_zero_total(self) -> None:
        self.assertEqual(percentage(5, 0), "0.0%")
