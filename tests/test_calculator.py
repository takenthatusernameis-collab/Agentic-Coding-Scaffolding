import math
import unittest

from calculator import (
    abs_difference,
    absolute,
    add,
    average_of_two,
    clamp,
    combination,
    distance,
    divide,
    factorial,
    floor_divide,
    gcd,
    hypotenuse,
    is_coprime,
    is_even,
    is_odd,
    is_perfect_square,
    is_power_of_two,
    is_prime,
    lcm,
    mod_pow,
    modulo,
    multiply,
    negate,
    percentage,
    permutation,
    power,
    prime_factors,
    reciprocal,
    round_to,
    sign,
    sqrt,
    subtract,
)


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_add_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            add("2", 3)
        with self.assertRaises(TypeError):
            add(2, "3")
        with self.assertRaises(TypeError):
            add(None, 2)

    def test_add_rejects_nan(self):
        with self.assertRaises(ValueError):
            add(float("nan"), 2)
        with self.assertRaises(ValueError):
            add(2, float("nan"))

    def test_add_rejects_infinity(self):
        with self.assertRaises(ValueError):
            add(float("inf"), 2)
        with self.assertRaises(ValueError):
            add(2, float("-inf"))

    def test_add_rejects_bool(self):
        with self.assertRaises(TypeError):
            add(True, 2)
        with self.assertRaises(TypeError):
            add(2, False)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(-1, -1), 0)

    def test_subtract_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            subtract("5", 3)
        with self.assertRaises(TypeError):
            subtract(5, "3")
        with self.assertRaises(TypeError):
            subtract(None, 3)

    def test_subtract_rejects_bool(self):
        with self.assertRaises(TypeError):
            subtract(True, 3)
        with self.assertRaises(TypeError):
            subtract(5, False)

    def test_subtract_rejects_nan(self):
        with self.assertRaises(ValueError):
            subtract(float("nan"), 3)
        with self.assertRaises(ValueError):
            subtract(5, float("nan"))

    def test_subtract_rejects_infinity(self):
        with self.assertRaises(ValueError):
            subtract(float("inf"), 3)
        with self.assertRaises(ValueError):
            subtract(5, float("-inf"))

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 5), 0)

    def test_multiply_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            multiply("3", 4)
        with self.assertRaises(TypeError):
            multiply(3, "4")
        with self.assertRaises(TypeError):
            multiply(None, 4)

    def test_multiply_rejects_bool(self):
        with self.assertRaises(TypeError):
            multiply(True, 4)
        with self.assertRaises(TypeError):
            multiply(3, False)

    def test_multiply_rejects_nan(self):
        with self.assertRaises(ValueError):
            multiply(float("nan"), 4)
        with self.assertRaises(ValueError):
            multiply(3, float("nan"))

    def test_multiply_rejects_infinity(self):
        with self.assertRaises(ValueError):
            multiply(float("inf"), 4)
        with self.assertRaises(ValueError):
            multiply(3, float("-inf"))

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)
        self.assertEqual(divide(9, 3), 3)
        self.assertEqual(divide(-6, 3), -2)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(5, 0)

    def test_divide_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            divide("10", 2)
        with self.assertRaises(TypeError):
            divide(10, "2")
        with self.assertRaises(TypeError):
            divide(None, 2)

    def test_divide_rejects_bool(self):
        with self.assertRaises(TypeError):
            divide(True, 2)
        with self.assertRaises(TypeError):
            divide(10, False)

    def test_divide_rejects_nan(self):
        with self.assertRaises(ValueError):
            divide(float("nan"), 2)
        with self.assertRaises(ValueError):
            divide(10, float("nan"))

    def test_divide_rejects_infinity(self):
        with self.assertRaises(ValueError):
            divide(float("inf"), 2)
        with self.assertRaises(ValueError):
            divide(10, float("-inf"))

    def test_power_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            power("2", 3)
        with self.assertRaises(TypeError):
            power(2, "3")
        with self.assertRaises(TypeError):
            power(None, 3)

    def test_power_rejects_bool(self):
        with self.assertRaises(TypeError):
            power(True, 3)
        with self.assertRaises(TypeError):
            power(2, False)

    def test_power_overflow_raises_value_error(self):
        # Results beyond the finite float range must surface as ValueError
        # (the documented contract), not a leaked OverflowError.
        with self.assertRaises(ValueError):
            power(10, 400)
        with self.assertRaises(ValueError):
            power(10.0, 400)
        with self.assertRaises(ValueError):
            power(2, 2000)

    def test_sqrt(self):
        self.assertEqual(sqrt(9), 3)
        self.assertEqual(sqrt(4), 2)
        with self.assertRaises(ValueError):
            sqrt(-1)

    def test_sqrt_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            sqrt("9")
        with self.assertRaises(TypeError):
            sqrt(None)

    def test_sqrt_rejects_bool(self):
        with self.assertRaises(TypeError):
            sqrt(True)

    def test_sqrt_accepts_huge_int(self):
        # A huge int whose square root is still too large for a finite float
        # must surface as ValueError (the documented contract), not a leaked
        # OverflowError from the float() conversion.
        with self.assertRaises(ValueError):
            sqrt(10**400)
        with self.assertRaises(ValueError):
            sqrt(2**2000)

    def test_negate(self):
        self.assertEqual(negate(5), -5)
        self.assertEqual(negate(-3), 3)
        self.assertEqual(negate(0), 0)

    def test_negate_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            negate("5")
        with self.assertRaises(TypeError):
            negate(None)

    def test_negate_rejects_bool(self):
        with self.assertRaises(TypeError):
            negate(True)

    def test_negate_rejects_nan(self):
        with self.assertRaises(ValueError):
            negate(float("nan"))

    def test_negate_rejects_infinity(self):
        with self.assertRaises(ValueError):
            negate(float("inf"))
        with self.assertRaises(ValueError):
            negate(float("-inf"))

    def test_absolute(self):
        self.assertEqual(absolute(5), 5)
        self.assertEqual(absolute(-3), 3)
        self.assertEqual(absolute(0), 0)

    def test_absolute_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            absolute("5")
        with self.assertRaises(TypeError):
            absolute(None)

    def test_absolute_rejects_bool(self):
        with self.assertRaises(TypeError):
            absolute(True)

    def test_absolute_rejects_nan(self):
        with self.assertRaises(ValueError):
            absolute(float("nan"))

    def test_absolute_rejects_infinity(self):
        with self.assertRaises(ValueError):
            absolute(float("inf"))
        with self.assertRaises(ValueError):
            absolute(float("-inf"))

    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-1, 0, 10), 0)
        self.assertEqual(clamp(11, 0, 10), 10)

    def test_clamp_rejects_low_greater_than_high(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)

    def test_clamp_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            clamp("5", 0, 10)
        with self.assertRaises(TypeError):
            clamp(5, "0", 10)
        with self.assertRaises(TypeError):
            clamp(5, 0, "10")
        with self.assertRaises(TypeError):
            clamp(None, 0, 10)

    def test_clamp_rejects_bool(self):
        with self.assertRaises(TypeError):
            clamp(True, 0, 10)
        with self.assertRaises(TypeError):
            clamp(5, False, 10)
        with self.assertRaises(TypeError):
            clamp(5, 0, False)


