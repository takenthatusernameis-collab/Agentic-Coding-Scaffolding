"""Number utility functions."""

from __future__ import annotations

import math
from typing import List, Union

Number = Union[int, float]

__all__: List[str] = [
    "clamp",
    "round_to",
    "is_integer",
    "format_number",
    "percentage",
    "lerp",
    "map_range",
    "remap",
    "sign",
    "is_even",
    "is_odd",
    "is_pronic_number",
    "is_negative",
    "is_positive",
    "is_zero",
    "is_non_negative",
    "is_non_positive",
    "is_between",
    "is_close",
    "in_range",
    "is_finite",
    "is_infinite",
    "is_nan",
    "safe_divide",
    "is_perfect_cube",
    "is_perfect_square",
    "is_power_of_two",
    "is_palindromic_number",
    "round_half_up",
    "gcd",
    "lcm",
    "ceil_div",
    "is_divisible_by",
    "is_multiple_of",
    "divides",
    "is_coprime",
    "digit_sum",
    "digit_count",
    "digit_product",
    "digital_root",
    "is_triangular_number",
    "is_perfect_number",
    "is_automorphic_number",
    "is_happy_number",
    "is_harshad_number",
    "is_kaprekar_number",
    "is_armstrong_number",
    "is_neon_number",
    "is_strong_number",
    "is_fibonacci_number",
    "is_lucas_number",
]

def _require_number(value: object, name: str) -> Number:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    return value  # type: ignore[return-value]


def clamp(value: Number, minimum: Number, maximum: Number) -> Number:
    """Clamp a value to a closed interval [minimum, maximum].

    Args:
        value: The value to clamp.
        minimum: The lower bound of the interval.
        maximum: The upper bound of the interval.

    Returns:
        *value* constrained to [minimum, maximum].

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If *minimum* exceeds *maximum*.
    """
    _require_number(value, "value")
    _require_number(minimum, "minimum")
    _require_number(maximum, "maximum")
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    return max(minimum, min(maximum, value))


def round_to(value: float, places: int = 0) -> float:
    """Round a value to the given number of decimal places.

    Args:
        value: The value to round.
        places: The number of decimal places.

    Returns:
        The rounded value.

    Raises:
        TypeError: If *value* is not a number or *places* is not an int.
        ValueError: If *places* is negative.
    """
    _require_number(value, "value")
    if isinstance(places, bool) or not isinstance(places, int):
        raise TypeError(f"places must be an int, got {type(places).__name__}")
    if places < 0:
        raise ValueError("places must be non-negative")
    return round(value, places)


def round_half_up(value: Number, places: int = 0) -> float:
    """Round a value to the given number of decimal places, rounding halves away from zero.

    Unlike :func:`round_to`, which uses banker's rounding (round-half-to-even),
    this helper rounds a value whose fractional part is exactly 0.5 (at the
    requested precision) away from zero: ``2.5`` rounds to ``3`` and
    ``-2.5`` rounds to ``-3``.

    Args:
        value: The value to round.
        places: The number of decimal places.

    Returns:
        The rounded value.

    Raises:
        TypeError: If *value* is not a number or *places* is not an int.
        ValueError: If *places* is negative.

    Examples:
        >>> round_half_up(2.5)
        3.0
        >>> round_half_up(-2.5)
        -3.0
        >>> round_half_up(3.14159, 2)
        3.14
    """
    _require_number(value, "value")
    if isinstance(places, bool) or not isinstance(places, int):
        raise TypeError(f"places must be an int, got {type(places).__name__}")
    if places < 0:
        raise ValueError("places must be non-negative")
    factor = 10 ** places
    scaled = value * factor
    if scaled >= 0:
        return float(math.floor(scaled + 0.5) / factor)
    return float(math.ceil(scaled - 0.5) / factor)


