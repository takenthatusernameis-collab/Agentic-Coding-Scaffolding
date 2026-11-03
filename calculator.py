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
    "reciprocal",
    "percentage",
    "average_of_two",
    "round_to",
    "factorial",
    "gcd",
    "lcm",
    "is_even",
    "is_odd",
    "is_prime",
    "combination",
    "permutation",
    "mod_pow",
]


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
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
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
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
    return a % b


def floor_divide(a: float, b: float) -> float:
    """Return the floor division of a by b.

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
    return a // b


def power(a: float, b: float) -> float:
    """Return a raised to the power b."""
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
    return float(a**b)


def sqrt(a: float) -> float:
    """Return the square root of a.

    Raises:
        TypeError: If a is not a real number (int or float).
        ValueError: If a is negative.
    """
    if isinstance(a, bool) or not isinstance(a, (int, float)):
        raise TypeError("a must be a real number")
    if a < 0:
        raise ValueError("Cannot take square root of negative number.")
    return float(a**0.5)


def negate(a: float) -> float:
    """Return the negation of a."""
    if isinstance(a, bool) or not isinstance(a, (int, float)):
        raise TypeError("a must be a real number")
    return -a


def absolute(a: float) -> float:
    """Return the absolute value of a."""
    if isinstance(a, bool) or not isinstance(a, (int, float)):
        raise TypeError("a must be a real number")
    return abs(a)


def clamp(value: float, low: float, high: float) -> float:
    """Clamp value to the inclusive range [low, high].

    Raises:
        TypeError: If any argument is not a real number (int or float).
        ValueError: If low > high.
    """
    if (
        isinstance(value, bool)
        or isinstance(low, bool)
        or isinstance(high, bool)
        or not isinstance(value, (int, float))
        or not isinstance(low, (int, float))
        or not isinstance(high, (int, float))
    ):
        raise TypeError("value, low, and high must be real numbers")
    if low > high:
        raise ValueError("low must not exceed high.")
    return max(low, min(high, value))


def reciprocal(x: float) -> float:
    """Return 1/x."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError("x must be a real number")
    if x == 0:
        raise ValueError("Cannot divide by zero")
    return float(1.0 / x)


def percentage(value: float, percent: float) -> float:
    """Return (value * percent) / 100."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be a real number")
    if isinstance(percent, bool) or not isinstance(percent, (int, float)):
        raise TypeError("percent must be a real number")
    return float((value * percent) / 100.0)


def average_of_two(a: float, b: float) -> float:
    """Return the average of a and b."""
    if (
        isinstance(a, bool)
        or isinstance(b, bool)
        or not isinstance(a, (int, float))
        or not isinstance(b, (int, float))
    ):
        raise TypeError("a and b must be real numbers")
    return float((a + b) / 2.0)


def round_to(value: float, places: int = 0) -> float:
    """Round a value to the given number of decimal places.

    Uses banker's rounding (round-half-to-even), matching Python's built-in
    :func:`round`.

    Args:
        value: The value to round.
        places: The number of decimal places. Must be non-negative.

    Returns:
        The rounded value.

    Raises:
        TypeError: If *value* is not a real number (int or float) or *places*
            is not an int.
        ValueError: If *places* is negative.

    Examples:
        >>> round_to(2.5)
        2.0
        >>> round_to(3.5)
        4.0
        >>> round_to(3.14159, 2)
        3.14
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("value must be a real number")
    if isinstance(places, bool) or not isinstance(places, int):
        raise TypeError(f"places must be an int, got {type(places).__name__}")
    if places < 0:
        raise ValueError("places must be non-negative")
    return float(round(value, places))


def factorial(n: int) -> int:
    """Return n factorial (n!).

    Args:
        n: The non-negative integer to compute factorial of.

    Returns:
        The factorial of n as an integer.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is negative.

    Examples:
        >>> factorial(0)
        1
        >>> factorial(5)
        120
        >>> factorial(3)
        6
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of a and b.

    Uses Euclid's algorithm. Both numbers must be integers; only
    non-negative results are returned (gcd(0,0) returns 0).

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The greatest common divisor of |a| and |b|.

    Raises:
        TypeError: If *a* or *b* is not an int (bools rejected).
        ValueError: If either value is negative.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("a and b must be ints")
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a and b must be ints")
    if a < 0 or b < 0:
        raise ValueError("a and b must be non-negative")
    a_abs = abs(a)
    b_abs = abs(b)
    while b_abs:
        a_abs, b_abs = b_abs, a_abs % b_abs
    return a_abs


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of a and b.

    Both numbers must be integers and non-negative.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        The least common multiple of a and b.

    Raises:
        TypeError: If *a* or *b* is not an int (bools rejected).
        ValueError: If either value is negative.
    """
    if isinstance(a, bool) or isinstance(b, bool):
        raise TypeError("a and b must be ints")
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("a and b must be ints")
    if a < 0 or b < 0:
        raise ValueError("a and b must be non-negative")
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def is_even(value: int) -> bool:
    """Return True if value is an even integer.

    Args:
        value: The integer to test.

    Returns:
        True if value is even.

    Raises:
        TypeError: If value is not an int (bools rejected).
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    return value % 2 == 0


def is_odd(value: int) -> bool:
    """Return True if value is an odd integer.

    Args:
        value: The integer to test.

    Returns:
        True if value is odd.

    Raises:
        TypeError: If value is not an int (bools rejected).
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    return value % 2 != 0


def combination(n: int, k: int) -> int:
    """Return the number of combinations of *n* items taken *k* at a time.

    This is C(n, k) = n! / (k! * (n - k)!).
    """
    if isinstance(n, bool) or isinstance(k, bool):
        raise TypeError("n and k must be ints")
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be ints")
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0:
        raise ValueError("k must be non-negative")
    if k > n:
        raise ValueError("k must not be greater than n")
    k_small = min(k, n - k)
    numerator = 1
    denominator = 1
    for i in range(n - k_small + 1, n + 1):
        numerator *= i
    for i in range(1, k_small + 1):
        denominator *= i
    return numerator // denominator


def permutation(n: int, k: int) -> int:
    """Return the number of permutations of *n* items taken *k* at a time.

    This is P(n, k) = n! / (n - k)!.
    """
    if isinstance(n, bool) or isinstance(k, bool):
        raise TypeError("n and k must be ints")
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be ints")
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0:
        raise ValueError("k must be non-negative")
    if k > n:
        raise ValueError("k must not be greater than n")
    result = 1
    for i in range(n - k + 1, n + 1):
        result *= i
    return result


def is_prime(n: int) -> bool:
    """Return True if n is a prime number.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n is less than 2.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 2:
        raise ValueError("n must be >= 2")
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    # Simple test
    for _ in range(128):
        a = 2
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def mod_pow(base: int, exp: int, mod: int) -> int:
    """Return (base ** exp) mod mod.

    Raises:
        TypeError: If base, exp, or mod are not ints.
        ValueError: If exp is negative or mod <= 0.
    """
    if isinstance(base, bool) or isinstance(exp, bool) or isinstance(mod, bool):
        raise TypeError("base, exp, and mod must be ints")
    if not isinstance(base, int) or not isinstance(exp, int) or not isinstance(mod, int):
        raise TypeError("base, exp, and mod must be ints")
    if exp < 0:
        raise ValueError("exp must be non-negative")
    if mod <= 0:
        raise ValueError("mod must be positive")
    return pow(base, exp, mod)