class TestAbsDifference(unittest.TestCase):
    def test_abs_difference_positive(self):
        self.assertEqual(abs_difference(5, 3), 2)

    def test_abs_difference_reversed(self):
        self.assertEqual(abs_difference(3, 5), 2)

    def test_abs_difference_equal(self):
        self.assertEqual(abs_difference(4, 4), 0)

    def test_abs_difference_both_negative(self):
        self.assertEqual(abs_difference(-2, -5), 3)

    def test_abs_difference_mixed_signs(self):
        self.assertEqual(abs_difference(-3, 5), 8)

    def test_abs_difference_floats(self):
        self.assertEqual(abs_difference(5.5, 3.2), 2.3)

    def test_abs_difference_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            abs_difference("5", 3)
        with self.assertRaises(TypeError):
            abs_difference(5, "3")
        with self.assertRaises(TypeError):
            abs_difference(None, 3)

    def test_abs_difference_rejects_bool(self):
        with self.assertRaises(TypeError):
            abs_difference(True, 3)
        with self.assertRaises(TypeError):
            abs_difference(5, False)

    def test_abs_difference_rejects_nan(self):
        with self.assertRaises(ValueError):
            abs_difference(float("nan"), 3)
        with self.assertRaises(ValueError):
            abs_difference(5, float("nan"))

    def test_abs_difference_rejects_infinity(self):
        with self.assertRaises(ValueError):
            abs_difference(float("inf"), 3)
        with self.assertRaises(ValueError):
            abs_difference(5, float("-inf"))