def is_integer(value: Number) -> bool:
    """Return True if the value is integral.

    Args:
        value: The value to test.

    Returns:
        True if *value* is an integral number.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return isinstance(value, int) or float(value).is_integer()


def format_number(value: Number, precision: int = 2) -> str:
    """Format a number with thousands separators and fixed decimals.

    Args:
        value: The number to format.
        precision: The number of decimal places.

    Returns:
        A formatted string.

    Raises:
        TypeError: If *value* is not a number or *precision* is not an int.
        ValueError: If *precision* is negative.
    """
    _require_number(value, "value")
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise TypeError(f"precision must be an int, got {type(precision).__name__}")
    if precision < 0:
        raise ValueError("precision must be non-negative")
    return f"{value:,.{precision}f}"


def percentage(part: Number, total: Number, precision: int = 1) -> str:
    """Return part as a percentage of total formatted as string.

    Args:
        part: The numerator.
        total: The denominator.
        precision: The number of decimal places.

    Returns:
        A percentage string.

    Raises:
        TypeError: If any argument has an invalid type.
        ValueError: If *precision* is negative.
        ZeroDivisionError: Not raised; zero total returns "0.0%".
    """
    _require_number(part, "part")
    _require_number(total, "total")
    if isinstance(precision, bool) or not isinstance(precision, int):
        raise TypeError(f"precision must be an int, got {type(precision).__name__}")
    if precision < 0:
        raise ValueError("precision must be non-negative")
    if total == 0:
        return "0.0%"
    return f"{(part / total) * 100:.{precision}f}%"


def lerp(start: Number, stop: Number, t: Number) -> float:
    """Linearly interpolate between start and stop by factor t.

    Args:
        start: The start value.
        stop: The stop value.
        t: The interpolation factor (typically 0.0 to 1.0).

    Returns:
        The interpolated value.

    Raises:
        TypeError: If any argument is not a number.
    """
    _require_number(start, "start")
    _require_number(stop, "stop")
    _require_number(t, "t")
    return start + (stop - start) * t


def map_range(
    value: Number,
    from_min: Number,
    from_max: Number,
    to_min: Number,
    to_max: Number,
) -> float:
    """Map a value from one range to another.

    Args:
        value: The value to map.
        from_min: The minimum of the source range.
        from_max: The maximum of the source range.
        to_min: The minimum of the target range.
        to_max: The maximum of the target range.

    Returns:
        The mapped value in the target range.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If the source range has zero span.
    """
    _require_number(value, "value")
    _require_number(from_min, "from_min")
    _require_number(from_max, "from_max")
    _require_number(to_min, "to_min")
    _require_number(to_max, "to_max")
    if from_max == from_min:
        raise ValueError("source range must have non-zero span")
    t = (value - from_min) / (from_max - from_min)
    return to_min + t * (to_max - to_min)


# Alias for map_range
remap = map_range


def sign(value: Number) -> int:
    """Return the sign of a number: -1, 0, or 1.

    Args:
        value: The number whose sign is requested.

    Returns:
        -1 if *value* is negative, 1 if positive, 0 if zero.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0


def is_even(value: Number) -> bool:
    """Return True if *value* is an even integer-valued number.

    Args:
        value: The number to test.

    Returns:
        True if *value* is even.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return int(value) == value and int(value) % 2 == 0


def is_odd(value: Number) -> bool:
    """Return True if *value* is an odd integer-valued number.

    Args:
        value: The number to test.

    Returns:
        True if *value* is odd.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return int(value) == value and int(value) % 2 != 0


def is_pronic_number(value: Number) -> bool:
    """Return True if *value* is a pronic number.

    A pronic number is a product of two consecutive integers (n*(n+1)).

    Args:
        value: The number to test.

    Returns:
        True if *value* is a pronic number.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if int(value) != value or value < 0:
        return False
    n = int(value)
    root = int(n ** 0.5)
    return root * (root + 1) == n or (root + 1) * (root + 2) == n


def is_negative(value: Number) -> bool:
    """Return True if *value* is less than zero.

    Args:
        value: The number to test.

    Returns:
        True if *value* is negative.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return value < 0


