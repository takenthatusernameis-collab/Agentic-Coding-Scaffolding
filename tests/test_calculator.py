import unittest

from calculator import (
    absolute,
    clamp,
    abs_difference,
    add,
    divide,
    floor_divide,
    modulo,
    multiply,
    negate,
    power,
    sqrt,
    subtract,
)


class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 5), 0)

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

    def test_modulo(self):
        self.assertEqual(modulo(10, 3), 1)
        self.assertEqual(modulo(9, 3), 0)
        with self.assertRaises(ValueError):
            modulo(5, 0)

    def test_floor_divide(self):
        self.assertEqual(floor_divide(10, 3), 3)
        self.assertEqual(floor_divide(9, 3), 3)
        with self.assertRaises(ValueError):
            floor_divide(5, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(4, 0.5), 2)
        self.assertEqual(power(5, 0), 1)

    def test_sqrt(self):
        self.assertEqual(sqrt(9), 3)
        self.assertEqual(sqrt(4), 2)
        with self.assertRaises(ValueError):
            sqrt(-1)

    def test_negate(self):
        self.assertEqual(negate(5), -5)
        self.assertEqual(negate(-3), 3)
        self.assertEqual(negate(0), 0)

    def test_absolute(self):
        self.assertEqual(absolute(5), 5)
        self.assertEqual(absolute(-3), 3)
        self.assertEqual(absolute(0), 0)


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


if __name__ == "__main__":
    unittest.main()