class TestClamp(unittest.TestCase):
    def test_clamp_within_range(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_clamp_below_low(self):
        self.assertEqual(clamp(-3, 0, 10), 0)

    def test_clamp_above_high(self):
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_clamp_boundary(self):
        self.assertEqual(clamp(0, 0, 10), 0)
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_clamp_invalid_range(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)

    def test_clamp_accepts_huge_int_endpoints(self):
        # ``math.isnan`` raises ``OverflowError`` for an int too large to
        # convert to a float; a huge int is a valid real endpoint and must not
        # crash the NaN guard before clamping runs.
        self.assertEqual(clamp(15, 0, 10**400), 15)
        self.assertEqual(clamp(10**400, 0, 10), 10)
        self.assertEqual(clamp(-(10**400), 0, 10), 0)

    def test_reciprocal(self):
        self.assertEqual(reciprocal(2), 0.5)
        with self.assertRaises(ValueError):
            reciprocal(0)
        with self.assertRaises(TypeError):
            reciprocal(True)

    def test_reciprocal_rejects_nan(self):
        with self.assertRaises(ValueError):
            reciprocal(float("nan"))

    def test_reciprocal_rejects_infinity(self):
        with self.assertRaises(ValueError):
            reciprocal(float("inf"))
        with self.assertRaises(ValueError):
            reciprocal(float("-inf"))

    def test_float_only_conversions_reject_huge_int(self):
        # Huge ints pass the isinstance((int, float)) + finite checks, so the
        # float-only result conversions must surface OverflowError as the
        # documented ValueError rather than leaking it.
        with self.assertRaises(ValueError):
            reciprocal(10**400)
        with self.assertRaises(ValueError):
            percentage(10**400, 10**400)
        with self.assertRaises(ValueError):
            average_of_two(10**400, 10**400)
        with self.assertRaises(ValueError):
            round_to(10**400, 0)

    def test_percentage(self):
        self.assertEqual(percentage(200, 10), 20.0)
        with self.assertRaises(TypeError):
            percentage(True, 10)

    def test_percentage_rejects_nan(self):
        with self.assertRaises(ValueError):
            percentage(float("nan"), 10)
        with self.assertRaises(ValueError):
            percentage(10, float("nan"))

    def test_percentage_rejects_infinity(self):
        with self.assertRaises(ValueError):
            percentage(float("inf"), 10)
        with self.assertRaises(ValueError):
            percentage(10, float("-inf"))

    def test_average_of_two(self):
        self.assertEqual(average_of_two(2, 4), 3.0)
        with self.assertRaises(TypeError):
            average_of_two(True, 4)

    def test_average_of_two_rejects_nan(self):
        with self.assertRaises(ValueError):
            average_of_two(float("nan"), 4)
        with self.assertRaises(ValueError):
            average_of_two(4, float("nan"))

    def test_average_of_two_rejects_infinity(self):
        with self.assertRaises(ValueError):
            average_of_two(float("inf"), 4)
        with self.assertRaises(ValueError):
            average_of_two(4, float("-inf"))


class TestRoundTo(unittest.TestCase):
    def test_round_to_zero_places(self):
        self.assertEqual(round_to(2.5), 2.0)
        self.assertEqual(round_to(3.5), 4.0)
        self.assertEqual(round_to(2.4), 2.0)
        self.assertEqual(round_to(-2.5), -2.0)

    def test_round_to_custom_places(self):
        self.assertEqual(round_to(3.14159, 2), 3.14)
        self.assertEqual(round_to(3.146, 2), 3.15)
        self.assertEqual(round_to(2.674, 2), 2.67)
        self.assertEqual(round_to(10, 0), 10.0)

    def test_round_to_integer_input(self):
        self.assertEqual(round_to(7), 7.0)
        self.assertEqual(round_to(7, 3), 7.0)

    def test_round_to_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            round_to("2.5")
        with self.assertRaises(TypeError):
            round_to(None)
        with self.assertRaises(TypeError):
            round_to([1, 2])

    def test_round_to_rejects_bool(self):
        with self.assertRaises(TypeError):
            round_to(True)
        with self.assertRaises(TypeError):
            round_to(False)

    def test_round_to_rejects_non_int_places(self):
        with self.assertRaises(TypeError):
            round_to(2.5, "2")
        with self.assertRaises(TypeError):
            round_to(2.5, None)
        with self.assertRaises(TypeError):
            round_to(2.5, True)

    def test_round_to_rejects_negative_places(self):
        with self.assertRaises(ValueError):
            round_to(2.5, -1)


class TestFactorial(unittest.TestCase):
    def test_factorial_base_cases(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(3), 6)
        self.assertEqual(factorial(5), 120)

    def test_factorial_rejects_non_int(self):
        with self.assertRaises(TypeError):
            factorial(5.0)
        with self.assertRaises(TypeError):
            factorial("5")
        with self.assertRaises(TypeError):
            factorial(None)

    def test_factorial_rejects_bool(self):
        with self.assertRaises(TypeError):
            factorial(True)
        with self.assertRaises(TypeError):
            factorial(False)

    def test_factorial_rejects_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)