def is_positive(value: Number) -> bool:
    """Return True if *value* is greater than zero.

    Args:
        value: The number to test.

    Returns:
        True if *value* is positive.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return value > 0


def is_zero(value: Number) -> bool:
    """Return True if *value* equals zero.

    Args:
        value: The number to test.

    Returns:
        True if *value* is zero.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return value == 0


def is_non_negative(value: Number) -> bool:
    """Return True if *value* is greater than or equal to zero.

    Args:
        value: The number to test.

    Returns:
        True if *value* is non-negative.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return value >= 0


def is_non_positive(value: Number) -> bool:
    """Return True if *value* is less than or equal to zero.

    Args:
        value: The number to test.

    Returns:
        True if *value* is non-positive.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    return value <= 0


def is_between(value: Number, lower: Number, upper: Number, inclusive: bool = True) -> bool:
    """Return True if *value* is between *lower* and *upper*.

    Args:
        value: The number to test.
        lower: The lower bound.
        upper: The upper bound.
        inclusive: If True (default), bounds are inclusive.

    Returns:
        True if *value* is between the bounds.

    Raises:
        TypeError: If *value*, *lower*, or *upper* are not numbers or *inclusive* is not a bool.
        ValueError: If *lower* exceeds *upper*.
    """
    _require_number(value, "value")
    _require_number(lower, "lower")
    _require_number(upper, "upper")
    if isinstance(inclusive, bool) is False or not isinstance(inclusive, bool):
        raise TypeError(f"inclusive must be a bool, got {type(inclusive).__name__}")
    if lower > upper:
        raise ValueError("lower must not exceed upper")
    if inclusive:
        return lower <= value <= upper
    return lower < value < upper


def is_close(
    a: Number,
    b: Number,
    *,
    rel_tol: Number = 1e-09,
    abs_tol: Number = 0.0,
) -> bool:
    """Return True if *a* and *b* are close to each other.

    Two values are considered close when the absolute difference between them
    is at most ``abs_tol + rel_tol * abs(b)``, matching :func:`math.isclose`.

    Args:
        a: The first number to compare.
        b: The second number to compare.
        rel_tol: The relative tolerance, must be non-negative.
        abs_tol: The minimum absolute tolerance, must be non-negative.

    Returns:
        True if *a* and *b* are within the tolerances of each other.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If *rel_tol* or *abs_tol* is negative.

    Examples:
        >>> is_close(1.0, 1.000000001)
        True
        >>> is_close(1.0, 2.0)
        False
        >>> is_close(1.0, 1.1, abs_tol=0.2)
        True
    """
    _require_number(a, "a")
    _require_number(b, "b")
    _require_number(rel_tol, "rel_tol")
    _require_number(abs_tol, "abs_tol")
    if rel_tol < 0:
        raise ValueError("rel_tol must be non-negative")
    if abs_tol < 0:
        raise ValueError("abs_tol must be non-negative")
    return math.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)


def is_finite(value: Number) -> bool:
    """Return True if *value* is finite (not infinite and not NaN).

    Args:
        value: The number to test.

    Returns:
        True if *value* is finite.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if isinstance(value, float):
        return math.isfinite(value)
    return True


def is_infinite(value: Number) -> bool:
    """Return True if *value* is infinite (positive or negative infinity).

    Args:
        value: The number to test.

    Returns:
        True if *value* is infinite.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if isinstance(value, float):
        return math.isinf(value)
    return False


def is_nan(value: Number) -> bool:
    """Return True if *value* is NaN (Not a Number).

    Args:
        value: The number to test.

    Returns:
        True if *value* is NaN.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if isinstance(value, float):
        return math.isnan(value)
    return False


def is_perfect_cube(value: Number) -> bool:
    """Return True if *value* is a perfect cube of an integer.

    Args:
        value: The number to test.

    Returns:
        True if *value* is a perfect cube.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if not is_integer(value):
        return False
    n = int(value)
    root = int(round(abs(n) ** (1.0 / 3.0)))
    while (root + 1) ** 3 <= abs(n):
        root += 1
    while root ** 3 > abs(n):
        root -= 1
    return root ** 3 == abs(n)


