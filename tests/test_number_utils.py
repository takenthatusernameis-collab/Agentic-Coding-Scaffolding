"""Tests for number_utils module."""

import unittest

from number_utils import (
    clamp,
    digit_count,
    digit_product,
    digit_sum,
    digital_root,
    format_number,
    is_armstrong_number,
    is_automorphic_number,
    is_between,
    is_close,
    is_coprime,
    is_fibonacci_number,
    is_finite,
    is_happy_number,
    is_harshad_number,
    is_infinite,
    is_integer,
    is_lucas_number,
    is_nan,
    is_negative,
    is_neon_number,
    is_non_negative,
    is_non_positive,
    is_perfect_cube,
    is_perfect_number,
    is_perfect_square,
    is_positive,
    is_power_of_two,
    is_pronic_number,
    is_spy_number,
    is_strong_number,
    is_triangular_number,
    is_zero,
    lerp,
    map_range,
    percentage,
    remap,
    round_half_up,
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


class TestRoundHalfUp(unittest.TestCase):
    def test_default_places(self) -> None:
        self.assertEqual(round_half_up(2.5), 3)
        self.assertEqual(round_half_up(2.4), 2)
        self.assertEqual(round_half_up(2.6), 3)

    def test_negative_halves_away_from_zero(self) -> None:
        self.assertEqual(round_half_up(-2.5), -3)
        self.assertEqual(round_half_up(-2.4), -2)
        self.assertEqual(round_half_up(-2.6), -3)

    def test_places(self) -> None:
        self.assertEqual(round_half_up(3.14159, 2), 3.14)
        self.assertEqual(round_half_up(3.145, 2), 3.15)
        self.assertEqual(round_half_up(3.135, 2), 3.14)

    def test_negative_with_places(self) -> None:
        self.assertEqual(round_half_up(-3.145, 2), -3.15)
        self.assertEqual(round_half_up(-3.135, 2), -3.14)

    def test_zero_places_integers(self) -> None:
        self.assertEqual(round_half_up(0.5), 1)
        self.assertEqual(round_half_up(1.5), 2)
        self.assertEqual(round_half_up(2.5), 3)
        self.assertEqual(round_half_up(9.5), 10)

    def test_no_rounding_needed(self) -> None:
        self.assertEqual(round_half_up(3.0), 3)
        self.assertEqual(round_half_up(3.14159, 0), 3)
        self.assertEqual(round_half_up(3.14159, 6), 3.14159)

    def test_zero_value(self) -> None:
        self.assertEqual(round_half_up(0), 0)
        self.assertEqual(round_half_up(0.0, 2), 0.0)

    def test_large_places(self) -> None:
        self.assertEqual(round_half_up(1.23456789, 4), 1.2346)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            round_half_up("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            round_half_up(2.5, "2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            round_half_up(2.5, True)

    def test_negative_places_raises(self) -> None:
        with self.assertRaises(ValueError):
            round_half_up(2.5, -1)


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


class TestIsClose(unittest.TestCase):
    def test_equal_values(self) -> None:
        self.assertTrue(is_close(5, 5))
        self.assertTrue(is_close(1.5, 1.5))

    def test_within_default_tolerance(self) -> None:
        self.assertTrue(is_close(1.0, 1.0000000001))
        self.assertTrue(is_close(1.0, 1 + 1e-10))

    def test_outside_default_tolerance(self) -> None:
        self.assertFalse(is_close(1.0, 1.1))
        self.assertFalse(is_close(100.0, 101.0))

    def test_abs_tol(self) -> None:
        self.assertTrue(is_close(1.0, 1.1, abs_tol=0.2))
        self.assertFalse(is_close(1.0, 1.3, abs_tol=0.2))

    def test_rel_tol(self) -> None:
        self.assertTrue(is_close(100.0, 100.001, rel_tol=1e-4))
        self.assertFalse(is_close(100.0, 100.1, rel_tol=1e-4))

    def test_negative_values(self) -> None:
        self.assertTrue(is_close(-5.0, -5.000000001))
        self.assertFalse(is_close(-5.0, -5.1))

    def test_zeros(self) -> None:
        self.assertTrue(is_close(0.0, 0.0))
        self.assertTrue(is_close(0.0, 1e-12, abs_tol=1e-9))
        self.assertFalse(is_close(0.0, 1.0, abs_tol=0.5))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_close("x", 1.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_close(1.0, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_close(1.0, 1.0, rel_tol="x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_close(1.0, 1.0, abs_tol=None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_close(True, 1.0)  # type: ignore[arg-type]

    def test_negative_tolerances_raise(self) -> None:
        with self.assertRaises(ValueError):
            is_close(1.0, 1.0, rel_tol=-0.1)
        with self.assertRaises(ValueError):
            is_close(1.0, 1.0, abs_tol=-0.1)



class TestIsHappyNumber(unittest.TestCase):
    def test_happy_numbers(self) -> None:
        self.assertTrue(is_happy_number(1))
        self.assertTrue(is_happy_number(7))
        self.assertTrue(is_happy_number(10))
        self.assertTrue(is_happy_number(19))

    def test_unhappy_numbers(self) -> None:
        self.assertFalse(is_happy_number(2))
        self.assertFalse(is_happy_number(4))
        self.assertFalse(is_happy_number(3))
        self.assertFalse(is_happy_number(-1))
        self.assertFalse(is_happy_number(0))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_happy_number("7")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_happy_number(7.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_happy_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_happy_number(None)  # type: ignore[arg-type]


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


class TestIsDivisibleBy(unittest.TestCase):
    def test_divisible(self) -> None:
        from number_utils import is_divisible_by

        self.assertTrue(is_divisible_by(10, 2))
        self.assertFalse(is_divisible_by(10, 3))

    def test_zero_dividend(self) -> None:
        from number_utils import is_divisible_by

        self.assertTrue(is_divisible_by(0, 5))

    def test_negative(self) -> None:
        from number_utils import is_divisible_by

        self.assertTrue(is_divisible_by(-9, 3))

    def test_division_by_zero(self) -> None:
        from number_utils import is_divisible_by

        with self.assertRaises(ValueError):
            is_divisible_by(10, 0)

    def test_type_errors(self) -> None:
        from number_utils import is_divisible_by

        with self.assertRaises(TypeError):
            is_divisible_by(10.0, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_divisible_by(10, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_divisible_by(True, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_divisible_by(1, False)  # type: ignore[arg-type]


class TestIsMultipleOfDivides(unittest.TestCase):
    def test_aliases(self) -> None:
        from number_utils import divides, is_divisible_by, is_multiple_of



        self.assertTrue(is_multiple_of(10, 2))
        self.assertTrue(divides(2, 10))
        self.assertTrue(is_multiple_of(0, 3))
        self.assertFalse(is_multiple_of(10, 3))
        self.assertFalse(divides(3, 10))
        with self.assertRaises(ValueError):
            is_multiple_of(10, 0)
        with self.assertRaises(ValueError):
            divides(0, 10)
        with self.assertRaises(TypeError):
            is_multiple_of(1.5, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            divides(1, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_divisible_by(10, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_divisible_by(True, 2)  # type: ignore[arg-type]



class TestIsEven(unittest.TestCase):
    def test_even(self) -> None:
        from number_utils import is_even

        self.assertTrue(is_even(0))
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(-4))

    def test_odd(self) -> None:
        from number_utils import is_even

        self.assertFalse(is_even(1))
        self.assertFalse(is_even(-3))

    def test_type_errors(self) -> None:
        from number_utils import is_even

        with self.assertRaises(TypeError):
            is_even("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even(True)  # type: ignore[arg-type]


class TestIsOdd(unittest.TestCase):
    def test_odd(self) -> None:
        from number_utils import is_odd

        self.assertTrue(is_odd(1))
        self.assertTrue(is_odd(-3))

    def test_even(self) -> None:
        from number_utils import is_odd

        self.assertFalse(is_odd(0))
        self.assertFalse(is_odd(2))

    def test_type_errors(self) -> None:
        from number_utils import is_odd

        with self.assertRaises(TypeError):
            is_odd("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(True)  # type: ignore[arg-type]


class TestDigitSum(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(digit_sum(0), 0)
        self.assertEqual(digit_sum(5), 5)
        self.assertEqual(digit_sum(123), 6)
        self.assertEqual(digit_sum(999), 27)
        self.assertEqual(digit_sum(1001), 2)

    def test_sign_ignored(self) -> None:
        self.assertEqual(digit_sum(-123), 6)
        self.assertEqual(digit_sum(-5), 5)
        self.assertEqual(digit_sum(-1001), 2)

    def test_single_digit(self) -> None:
        for n in range(10):
            self.assertEqual(digit_sum(n), n)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            digit_sum("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_sum(12.3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_sum(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_sum(None)  # type: ignore[arg-type]


class TestDigitCount(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(digit_count(0), 1)
        self.assertEqual(digit_count(5), 1)
        self.assertEqual(digit_count(123), 3)
        self.assertEqual(digit_count(999), 3)
        self.assertEqual(digit_count(1001), 4)

    def test_sign_ignored(self) -> None:
        self.assertEqual(digit_count(-123), 3)
        self.assertEqual(digit_count(-5), 1)
        self.assertEqual(digit_count(-1001), 4)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            digit_count("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_count(12.3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_count(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_count(None)  # type: ignore[arg-type]


class TestIsCoprime(unittest.TestCase):
    def test_coprime_pairs(self) -> None:
        self.assertTrue(is_coprime(8, 9))
        self.assertTrue(is_coprime(14, 25))
        self.assertTrue(is_coprime(1, 100))
        self.assertTrue(is_coprime(1, 1))
        self.assertTrue(is_coprime(17, 19))

    def test_non_coprime_pairs(self) -> None:
        self.assertFalse(is_coprime(8, 12))
        self.assertFalse(is_coprime(21, 14))
        self.assertFalse(is_coprime(100, 10))
        self.assertFalse(is_coprime(0, 5))
        self.assertFalse(is_coprime(0, 0))

    def test_sign_and_zero_edge_cases(self) -> None:
        self.assertTrue(is_coprime(-8, 9))
        self.assertTrue(is_coprime(8, -9))
        self.assertTrue(is_coprime(-8, -9))
        self.assertTrue(is_coprime(0, 1))
        self.assertFalse(is_coprime(0, 0))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_coprime("8", 9)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(8, "9")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(True, 9)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(8, True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(8.0, 9)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_coprime(8, None)  # type: ignore[arg-type]


class TestDigitProduct(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(digit_product(0), 0)
        self.assertEqual(digit_product(5), 5)
        self.assertEqual(digit_product(123), 6)
        self.assertEqual(digit_product(999), 729)
        self.assertEqual(digit_product(1001), 0)

    def test_sign_ignored(self) -> None:
        self.assertEqual(digit_product(-123), 6)
        self.assertEqual(digit_product(-5), 5)
        self.assertEqual(digit_product(-1001), 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            digit_product("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_product(12.3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_product(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digit_product(None)  # type: ignore[arg-type]


class TestDigitalRoot(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(digital_root(0), 0)
        self.assertEqual(digital_root(5), 5)
        self.assertEqual(digital_root(9), 9)
        self.assertEqual(digital_root(123), 6)
        self.assertEqual(digital_root(99), 9)
        self.assertEqual(digital_root(199), 1)
        self.assertEqual(digital_root(999), 9)

    def test_sign_ignored(self) -> None:
        self.assertEqual(digital_root(-123), 6)
        self.assertEqual(digital_root(-5), 5)
        self.assertEqual(digital_root(-99), 9)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            digital_root("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digital_root(12.3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digital_root(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            digital_root(None)  # type: ignore[arg-type]


class TestIsPerfectNumber(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertTrue(is_perfect_number(6))
        self.assertTrue(is_perfect_number(28))
        self.assertFalse(is_perfect_number(12))
        self.assertFalse(is_perfect_number(1))
        self.assertFalse(is_perfect_number(0))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_perfect_number("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_perfect_number(True)  # type: ignore[arg-type]


class TestIsTriangularNumber(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertTrue(is_triangular_number(0))
        self.assertTrue(is_triangular_number(1))
        self.assertTrue(is_triangular_number(3))
        self.assertTrue(is_triangular_number(6))
        self.assertTrue(is_triangular_number(10))
        self.assertTrue(is_triangular_number(15))
        self.assertFalse(is_triangular_number(4))
        self.assertFalse(is_triangular_number(2))
        self.assertFalse(is_triangular_number(-1))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_triangular_number("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_triangular_number(True)  # type: ignore[arg-type]



class TestIsArmstrongNumber(unittest.TestCase):
    def test_armstrong_numbers(self) -> None:
        self.assertTrue(is_armstrong_number(0))
        self.assertTrue(is_armstrong_number(1))
        self.assertTrue(is_armstrong_number(153))
        self.assertTrue(is_armstrong_number(370))
        self.assertTrue(is_armstrong_number(371))
        self.assertTrue(is_armstrong_number(407))
        self.assertTrue(is_armstrong_number(9474))

    def test_non_armstrong_numbers(self) -> None:
        self.assertFalse(is_armstrong_number(10))
        self.assertFalse(is_armstrong_number(123))
        self.assertFalse(is_armstrong_number(100))
        self.assertFalse(is_armstrong_number(-153))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_armstrong_number("153")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_armstrong_number(153.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_armstrong_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_armstrong_number(None)  # type: ignore[arg-type]


class TestIsHarshadNumber(unittest.TestCase):
    def test_harshad_numbers(self) -> None:
        self.assertTrue(is_harshad_number(18))
        self.assertTrue(is_harshad_number(21))
        self.assertTrue(is_harshad_number(24))
        self.assertTrue(is_harshad_number(36))
        self.assertTrue(is_harshad_number(48))
        self.assertTrue(is_harshad_number(1))
        self.assertTrue(is_harshad_number(10))
        self.assertTrue(is_harshad_number(12))

    def test_non_harshad_numbers(self) -> None:
        self.assertFalse(is_harshad_number(19))
        self.assertFalse(is_harshad_number(23))
        self.assertFalse(is_harshad_number(103))
        self.assertFalse(is_harshad_number(-18))

    def test_zero_raises(self) -> None:
        with self.assertRaises(ValueError):
            is_harshad_number(0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_harshad_number("18")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_harshad_number(18.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_harshad_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_harshad_number(None)  # type: ignore[arg-type]


class TestIsAutomorphicNumber(unittest.TestCase):
    def test_automorphic_numbers(self) -> None:
        self.assertTrue(is_automorphic_number(0))
        self.assertTrue(is_automorphic_number(1))
        self.assertTrue(is_automorphic_number(5))
        self.assertTrue(is_automorphic_number(6))
        self.assertTrue(is_automorphic_number(25))
        self.assertTrue(is_automorphic_number(76))
        self.assertTrue(is_automorphic_number(376))
        self.assertTrue(is_automorphic_number(625))
        self.assertTrue(is_automorphic_number(9376))

    def test_non_automorphic_numbers(self) -> None:
        self.assertFalse(is_automorphic_number(2))
        self.assertFalse(is_automorphic_number(7))
        self.assertFalse(is_automorphic_number(10))
        self.assertFalse(is_automorphic_number(12))
        self.assertFalse(is_automorphic_number(100))
        self.assertFalse(is_automorphic_number(-5))

    def test_large_automorphic(self) -> None:
        self.assertTrue(is_automorphic_number(90625))
        self.assertTrue(is_automorphic_number(109376))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_automorphic_number("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_automorphic_number(5.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_automorphic_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_automorphic_number(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestIsNeonNumber(unittest.TestCase):
    def test_neon(self) -> None:
        self.assertTrue(is_neon_number(0))
        self.assertTrue(is_neon_number(1))
        self.assertTrue(is_neon_number(9))

    def test_not_neon(self) -> None:
        self.assertFalse(is_neon_number(10))
        self.assertFalse(is_neon_number(2))

    def test_negative(self) -> None:
        self.assertFalse(is_neon_number(-9))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_neon_number("9")  # type: ignore[arg-type]


class TestIsStrongNumber(unittest.TestCase):
    def test_strong(self) -> None:
        self.assertTrue(is_strong_number(1))
        self.assertTrue(is_strong_number(2))
        self.assertTrue(is_strong_number(145))
        self.assertTrue(is_strong_number(40585))

    def test_not_strong(self) -> None:
        self.assertFalse(is_strong_number(123))
        self.assertFalse(is_strong_number(4))

    def test_negative(self) -> None:
        self.assertFalse(is_strong_number(-145))

    def test_zero(self) -> None:
        self.assertFalse(is_strong_number(0))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_strong_number("145")  # type: ignore[arg-type]


class TestIsFibonacciNumber(unittest.TestCase):
    def test_known_fibonacci(self) -> None:
        for n in (0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987):
            self.assertTrue(is_fibonacci_number(n), n)

    def test_not_fibonacci(self) -> None:
        for n in (4, 6, 7, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20):
            self.assertFalse(is_fibonacci_number(n), n)

    def test_negative(self) -> None:
        self.assertFalse(is_fibonacci_number(-1))
        self.assertFalse(is_fibonacci_number(-8))

    def test_large_fibonacci(self) -> None:
        # 1597 is F(17); 2000 is not a Fibonacci number.
        self.assertTrue(is_fibonacci_number(1597))
        self.assertFalse(is_fibonacci_number(2000))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_fibonacci_number("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_fibonacci_number(5.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_fibonacci_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_fibonacci_number(None)  # type: ignore[arg-type]


class TestIsLucasNumber(unittest.TestCase):
    def test_known_lucas(self) -> None:
        for n in (2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322):
            self.assertTrue(is_lucas_number(n), n)

    def test_not_lucas(self) -> None:
        for n in (0, 5, 6, 8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 1000):
            self.assertFalse(is_lucas_number(n), n)

    def test_negative(self) -> None:
        self.assertFalse(is_lucas_number(-1))
        self.assertFalse(is_lucas_number(-7))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_lucas_number("7")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_lucas_number(7.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_lucas_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_lucas_number(None)  # type: ignore[arg-type]


class TestIsPronicNumber(unittest.TestCase):
    def test_known_pronic_numbers(self) -> None:
        # n*(n+1) for n in 0..12: 0, 2, 6, 12, 20, 30, 42, 56, 72, 90, 110, 132, 156
        for n in (0, 2, 6, 12, 20, 30, 42, 56, 72, 90, 110, 132, 156):
            self.assertTrue(is_pronic_number(n), n)

    def test_non_pronic_numbers(self) -> None:
        for n in (1, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 21):
            self.assertFalse(is_pronic_number(n), n)

    def test_negative(self) -> None:
        for n in (-1, -2, -6, -12, -20):
            self.assertFalse(is_pronic_number(n), n)

    def test_non_integer(self) -> None:
        self.assertFalse(is_pronic_number(2.5))
        self.assertTrue(is_pronic_number(6.0))  # integral float accepted
        self.assertFalse(is_pronic_number(12.5))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_pronic_number("2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_pronic_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_pronic_number(None)  # type: ignore[arg-type]



class TestIsSpyNumber(unittest.TestCase):
    def test_known_spy_numbers(self) -> None:
        for n in (123, 1124, 22):
            self.assertTrue(is_spy_number(n), n)

    def test_not_spy_numbers(self) -> None:
        for n in (1234, 12, 102, 124):
            self.assertFalse(is_spy_number(n), n)

    def test_zero_and_negative(self) -> None:
        for n in (0, -123, -1124):
            self.assertFalse(is_spy_number(n), n)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_spy_number("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_spy_number(123.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_spy_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_spy_number(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