class TestGCD(unittest.TestCase):
    def test_gcd_basic(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(18, 48), 6)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(0, 0), 0)

    def test_gcd_rejects_non_int(self):
        with self.assertRaises(TypeError):
            gcd(4.0, 2)
        with self.assertRaises(TypeError):
            gcd(4, "2")

    def test_gcd_rejects_bool(self):
        with self.assertRaises(TypeError):
            gcd(True, 2)
        with self.assertRaises(TypeError):
            gcd(2, False)

    def test_gcd_rejects_negative(self):
        with self.assertRaises(ValueError):
            gcd(-1, 2)
        with self.assertRaises(ValueError):
            gcd(1, -1)


class TestLCM(unittest.TestCase):
    def test_lcm_basic(self):
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(3, 5), 15)
        self.assertEqual(lcm(0, 5), 0)
        self.assertEqual(lcm(5, 0), 0)

    def test_lcm_rejects_non_int(self):
        with self.assertRaises(TypeError):
            lcm(4.0, 2)
        with self.assertRaises(TypeError):
            lcm(4, "2")

    def test_lcm_rejects_bool(self):
        with self.assertRaises(TypeError):
            lcm(True, 2)
        with self.assertRaises(TypeError):
            lcm(2, False)

    def test_lcm_rejects_negative(self):
        with self.assertRaises(ValueError):
            lcm(-1, 2)
        with self.assertRaises(ValueError):
            lcm(1, -1)


class TestIsEven(unittest.TestCase):
    def test_is_even_basic(self):
        self.assertTrue(is_even(2))
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(-4))
        self.assertFalse(is_even(3))
        self.assertFalse(is_even(-1))

    def test_is_even_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_even(2.0)
        with self.assertRaises(TypeError):
            is_even("2")

    def test_is_even_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_even(True)
        with self.assertRaises(TypeError):
            is_even(False)


class TestIsOdd(unittest.TestCase):
    def test_is_odd_basic(self):
        self.assertTrue(is_odd(3))
        self.assertTrue(is_odd(-1))
        self.assertFalse(is_odd(2))
        self.assertFalse(is_odd(0))

    def test_is_odd_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_odd(3.0)
        with self.assertRaises(TypeError):
            is_odd("3")

    def test_is_odd_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_odd(True)
        with self.assertRaises(TypeError):
            is_odd(False)