def is_perfect_square(value: Number) -> bool:
    """Return True if *value* is a perfect square of an integer.

    Args:
        value: The number to test.

    Returns:
        True if *value* is a perfect square.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if not is_integer(value):
        return False
    n = int(value)
    if n < 0:
        return False
    root = int(round(abs(n) ** 0.5))
    while (root + 1) ** 2 <= abs(n):
        root += 1
    while root ** 2 > abs(n):
        root -= 1
    return root ** 2 == abs(n)


def is_power_of_two(value: Number) -> bool:
    """Return True if *value* is a positive power of two.

    Args:
        value: The number to test.

    Returns:
        True if *value* is a positive power of two.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if not is_integer(value):
        return False
    n = int(value)
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def is_palindromic_number(value: Number) -> bool:
    """Return True if the decimal representation of *value* is a palindrome.

    Args:
        value: The number to test.

    Returns:
        True if *value* reads the same forwards and backwards.

    Raises:
        TypeError: If *value* is not a number.
    """
    _require_number(value, "value")
    if isinstance(value, bool):
        raise TypeError("value must be a number, got bool")
    if isinstance(value, float):
        return False
    if not isinstance(value, int):
        # try to convert
        try:
            f = float(value)
        except (TypeError, ValueError):
            raise TypeError(f"value must be a number, got {type(value).__name__}")
        if not f.is_integer():
            return False
        value_int = int(f)
        if value_int < 0:
            return False
        s = str(value_int)
        return s == s[::-1]
    n = int(value)
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]


def safe_divide(numerator: Number, denominator: Number) -> float:
    """Divide numerator by denominator, returning 0.0 when denominator is zero.

    Args:
        numerator: The dividend.
        denominator: The divisor.

    Returns:
        The quotient, or 0.0 if *denominator* is zero.

    Raises:
        TypeError: If either argument is not a number.
    """
    _require_number(numerator, "numerator")
    _require_number(denominator, "denominator")
    if denominator == 0:
        return 0.0
    return numerator / denominator



