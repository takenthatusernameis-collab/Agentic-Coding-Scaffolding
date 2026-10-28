"""Tests for number_utils module."""

import unittest

from number_utils import (
    clamp,
    format_number,
    is_between,
    is_even,
    is_finite,
    is_infinite,
    is_integer,
    is_nan,
    is_negative,
    is_non_negative,
    is_non_positive,
    is_odd,
    is_perfect_cube,
    is_perfect_square,
    is_positive,
    is_power_of_two,
    is_zero,
    lerp,
    map_range,
    percentage,
    remap,
    round_to,
    safe_divide,
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


class TestIsBetween(unittest.TestCase):
    def test_inclusive_default(self) -> None:
        self.assertTrue(is_between(5, 0, 10))
        self.assertTrue(is_between(0, 0, 10))
        self.assertTrue(is_between(10, 0, 10))
        self.assertFalse(is_between(-1, 0, 10))
        self.assertFalse(is_between(11, 0, 10))

    def test_exclusive(self) -> None:
        self.assertTrue(is_between(5, 0, 10, inclusive=False))
        self.assertFalse(is_between(0, 0, 10, inclusive=False))
        self.assertFalse(is_between(10, 0, 10, inclusive=False))

    def test_floats(self) -> None:
        self.assertTrue(is_between(2.5, 1.0, 3.0))
        self.assertTrue(is_between(1.0, 1.0, 3.0))

    def test_invalid_bounds(self) -> None:
        with self.assertRaises(ValueError):
            is_between(5, 10, 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_between("x", 0, 10)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_between(5, "x", 10)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_between(5, 0, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_between(5, 0, 10, inclusive="yes")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestIsPalindromicNumber(unittest.TestCase):
    def test_palindromes(self) -> None:
        from number_utils import is_palindromic_number

        for value in (0, 1, 11, 121, 1221, 1331, 12321):
            self.assertTrue(is_palindromic_number(value))
        for value in (10, 12, 102, 1210, 123):
            self.assertFalse(is_palindromic_number(value))

    def test_float_not_integer(self) -> None:
        from number_utils import is_palindromic_number

        self.assertFalse(is_palindromic_number(1.1))
        self.assertFalse(is_palindromic_number(11.0))

    def test_negative(self) -> None:
        from number_utils import is_palindromic_number

        self.assertFalse(is_palindromic_number(-121))

    def test_rejects_bool(self) -> None:
        from number_utils import is_palindromic_number

        with self.assertRaises(TypeError):
            is_palindromic_number(True)
        with self.assertRaises(TypeError):
            is_palindromic_number(False)

    def test_rejects_non_number(self) -> None:
        from number_utils import is_palindromic_number

        with self.assertRaises(TypeError):
            is_palindromic_number("121")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_palindromic_number(None)  # type: ignore[arg-type]


class TestIsEven(unittest.TestCase):
    def test_even_ints(self) -> None:
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(-4))

    def test_even_float(self) -> None:
        self.assertTrue(is_even(2.0))

    def test_odd(self) -> None:
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(-3))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_even("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even(True)  # type: ignore[arg-type]


class TestIsOdd(unittest.TestCase):
    def test_odd_ints(self) -> None:
        self.assertTrue(is_odd(1))
        self.assertTrue(is_odd(3))
        self.assertTrue(is_odd(-5))

    def test_odd_float(self) -> None:
        self.assertTrue(is_odd(3.0))

    def test_even(self) -> None:
        self.assertFalse(is_odd(2))
        self.assertFalse(is_odd(-4))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_odd("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(False)  # type: ignore[arg-type]


class TestIsFinite(unittest.TestCase):
    def test_finite_values(self) -> None:
        self.assertTrue(is_finite(0))
        self.assertTrue(is_finite(42))
        self.assertTrue(is_finite(3.14))

    def test_infinity(self) -> None:
        self.assertFalse(is_finite(float("inf")))
        self.assertFalse(is_finite(float("-inf")))

    def test_nan(self) -> None:
        self.assertFalse(is_finite(float("nan")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_finite("x")  # type: ignore[arg-type]


class TestIsInfinite(unittest.TestCase):
    def test_infinity(self) -> None:
        self.assertTrue(is_infinite(float("inf")))
        self.assertTrue(is_infinite(float("-inf")))

    def test_finite(self) -> None:
        self.assertFalse(is_infinite(0))
        self.assertFalse(is_infinite(3.14))

    def test_nan(self) -> None:
        self.assertFalse(is_infinite(float("nan")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_infinite(None)  # type: ignore[arg-type]


class TestIsNan(unittest.TestCase):
    def test_nan(self) -> None:
        self.assertTrue(is_nan(float("nan")))

    def test_finite(self) -> None:
        self.assertFalse(is_nan(0))
        self.assertFalse(is_nan(float("inf")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_nan("nan")  # type: ignore[arg-type]


class TestSafeDivide(unittest.TestCase):
    def test_normal(self) -> None:
        self.assertEqual(safe_divide(10, 2), 5.0)

    def test_zero_denominator(self) -> None:
        self.assertEqual(safe_divide(10, 0), 0.0)

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            safe_divide("a", 2)  # type: ignore[arg-type]


class TestIsPerfectCube(unittest.TestCase):
    def test_perfect_cubes(self) -> None:
        for n in (-27, -8, -1, 0, 1, 8, 27, 64, 125):
            self.assertTrue(is_perfect_cube(n))

    def test_non_cubes(self) -> None:
        for n in (2, 3, 4, 5, 9, 10, 26, 28):
            self.assertFalse(is_perfect_cube(n))

    def test_non_integer(self) -> None:
        self.assertFalse(is_perfect_cube(2.0))
        self.assertFalse(is_perfect_cube(8.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_perfect_cube("x")  # type: ignore[arg-type]


class TestIsPerfectSquare(unittest.TestCase):
    def test_perfect_squares(self) -> None:
        for n in (0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100):
            self.assertTrue(is_perfect_square(n))

    def test_negative_numbers(self) -> None:
        for n in (-1, -4, -9, -16):
            self.assertFalse(is_perfect_square(n))

    def test_non_squares(self) -> None:
        for n in (2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15):
            self.assertFalse(is_perfect_square(n))

    def test_non_integer(self) -> None:
        self.assertFalse(is_perfect_square(2.0))
        self.assertFalse(is_perfect_square(4.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_perfect_square("x")  # type: ignore[arg-type]


class TestIsPowerOfTwo(unittest.TestCase):
    def test_powers(self) -> None:
        for n in (1, 2, 4, 8, 16, 32, 64, 128, 256, 1024):
            self.assertTrue(is_power_of_two(n))

    def test_non_powers(self) -> None:
        for n in (0, 3, 5, 6, 7, 9, 10, 11, 12, 15, 17, -1, -2, -4):
            self.assertFalse(is_power_of_two(n))

    def test_non_integer(self) -> None:
        self.assertFalse(is_power_of_two(2.5))
        self.assertFalse(is_power_of_two(4.5))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_power_of_two("x")  # type: ignore[arg-type]


class TestMapRange(unittest.TestCase):
    def test_basic_mapping(self) -> None:
        self.assertEqual(map_range(0, 0, 10, 0, 100), 0)
        self.assertEqual(map_range(5, 0, 10, 0, 100), 50)
        self.assertEqual(map_range(10, 0, 10, 0, 100), 100)

    def test_different_ranges(self) -> None:
        self.assertAlmostEqual(map_range(50, 0, 100, 0, 1), 0.5)
        self.assertAlmostEqual(map_range(25, 0, 100, -1, 1), -0.5)

    def test_inverted_target_range(self) -> None:
        self.assertEqual(map_range(0, 0, 10, 100, 0), 100)
        self.assertEqual(map_range(10, 0, 10, 100, 0), 0)
        self.assertEqual(map_range(5, 0, 10, 100, 0), 50)

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            map_range("x", 0, 10, 0, 100)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            map_range(5, "x", 10, 0, 100)  # type: ignore[arg-type]

    def test_zero_source_span(self) -> None:
        with self.assertRaises(ValueError):
            map_range(5, 10, 10, 0, 100)

    def test_remap_alias(self) -> None:
        self.assertEqual(remap(5, 0, 10, 0, 100), map_range(5, 0, 10, 0, 100))


class TestInRange(unittest.TestCase):
    def test_inclusive_default(self) -> None:
        from number_utils import in_range

        self.assertTrue(in_range(5, 0, 10))
        self.assertTrue(in_range(0, 0, 10))
        self.assertTrue(in_range(10, 0, 10))
        self.assertFalse(in_range(-1, 0, 10))
        self.assertFalse(in_range(11, 0, 10))

    def test_exclusive(self) -> None:
        from number_utils import in_range

        self.assertTrue(in_range(5, 0, 10, inclusive=False))
        self.assertFalse(in_range(0, 0, 10, inclusive=False))
        self.assertFalse(in_range(10, 0, 10, inclusive=False))

    def test_invalid_bounds(self) -> None:
        from number_utils import in_range

        with self.assertRaises(ValueError):
            in_range(5, 10, 0)

    def test_type_errors(self) -> None:
        from number_utils import in_range

        with self.assertRaises(TypeError):
            in_range("x", 0, 10)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            in_range(5, "x", 10)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            in_range(5, 0, "x")  # type: ignore[arg-type]