class TestIsPerfectSquare(unittest.TestCase):
    def test_is_perfect_square_basic(self):
        self.assertTrue(is_perfect_square(0))
        self.assertTrue(is_perfect_square(1))
        self.assertTrue(is_perfect_square(4))
        self.assertTrue(is_perfect_square(9))
        self.assertTrue(is_perfect_square(16))
        self.assertTrue(is_perfect_square(25))
        self.assertTrue(is_perfect_square(144))
        self.assertFalse(is_perfect_square(2))
        self.assertFalse(is_perfect_square(3))
        self.assertFalse(is_perfect_square(8))
        self.assertFalse(is_perfect_square(10))
        self.assertFalse(is_perfect_square(2))
        self.assertFalse(is_perfect_square(50))

    def test_is_perfect_square_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_perfect_square(4.0)
        with self.assertRaises(TypeError):
            is_perfect_square("4")

    def test_is_perfect_square_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_perfect_square(True)
        with self.assertRaises(TypeError):
            is_perfect_square(False)

    def test_is_perfect_square_rejects_negative(self):
        with self.assertRaises(ValueError):
            is_perfect_square(-1)
        with self.assertRaises(ValueError):
            is_perfect_square(-4)

    def test_is_perfect_square_large_perfect_square(self):
        # A large perfect square must be recognised. Float-based ``n**0.5``
        # loses precision here (10**50 is (10**25)**2) and underflows the
        # estimate, so the exact integer check is required.
        self.assertTrue(is_perfect_square(10**50))
        self.assertTrue(is_perfect_square((10**25) ** 2))
        self.assertTrue(is_perfect_square((2**200) ** 2))

    def test_is_perfect_square_large_non_square(self):
        # A large non-square must not be misreported as a square.
        self.assertFalse(is_perfect_square(10**50 + 1))

    def test_is_perfect_square_does_not_overflow(self):
        # ``n**0.5`` raises OverflowError for integers too large to convert to
        # float; the exact integer check must handle arbitrarily large ints.
        self.assertTrue(is_perfect_square(10**400))
        self.assertFalse(is_perfect_square(10**400 + 1))


class TestIsCoprime(unittest.TestCase):
    def test_is_coprime_basic(self):
        self.assertTrue(is_coprime(2, 3))
        self.assertTrue(is_coprime(3, 2))
        self.assertTrue(is_coprime(4, 9))
        self.assertTrue(is_coprime(1, 5))
        self.assertTrue(is_coprime(5, 1))
        self.assertFalse(is_coprime(4, 6))
        self.assertFalse(is_coprime(6, 9))
        self.assertTrue(is_coprime(0, 1))
        self.assertTrue(is_coprime(1, 0))

    def test_is_coprime_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_coprime(2.0, 3)
        with self.assertRaises(TypeError):
            is_coprime(2, "3")

    def test_is_coprime_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_coprime(True, 3)
        with self.assertRaises(TypeError):
            is_coprime(2, False)

    def test_is_coprime_rejects_negative(self):
        with self.assertRaises(ValueError):
            is_coprime(-1, 2)
        with self.assertRaises(ValueError):
            is_coprime(2, -3)


class TestModulo(unittest.TestCase):
    def test_modulo_basic(self):
        self.assertEqual(modulo(10, 3), 1)
        self.assertEqual(modulo(10, 5), 0)
        self.assertEqual(modulo(-10, 3), 2)
        self.assertEqual(modulo(10, -3), -2)
        self.assertEqual(modulo(0, 5), 0)

    def test_modulo_by_zero(self):
        with self.assertRaises(ValueError):
            modulo(5, 0)

    def test_modulo_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            modulo("10", 3)
        with self.assertRaises(TypeError):
            modulo(10, "3")
        with self.assertRaises(TypeError):
            modulo(None, 3)

    def test_modulo_rejects_bool(self):
        with self.assertRaises(TypeError):
            modulo(True, 3)
        with self.assertRaises(TypeError):
            modulo(10, False)


class TestFloorDivide(unittest.TestCase):
    def test_floor_divide_basic(self):
        self.assertEqual(floor_divide(10, 3), 3)
        self.assertEqual(floor_divide(10, 5), 2)
        self.assertEqual(floor_divide(-10, 3), -4)
        self.assertEqual(floor_divide(0, 5), 0)

    def test_floor_divide_by_zero(self):
        with self.assertRaises(ValueError):
            floor_divide(5, 0)

    def test_floor_divide_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            floor_divide("10", 3)
        with self.assertRaises(TypeError):
            floor_divide(10, "3")
        with self.assertRaises(TypeError):
            floor_divide(None, 3)

    def test_floor_divide_rejects_bool(self):
        with self.assertRaises(TypeError):
            floor_divide(True, 3)
        with self.assertRaises(TypeError):
            floor_divide(10, False)


