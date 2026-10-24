"""Geometry utilities for calculating areas and perimeters of common shapes."""

import math
from typing import List

__all__: List[str] = [
    "circle_area",
    "circle_diameter",
    "circle_perimeter",
    "rectangle_area",
    "rectangle_diagonal",
    "rectangle_perimeter",
    "triangle_area",
    "triangle_perimeter",
    "square_area",
    "square_perimeter",
    "rhombus_area",
    "rhombus_perimeter",
    "trapezoid_area",
    "triangle_heron_area",
    "parallelogram_area",
    "parallelogram_perimeter",
    "ellipse_area",
    "polygon_area",
    "regular_polygon_area",
    "regular_polygon_perimeter",
]


def _require_non_negative(value: float, name: str) -> None:
    """Validate that a value is non-negative."""
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")


def circle_area(radius: float) -> float:
    """Return the area of a circle with the given radius.

    Args:
        radius: The radius of the circle.

    Raises:
        ValueError: If radius is negative.

    Examples:
        >>> circle_area(1)
        3.141592653589793
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return math.pi * radius ** 2


def circle_perimeter(radius: float) -> float:
    """Return the perimeter (circumference) of a circle with the given radius.

    Args:
        radius: The radius of the circle.

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return 2 * math.pi * radius


def rectangle_area(length: float, width: float) -> float:
    """Return the area of a rectangle.

    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.

    Raises:
        ValueError: If length or width is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return length * width


def rectangle_perimeter(length: float, width: float) -> float:
    """Return the perimeter of a rectangle.

    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.

    Raises:
        ValueError: If length or width is negative.
    """
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return 2 * (length + width)


def triangle_area(base: float, height: float) -> float:
    """Return the area of a triangle given its base and height.

    Args:
        base: The base length of the triangle.
        height: The height of the triangle.

    Raises:
        ValueError: If base or height is negative.
    """
    if base < 0 or height < 0:
        raise ValueError("Base and height cannot be negative.")
    return 0.5 * base * height


def triangle_perimeter(side_a: float, side_b: float, side_c: float) -> float:
    """Return the perimeter of a triangle given its three sides.

    Args:
        side_a: Length of the first side.
        side_b: Length of the second side.
        side_c: Length of the third side.

    Raises:
        ValueError: If any side is negative or the sides violate the triangle inequality.
    """
    if side_a < 0 or side_b < 0 or side_c < 0:
        raise ValueError("Sides cannot be negative.")
    if not (side_a + side_b > side_c and side_a + side_c > side_b and side_b + side_c > side_a):
        raise ValueError("Sides do not form a valid triangle.")
    return side_a + side_b + side_c


def square_area(side: float) -> float:
    """Return the area of a square with the given side length.

    Args:
        side: The side length of the square.

    Raises:
        ValueError: If side is negative.

    Examples:
        >>> square_area(4)
        16
        >>> square_area(0)
        0
    """
    if side < 0:
        raise ValueError("Side cannot be negative.")
    return side * side


def square_perimeter(side: float) -> float:
    """Return the perimeter of a square with the given side length.

    Args:
        side: The side length of the square.

    Raises:
        ValueError: If side is negative.

    Examples:
        >>> square_perimeter(4)
        16
        >>> square_perimeter(0)
        0
    """
    if side < 0:
        raise ValueError("Side cannot be negative.")
    return 4 * side


def rhombus_area(diagonal1: float, diagonal2: float) -> float:
    """Return the area of a rhombus given its two diagonals.

    Args:
        diagonal1: Length of the first diagonal.
        diagonal2: Length of the second diagonal.

    Raises:
        ValueError: If either diagonal is negative.

    Examples:
        >>> rhombus_area(6, 8)
        24.0
    """
    if diagonal1 < 0 or diagonal2 < 0:
        raise ValueError("Diagonals cannot be negative.")
    return 0.5 * diagonal1 * diagonal2


def rhombus_perimeter(side: float) -> float:
    """Return the perimeter of a rhombus given its side length.

    Args:
        side: The side length of the rhombus.

    Raises:
        ValueError: If side is negative.

    Examples:
        >>> rhombus_perimeter(5)
        20
    """
    if side < 0:
        raise ValueError("Side cannot be negative.")
    return 4 * side


def trapezoid_area(base1: float, base2: float, height: float) -> float:
    """Return the area of a trapezoid given its two bases and height.

    Args:
        base1: Length of the first base.
        base2: Length of the second base.
        height: The height of the trapezoid.

    Raises:
        ValueError: If any dimension is negative.

    Examples:
        >>> trapezoid_area(4, 6, 5)
        25.0
    """
    if base1 < 0 or base2 < 0 or height < 0:
        raise ValueError("Dimensions cannot be negative.")
    return 0.5 * (base1 + base2) * height


def triangle_heron_area(side_a: float, side_b: float, side_c: float) -> float:
    """Return the area of a triangle given its three sides using Heron's formula.

    Args:
        side_a: Length of the first side.
        side_b: Length of the second side.
        side_c: Length of the third side.

    Raises:
        ValueError: If any side is negative or the sides violate the triangle inequality.

    Examples:
        >>> triangle_heron_area(3, 4, 5)
        6.0
    """
    if side_a < 0 or side_b < 0 or side_c < 0:
        raise ValueError("Sides cannot be negative.")
    if not (side_a + side_b > side_c and side_a + side_c > side_b and side_b + side_c > side_a):
        raise ValueError("Sides do not form a valid triangle.")
    semi_perimeter = (side_a + side_b + side_c) / 2.0
    return math.sqrt(
        semi_perimeter
        * (semi_perimeter - side_a)
        * (semi_perimeter - side_b)
        * (semi_perimeter - side_c)
    )


def parallelogram_area(base: float, height: float) -> float:
    """Return the area of a parallelogram given its base and height.

    Args:
        base: The base length of the parallelogram.
        height: The perpendicular height.

    Raises:
        ValueError: If base or height is negative.

    Examples:
        >>> parallelogram_area(4, 5)
        20
    """
    if base < 0 or height < 0:
        raise ValueError("Base and height cannot be negative.")
    return base * height


def parallelogram_perimeter(side_a: float, side_b: float) -> float:
    """Return the perimeter of a parallelogram given its two side lengths.

    Args:
        side_a: Length of the first side.
        side_b: Length of the adjacent side.

    Raises:
        ValueError: If either side is negative.

    Examples:
        >>> parallelogram_perimeter(4, 6)
        20
    """
    if side_a < 0 or side_b < 0:
        raise ValueError("Sides cannot be negative.")
    return 2 * (side_a + side_b)


def ellipse_area(a: float, b: float) -> float:
    """Return the area of an ellipse with semi-axes a and b.

    Args:
        a: Length of the semi-major or semi-minor axis.
        b: Length of the other semi-axis.

    Raises:
        ValueError: If either semi-axis is negative.

    Examples:
        >>> ellipse_area(2, 1)
        6.283185307179586
    """
    if a < 0 or b < 0:
        raise ValueError("Semi-axes cannot be negative.")
    return math.pi * a * b


def polygon_area(vertices: List[tuple[float, float]]) -> float:
    """Return the area of a polygon given vertices using the shoelace formula.

    Args:
        vertices: List of (x, y) tuples in order (either clockwise or counterclockwise).

    Returns:
        The area of the polygon.

    Raises:
        TypeError: If vertices is not a list or contains invalid elements.
        ValueError: If fewer than 3 vertices are provided.

    Examples:
        >>> polygon_area([(0, 0), (2, 0), (0, 2)])
        2.0
    """
    if not isinstance(vertices, list):
        raise TypeError("vertices must be a list")
    if len(vertices) < 3:
        raise ValueError("polygon must have at least 3 vertices")
    n = len(vertices)
    s1 = 0.0
    s2 = 0.0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        s1 += x1 * y2
        s2 += y1 * x2
    return abs(s1 - s2) / 2.0


def regular_polygon_area(n: int, side_length: float) -> float:
    """Return the area of a regular polygon with n sides.

    Args:
        n: Number of sides (must be >= 3).
        side_length: Length of each side.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n < 3 or side_length is negative.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 3:
        raise ValueError("n must be at least 3")
    if side_length < 0:
        raise ValueError("Side length cannot be negative.")
    return (n * side_length ** 2) / (4 * math.tan(math.pi / n))

def regular_polygon_perimeter(n: int, side_length: float) -> float:
    """Return the perimeter of a regular polygon."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 3:
        raise ValueError("A polygon must have at least 3 sides")
    if side_length < 0:
        raise ValueError("Side length cannot be negative")
    return float(n * side_length)


def circle_diameter(radius: float) -> float:
    """Return the diameter of a circle with the given radius."""
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return 2 * radius


def rectangle_diagonal(length: float, width: float) -> float:
    """Return the diagonal of a rectangle."""
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return float((length ** 2 + width ** 2) ** 0.5)
