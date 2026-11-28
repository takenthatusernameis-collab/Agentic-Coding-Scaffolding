"""Geometry utilities for calculating areas and perimeters of common shapes."""

import math
from typing import List

__all__: List[str] = [
    "circle_area",
    "circle_perimeter",
    "rectangle_area",
    "rectangle_perimeter",
    "triangle_area",
    "triangle_perimeter",
    "square_area",
    "square_perimeter",
    "rhombus_area",
    "rhombus_perimeter",
    "trapezoid_area",
    "triangle_heron_area",
    "triangle_inradius",
    "triangle_circumradius",
    "parallelogram_area",
    "parallelogram_perimeter",
    "ellipse_area",
    "polygon_area",
    "regular_polygon_area",
    "regular_polygon_perimeter",
    "circle_diameter",
    "rectangle_diagonal",
    "sector_area",
    "arc_length",
    "ellipse_circumference",
    "sphere_surface_area",
    "sphere_volume",
    "cube_surface_area",
    "cube_volume",
    "cuboid_surface_area",
    "cuboid_volume",
    "rectangular_prism_surface_area",
    "rectangular_prism_volume",
    "cylinder_surface_area",
    "cylinder_volume",
    "cone_surface_area",
    "cone_volume",
    "point_distance",
    "midpoint",
    "point_in_circle",
    "point_in_rectangle",
]


def _require_number(value: object, name: str) -> float:
    """Validate that *value* is a real number (int or float, not bool)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        raise ValueError(f"{name} must be a finite number")
    return value


def circle_area(radius: float) -> float:
    """Return the area of a circle with the given radius.

    Args:
        radius: The radius of the circle.

    Raises:
        ValueError: If radius is negative, or if the result is too large
            to represent as a finite float.

    Examples:
        >>> circle_area(1)
        3.141592653589793
    """
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    try:
        return math.pi * radius**2
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def circle_perimeter(radius: float) -> float:
    """Return the perimeter (circumference) of a circle with the given radius.

    Args:
        radius: The radius of the circle.

    Raises:
        TypeError: If radius is not a number.
        ValueError: If radius is negative.
    """
    radius = _require_number(radius, "radius")
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
    length = _require_number(length, "length")
    width = _require_number(width, "width")
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    return length * width


def rectangle_perimeter(length: float, width: float) -> float:
    """Return the perimeter of a rectangle.

    Args:
        length: The length of the rectangle.
        width: The width of the rectangle.

    Raises:
        TypeError: If length or width is not a number.
        ValueError: If length or width is negative.
    """
    length = _require_number(length, "length")
    width = _require_number(width, "width")
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
    base = _require_number(base, "base")
    height = _require_number(height, "height")
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
        TypeError: If any side is not a number.
        ValueError: If any side is negative or the sides violate the triangle inequality.
    """
    side_a = _require_number(side_a, "side_a")
    side_b = _require_number(side_b, "side_b")
    side_c = _require_number(side_c, "side_c")
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
    side = _require_number(side, "side")
    if side < 0:
        raise ValueError("Side cannot be negative.")
    return side * side


def square_perimeter(side: float) -> float:
    """Return the perimeter of a square with the given side length.

    Args:
        side: The side length of the square.

    Raises:
        TypeError: If side is not a number.
        ValueError: If side is negative.

    Examples:
        >>> square_perimeter(4)
        16
        >>> square_perimeter(0)
        0
    """
    side = _require_number(side, "side")
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
    diagonal1 = _require_number(diagonal1, "diagonal1")
    diagonal2 = _require_number(diagonal2, "diagonal2")
    if diagonal1 < 0 or diagonal2 < 0:
        raise ValueError("Diagonals cannot be negative.")
    return 0.5 * diagonal1 * diagonal2


def rhombus_perimeter(side: float) -> float:
    """Return the perimeter of a rhombus given its side length.

    Args:
        side: The side length of the rhombus.

    Raises:
        TypeError: If side is not a number.
        ValueError: If side is negative.

    Examples:
        >>> rhombus_perimeter(5)
        20
    """
    side = _require_number(side, "side")
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
    base1 = _require_number(base1, "base1")
    base2 = _require_number(base2, "base2")
    height = _require_number(height, "height")
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
    side_a = _require_number(side_a, "side_a")
    side_b = _require_number(side_b, "side_b")
    side_c = _require_number(side_c, "side_c")
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


def triangle_inradius(side_a: float, side_b: float, side_c: float) -> float:
    """Return the inradius (radius of inscribed circle) of a triangle.

    Args:
        side_a: Length of the first side.
        side_b: Length of the second side.
        side_c: Length of the third side.

    Raises:
        ValueError: If any side is negative or the sides violate the triangle inequality.
    """
    area = triangle_heron_area(side_a, side_b, side_c)
    perimeter = side_a + side_b + side_c
    return (2 * area) / perimeter