class TestCombination(unittest.TestCase):
    def test_combination_basic(self):
        self.assertEqual(combination(5, 2), 10)
        self.assertEqual(combination(5, 0), 1)
        self.assertEqual(combination(5, 5), 1)
        self.assertEqual(combination(0, 0), 1)
        self.assertEqual(combination(10, 3), 120)

    def test_combination_rejects_non_int(self):
        with self.assertRaises(TypeError):
            combination(5.0, 2)
        with self.assertRaises(TypeError):
            combination(5, "2")
        with self.assertRaises(TypeError):
            combination(None, 2)

    def test_combination_rejects_bool(self):
        with self.assertRaises(TypeError):
            combination(True, 2)
        with self.assertRaises(TypeError):
            combination(5, False)

    def test_combination_rejects_negative(self):
        with self.assertRaises(ValueError):
            combination(-1, 2)
        with self.assertRaises(ValueError):
            combination(5, -1)

    def test_combination_rejects_k_greater_than_n(self):
        with self.assertRaises(ValueError):
            combination(2, 3)


class TestPermutation(unittest.TestCase):
    def test_permutation_basic(self):
        self.assertEqual(permutation(5, 2), 20)
        self.assertEqual(permutation(5, 0), 1)
        self.assertEqual(permutation(5, 5), 120)
        self.assertEqual(permutation(0, 0), 1)
        self.assertEqual(permutation(10, 3), 720)
        self.assertEqual(permutation(4, 1), 4)
        self.assertEqual(permutation(6, 6), 720)

    def test_permutation_rejects_non_int(self):
        with self.assertRaises(TypeError):
            permutation(5.0, 2)
        with self.assertRaises(TypeError):
            permutation(5, "2")
        with self.assertRaises(TypeError):
            permutation(None, 2)

    def test_permutation_rejects_bool(self):
        with self.assertRaises(TypeError):
            permutation(True, 2)
        with self.assertRaises(TypeError):
            permutation(5, False)

    def test_permutation_rejects_negative(self):
        with self.assertRaises(ValueError):
            permutation(-1, 2)
        with self.assertRaises(ValueError):
            permutation(5, -1)

    def test_permutation_rejects_k_greater_than_n(self):
        with self.assertRaises(ValueError):
            permutation(2, 3)


class TestIsPowerOfTwo(unittest.TestCase):
    def test_is_power_of_two_basic(self):
        self.assertTrue(is_power_of_two(1))
        self.assertTrue(is_power_of_two(2))
        self.assertTrue(is_power_of_two(4))
        self.assertTrue(is_power_of_two(8))
        self.assertTrue(is_power_of_two(1024))
        self.assertFalse(is_power_of_two(0))
        self.assertFalse(is_power_of_two(3))
        self.assertFalse(is_power_of_two(5))
        self.assertFalse(is_power_of_two(6))
        self.assertFalse(is_power_of_two(1023))

    def test_is_power_of_two_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_power_of_two(4.0)
        with self.assertRaises(TypeError):
            is_power_of_two("4")

    def test_is_power_of_two_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_power_of_two(True)
        with self.assertRaises(TypeError):
            is_power_of_two(False)


class TestPower(unittest.TestCase):
    def test_power_basic(self):
        self.assertEqual(power(2, 3), 8.0)
        self.assertEqual(power(5, 0), 1.0)
        self.assertEqual(power(4, 0.5), 2.0)
        self.assertEqual(power(2, -1), 0.5)

    def test_power_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            power("2", 3)
        with self.assertRaises(TypeError):
            power(2, "3")
        with self.assertRaises(TypeError):
            power(None, 3)

    def test_power_rejects_bool(self):
        with self.assertRaises(TypeError):
            power(True, 3)
        with self.assertRaises(TypeError):
            power(2, False)

    def test_power_rejects_nan(self):
        with self.assertRaises(ValueError):
            power(float("nan"), 2)
        with self.assertRaises(ValueError):
            power(2, float("nan"))

    def test_power_rejects_infinity(self):
        with self.assertRaises(ValueError):
            power(float("inf"), 2)
        with self.assertRaises(ValueError):
            power(float("-inf"), 2)
        with self.assertRaises(ValueError):
            power(2, float("inf"))
        with self.assertRaises(ValueError):
            power(2, float("-inf"))

    def test_power_rejects_negative_base_fractional_exponent(self):
        with self.assertRaises(ValueError):
            power(-1, 0.5)
        with self.assertRaises(ValueError):
            power(-2, 1.5)

    def test_power_rejects_zero_base_negative_exponent(self):
        with self.assertRaises(ValueError):
            power(0, -1)
        with self.assertRaises(ValueError):
            power(0, -2.5)


