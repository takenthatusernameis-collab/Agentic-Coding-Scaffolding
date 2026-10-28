def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of a and b.

    Raises:
        ValueError: If b is zero.
    """
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
    return a ** b


def sqrt(a: float) -> float:
    """Return the square root of a.

    Raises:
        ValueError: If a is negative.
    """
    if a < 0:
        raise ValueError("Cannot take square root of negative number.")
    return a ** 0.5


def negate(a: float) -> float:
    """Return the negation of a."""
    return -a


def absolute(a: float) -> float:
    """Return the absolute value of a."""
    return abs(a)