def triangle_circumradius(side_a: float, side_b: float, side_c: float) -> float:
    """Return the circumradius (radius of circumscribed circle) of a triangle.

    Args:
        side_a: Length of the first side.
        side_b: Length of the second side.
        side_c: Length of the third side.

    Raises:
        ValueError: If any side is negative or the sides violate the triangle inequality.
    """
    area = triangle_heron_area(side_a, side_b, side_c)
    if area == 0:
        raise ValueError("Sides do not form a valid triangle.")
    return (side_a * side_b * side_c) / (4 * area)


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
    base = _require_number(base, "base")
    height = _require_number(height, "height")
    if base < 0 or height < 0:
        raise ValueError("Base and height cannot be negative.")
    return base * height


def parallelogram_perimeter(side_a: float, side_b: float) -> float:
    """Return the perimeter of a parallelogram given its two side lengths.

    Args:
        side_a: Length of the first side.
        side_b: Length of the adjacent side.

    Raises:
        TypeError: If either side is not a number.
        ValueError: If either side is negative.

    Examples:
        >>> parallelogram_perimeter(4, 6)
        20
    """
    side_a = _require_number(side_a, "side_a")
    side_b = _require_number(side_b, "side_b")
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
    a = _require_number(a, "a")
    b = _require_number(b, "b")
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
        TypeError: If vertices is not iterable, a vertex is not a 2-tuple of
            numbers, or a vertex component is not a number.
        ValueError: If fewer than 3 vertices are provided.

    Examples:
        >>> polygon_area([(0, 0), (2, 0), (0, 2)])
        2.0
    """
    try:
        vertices_list = list(vertices)
    except TypeError:
        raise TypeError("vertices must be iterable")
    if len(vertices_list) < 3:
        raise ValueError("polygon must have at least 3 vertices")
    for vertex in vertices_list:
        if not isinstance(vertex, (tuple, list)) or len(vertex) != 2:
            raise TypeError("each vertex must be a 2-tuple of numbers")
        _require_number(vertex[0], "vertex x")
        _require_number(vertex[1], "vertex y")
    n = len(vertices_list)
    s1 = 0.0
    s2 = 0.0
    for i in range(n):
        x1, y1 = vertices_list[i]
        x2, y2 = vertices_list[(i + 1) % n]
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
        ValueError: If n < 3, side_length is negative, or if the result is too large
            to represent as a finite float.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 3:
        raise ValueError("n must be at least 3")
    side_length = _require_number(side_length, "side_length")
    if side_length < 0:
        raise ValueError("Side length cannot be negative.")
    try:
        return (n * side_length**2) / (4 * math.tan(math.pi / n))
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def regular_polygon_perimeter(n: int, side_length: float) -> float:
    """Return the perimeter of a regular polygon with n sides.

    Args:
        n: Number of sides (must be >= 3).
        side_length: Length of each side.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n < 3 or side_length is negative.

    Examples:
        >>> regular_polygon_perimeter(4, 2)
        8.0
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 3:
        raise ValueError("A polygon must have at least 3 sides")
    side_length = _require_number(side_length, "side_length")
    if side_length < 0:
        raise ValueError("Side length cannot be negative")
    return float(n * side_length)


def circle_diameter(radius: float) -> float:
    """Return the diameter of a circle with the given radius."""
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    return 2 * radius


def rectangle_diagonal(length: float, width: float) -> float:
    """Return the diagonal of a rectangle.

    Uses :func:`math.hypot`, which rescales internally so that large but
    finite sides (for example ``1e200``) do not overflow the intermediate
    ``length**2 + width**2`` to infinity.

    Raises:
        ValueError: If length or width is negative, or if the result is too large
            to represent as a finite float.
    """

    length = _require_number(length, "length")
    width = _require_number(width, "width")
    if length < 0 or width < 0:
        raise ValueError("Length and width cannot be negative.")
    result = math.hypot(length, width)
    if math.isinf(result):
        raise ValueError("result is too large to represent as a finite float")
    return result