class TestIsPrime(unittest.TestCase):
    def test_is_prime_basic(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(9))

    def test_is_prime_rejects_non_int(self):
        with self.assertRaises(TypeError):
            is_prime(3.0)
        with self.assertRaises(TypeError):
            is_prime("3")

    def test_is_prime_rejects_bool(self):
        with self.assertRaises(TypeError):
            is_prime(True)
        with self.assertRaises(TypeError):
            is_prime(False)

    def test_is_prime_rejects_less_than_two(self):
        with self.assertRaises(ValueError):
            is_prime(0)
        with self.assertRaises(ValueError):
            is_prime(1)
        with self.assertRaises(ValueError):
            is_prime(-2)

    def test_is_prime_rejects_pseudoprimes(self):
        # 2047 is the smallest strong pseudoprime to base 2 (23 * 89).
        self.assertFalse(is_prime(2047))
        # Other Carmichael numbers / strong pseudoprimes.
        self.assertFalse(is_prime(2465))
        self.assertFalse(is_prime(2821))
        self.assertFalse(is_prime(6601))
        self.assertFalse(is_prime(8911))

    def test_is_prime_known_primes(self):
        for p in (2, 3, 7, 11, 13, 17, 19, 23, 29, 31, 104729, 2147483647):
            self.assertTrue(is_prime(p), f"{p} should be prime")

    def test_is_prime_known_composites(self):
        for c in (4, 6, 8, 10, 100, 1000, 1000000):
            self.assertFalse(is_prime(c), f"{c} should be composite")


class TestPrimeFactors(unittest.TestCase):
    def test_prime_factors_basic(self):
        self.assertEqual(prime_factors(12), [2, 2, 3])
        self.assertEqual(prime_factors(17), [17])
        self.assertEqual(prime_factors(100), [2, 2, 5, 5])
        self.assertEqual(prime_factors(2), [2])

    def test_prime_factors_product_equals_n(self):
        for n in (2, 3, 4, 12, 17, 100, 9973, 1000000):
            factors = prime_factors(n)
            product = 1
            for factor in factors:
                product *= factor
            self.assertEqual(product, n)

    def test_prime_factors_non_decreasing(self):
        for n in (12, 100, 9973, 1000000):
            factors = prime_factors(n)
            self.assertEqual(factors, sorted(factors))

    def test_prime_factors_all_prime(self):
        for n in (12, 100, 9973, 1000000):
            for factor in prime_factors(n):
                self.assertTrue(is_prime(factor))

    def test_prime_factors_rejects_non_int(self):
        with self.assertRaises(TypeError):
            prime_factors(3.0)
        with self.assertRaises(TypeError):
            prime_factors("12")

    def test_prime_factors_rejects_bool(self):
        with self.assertRaises(TypeError):
            prime_factors(True)
        with self.assertRaises(TypeError):
            prime_factors(False)

    def test_prime_factors_rejects_less_than_two(self):
        with self.assertRaises(ValueError):
            prime_factors(0)
        with self.assertRaises(ValueError):
            prime_factors(1)
        with self.assertRaises(ValueError):
            prime_factors(-5)


class TestModPow(unittest.TestCase):
    def test_mod_pow_basic(self):
        self.assertEqual(mod_pow(2, 10, 1000), 24)
        self.assertEqual(mod_pow(3, 2, 10), 9)

    def test_mod_pow_rejects_non_int(self):
        with self.assertRaises(TypeError):
            mod_pow(2.0, 10, 1000)
        with self.assertRaises(TypeError):
            mod_pow(2, "10", 1000)
        with self.assertRaises(TypeError):
            mod_pow(2, 10, 1000.0)

    def test_mod_pow_rejects_bool(self):
        with self.assertRaises(TypeError):
            mod_pow(True, 2, 10)
        with self.assertRaises(TypeError):
            mod_pow(2, False, 10)
        with self.assertRaises(TypeError):
            mod_pow(2, 2, True)

    def test_mod_pow_rejects_negative_exp(self):
        with self.assertRaises(ValueError):
            mod_pow(2, -1, 10)

    def test_mod_pow_rejects_non_positive_mod(self):
        with self.assertRaises(ValueError):
            mod_pow(2, 1, 0)
        with self.assertRaises(ValueError):
            mod_pow(2, 1, -3)


