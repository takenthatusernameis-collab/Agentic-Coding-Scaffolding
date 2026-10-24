import math
import unittest

from shapes import (
    circle_area,
    circle_diameter,
    circle_perimeter,
    ellipse_area,
    parallelogram_area,
    parallelogram_perimeter,
    polygon_area,
    rectangle_area,
    rectangle_diagonal,
    rectangle_perimeter,
    regular_polygon_area,
    rhombus_area,
    rhombus_perimeter,
    square_area,
    square_perimeter,
    trapezoid_area,
    triangle_area,
    triangle_heron_area,
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


class TestSquare(unittest.TestCase):
    def test_area(self):
        self.assertEqual(square_area(4), 16)
        self.assertEqual(square_area(0), 0)
        self.assertEqual(square_area(2.5), 6.25)

    def test_perimeter(self):
        self.assertEqual(square_perimeter(4), 16)
        self.assertEqual(square_perimeter(0), 0)
        self.assertEqual(square_perimeter(2.5), 10)

    def test_negative_side_area(self):
        with self.assertRaises(ValueError):
            square_area(-1)

    def test_negative_side_perimeter(self):
        with self.assertRaises(ValueError):
            square_perimeter(-3)


class TestRhombus(unittest.TestCase):
    def test_area(self):
        self.assertEqual(rhombus_area(6, 8), 24.0)
        self.assertEqual(rhombus_area(0, 8), 0.0)

    def test_perimeter(self):
        self.assertEqual(rhombus_perimeter(5), 20)
        self.assertEqual(rhombus_perimeter(0), 0)

    def test_negative_diagonal_area(self):
        with self.assertRaises(ValueError):
            rhombus_area(-1, 8)

    def test_negative_side_perimeter(self):
        with self.assertRaises(ValueError):
            rhombus_perimeter(-4)


class TestTrapezoid(unittest.TestCase):
    def test_area(self):
        self.assertEqual(trapezoid_area(4, 6, 5), 25.0)
        self.assertEqual(trapezoid_area(0, 6, 5), 15.0)
        self.assertEqual(trapezoid_area(4, 6, 0), 0.0)

    def test_negative_base1_area(self):
        with self.assertRaises(ValueError):
            trapezoid_area(-1, 6, 5)

    def test_negative_height_area(self):
        with self.assertRaises(ValueError):
            trapezoid_area(4, 6, -2)


class TestTriangleHeron(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(triangle_heron_area(3, 4, 5), 6.0)
        self.assertAlmostEqual(triangle_heron_area(5, 5, 5), 10.825317547305483)

    def test_invalid_inequality(self):
        with self.assertRaises(ValueError):
            triangle_heron_area(1, 2, 10)

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            triangle_heron_area(-1, 4, 5)


class TestParallelogram(unittest.TestCase):
    def test_area(self):
        self.assertEqual(parallelogram_area(4, 5), 20)
        self.assertEqual(parallelogram_area(0, 5), 0)

    def test_perimeter(self):
        self.assertEqual(parallelogram_perimeter(4, 6), 20)
        self.assertEqual(parallelogram_perimeter(0, 6), 12)

    def test_negative_base_area(self):
        with self.assertRaises(ValueError):
            parallelogram_area(-1, 5)

    def test_negative_side_perimeter(self):
        with self.assertRaises(ValueError):
            parallelogram_perimeter(4, -2)


class TestEllipse(unittest.TestCase):
    def test_area(self):
        self.assertAlmostEqual(ellipse_area(2, 1), 2 * math.pi)
        self.assertAlmostEqual(ellipse_area(0, 1), 0)
        self.assertAlmostEqual(ellipse_area(3, 4), 12 * math.pi)

    def test_negative_axis_area(self):
        with self.assertRaises(ValueError):
            ellipse_area(-1, 2)


class TestPolygonArea(unittest.TestCase):
    def test_triangle(self):
        self.assertAlmostEqual(polygon_area([(0, 0), (2, 0), (0, 2)]), 2.0)

    def test_square(self):
        self.assertAlmostEqual(polygon_area([(0, 0), (4, 0), (4, 4), (0, 4)]), 16.0)

    def test_clockwise_and_counterclockwise(self):
        poly = [(0, 0), (4, 0), (4, 4), (0, 4)]
        self.assertAlmostEqual(polygon_area(poly), 16.0)
        self.assertAlmostEqual(polygon_area(list(reversed(poly))), 16.0)

    def test_fewer_than_three_vertices(self):
        with self.assertRaises(ValueError):
            polygon_area([(0, 0), (1, 1)])

    def test_non_list(self):
        with self.assertRaises(TypeError):
            polygon_area((0, 0), (1, 1), (2, 0))  # type: ignore[arg-type]


class TestRegularPolygonArea(unittest.TestCase):
    def test_square(self):
        self.assertAlmostEqual(regular_polygon_area(4, 2), 4.0)

    def test_triangle(self):
        self.assertAlmostEqual(regular_polygon_area(3, 2), math.sqrt(3))

    def test_negative_side(self):
        with self.assertRaises(ValueError):
            regular_polygon_area(5, -1)

    def test_too_few_sides(self):
        with self.assertRaises(ValueError):
            regular_polygon_area(2, 1)
        with self.assertRaises(TypeError):
            regular_polygon_area(3.5, 1)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()


class TestCircleDiameter(unittest.TestCase):
    def test_diameter(self):
        self.assertEqual(circle_diameter(0), 0)
        self.assertEqual(circle_diameter(1), 2)
        self.assertEqual(circle_diameter(2.5), 5.0)

    def test_negative(self):
        with self.assertRaises(ValueError):
            circle_diameter(-1)


class TestRectangleDiagonal(unittest.TestCase):
    def test_diagonal(self):
        self.assertEqual(rectangle_diagonal(3, 4), 5.0)
        self.assertEqual(rectangle_diagonal(0, 0), 0.0)

    def test_negative(self):
        with self.assertRaises(ValueError):
            rectangle_diagonal(-1, 4)
