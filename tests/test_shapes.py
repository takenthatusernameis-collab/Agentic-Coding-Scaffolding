import math
import unittest

from shapes import (
    circle_area,
    circle_perimeter,
    rectangle_area,
    rectangle_perimeter,
    triangle_area,
    triangle_perimeter,
)


class TestCircle(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(circle_area(0), 0)
        self.assertAlmostEqual(circle_area(1), math.pi)
        self.assertAlmostEqual(circle_area(2), math.pi * 4)

    def test_perimeter(self):
        self.assertAlmostEqual(circle_perimeter(0), 0)
        self.assertAlmostEqual(circle_perimeter(1), 2 * math.pi)
        self.assertAlmostEqual(circle_perimeter(2), 4 * math.pi)

    def test_negative_radius_area(self):
        with self.assertRaises(ValueError):
            circle_area(-1)

    def test_negative_radius_perimeter(self):
        with self.assertRaises(ValueError):
            circle_perimeter(-5)


class TestRectangle(unittest.TestCase):
    def test_area(self):
        self.assertEqual(rectangle_area(3, 4), 12)
        self.assertEqual(rectangle_area(0, 5), 0)
        self.assertEqual(rectangle_area(2.5, 4), 10)

    def test_perimeter(self):
        self.assertEqual(rectangle_perimeter(3, 4), 14)
        self.assertEqual(rectangle_perimeter(0, 0), 0)

    def test_negative_length_area(self):
        with self.assertRaises(ValueError):
            rectangle_area(-1, 4)

    def test_negative_width_perimeter(self):
        with self.assertRaises(ValueError):
            rectangle_perimeter(3, -2)


class TestTriangle(unittest.TestCase):
    def test_area(self):
        self.assertEqual(triangle_area(4, 3), 6)
        self.assertEqual(triangle_area(10, 5), 25)
        self.assertEqual(triangle_area(0, 5), 0)

    def test_perimeter(self):
        self.assertEqual(triangle_perimeter(3, 4, 5), 12)
        self.assertEqual(triangle_perimeter(1, 1, 1), 3)

    def test_invalid_triangle_inequality(self):
        with self.assertRaises(ValueError):
            triangle_perimeter(1, 2, 10)

    def test_negative_base_area(self):
        with self.assertRaises(ValueError):
            triangle_area(-1, 3)

    def test_negative_side_perimeter(self):
        with self.assertRaises(ValueError):
            triangle_perimeter(3, 4, -5)


if __name__ == "__main__":
    unittest.main()