class TestSign(unittest.TestCase):
    def test_sign_basic(self):
        self.assertEqual(sign(5), 1)
        self.assertEqual(sign(-3), -1)
        self.assertEqual(sign(0), 0)
        self.assertEqual(sign(3.14), 1)
        self.assertEqual(sign(-0.5), -1)
        self.assertEqual(sign(-0.0), 0)

    def test_sign_rejects_bool(self):
        with self.assertRaises(TypeError):
            sign(True)
        with self.assertRaises(TypeError):
            sign(False)

    def test_sign_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            sign("5")
        with self.assertRaises(TypeError):
            sign(None)
        with self.assertRaises(TypeError):
            sign([])

    def test_sign_rejects_nan(self):
        with self.assertRaises(ValueError):
            sign(float("nan"))

    def test_sign_accepts_huge_int(self):
        # ``math.isnan`` raises ``OverflowError`` for an int too large to
        # convert to a float; the sign of a huge int is well defined and must
        # not leak that undocumented error.
        self.assertEqual(sign(10**400), 1)
        self.assertEqual(sign(-(10**400)), -1)


class TestHypotenuse(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(hypotenuse(3, 4), 5)
        self.assertEqual(hypotenuse(0, 0), 0)
        self.assertAlmostEqual(hypotenuse(1, 1), 1.4142135623730951)

    def test_hypotenuse_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            hypotenuse("3", 4)
        with self.assertRaises(TypeError):
            hypotenuse(3, None)
        with self.assertRaises(TypeError):
            hypotenuse([], 4)

    def test_hypotenuse_rejects_bool(self):
        with self.assertRaises(TypeError):
            hypotenuse(True, 4)
        with self.assertRaises(TypeError):
            hypotenuse(3, False)

    def test_hypotenuse_rejects_negative(self):
        with self.assertRaises(ValueError):
            hypotenuse(-3, 4)
        with self.assertRaises(ValueError):
            hypotenuse(3, -4)

    def test_hypotenuse_avoids_intermediate_overflow(self):
        self.assertAlmostEqual(
            hypotenuse(1e200, 1e200), math.hypot(1e200, 1e200)
        )
        self.assertAlmostEqual(
            hypotenuse(1e155, 1e155), math.hypot(1e155, 1e155)
        )


class TestDistance(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(distance(0, 0, 3, 4), 5)
        self.assertEqual(distance(0, 0, 0, 0), 0)
        self.assertAlmostEqual(distance(1, 1, 4, 5), 5)

    def test_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            distance("0", 0, 3, 4)
        with self.assertRaises(TypeError):
            distance(0, None, 3, 4)
        with self.assertRaises(TypeError):
            distance(0, 0, [], 4)

    def test_rejects_bool(self):
        with self.assertRaises(TypeError):
            distance(True, 0, 3, 4)
        with self.assertRaises(TypeError):
            distance(0, False, 3, 4)

    def test_distance_avoids_intermediate_overflow(self):
        self.assertAlmostEqual(
            distance(0, 0, 1e200, 1e200), math.hypot(1e200, 1e200)
        )
        self.assertAlmostEqual(
            distance(1e200, 1e200, 0, 0), math.hypot(1e200, 1e200)
        )

    def test_distance_huge_int_raises_value_error(self):
        # ``math.hypot`` converts its arguments to float, so an int too large
        # to convert (for example ``10 ** 400``) raises ``OverflowError``; the
        # documented finite-float contract must surface ``ValueError`` instead.
        with self.assertRaisesRegex(
            ValueError, "result is too large to represent as a finite float"
        ):
            distance(0, 0, 10**400, 0)


if __name__ == "__main__":
    unittest.main()
