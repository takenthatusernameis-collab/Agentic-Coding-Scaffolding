"""Mathematical utility functions."""

from __future__ import annotations

import math
from typing import List

__all__: List[str] = [
    "factorial",
    "fibonacci",
    "gcd",
    "lcm",
    "is_prime",
    "clamp",
    "is_even",
]


def _require_int(value: object, name: str) -> int:
    """Validate that *value* is an int (rejecting bool) and return it."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer n.

    Args:
        n: The number to calculate factorial for.

    Returns:
        The factorial of n (n!).

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is negative.

    Examples:
        >>> factorial(0)
        1
        >>> factorial(5)
        120
    """
    n = _require_int(n, "n")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.

    Args:
        n: The index of the Fibonacci number (n >= 0).

    Returns:
        The nth Fibonacci number.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is negative.

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
    """
    n = _require_int(n, "n")
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def gcd(a: int, b: int) -> int:
    """Calculate the Greatest Common Divisor of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The GCD of a and b.

    Raises:
        TypeError: If *a* or *b* is not an int.

    Examples:
        >>> gcd(48, 18)
        6
        >>> gcd(17, 13)
        1
    """
    a = _require_int(a, "a")
    b = _require_int(b, "b")
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """Calculate the Least Common Multiple of two integers.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The LCM of a and b.

    Raises:
        TypeError: If *a* or *b* is not an int.

    Examples:
        >>> lcm(4, 6)
        12
        >>> lcm(3, 5)
        15
    """
    a = _require_int(a, "a")
    b = _require_int(b, "b")
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n: The number to check.

    Returns:
        True if n is prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* < 2.

    Examples:
        >>> is_prime(2)
        True
        >>> is_prime(9)
        False
        >>> is_prime(17)
        True
    """
    n = _require_int(n, "n")
    if n < 2:
        raise ValueError("Prime check is only defined for integers >= 2")
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min_val and max_val.

    Args:
        value: The value to clamp.
        min_val: The minimum allowed value.
        max_val: The maximum allowed value.

    Returns:
        The clamped value.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If min_val > max_val.

    Examples:
        >>> clamp(5, 0, 10)
        5
        >>> clamp(-5, 0, 10)
        0
        >>> clamp(15, 0, 10)
        10
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"value must be a number, got {type(value).__name__}")
    if isinstance(min_val, bool) or not isinstance(min_val, (int, float)):
        raise TypeError(f"min_val must be a number, got {type(min_val).__name__}")
    if isinstance(max_val, bool) or not isinstance(max_val, (int, float)):
        raise TypeError(f"max_val must be a number, got {type(max_val).__name__}")
    if min_val > max_val:
        raise ValueError("min_val must be <= max_val")
    return max(min_val, min(value, max_val))


def is_even(value: int) -> bool:
    """Return True if *value* is an even integer.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is even.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_even(2)
        True
        >>> is_even(3)
        False
    """
    value = _require_int(value, "value")
    return value % 2 == 0
