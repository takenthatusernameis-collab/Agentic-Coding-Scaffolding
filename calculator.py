__all__ = [
    "add",
    "abs_difference",
    "subtract",
    "multiply",
    "divide",
    "modulo",
    "floor_divide",
    "power",
    "sqrt",
    "negate",
    "absolute",
    "clamp",
]


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def abs_difference(a: float, b: float) -> float:
    """Return the absolute difference |a - b|.

    Args:
        a: The first number.
        b: The second number.

    Raises:
        TypeError: If either argument is not a real number (int or float).

    Examples:
        >>> abs_difference(5, 3)
        2
        >>> abs_difference(3, 5)
        2
        >>> abs_difference(-2, -5)
        3
    """
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
    return abs(a - b)


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of a and b.

    Raises:
        TypeError: If either argument is not a real number (int or float).
        ValueError: If b is zero.
    """
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


def modulo(a: float, b: float) -> float:
    """Return the remainder of a divided by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a % b


def floor_divide(a: float, b: float) -> float:
    """Return the floor division of a by b.

    Raises:
        ValueError: If b is zero.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a // b


def power(a: float, b: float) -> float:
    """Return a raised to the power b."""
    return float(a ** b)


def sqrt(a: float) -> float:
    """Return the square root of a.

    Raises:
        ValueError: If a is negative.
    """
    if a < 0:
        raise ValueError("Cannot take square root of negative number.")
    return float(a ** 0.5)


def negate(a: float) -> float:
    """Return the negation of a."""
    return -a


def absolute(a: float) -> float:
    """Return the absolute value of a."""
    return abs(a)


def clamp(value: float, low: float, high: float) -> float:
    """Clamp value to the inclusive range [low, high].

    Raises:
        ValueError: If low > high.
    """
    if low > high:
        raise ValueError("low must not exceed high.")
    return max(low, min(high, value))