def sector_area(radius: float, angle_degrees: float) -> float:
    """Return the area of a circular sector.

    Args:
        radius: The radius of the circle.
        angle_degrees: The central angle of the sector in degrees.

    Raises:
        ValueError: If radius is negative, angle_degrees is outside [0, 360],
            or if the result is too large to represent as a finite float.

    Examples:
        >>> sector_area(1, 90)
        0.7853981633974483
    """
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    angle_degrees = _require_number(angle_degrees, "angle_degrees")
    if angle_degrees < 0 or angle_degrees > 360:
        raise ValueError("angle_degrees must be between 0 and 360")
    try:
        return (angle_degrees / 360.0) * math.pi * radius**2
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def arc_length(radius: float, angle_degrees: float) -> float:
    """Return the length of a circular arc.

    Args:
        radius: The radius of the circle.
        angle_degrees: The central angle of the arc in degrees.

    Raises:
        ValueError: If radius is negative or angle_degrees is outside [0, 360].
        TypeError: If angle_degrees is not a number.

    Examples:
        >>> arc_length(1, 90)
        1.5707963267948966
    """
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    angle_degrees = _require_number(angle_degrees, "angle_degrees")
    if angle_degrees < 0 or angle_degrees > 360:
        raise ValueError("angle_degrees must be between 0 and 360")
    return (angle_degrees / 360.0) * 2 * math.pi * radius


def ellipse_circumference(a: float, b: float) -> float:
    """Return the approximate circumference (perimeter) of an ellipse.

    Uses Ramanujan's approximation.

    Args:
        a: Semi-major or semi-minor axis length.
        b: The other semi-axis length.

    Raises:
        ValueError: If a or b is negative.
        TypeError: If a or b is not a number.
    """
    a = _require_number(a, "a")
    b = _require_number(b, "b")
    if a < 0 or b < 0:
        raise ValueError("a and b must be non-negative")
    a_f = float(a)
    b_f = float(b)
    return float(math.pi * (3 * (a_f + b_f) - math.sqrt((3 * a_f + b_f) * (a_f + 3 * b_f))))


def sphere_surface_area(radius: float) -> float:
    """Return the surface area of a sphere.

    Raises:
        ValueError: If radius is negative, or if the result is too large
            to represent as a finite float.
    """
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    try:
        return float(4 * math.pi * radius**2)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def sphere_volume(radius: float) -> float:
    """Return the volume of a sphere.

    Raises:
        ValueError: If radius is negative, or if the result is too large
            to represent as a finite float.
    """
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    try:
        return float((4 / 3) * math.pi * radius**3)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def cube_surface_area(side: float) -> float:
    """Return the surface area of a cube.

    Raises:
        ValueError: If side is negative, or if the result is too large
            to represent as a finite float.
    """
    side = _require_number(side, "side")
    if side < 0:
        raise ValueError("Side cannot be negative.")
    try:
        return float(6 * side**2)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def cube_volume(side: float) -> float:
    """Return the volume of a cube.

    Raises:
        ValueError: If side is negative, or if the result is too large
            to represent as a finite float.
    """
    side = _require_number(side, "side")
    if side < 0:
        raise ValueError("Side cannot be negative.")
    try:
        return float(side**3)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def cuboid_surface_area(length: float, width: float, height: float) -> float:
    """Return the surface area of a cuboid (rectangular prism)."""
    length = _require_number(length, "length")
    width = _require_number(width, "width")
    height = _require_number(height, "height")
    if length < 0:
        raise ValueError("Length cannot be negative.")
    if width < 0:
        raise ValueError("Width cannot be negative.")
    if height < 0:
        raise ValueError("Height cannot be negative.")
    return float(2 * (length * width + length * height + width * height))


def cuboid_volume(length: float, width: float, height: float) -> float:
    """Return the volume of a cuboid (rectangular prism)."""
    length = _require_number(length, "length")
    width = _require_number(width, "width")
    height = _require_number(height, "height")
    if length < 0:
        raise ValueError("Length cannot be negative.")
    if width < 0:
        raise ValueError("Width cannot be negative.")
    if height < 0:
        raise ValueError("Height cannot be negative.")
    return float(length * width * height)


rectangular_prism_surface_area = cuboid_surface_area
rectangular_prism_volume = cuboid_volume


