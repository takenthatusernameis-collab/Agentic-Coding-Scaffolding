import unittest

from calculator import (
    abs_difference,
    absolute,
    add,
    average_of_two,
    clamp,
    divide,
    factorial,
    gcd,
    is_even,
    is_odd,
    is_prime,
    lcm,
    mod_pow,
    multiply,
    negate,
    percentage,
    permutation,
    power,
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

    def test_reciprocal(self):
        self.assertEqual(reciprocal(2), 0.5)
        with self.assertRaises(ValueError):
            reciprocal(0)
        with self.assertRaises(TypeError):
            reciprocal(True)

    def test_percentage(self):
        self.assertEqual(percentage(200, 10), 20.0)
        with self.assertRaises(TypeError):
            percentage(True, 10)

    def test_average_of_two(self):
        self.assertEqual(average_of_two(2, 4), 3.0)
        with self.assertRaises(TypeError):
            average_of_two(True, 4)


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


if __name__ == "__main__":
    unittest.main()

    def test_permutation_rejects_negative(self):
        with self.assertRaises(ValueError):
            permutation(-1, 2)
        with self.assertRaises(ValueError):
            permutation(1, -1)

    def test_permutation_rejects_k_greater_than_n(self):
        with self.assertRaises(ValueError):
            permutation(2, 3)


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
