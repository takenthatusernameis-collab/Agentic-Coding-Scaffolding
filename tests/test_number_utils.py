"""Tests for number_utils module."""

import unittest

from number_utils import (
    clamp,
    format_number,
    is_integer,
    is_negative,
    is_non_negative,
    is_non_positive,
    is_positive,
    is_zero,
    lerp,
    percentage,
    round_to,
)


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


class TestLerp(unittest.TestCase):
    def test_endpoints(self) -> None:
        self.assertEqual(lerp(0, 10, 0), 0)
        self.assertEqual(lerp(0, 10, 1), 10)

    def test_midpoint(self) -> None:
        self.assertEqual(lerp(0, 10, 0.5), 5.0)

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            lerp("a", 10, 0.5)  # type: ignore[arg-type]


class TestSign:
    def test_negative(self):
        from number_utils import sign
        assert sign(-5) == -1

    def test_zero(self):
        from number_utils import sign
        assert sign(0) == 0

    def test_positive(self):
        from number_utils import sign
        assert sign(3.5) == 1

    def test_non_number_raises(self):
        import pytest

        from number_utils import sign

        with pytest.raises(TypeError):
            sign("x")


class TestIsNegative(unittest.TestCase):
    def test_negative(self) -> None:
        self.assertTrue(is_negative(-5))
        self.assertTrue(is_negative(-0.5))

    def test_zero(self) -> None:
        self.assertFalse(is_negative(0))
        self.assertFalse(is_negative(0.0))

    def test_positive(self) -> None:
        self.assertFalse(is_negative(5))
        self.assertFalse(is_negative(0.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_negative("x")  # type: ignore[arg-type]


class TestIsPositive(unittest.TestCase):
    def test_positive(self) -> None:
        self.assertTrue(is_positive(5))
        self.assertTrue(is_positive(0.5))

    def test_zero(self) -> None:
        self.assertFalse(is_positive(0))
        self.assertFalse(is_positive(0.0))

    def test_negative(self) -> None:
        self.assertFalse(is_positive(-5))
        self.assertFalse(is_positive(-0.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_positive("x")  # type: ignore[arg-type]


class TestIsZero(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertTrue(is_zero(0))
        self.assertTrue(is_zero(0.0))

    def test_non_zero(self) -> None:
        self.assertFalse(is_zero(5))
        self.assertFalse(is_zero(-5))
        self.assertFalse(is_zero(0.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_zero("x")  # type: ignore[arg-type]


class TestIsNonNegative(unittest.TestCase):
    def test_non_negative(self) -> None:
        self.assertTrue(is_non_negative(0))
        self.assertTrue(is_non_negative(0.0))
        self.assertTrue(is_non_negative(5))
        self.assertTrue(is_non_negative(0.5))

    def test_negative(self) -> None:
        self.assertFalse(is_non_negative(-5))
        self.assertFalse(is_non_negative(-0.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_non_negative("x")  # type: ignore[arg-type]


class TestIsNonPositive(unittest.TestCase):
    def test_non_positive(self) -> None:
        self.assertTrue(is_non_positive(0))
        self.assertTrue(is_non_positive(0.0))
        self.assertTrue(is_non_positive(-5))
        self.assertTrue(is_non_positive(-0.5))

    def test_positive(self) -> None:
        self.assertFalse(is_non_positive(5))
        self.assertFalse(is_non_positive(0.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_non_positive("x")  # type: ignore[arg-type]