def cylinder_surface_area(radius: float, height: float) -> float:
    """Return the total surface area of a cylinder (including bases).

    Raises:
        ValueError: If radius or height is negative, or if the result is too large
            to represent as a finite float.
    """
    radius = _require_number(radius, "radius")
    height = _require_number(height, "height")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    if height < 0:
        raise ValueError("Height cannot be negative.")
    try:
        return float(2 * math.pi * radius**2 + 2 * math.pi * radius * height)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def cylinder_volume(radius: float, height: float) -> float:
    """Return the volume of a cylinder.

    Raises:
        ValueError: If radius or height is negative, or if the result is too large
            to represent as a finite float.
    """
    radius = _require_number(radius, "radius")
    height = _require_number(height, "height")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    if height < 0:
        raise ValueError("Height cannot be negative.")
    try:
        return float(math.pi * radius**2 * height)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def cone_surface_area(radius: float, slant_height: float) -> float:
    """Return the total surface area of a cone (including base).

    Raises:
        ValueError: If radius or slant_height is negative, or if the result is too large
            to represent as a finite float.
    """
    radius = _require_number(radius, "radius")
    slant_height = _require_number(slant_height, "slant_height")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    if slant_height < 0:
        raise ValueError("Slant height cannot be negative.")
    try:
        return float(math.pi * radius**2 + math.pi * radius * slant_height)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def cone_volume(radius: float, height: float) -> float:
    """Return the volume of a cone.

    Raises:
        ValueError: If radius or height is negative, or if the result is too large
            to represent as a finite float.
    """
    radius = _require_number(radius, "radius")
    height = _require_number(height, "height")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    if height < 0:
        raise ValueError("Height cannot be negative.")
    try:
        return float((1 / 3) * math.pi * radius**2 * height)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def point_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return the Euclidean distance between two points.

    Uses :func:`math.hypot`, which rescales internally so that large but
    finite coordinate separations (for example ``1e200``) do not overflow the
    intermediate squares to infinity.

    Raises:
        TypeError: If p1 or p2 is not a point (x, y).
        ValueError: If any coordinate is not finite, or if the result is too large
            to represent as a finite float.
    """
    if not isinstance(p1, (tuple, list)) or len(p1) != 2:
        raise TypeError("p1 must be a point (x, y)")
    if not isinstance(p2, (tuple, list)) or len(p2) != 2:
        raise TypeError("p2 must be a point (x, y)")
    x1, y1 = p1
    x2, y2 = p2
    x1 = _require_number(x1, "x1")
    y1 = _require_number(y1, "y1")
    x2 = _require_number(x2, "x2")
    y2 = _require_number(y2, "y2")
    result = math.hypot(x2 - x1, y2 - y1)
    if math.isinf(result):
        raise ValueError("result is too large to represent as a finite float")
    return result


def midpoint(p1: tuple[float, float], p2: tuple[float, float]) -> tuple[float, float]:
    """Return the midpoint between two points."""
    if not isinstance(p1, (tuple, list)) or len(p1) != 2:
        raise TypeError("p1 must be a point (x, y)")
    if not isinstance(p2, (tuple, list)) or len(p2) != 2:
        raise TypeError("p2 must be a point (x, y)")
    x1, y1 = p1
    x2, y2 = p2
    x1 = _require_number(x1, "x1")
    y1 = _require_number(y1, "y1")
    x2 = _require_number(x2, "x2")
    y2 = _require_number(y2, "y2")
    return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)


def point_in_circle(point: tuple[float, float], center: tuple[float, float], radius: float) -> bool:
    """Return True if point is inside or on the circle."""
    radius = _require_number(radius, "radius")
    if radius < 0:
        raise ValueError("Radius cannot be negative.")
    dist = point_distance(point, center)
    return dist <= radius + 1e-9


def point_in_rectangle(
    point: tuple[float, float],
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> bool:
    """Return True if *point* lies inside or on the rectangle defined by opposite corners.

    The rectangle is axis-aligned and defined by two opposite corners ``(x1, y1)``
    and ``(x2, y2)``; the bounds are normalized internally so the order of the
    corners does not matter. A point on the boundary counts as inside.

    Args:
        point: The ``(x, y)`` point to test.
        x1: X-coordinate of the first rectangle corner.
        y1: Y-coordinate of the first rectangle corner.
        x2: X-coordinate of the opposite rectangle corner.
        y2: Y-coordinate of the opposite rectangle corner.

    Returns:
        ``True`` if *point* is inside or on the rectangle, ``False`` otherwise.

    Raises:
        TypeError: If *point* is not a 2-tuple/list of numbers, or if any
            coordinate is not a number (booleans are rejected).
        ValueError: If any coordinate is NaN or infinite, or if the rectangle
            has zero or negative width/height.

    Examples:
        >>> point_in_rectangle((1, 1), 0, 0, 3, 3)
        True
        >>> point_in_rectangle((5, 5), 0, 0, 3, 3)
        False
        >>> point_in_rectangle((3, 0), 0, 0, 3, 3)
        True
        >>> point_in_rectangle((1, 1), 3, 3, 0, 0)
        True
    """
    if not isinstance(point, (tuple, list)) or len(point) != 2:
        raise TypeError("point must be a point (x, y)")
    px, py = point
    px = _require_number(px, "px")
    py = _require_number(py, "py")
    x1 = _require_number(x1, "x1")
    y1 = _require_number(y1, "y1")
    x2 = _require_number(x2, "x2")
    y2 = _require_number(y2, "y2")
    left = min(x1, x2)
    right = max(x1, x2)
    bottom = min(y1, y2)
    top = max(y1, y2)
    if right - left <= 0:
        raise ValueError("Rectangle width must be positive.")
    if top - bottom <= 0:
        raise ValueError("Rectangle height must be positive.")
    return left - 1e-9 <= px <= right + 1e-9 and bottom - 1e-9 <= py <= top + 1e-9
