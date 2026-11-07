"""Tests for number_utils module."""

import math
import unittest

from number_utils import (
    additive_persistence,
    ceil_div,
    clamp,
    clamp01,
    digit_count,
    digit_product,
    digit_sum,
    digital_root,
    format_number,
    gcd,
    gcd_list,
    integer_nth_root,
    is_abundant_number,
    is_armstrong_number,
    is_automorphic_number,
    is_between,
    is_catalan_number,
    is_close,
    is_coprime,
    is_deficient_number,
    is_disarium_number,
    is_evil_number,
    is_fibonacci_number,
    is_finite,
    is_happy_number,
    is_harshad_number,
    is_hexagonal_number,
    is_infinite,
    is_integer,
    is_kaprekar_number,
    is_lucas_number,
    is_mersenne_number,
    is_nan,
    is_negative,
    is_neon_number,
    is_non_negative,
    is_non_positive,
    is_odious_number,
    is_pentagonal_number,
    is_perfect_cube,
    is_perfect_number,
    is_perfect_power,
    is_perfect_square,
    is_positive,
    is_power_of,
    is_power_of_two,
    is_powerful_number,
    is_pronic_number,
    is_spy_number,
    is_squarefree_number,
    is_strong_number,
    is_triangular_number,
    is_ugly_number,
    is_zero,
    lcm,
    lcm_list,
    lerp,
    map_range,
    percentage,
    remap,
    round_half_up,
    round_to,
    safe_divide,
    sign,
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

    def test_nan_raises(self) -> None:
        for args in (
            (float("nan"), 0, 1),
            (0, float("nan"), 1),
            (0, 0, float("nan")),
        ):
            with self.assertRaises(ValueError):
                clamp(*args)

    def test_infinities(self) -> None:
        self.assertEqual(clamp(float("inf"), 0, 10), 10)
        self.assertEqual(clamp(float("-inf"), 0, 10), 0)
        self.assertEqual(clamp(5, float("-inf"), float("inf")), 5)
        with self.assertRaises(ValueError):
            clamp(5, float("inf"), 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            clamp("x", 0, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp(0, True, 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp(0, 0, None)  # type: ignore[arg-type]


class TestClamp01(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(clamp01(0.5), 0.5)
        self.assertEqual(clamp01(-1), 0)
        self.assertEqual(clamp01(2), 1)
        self.assertEqual(clamp01(0.0), 0.0)
        self.assertEqual(clamp01(1.0), 1.0)

    def test_nan_raises(self) -> None:
        with self.assertRaises(ValueError):
            clamp01(float("nan"))

    def test_infinities(self) -> None:
        self.assertEqual(clamp01(float("inf")), 1)
        self.assertEqual(clamp01(float("-inf")), 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            clamp01("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp01(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            clamp01(None)  # type: ignore[arg-type]


class TestRoundTo(unittest.TestCase):
    def test_default(self) -> None:
        self.assertEqual(round_to(3.14159), 3)

    def test_places(self) -> None:
        self.assertEqual(round_to(3.14159, 2), 3.14)

    def test_negative_places_raises(self) -> None:
        with self.assertRaises(ValueError):
            round_to(1.23, -1)

    def test_special_floats(self) -> None:
        import math

        self.assertTrue(math.isnan(round_to(float("nan"), 2)))
        self.assertTrue(math.isinf(round_to(float("inf"), 2)))
        self.assertTrue(math.isinf(round_to(float("-inf"), 2)))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            round_to("x", 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            round_to(1.23, 2.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            round_to(1.23, True)  # type: ignore[arg-type]


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
        self.assertTrue(is_integer(-5))
        self.assertTrue(is_integer(0))

    def test_float_integral(self) -> None:
        self.assertTrue(is_integer(5.0))
        self.assertTrue(is_integer(-3.0))
        self.assertTrue(is_integer(0.0))

    def test_float_non_integral(self) -> None:
        self.assertFalse(is_integer(5.5))
        self.assertFalse(is_integer(-2.7))
        self.assertFalse(is_integer(0.1))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_integer("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_integer(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_integer(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_integer(None)  # type: ignore[arg-type]


class TestFormatNumber(unittest.TestCase):
    def test_format(self) -> None:
        self.assertEqual(format_number(1234.5, 2), "1,234.50")


class TestPercentage(unittest.TestCase):
    def test_normal(self) -> None:
        self.assertEqual(percentage(1, 4), "25.0%")

    def test_zero_total(self) -> None:
        self.assertEqual(percentage(5, 0), "0.0%")

    def test_nan_propagates(self) -> None:
        import math

        self.assertTrue(math.isnan(float(percentage(float("nan"), 4).rstrip("%"))))
        self.assertTrue(math.isnan(float(percentage(1, float("nan")).rstrip("%"))))


class TestLerp(unittest.TestCase):
    def test_endpoints(self) -> None:
        self.assertEqual(lerp(0, 10, 0), 0)
        self.assertEqual(lerp(0, 10, 1), 10)

    def test_midpoint(self) -> None:
        self.assertEqual(lerp(0, 10, 0.5), 5.0)

    def test_extrapolation(self) -> None:
        self.assertEqual(lerp(0, 10, 2), 20)
        self.assertEqual(lerp(0, 10, -1), -10)

    def test_nan_propagates(self) -> None:
        self.assertTrue(math.isnan(lerp(0, 10, float("nan"))))
        self.assertTrue(math.isnan(lerp(float("nan"), 10, 0.5)))
        self.assertTrue(math.isnan(lerp(0, float("nan"), 0.5)))

    def test_infinities(self) -> None:
        self.assertTrue(math.isinf(lerp(0, 10, float("inf"))))
        self.assertTrue(math.isinf(lerp(0, float("inf"), 2)))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            lerp("a", 10, 0.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lerp(0, "b", 0.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lerp(0, 10, "c")  # type: ignore[arg-type]


class TestSign(unittest.TestCase):
    def test_negative(self) -> None:
        self.assertEqual(sign(-5), -1)

    def test_zero(self) -> None:
        self.assertEqual(sign(0), 0)

    def test_positive(self) -> None:
        self.assertEqual(sign(3.5), 1)

    def test_nan(self) -> None:
        self.assertEqual(sign(float("nan")), 0)

    def test_infinities(self) -> None:
        self.assertEqual(sign(float("inf")), 1)
        self.assertEqual(sign(float("-inf")), -1)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            sign("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sign(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sign(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            sign(None)  # type: ignore[arg-type]


class TestIsNegative(unittest.TestCase):
    def test_negative(self) -> None:
        self.assertTrue(is_negative(-5))
        self.assertTrue(is_negative(-0.5))
        self.assertTrue(is_negative(-float("inf")))

    def test_zero(self) -> None:
        self.assertFalse(is_negative(0))
        self.assertFalse(is_negative(0.0))
        self.assertFalse(is_negative(-0.0))

    def test_positive(self) -> None:
        self.assertFalse(is_negative(5))
        self.assertFalse(is_negative(0.5))
        self.assertFalse(is_negative(float("inf")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_negative("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_negative(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_negative(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_negative(None)  # type: ignore[arg-type]


class TestIsPositive(unittest.TestCase):
    def test_positive(self) -> None:
        self.assertTrue(is_positive(5))
        self.assertTrue(is_positive(0.5))
        self.assertTrue(is_positive(float("inf")))

    def test_zero(self) -> None:
        self.assertFalse(is_positive(0))
        self.assertFalse(is_positive(0.0))
        self.assertFalse(is_positive(-0.0))

    def test_negative(self) -> None:
        self.assertFalse(is_positive(-5))
        self.assertFalse(is_positive(-0.5))
        self.assertFalse(is_positive(-float("inf")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_positive("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_positive(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_positive(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_positive(None)  # type: ignore[arg-type]


class TestIsZero(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertTrue(is_zero(0))
        self.assertTrue(is_zero(0.0))
        self.assertTrue(is_zero(-0.0))

    def test_non_zero(self) -> None:
        self.assertFalse(is_zero(5))
        self.assertFalse(is_zero(-5))
        self.assertFalse(is_zero(0.5))
        self.assertFalse(is_zero(float("inf")))
        self.assertFalse(is_zero(float("nan")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_zero("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_zero(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_zero(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_zero(None)  # type: ignore[arg-type]


class TestIsNonNegative(unittest.TestCase):
    def test_non_negative(self) -> None:
        self.assertTrue(is_non_negative(0))
        self.assertTrue(is_non_negative(0.0))
        self.assertTrue(is_non_negative(-0.0))
        self.assertTrue(is_non_negative(5))
        self.assertTrue(is_non_negative(0.5))
        self.assertTrue(is_non_negative(float("inf")))

    def test_negative(self) -> None:
        self.assertFalse(is_non_negative(-5))
        self.assertFalse(is_non_negative(-0.5))
        self.assertFalse(is_non_negative(-float("inf")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_non_negative("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_non_negative(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_non_negative(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_non_negative(None)  # type: ignore[arg-type]


class TestIsNonPositive(unittest.TestCase):
    def test_non_positive(self) -> None:
        self.assertTrue(is_non_positive(0))
        self.assertTrue(is_non_positive(0.0))
        self.assertTrue(is_non_positive(-0.0))
        self.assertTrue(is_non_positive(-5))
        self.assertTrue(is_non_positive(-0.5))
        self.assertTrue(is_non_positive(-float("inf")))

    def test_positive(self) -> None:
        self.assertFalse(is_non_positive(5))
        self.assertFalse(is_non_positive(0.5))
        self.assertFalse(is_non_positive(float("inf")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_non_positive("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_non_positive(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_non_positive(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_non_positive(None)  # type: ignore[arg-type]


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

    def test_nan_comparisons_follow_python_semantics(self) -> None:
        self.assertFalse(is_between(float("nan"), 0, 10))
        self.assertFalse(is_between(5, float("nan"), 10))
        self.assertFalse(is_between(5, 0, float("nan")))
        self.assertFalse(is_between(float("nan"), float("nan"), float("nan")))

    def test_infinities(self) -> None:
        self.assertTrue(is_between(0, float("-inf"), float("inf")))
        self.assertTrue(is_between(float("inf"), 0, float("inf")))
        self.assertTrue(is_between(float("-inf"), float("-inf"), 0))

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
        self.assertTrue(is_finite(-42))
        self.assertTrue(is_finite(3.14))
        self.assertTrue(is_finite(0.0))
        self.assertTrue(is_finite(-0.0))

    def test_infinity(self) -> None:
        self.assertFalse(is_finite(float("inf")))
        self.assertFalse(is_finite(float("-inf")))

    def test_nan(self) -> None:
        self.assertFalse(is_finite(float("nan")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_finite("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_finite(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_finite(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_finite(None)  # type: ignore[arg-type]


class TestIsInfinite(unittest.TestCase):
    def test_infinity(self) -> None:
        self.assertTrue(is_infinite(float("inf")))
        self.assertTrue(is_infinite(float("-inf")))

    def test_finite(self) -> None:
        self.assertFalse(is_infinite(0))
        self.assertFalse(is_infinite(3.14))
        self.assertFalse(is_infinite(-42))
        self.assertFalse(is_infinite(0.0))

    def test_nan(self) -> None:
        self.assertFalse(is_infinite(float("nan")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_infinite(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_infinite("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_infinite(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_infinite(False)  # type: ignore[arg-type]


class TestIsNan(unittest.TestCase):
    def test_nan(self) -> None:
        self.assertTrue(is_nan(float("nan")))

    def test_finite(self) -> None:
        self.assertFalse(is_nan(0))
        self.assertFalse(is_nan(-0.0))
        self.assertFalse(is_nan(3.14))
        self.assertFalse(is_nan(float("inf")))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_nan("nan")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_nan(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_nan(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_nan(None)  # type: ignore[arg-type]


class TestSafeDivide(unittest.TestCase):
    def test_normal(self) -> None:
        self.assertEqual(safe_divide(10, 2), 5.0)
        self.assertEqual(safe_divide(7, 2), 3.5)
        self.assertEqual(safe_divide(-10, 2), -5.0)

    def test_zero_denominator(self) -> None:
        self.assertEqual(safe_divide(10, 0), 0.0)
        self.assertEqual(safe_divide(0, 0), 0.0)
        self.assertEqual(safe_divide(-5, 0), 0.0)

    def test_special_floats(self) -> None:
        import math

        self.assertTrue(math.isinf(safe_divide(float("inf"), 2)))
        self.assertTrue(math.isnan(safe_divide(float("nan"), 2)))
        self.assertTrue(math.isnan(safe_divide(1, float("nan"))))
        self.assertEqual(safe_divide(float("inf"), 0), 0.0)

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            safe_divide("a", 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            safe_divide(2, "b")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            safe_divide(True, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            safe_divide(2, False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            safe_divide(None, 2)  # type: ignore[arg-type]


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


class TestIsPowerOf(unittest.TestCase):
    def test_positive_base_powers(self) -> None:
        self.assertTrue(is_power_of(8, 2))
        self.assertTrue(is_power_of(9, 3))
        self.assertTrue(is_power_of(27, 3))
        self.assertTrue(is_power_of(16, 4))
        self.assertTrue(is_power_of(1, 5))
        self.assertTrue(is_power_of(1, 2))
        self.assertTrue(is_power_of(5, 5))

    def test_positive_base_non_powers(self) -> None:
        self.assertFalse(is_power_of(10, 2))
        self.assertFalse(is_power_of(6, 3))
        self.assertFalse(is_power_of(2, 4))
        self.assertFalse(is_power_of(0, 2))
        self.assertFalse(is_power_of(-8, 2))

    def test_base_one(self) -> None:
        self.assertTrue(is_power_of(1, 1))
        self.assertFalse(is_power_of(2, 1))
        self.assertFalse(is_power_of(0, 1))

    def test_base_zero(self) -> None:
        self.assertTrue(is_power_of(0, 0))
        self.assertFalse(is_power_of(1, 0))
        self.assertFalse(is_power_of(5, 0))

    def test_base_minus_one(self) -> None:
        self.assertTrue(is_power_of(1, -1))
        self.assertTrue(is_power_of(-1, -1))
        self.assertFalse(is_power_of(2, -1))
        self.assertFalse(is_power_of(0, -1))

    def test_negative_base(self) -> None:
        self.assertTrue(is_power_of(-8, -2))
        self.assertTrue(is_power_of(4, -2))
        self.assertTrue(is_power_of(16, -2))
        self.assertFalse(is_power_of(-4, -2))
        self.assertFalse(is_power_of(8, -2))
        self.assertTrue(is_power_of(1, -2))

    def test_non_integer_values(self) -> None:
        self.assertFalse(is_power_of(8.5, 2))
        self.assertFalse(is_power_of(8, 2.5))
        self.assertTrue(is_power_of(8.0, 2.0))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_power_of("8", 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_power_of(8, "2")  # type: ignore[arg-type]


class TestIsPerfectPower(unittest.TestCase):
    def test_perfect_powers(self) -> None:
        for n in (
            4,
            8,
            9,
            16,
            25,
            27,
            32,
            36,
            49,
            64,
            81,
            100,
            121,
            125,
            128,
            144,
            169,
            196,
            216,
            225,
            243,
            256,
            289,
            324,
            343,
            361,
            400,
            512,
            625,
            729,
            1000,
            1024,
            2**20,
            3**10,
            5**6,
        ):
            self.assertTrue(is_perfect_power(n), n)

    def test_non_perfect_powers(self) -> None:
        for n in (2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23):
            self.assertFalse(is_perfect_power(n), n)

    def test_one_and_zero(self) -> None:
        self.assertFalse(is_perfect_power(1))
        self.assertFalse(is_perfect_power(0))

    def test_negatives(self) -> None:
        for n in (-1, -4, -8, -16, -27):
            self.assertFalse(is_perfect_power(n), n)

    def test_non_integer(self) -> None:
        self.assertFalse(is_perfect_power(2.0))
        self.assertFalse(is_perfect_power(8.5))
        self.assertTrue(is_perfect_power(8.0))
        self.assertTrue(is_perfect_power(16.0))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_perfect_power("x")  # type: ignore[arg-type]


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

    def test_nan_propagates(self) -> None:
        import math

        self.assertTrue(math.isnan(map_range(float("nan"), 0, 10, 0, 100)))
        self.assertTrue(math.isnan(map_range(5, float("nan"), 10, 0, 100)))
        self.assertTrue(math.isnan(map_range(5, 0, 10, float("nan"), 100)))

    def test_type_error_all_args(self) -> None:
        for i in range(5):
            args = [5, 0, 10, 0, 100]
            args[i] = "x"
            with self.assertRaises(TypeError):
                map_range(*args)  # type: ignore[arg-type]

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

    def test_inclusive_type_error(self) -> None:
        from number_utils import in_range

        with self.assertRaises(TypeError):
            in_range(1, 0, 2, inclusive=1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            in_range(1, 0, 2, inclusive="true")  # type: ignore[arg-type]

    def test_nan_bounds(self) -> None:
        from number_utils import in_range

        self.assertFalse(in_range(float("nan"), 0, 1))
        self.assertFalse(in_range(0, float("nan"), 1))
        self.assertFalse(in_range(0, 0, float("nan")))

    def test_single_point_range(self) -> None:
        from number_utils import in_range

        self.assertTrue(in_range(5, 5, 5))
        self.assertFalse(in_range(5, 5, 5, inclusive=False))
        self.assertFalse(in_range(4, 5, 5))

    def test_negative_and_float(self) -> None:
        from number_utils import in_range

        self.assertTrue(in_range(-1.5, -2.0, 0.0))
        self.assertFalse(in_range(-2.5, -2.0, 0.0))



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
        self.assertTrue(is_even(2.0))
        self.assertTrue(is_even(0.0))

    def test_odd(self) -> None:
        from number_utils import is_even

        self.assertFalse(is_even(1))
        self.assertFalse(is_even(-3))
        self.assertFalse(is_even(3.5))

    def test_non_finite(self) -> None:
        from number_utils import is_even

        self.assertFalse(is_even(float("inf")))
        self.assertFalse(is_even(float("-inf")))
        self.assertFalse(is_even(float("nan")))

    def test_type_errors(self) -> None:
        from number_utils import is_even

        with self.assertRaises(TypeError):
            is_even("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_even(None)  # type: ignore[arg-type]


class TestIsOdd(unittest.TestCase):
    def test_odd(self) -> None:
        from number_utils import is_odd

        self.assertTrue(is_odd(1))
        self.assertTrue(is_odd(-3))
        self.assertTrue(is_odd(3.0))

    def test_even(self) -> None:
        from number_utils import is_odd

        self.assertFalse(is_odd(0))
        self.assertFalse(is_odd(2))
        self.assertFalse(is_odd(2.0))
        self.assertFalse(is_odd(2.5))

    def test_non_finite(self) -> None:
        from number_utils import is_odd

        self.assertFalse(is_odd(float("inf")))
        self.assertFalse(is_odd(float("-inf")))
        self.assertFalse(is_odd(float("nan")))

    def test_type_errors(self) -> None:
        from number_utils import is_odd

        with self.assertRaises(TypeError):
            is_odd("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(None)  # type: ignore[arg-type]


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


class TestAdditivePersistence(unittest.TestCase):
    def test_basic(self) -> None:
        self.assertEqual(additive_persistence(0), 0)
        self.assertEqual(additive_persistence(9), 0)
        self.assertEqual(additive_persistence(123), 1)
        self.assertEqual(additive_persistence(99), 2)
        self.assertEqual(additive_persistence(199), 3)
        self.assertEqual(additive_persistence(999), 2)

    def test_sign_ignored(self) -> None:
        self.assertEqual(additive_persistence(-123), 1)
        self.assertEqual(additive_persistence(-5), 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            additive_persistence("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            additive_persistence(12.3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            additive_persistence(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            additive_persistence(None)  # type: ignore[arg-type]


class TestMultiplicativePersistence(unittest.TestCase):
    def test_basic(self) -> None:
        from number_utils import multiplicative_persistence

        self.assertEqual(multiplicative_persistence(0), 0)
        self.assertEqual(multiplicative_persistence(4), 0)
        self.assertEqual(multiplicative_persistence(39), 3)
        self.assertEqual(multiplicative_persistence(77), 4)
        self.assertEqual(multiplicative_persistence(679), 5)
        self.assertEqual(multiplicative_persistence(999), 4)

    def test_sign_ignored(self) -> None:
        from number_utils import multiplicative_persistence

        self.assertEqual(multiplicative_persistence(-39), 3)
        self.assertEqual(multiplicative_persistence(-4), 0)

    def test_type_errors(self) -> None:
        from number_utils import multiplicative_persistence

        with self.assertRaises(TypeError):
            multiplicative_persistence("123")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            multiplicative_persistence(12.3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            multiplicative_persistence(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            multiplicative_persistence(None)  # type: ignore[arg-type]


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


class TestIsOdiousNumber(unittest.TestCase):
    def test_odious_numbers(self) -> None:

        for n in (1, 2, 4, 7, 8, 11, 13, 14, 19, 21, 22, 25, 26, 28, 31, 32):
            self.assertTrue(is_odious_number(n), n)

    def test_non_odious_numbers(self) -> None:

        for n in (0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30):
            self.assertFalse(is_odious_number(n), n)

    def test_negative_returns_false(self) -> None:

        self.assertFalse(is_odious_number(-1))
        self.assertFalse(is_odious_number(-7))

    def test_type_errors(self) -> None:

        with self.assertRaises(TypeError):
            is_odious_number("7")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odious_number(7.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odious_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odious_number(None)  # type: ignore[arg-type]


class TestIsEvilNumber(unittest.TestCase):
    def test_evil_numbers(self) -> None:

        for n in (0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30):
            self.assertTrue(is_evil_number(n), n)

    def test_non_evil_numbers(self) -> None:

        for n in (1, 2, 4, 7, 8, 11, 13, 14, 19, 21, 22, 25, 26, 28, 31, 32):
            self.assertFalse(is_evil_number(n), n)

    def test_negative_returns_false(self) -> None:

        self.assertFalse(is_evil_number(-1))
        self.assertFalse(is_evil_number(-6))

    def test_type_errors(self) -> None:

        with self.assertRaises(TypeError):
            is_evil_number("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_evil_number(6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_evil_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_evil_number(None)  # type: ignore[arg-type]


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


class TestIsDisariumNumber(unittest.TestCase):
    def test_disarium(self) -> None:
        self.assertTrue(is_disarium_number(0))
        self.assertTrue(is_disarium_number(135))
        self.assertTrue(is_disarium_number(175))

    def test_not_disarium(self) -> None:
        self.assertFalse(is_disarium_number(10))
        self.assertFalse(is_disarium_number(10))

    def test_negative(self) -> None:
        self.assertFalse(is_disarium_number(-9))

    def test_type_error(self) -> None:
        with self.assertRaises(TypeError):
            is_disarium_number("9")  # type: ignore[arg-type]


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


class TestIsAbundantNumber(unittest.TestCase):
    def test_known_abundant(self) -> None:
        for n in (12, 18, 20, 24, 30, 36, 40, 42, 48, 56):
            self.assertTrue(is_abundant_number(n), n)

    def test_perfect_and_deficient_are_false(self) -> None:
        for n in (1, 2, 3, 4, 6, 8, 10, 16, 28):
            self.assertFalse(is_abundant_number(n), n)

    def test_zero_and_negative(self) -> None:
        for n in (0, -12, -18):
            self.assertFalse(is_abundant_number(n), n)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_abundant_number(12.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_abundant_number("12")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_abundant_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_abundant_number(None)  # type: ignore[arg-type]


class TestIsDeficientNumber(unittest.TestCase):
    def test_known_deficient(self) -> None:
        for n in (1, 2, 3, 4, 8, 10, 14, 16, 17):
            self.assertTrue(is_deficient_number(n), n)

    def test_perfect_and_abundant_are_false(self) -> None:
        for n in (6, 12, 18, 20, 28):
            self.assertFalse(is_deficient_number(n), n)

    def test_zero_and_negative(self) -> None:
        for n in (0, -1, -12):
            self.assertFalse(is_deficient_number(n), n)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_deficient_number(12.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_deficient_number("12")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_deficient_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_deficient_number(None)  # type: ignore[arg-type]


class TestGcd(unittest.TestCase):
    def test_known_pairs(self) -> None:
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(54, 24), 6)
        self.assertEqual(gcd(17, 19), 1)
        self.assertEqual(gcd(100, 10), 10)

    def test_one_argument_is_zero(self) -> None:
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(7, 0), 7)
        self.assertEqual(gcd(0, 0), 0)

    def test_sign_ignored(self) -> None:
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)
        self.assertEqual(gcd(-48, -18), 6)

    def test_large_values(self) -> None:
        self.assertEqual(gcd(1071, 462), 21)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            gcd("48", 18)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            gcd(48, 18.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            gcd(True, 18)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            gcd(48, None)  # type: ignore[arg-type]


class TestLcm(unittest.TestCase):
    def test_known_pairs(self) -> None:
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(12, 18), 36)
        self.assertEqual(lcm(7, 13), 91)
        self.assertEqual(lcm(1, 100), 100)

    def test_one_argument_is_zero(self) -> None:
        self.assertEqual(lcm(0, 5), 0)
        self.assertEqual(lcm(7, 0), 0)

    def test_sign_ignored(self) -> None:
        self.assertEqual(lcm(-4, 6), 12)
        self.assertEqual(lcm(4, -6), 12)
        self.assertEqual(lcm(-4, -6), 12)

    def test_both_zero_raises(self) -> None:
        with self.assertRaises(ValueError):
            lcm(0, 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            lcm("4", 6)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lcm(4, 6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lcm(True, 6)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lcm(4, None)  # type: ignore[arg-type]


class TestCeilDiv(unittest.TestCase):
    def test_exact_division(self) -> None:
        self.assertEqual(ceil_div(6, 3), 2)
        self.assertEqual(ceil_div(9, 3), 3)

    def test_rounds_up(self) -> None:
        self.assertEqual(ceil_div(7, 3), 3)
        self.assertEqual(ceil_div(10, 4), 3)

    def test_zero_numerator(self) -> None:
        self.assertEqual(ceil_div(0, 5), 0)

    def test_negative_numerator(self) -> None:
        self.assertEqual(ceil_div(-7, 3), -2)
        self.assertEqual(ceil_div(-6, 3), -2)

    def test_negative_divisor(self) -> None:
        self.assertEqual(ceil_div(7, -3), -2)

    def test_division_by_zero_raises(self) -> None:
        with self.assertRaises(ValueError):
            ceil_div(7, 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            ceil_div("7", 3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ceil_div(7, 3.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ceil_div(True, 3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ceil_div(7, None)  # type: ignore[arg-type]


class TestIsKaprekarNumber(unittest.TestCase):
    def test_known_kaprekar_numbers(self) -> None:
        for n in (1, 9, 45, 55, 99, 297, 703, 2223, 2728, 7777):
            self.assertTrue(is_kaprekar_number(n), n)

    def test_zero_is_kaprekar(self) -> None:
        self.assertTrue(is_kaprekar_number(0))

    def test_non_kaprekar_numbers(self) -> None:
        for n in (2, 7, 10, 22, 28, 36, 42, 100):
            self.assertFalse(is_kaprekar_number(n), n)

    def test_negative(self) -> None:
        self.assertFalse(is_kaprekar_number(-1))
        self.assertFalse(is_kaprekar_number(-45))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_kaprekar_number("45")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_kaprekar_number(45.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_kaprekar_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_kaprekar_number(None)  # type: ignore[arg-type]


class TestIsPentagonalNumber(unittest.TestCase):
    def test_known_pentagonal_numbers(self) -> None:
        for n in (0, 1, 5, 12, 22, 35, 51, 70):
            self.assertTrue(is_pentagonal_number(n), n)

    def test_non_pentagonal_numbers(self) -> None:
        for n in (2, 3, 4, 6, 7, 8, 9, 10, 11):
            self.assertFalse(is_pentagonal_number(n), n)

    def test_negatives(self) -> None:
        for n in (-1, -5):
            self.assertFalse(is_pentagonal_number(n), n)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_pentagonal_number("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_pentagonal_number(5.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_pentagonal_number(True)  # type: ignore[arg-type]


class TestIsHexagonalNumber(unittest.TestCase):
    def test_known_hexagonal_numbers(self) -> None:
        for n in (0, 1, 6, 15, 28, 45, 66, 91):
            self.assertTrue(is_hexagonal_number(n), n)

    def test_non_hexagonal_numbers(self) -> None:
        for n in (2, 3, 4, 5, 7, 8, 9, 10, 11, 12):
            self.assertFalse(is_hexagonal_number(n), n)

    def test_negatives(self) -> None:
        for n in (-1, -6):
            self.assertFalse(is_hexagonal_number(n), n)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_hexagonal_number("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_hexagonal_number(6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_hexagonal_number(True)  # type: ignore[arg-type]


class TestIsUglyNumber(unittest.TestCase):
    def test_known_ugly_numbers(self) -> None:
        for n in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30):
            self.assertTrue(is_ugly_number(n), n)

    def test_non_ugly_numbers(self) -> None:
        for n in (7, 11, 13, 14, 17, 19, 21, 22, 26, 28, 49, 77):
            self.assertFalse(is_ugly_number(n), n)

    def test_zero_and_negatives(self) -> None:
        self.assertFalse(is_ugly_number(0))
        for n in (-1, -6, -30):
            self.assertFalse(is_ugly_number(n))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_ugly_number("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_ugly_number(6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_ugly_number(True)  # type: ignore[arg-type]


class TestIsSquarefreeNumber(unittest.TestCase):
    def test_squarefree_numbers(self) -> None:

        for n in (1, 2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 21, 22, 23, 26, 29, 30):
            self.assertTrue(is_squarefree_number(n), n)

    def test_non_squarefree_numbers(self) -> None:

        for n in (4, 8, 9, 12, 16, 18, 20, 24, 25, 27, 28, 32, 36, 40, 44, 45, 48, 49, 50):
            self.assertFalse(is_squarefree_number(n), n)

    def test_zero_and_negatives(self) -> None:

        self.assertFalse(is_squarefree_number(0))
        for n in (-1, -4, -12):
            self.assertFalse(is_squarefree_number(n))

    def test_type_errors(self) -> None:

        with self.assertRaises(TypeError):
            is_squarefree_number("6")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_squarefree_number(6.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_squarefree_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_squarefree_number(None)  # type: ignore[arg-type]


class TestIsOblongNumber(unittest.TestCase):
    def test_oblong_numbers(self) -> None:
        from number_utils import is_oblong_number

        for n in (0, 2, 6, 12, 20, 30, 42, 56, 72, 90):
            self.assertTrue(is_oblong_number(n), n)

    def test_non_oblong_numbers(self) -> None:
        from number_utils import is_oblong_number

        for n in (1, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19):
            self.assertFalse(is_oblong_number(n), n)

    def test_negatives(self) -> None:
        from number_utils import is_oblong_number

        self.assertFalse(is_oblong_number(-1))

    def test_type_errors(self) -> None:
        from number_utils import is_duck_number

        with self.assertRaises(TypeError):
            is_duck_number("10")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_duck_number(10.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_duck_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_duck_number(None)  # type: ignore[arg-type]


class TestIsPowerfulNumber(unittest.TestCase):
    def test_powerful_numbers(self) -> None:
        for n in (1, 4, 8, 9, 16, 25, 27, 32, 36, 49, 64, 72, 81, 100, 108, 121, 125, 128,
                  144, 169, 196, 200):
            self.assertTrue(is_powerful_number(n), n)

    def test_non_powerful_numbers(self) -> None:
        for n in (0, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26,
                  28, 30, 44, 45, 50, 52, 54, 56, 60, 66, 68, 70, 75, 78, 90, 98, 99):
            self.assertFalse(is_powerful_number(n), n)

    def test_negatives(self) -> None:
        self.assertFalse(is_powerful_number(-1))
        self.assertFalse(is_powerful_number(-4))
        self.assertFalse(is_powerful_number(-72))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_powerful_number("4")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_powerful_number(4.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_powerful_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_powerful_number(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestIsMersenneNumber(unittest.TestCase):
    def test_mersenne_numbers(self) -> None:
        for n in (1, 3, 7, 15, 31, 63, 127, 255, 511, 1023):
            self.assertTrue(is_mersenne_number(n), n)

    def test_non_mersenne_numbers(self) -> None:
        for n in (0, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17, 23):
            self.assertFalse(is_mersenne_number(n), n)

    def test_float_values(self) -> None:
        self.assertTrue(is_mersenne_number(7.0))
        self.assertFalse(is_mersenne_number(5.0))
        self.assertFalse(is_mersenne_number(7.5))
        self.assertFalse(is_mersenne_number(float("nan")))
        self.assertFalse(is_mersenne_number(float("inf")))
        self.assertFalse(is_mersenne_number(float("-inf")))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_mersenne_number("7")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_mersenne_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_mersenne_number(None)  # type: ignore[arg-type]


class TestIsDuckNumber(unittest.TestCase):
    def test_duck_numbers(self) -> None:
        from number_utils import is_duck_number

        for n in (10, 20, 101, 102, 120, 203, 1000, 1203):
            self.assertTrue(is_duck_number(n), n)

    def test_non_duck_numbers(self) -> None:
        from number_utils import is_duck_number

        for n in (0, 1, 5, 9, 12, 123, 999, -10):
            self.assertFalse(is_duck_number(n), n)

    def test_type_errors(self) -> None:
        from number_utils import is_duck_number

        with self.assertRaises(TypeError):
            is_duck_number("10")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_duck_number(10.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_duck_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_duck_number(None)  # type: ignore[arg-type]


class TestIsMersennePrime(unittest.TestCase):
    def test_mersenne_primes(self) -> None:
        from number_utils import is_mersenne_prime

        for n in (3, 7, 31, 127, 8191):
            self.assertTrue(is_mersenne_prime(n), n)

    def test_non_mersenne_primes(self) -> None:
        from number_utils import is_mersenne_prime

        # Mersenne numbers but not prime, primes not of form 2^p-1, and other values
        for n in (1, 15, 63, 255, 511, 2, 5, 11, 13, 17, 8193):
            self.assertFalse(is_mersenne_prime(n), n)

    def test_type_errors(self) -> None:
        from number_utils import is_mersenne_prime

        with self.assertRaises(TypeError):
            is_mersenne_prime(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_mersenne_prime(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_mersenne_prime("7")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_mersenne_prime(None)  # type: ignore[arg-type]

    def test_special_floats(self) -> None:
        from number_utils import is_mersenne_prime

        self.assertFalse(is_mersenne_prime(float("nan")))
        self.assertFalse(is_mersenne_prime(float("inf")))
        self.assertFalse(is_mersenne_prime(float("-inf")))
        self.assertFalse(is_mersenne_prime(7.5))


class TestGcdList(unittest.TestCase):
    def test_known(self) -> None:
        self.assertEqual(gcd_list([48, 18, 30]), 6)
        self.assertEqual(gcd_list([17, 19]), 1)

    def test_single(self) -> None:
        self.assertEqual(gcd_list([5]), 5)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            gcd_list([])

    def test_all_equal(self) -> None:
        self.assertEqual(gcd_list([7, 7, 7]), 7)

    def test_negative_values(self) -> None:
        self.assertEqual(gcd_list([-12, 18]), 6)
        self.assertEqual(gcd_list([-4, -6]), 2)

    def test_tuple_input(self) -> None:
        self.assertEqual(gcd_list((12, 18, 24)), 6)

    def test_zeros(self) -> None:
        self.assertEqual(gcd_list([0]), 0)
        self.assertEqual(gcd_list([0, 5]), 5)
        self.assertEqual(gcd_list([0, 0]), 0)
        self.assertEqual(gcd_list([0, 0, 0]), 0)

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            gcd_list("abc")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            gcd_list([1, 2.0])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            gcd_list([1, True])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            gcd_list([False, 1])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            gcd_list([float("nan")])  # type: ignore[list-item]


class TestLcmList(unittest.TestCase):
    def test_known(self) -> None:
        self.assertEqual(lcm_list([4, 6, 8]), 24)
        self.assertEqual(lcm_list([7, 13]), 91)

    def test_single(self) -> None:
        self.assertEqual(lcm_list([5]), 5)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            lcm_list([])

    def test_all_equal(self) -> None:
        self.assertEqual(lcm_list([6, 6, 6]), 6)

    def test_negative_values(self) -> None:
        self.assertEqual(lcm_list([-4, 6]), 12)

    def test_tuple_input(self) -> None:
        self.assertEqual(lcm_list((4, 6)), 12)

    def test_zero_single(self) -> None:
        self.assertEqual(lcm_list([0]), 0)

    def test_zero_with_nonzero(self) -> None:
        self.assertEqual(lcm_list([0, 5]), 0)
        self.assertEqual(lcm_list([4, 0]), 0)

    def test_all_zero_raises(self) -> None:
        with self.assertRaises(ValueError):
            lcm_list([0, 0])

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            lcm_list("abc")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lcm_list([1, 2.0])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            lcm_list([1, True])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            lcm_list([False, 1])  # type: ignore[list-item]
        with self.assertRaises(TypeError):
            lcm_list([float("inf")])  # type: ignore[list-item]


class TestIsPrime(unittest.TestCase):
    def test_primes(self) -> None:
        from number_utils import is_prime

        for n in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 97, 7919):
            self.assertTrue(is_prime(n), n)

    def test_non_primes(self) -> None:
        from number_utils import is_prime

        for n in (0, 1, -7, 4, 6, 8, 9, 15, 21, 25, 27, 100, 7921):
            self.assertFalse(is_prime(n), n)

    def test_type_errors(self) -> None:
        from number_utils import is_prime

        with self.assertRaises(TypeError):
            is_prime(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime(2.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime("7")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_prime(None)  # type: ignore[arg-type]


class TestIntegerNthRoot(unittest.TestCase):
    def test_exact_roots(self) -> None:
        self.assertEqual(integer_nth_root(27, 3), (3, True))
        self.assertEqual(integer_nth_root(16, 4), (2, True))
        self.assertEqual(integer_nth_root(0, 5), (0, True))
        self.assertEqual(integer_nth_root(1, 10), (1, True))
        self.assertEqual(integer_nth_root(81, 2), (9, True))
        self.assertEqual(integer_nth_root(2**60, 2), (2**30, True))

    def test_non_exact_roots(self) -> None:
        self.assertEqual(integer_nth_root(10, 2), (3, False))
        self.assertEqual(integer_nth_root(26, 3), (2, False))
        self.assertEqual(integer_nth_root(2, 3), (1, False))

    def test_negative_odd_root(self) -> None:
        self.assertEqual(integer_nth_root(-8, 3), (-2, True))
        self.assertEqual(integer_nth_root(-27, 3), (-3, True))
        self.assertEqual(integer_nth_root(-10, 3), (-2, False))

    def test_integer_valued_floats(self) -> None:
        self.assertEqual(integer_nth_root(27.0, 3.0), (3, True))

    def test_invalid_degree(self) -> None:
        with self.assertRaises(ValueError):
            integer_nth_root(8, 0)
        with self.assertRaises(ValueError):
            integer_nth_root(8, -2)
        with self.assertRaises(ValueError):
            integer_nth_root(8, 2.5)

    def test_non_integer_value(self) -> None:
        with self.assertRaises(ValueError):
            integer_nth_root(2.5, 2)

    def test_even_root_negative(self) -> None:
        with self.assertRaises(ValueError):
            integer_nth_root(-16, 2)
        with self.assertRaises(ValueError):
            integer_nth_root(-1, 4)

    def test_special_value_rejection(self) -> None:
        for v in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                integer_nth_root(v, 2)  # type: ignore[arg-type]
            with self.assertRaises(ValueError):
                integer_nth_root(2, v)  # type: ignore[arg-type]

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            integer_nth_root("27", 3)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            integer_nth_root(27, "3")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            integer_nth_root(True, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            integer_nth_root(8, False)  # type: ignore[arg-type]


class TestIsCatalanNumber(unittest.TestCase):
    def test_catalan_numbers(self) -> None:
        for n in (1, 2, 5, 14, 42, 132, 429, 1430, 4862):
            self.assertTrue(is_catalan_number(n), n)

    def test_non_catalan_numbers(self) -> None:
        for n in (3, 4, 6, 13, 15, 41, 43, 100):
            self.assertFalse(is_catalan_number(n), n)

    def test_zero_and_negative(self) -> None:
        self.assertFalse(is_catalan_number(0))
        self.assertFalse(is_catalan_number(-1))
        self.assertFalse(is_catalan_number(-14))

    def test_type_errors(self) -> None:
        with self.assertRaises(TypeError):
            is_catalan_number(True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_catalan_number(False)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_catalan_number("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_catalan_number(5.0)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_catalan_number(None)  # type: ignore[arg-type]


class TestBoolRejectionNumberUtils(unittest.TestCase):
    def test_clamp_rejects_bool(self):
        with self.assertRaises(TypeError):
            clamp(True, 0, 1)

    def test_gcd_rejects_bool(self):
        with self.assertRaises(TypeError):
            gcd(True, 2)

    def test_is_even_rejects_bool(self):
        from number_utils import is_even
        with self.assertRaises(TypeError):
            is_even(True)

    def test_is_odd_rejects_bool(self):
        from number_utils import is_odd
        with self.assertRaises(TypeError):
            is_odd(True)

    def test_is_integer_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_integer(True)

    def test_sign_rejects_bool(self):
        with self.assertRaises(TypeError):
            sign(True)

    def test_safe_divide_rejects_bool(self):
        with self.assertRaises(TypeError):
            safe_divide(True, 2)

    def test_lerp_rejects_bool(self):
        with self.assertRaises(TypeError):
            lerp(True, 0, 1)

    def test_is_between_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_between(True, 0, 1)

    def test_integer_nth_root_rejects_bool(self):
        with self.assertRaises(TypeError):
            integer_nth_root(True, 2)
