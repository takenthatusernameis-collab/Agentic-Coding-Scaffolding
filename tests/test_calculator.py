import unittest

from calculator import add, divide, multiply, subtract, modulo, floor_divide, power, sqrt, negate, absolute


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


if __name__ == "__main__":
    unittest.main()