def in_range(value: Number, min_value: Number, max_value: Number, inclusive: bool = True) -> bool:
    """Check if a value is within a range.

    Args:
        value: The value to check.
        min_value: The minimum of the range.
        max_value: The maximum of the range.
        inclusive: Whether the range is inclusive (default True).

    Returns:
        True if value is in range, False otherwise.

    Raises:
        TypeError: If any numeric argument is not a number.
        ValueError: If min_value > max_value.
    """
    _require_number(value, "value")
    _require_number(min_value, "min_value")
    _require_number(max_value, "max_value")
    if min_value > max_value:
        raise ValueError("min_value must be <= max_value")
    if inclusive:
        return min_value <= value <= max_value
    return min_value < value < max_value


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of a and b.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The GCD of |a| and |b|.

    Raises:
        TypeError: If either argument is not an int.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of a and b.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The LCM of a and b.

    Raises:
        TypeError: If either argument is not an int.
        ValueError: If both are zero.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    if a == 0 and b == 0:
        raise ValueError("lcm() is not defined for both arguments being zero")
    return abs((a * b) // gcd(a, b))


def ceil_div(a: int, b: int) -> int:
    """Return the ceiling of ``a / b`` for integers.

    Args:
        a: Dividend.
        b: Divisor.

    Returns:
        The smallest integer greater than or equal to ``a / b``.

    Raises:
        TypeError: If either argument is not an int.
        ValueError: If ``b`` is zero.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    if b == 0:
        raise ValueError("ceil_div() division by zero")
    return -((-a) // b)


def is_divisible_by(a: int, b: int) -> bool:
    """Return True if *a* is divisible by *b* (i.e. *b* divides *a* evenly).

    Args:
        a: The number to test for divisibility.
        b: The divisor.

    Returns:
        True if *b* divides *a* evenly, otherwise False.

    Raises:
        TypeError: If either argument is not an int.
        ValueError: If *b* is zero.
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError("a must be an int")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError("b must be an int")
    if b == 0:
        raise ValueError("is_divisible_by() division by zero")
    return a % b == 0


def is_multiple_of(a: int, b: int) -> bool:
    """Return True if *a* is a multiple of *b* (i.e. *b* divides *a* evenly)."""
    return is_divisible_by(a, b)


def divides(a: int, b: int) -> bool:
    """Return True if *a* divides *b* (i.e. *a* divides *b* evenly)."""
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError("a must be an int")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError("b must be an int")
    if a == 0:
        raise ValueError("divides() division by zero")
    return b % a == 0


def is_coprime(a: int, b: int) -> bool:
    """Return True if *a* and *b* are coprime (gcd is 1).

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        True if *a* and *b* have no common positive factors other than 1.

    Raises:
        TypeError: If either argument is not an int.

    Examples:
        >>> is_coprime(8, 9)
        True
        >>> is_coprime(8, 12)
        False
        >>> is_coprime(1, 100)
        True
    """
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    return gcd(a, b) == 1


def digit_sum(value: int) -> int:
    """Return the sum of the decimal digits of *value*.

    The sign of *value* is ignored, so ``digit_sum(-123)`` returns ``6``.
    Only the absolute value's decimal digits are summed.

    Args:
        value: The integer whose decimal digits are summed.

    Returns:
        The sum of the decimal digits of *value*.

    Raises:
        TypeError: If *value* is not an int.
        ValueError: If *value* is negative.

    Examples:
        >>> digit_sum(123)
        6
        >>> digit_sum(-123)
        6
        >>> digit_sum(0)
        0
        >>> digit_sum(1001)
        2
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    return sum(int(digit) for digit in str(abs(value)))


def digit_count(value: int) -> int:
    """Return the number of decimal digits of *value*.

    The sign of *value* is ignored, so ``digit_count(-123)`` returns ``3``.
    ``digit_count(0)`` returns ``1``.

    Args:
        value: The integer whose decimal digits are counted.

    Returns:
        The number of decimal digits of *value*.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> digit_count(123)
        3
        >>> digit_count(-123)
        3
        >>> digit_count(0)
        1
        >>> digit_count(1001)
        4
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    return len(str(abs(value)))


def digit_product(value: int) -> int:
    """Return the product of the decimal digits of *value*.

    The sign of *value* is ignored, so ``digit_product(-123)`` returns ``6``.
    ``digit_product(0)`` returns ``0``.

    Args:
        value: The integer whose decimal digits are multiplied.

    Returns:
        The product of the decimal digits of *value*.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> digit_product(123)
        6
        >>> digit_product(-123)
        6
        >>> digit_product(0)
        0
        >>> digit_product(1001)
        0
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    product = 1
    for digit in str(abs(value)):
        product *= int(digit)
    return product


def digital_root(value: int) -> int:
    """Return the digital root of *value*.

    The digital root is the single-digit result obtained by an iterative process
    of summing digits, on each iteration using the result from the previous
    iteration to compute a digit sum. The process continues until a single-digit
    number is reached.

    The sign of *value* is ignored, so ``digital_root(-123)`` returns ``6``.
    ``digital_root(0)`` returns ``0``.

    Args:
        value: The integer to compute the digital root for.

    Returns:
        The single-digit digital root of *value* (0-9).

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> digital_root(123)
        6
        >>> digital_root(-123)
        6
        >>> digital_root(0)
        0
        >>> digital_root(9)
        9
        >>> digital_root(99)
        9
        >>> digital_root(199)
        1
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value == 0:
        return 0
    n = abs(value)
    while n >= 10:
        n = sum(int(digit) for digit in str(n))
    return n


def is_perfect_number(value: int) -> bool:
    """Return whether *value* is a perfect number.

    A perfect number is a positive integer that equals the sum of its proper
    positive divisors (excluding itself).

    Args:
        value: The integer to check.

    Returns:
        ``True`` if *value* is a perfect number, otherwise ``False``.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_perfect_number(6)
        True
        >>> is_perfect_number(28)
        True
        >>> is_perfect_number(12)
        False
        >>> is_perfect_number(1)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 2:
        return False
    total = 1
    i = 2
    while i * i <= value:
        if value % i == 0:
            total += i
            if i != value // i:
                total += value // i
        i += 1
    return total == value


def is_triangular_number(value: int) -> bool:
    """Return whether *value* is a triangular number.

    A triangular number is a number that can be represented as the sum of
    the first *n* natural numbers (``n * (n + 1) // 2``) for some
    non-negative integer *n*.

    Args:
        value: The integer to check.

    Returns:
        ``True`` if *value* is a triangular number, otherwise ``False``.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_triangular_number(0)
        True
        >>> is_triangular_number(1)
        True
        >>> is_triangular_number(3)
        True
        >>> is_triangular_number(6)
        True
        >>> is_triangular_number(10)
        True
        >>> is_triangular_number(4)
        False
        >>> is_triangular_number(-1)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    # n*(n+1)/2 = value => (8*value+1) must be a perfect square
    discriminant = 8 * value + 1
    root = math.isqrt(discriminant)
    return root * root == discriminant


def is_automorphic_number(value: int) -> bool:
    """Return True if *value* is an automorphic number.

    An automorphic number is a non-negative integer whose square ends with
    the decimal representation of the number itself. For example, ``5`` is
    automorphic because ``5 * 5 = 25`` ends in ``5``, and ``25`` is automorphic
    because ``25 * 25 = 625`` ends in ``25``. Zero is automorphic.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is automorphic, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_automorphic_number(0)
        True
        >>> is_automorphic_number(5)
        True
        >>> is_automorphic_number(6)
        True
        >>> is_automorphic_number(25)
        True
        >>> is_automorphic_number(7)
        False
        >>> is_automorphic_number(10)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    square = value * value
    return str(square).endswith(str(value))


def is_happy_number(value: int) -> bool:
    """Return True if *value* is a happy number.

    A happy number is a positive integer that, when replaced by the sum of
    the squares of its decimal digits repeatedly, eventually reaches 1. A
    number that enters a cycle not containing 1 is unhappy. Zero is happy.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is happy, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_happy_number(1)
        True
        >>> is_happy_number(7)
        True
        >>> is_happy_number(19)
        True
        >>> is_happy_number(2)
        False
        """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    seen: set[int] = set()
    n = value
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) * int(d) for d in str(n))
    return n == 1



def is_kaprekar_number(value: int) -> bool:
    """Return True if *value* is a Kaprekar number.

    A Kaprekar number is a non-negative integer whose square can be split into
    two parts that sum to the original number. The right part has the same number
    of digits as the original number (leading zeros in the right part are
    allowed). Zero and one are Kaprekar numbers.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is Kaprekar, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_kaprekar_number(1)
        True
        >>> is_kaprekar_number(9)
        True
        >>> is_kaprekar_number(45)
        True
        >>> is_kaprekar_number(297)
        True
        >>> is_kaprekar_number(7)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    if value == 0:
        return True
    square = value * value
    s = str(square)
    n = len(str(value))
    # right part must have n digits; left part may be empty
    if len(s) < n:
        return False
    right_str = s[-n:]
    left_str = s[:-n]
    left = int(left_str) if left_str else 0
    right = int(right_str)
    if right == 0:
        return False
    return left + right == value


def is_armstrong_number(value: int) -> bool:
    """Return True if *value* is an Armstrong (narcissistic) number.

    An Armstrong number is a non-negative integer that equals the sum of its
    own digits each raised to the power of the number of digits. For example,
    ``153`` is an Armstrong number because ``1**3 + 5**3 + 3**3 == 153``.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is an Armstrong number, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_armstrong_number(0)
        True
        >>> is_armstrong_number(1)
        True
        >>> is_armstrong_number(153)
        True
        >>> is_armstrong_number(9474)
        True
        >>> is_armstrong_number(10)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    digits = str(value)
    n = len(digits)
    return value == int(sum(int(d) ** n for d in digits))


def is_harshad_number(value: int) -> bool:
    """Return True if *value* is a Harshad (Niven) number.

    A Harshad number is a positive integer divisible by the sum of its
    decimal digits.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is Harshad, False otherwise.

    Raises:
        TypeError: If *value* is not an int.
        ValueError: If *value* is 0.

    Examples:
        >>> is_harshad_number(18)
        True
        >>> is_harshad_number(19)
        False
        >>> is_harshad_number(21)
        True
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value == 0:
        raise ValueError("value must be a positive integer, got 0")
    if value < 0:
        return False
    digits = str(abs(value))
    s = sum(int(d) for d in digits)
    if s == 0:
        return False
    return value % s == 0


def is_neon_number(value: int) -> bool:
    """Return True if *value* is a neon number.

    A neon number is a non-negative integer whose square's digit sum equals
    the number itself. For example, ``9`` is neon because ``9 * 9 = 81``
    and ``8 + 1 = 9``.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is a neon number, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_neon_number(0)
        True
        >>> is_neon_number(1)
        True
        >>> is_neon_number(9)
        True
        >>> is_neon_number(10)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must an int, got {type(value).__name__}")
    if value < 0:
        return False
    square = value * value
    return sum(int(d) for d in str(square)) == value


def is_strong_number(value: int) -> bool:
    """Return True if *value* is a strong number.

    A strong number is a positive integer whose sum of the factorial of its
    decimal digits equals the number itself. For example, ``145`` is strong
    because ``1! + 4! + 5! = 1 + 24 + 120 = 145``. Zero is not considered
    a strong number by this definition.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is a strong number, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_strong_number(145)
        True
        >>> is_strong_number(1)
        True
        >>> is_strong_number(2)
        True
        >>> is_strong_number(40585)
        True
        >>> is_strong_number(123)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 1:
        return False

    def _factorial(n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    return sum(_factorial(int(d)) for d in str(value)) == value


def is_fibonacci_number(value: int) -> bool:
    """Return True if *value* is a Fibonacci number.

    A Fibonacci number is a non-negative integer that appears in the
    Fibonacci sequence defined by ``F(0) = 0``, ``F(1) = 1``, and
    ``F(n) = F(n-1) + F(n-2)`` for ``n >= 2``. This helper uses the
    closed-form identity that ``5 * value**2 + 4`` or ``5 * value**2 - 4``
    must be a perfect square, which is hermetic and avoids generating the
    whole sequence.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is a Fibonacci number, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_fibonacci_number(0)
        True
        >>> is_fibonacci_number(1)
        True
        >>> is_fibonacci_number(2)
        True
        >>> is_fibonacci_number(3)
        True
        >>> is_fibonacci_number(5)
        True
        >>> is_fibonacci_number(8)
        True
        >>> is_fibonacci_number(13)
        True
        >>> is_fibonacci_number(4)
        False
        >>> is_fibonacci_number(6)
        False
        >>> is_fibonacci_number(-5)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    if value == 0:
        return True
    x = value * value
    return is_perfect_square(5 * x + 4) or is_perfect_square(5 * x - 4)


def is_lucas_number(value: int) -> bool:
    """Return True if *value* is a Lucas number.

    A Lucas number is an integer in the Lucas sequence defined by
    ``L(0) = 2``, ``L(1) = 1``, and ``L(n) = L(n-1) + L(n-2)`` for ``n >= 2``.
    The sequence begins 2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, ... This
    helper generates the sequence iteratively up to *value*, which is
    hermetic and avoids storing the whole sequence.

    Args:
        value: The integer to test.

    Returns:
        True if *value* is a Lucas number, False otherwise.

    Raises:
        TypeError: If *value* is not an int.

    Examples:
        >>> is_lucas_number(2)
        True
        >>> is_lucas_number(1)
        True
        >>> is_lucas_number(3)
        True
        >>> is_lucas_number(4)
        True
        >>> is_lucas_number(7)
        True
        >>> is_lucas_number(11)
        True
        >>> is_lucas_number(5)
        False
        >>> is_lucas_number(0)
        False
        >>> is_lucas_number(-1)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    if value < 0:
        return False
    if value in (1, 2):
        return True
    a, b = 1, 3
    while a < value:
        a, b = b, a + b
    return a == value
