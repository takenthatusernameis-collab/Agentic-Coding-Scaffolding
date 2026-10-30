"""Utilities for numeric abstract base classes (wrapping :mod:`numbers`).

This module re-exports the numeric abstract base classes of the standard
library :mod:`numbers` module and adds small, hermetic predicates that work
for any object, regardless of whether it is registered with the ABC system.
Every helper validates its arguments before the computation starts, so a
caller gets a clear :class:`TypeError` instead of an opaque failure.
"""

from __future__ import annotations

import numbers as _numbers

__all__: list[str] = [
    "Number",
    "Complex",
    "Real",
    "Rational",
    "Integral",
    "is_number",
    "is_integral",
    "is_perfect_number",
    "is_abundant_number",
    "is_deficient_number",
    "is_strong_number",
    "is_harshad_number",
    "is_neon_number",
    "is_armstrong_number",
    "is_automorphic_number",
]

#: The abstract base class for all numbers.
Number = _numbers.Number

#: The abstract base class for complex numbers.
Complex = _numbers.Complex

#: The abstract base class for real numbers.
Real = _numbers.Real

#: The abstract base class for rational numbers.
Rational = _numbers.Rational

#: The abstract base class for integral numbers.
Integral = _numbers.Integral


def is_number(obj: object) -> bool:
    """Return ``True`` when *obj* is a number.

    A number is any object registered with (or subclass of) the
    :class:`numbers.Number` abstract base class, which covers ``int``,
    ``float``, ``complex``, ``Fraction``, ``Decimal``, and similar types.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is a number, ``False`` otherwise.

    Examples:
        >>> is_number(5)
        True
        >>> is_number(1.5)
        True
        >>> is_number(2 + 3j)
        True
        >>> is_number("x")
        False
    """
    return isinstance(obj, Number)


def is_integral(obj: object) -> bool:
    """Return ``True`` when *obj* is an integral number.

    An integral number is any object registered with (or subclass of) the
    :class:`numbers.Integral` abstract base class, which covers ``int``,
    ``bool``, and other exact integer-like types, but not ``float`` or
    ``complex``.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is an integral number, ``False`` otherwise.

    Examples:
        >>> is_integral(5)
        True
        >>> is_integral(True)
        True
        >>> is_integral(1.5)
        False
        >>> is_integral("x")
        False
    """
    return isinstance(obj, Integral)

def is_abundant_number(n: int) -> bool:
    """Return ``True`` when *n* is an abundant number.

    An abundant number is a positive integer whose sum of proper divisors
    (the divisors excluding the number itself) is greater than the number.
    The smallest abundant number is 12 (= 1 + 2 + 3 + 4 + 6).

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an abundant number, ``False`` otherwise. Numbers
        below 2 are never abundant.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_abundant_number(12)
        True
        >>> is_abundant_number(24)
        True
        >>> is_abundant_number(6)
        False
        >>> is_abundant_number(1)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 2:
        return False
    total = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate:
                total += other
        candidate += 1
    return bool(total > n)


def is_deficient_number(n: int) -> bool:
    """Return ``True`` when *n* is a deficient number.

    A deficient number is a positive integer whose sum of proper divisors
    (the divisors excluding the number itself) is less than the number.
    The smallest deficient number is 1 (sum is 0) and most numbers are
    deficient; primes p have sum of proper divisors 1 < p for p > 1.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a deficient number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_deficient_number(1)
        True
        >>> is_deficient_number(2)
        True
        >>> is_deficient_number(4)
        True
        >>> is_deficient_number(6)
        False
        >>> is_deficient_number(12)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    if n == 1:
        return True
    total = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate:
                total += other
        candidate += 1
    return bool(total < n)


def is_perfect_number(n: int) -> bool:
    """Return ``True`` when *n* is a perfect number.

    A perfect number is a positive integer that is equal to the sum of its
    proper positive divisors (the divisors excluding the number itself).
    The first few perfect numbers are 6, 28, 496, 8128, ...

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a perfect number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_perfect_number(6)
        True
        >>> is_perfect_number(28)
        True
        >>> is_perfect_number(496)
        True
        >>> is_perfect_number(12)
        False
        >>> is_perfect_number(1)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    if n == 1:
        return False
    total = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate:
                total += other
        candidate += 1
    return bool(total == n)


def proper_divisors(n: int) -> list[int]:
    """Return the proper divisors of *n* (divisors excluding *n* itself).

    Args:
        n: The positive integer whose proper divisors are returned.

    Returns:
        A sorted list of the proper divisors of *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.

    Examples:
        >>> proper_divisors(1)
        []
        >>> proper_divisors(6)
        [1, 2, 3]
        >>> proper_divisors(28)
        [1, 2, 4, 7, 14]
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError(f"n must be a positive integer, got {n}")
    if n == 1:
        return []
    result = [1]
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            result.append(candidate)
            other = n // candidate
            if other != candidate and other != n:
                result.append(other)
        candidate += 1
    result = sorted(set(result))
    if n in result:
        result.remove(n)
    return result


def is_strong_number(n: int) -> bool:
    """Return ``True`` when *n* is a strong number.

    A strong number (also called a factorial number) is a positive integer
    whose sum of the factorial of its digits is equal to the number itself.
    The first few strong numbers are 1, 2, 145, 40585, 40585, ...

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a strong number, ``False`` otherwise. Numbers
        below 1 are never strong.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_strong_number(1)
        True
        >>> is_strong_number(2)
        True
        >>> is_strong_number(145)
        True
        >>> is_strong_number(40585)
        True
        >>> is_strong_number(123)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False

    def _factorial(x: int) -> int:
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result

    total = 0
    for digit in str(n):
        total += _factorial(int(digit))
    return bool(total == n)


def is_harshad_number(n: int) -> bool:
    """Return ``True`` when *n* is a harshad (Niven) number.

    A harshad number is an integer divisible by the sum of its decimal
    digits. Also known as a Niven number.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is divisible by the sum of its digits,
        ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_harshad_number(18)
        True
        >>> is_harshad_number(19)
        False
        >>> is_harshad_number(1)
        True
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n == 0:
        return True
    digit_sum = sum(int(d) for d in str(abs(n)))
    if digit_sum == 0:
        return False
    return n % digit_sum == 0


def is_neon_number(n: int) -> bool:
    """Return ``True`` when *n* is a neon number.

    A neon number is a number where the sum of the digits of its square is
    equal to the number itself (e.g. 9 is neon because 9^2 = 81 and 8 + 1 = 9).
    The only neon numbers are 0, 1, and 9.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a neon number, ``False`` otherwise. Numbers below 0
        are never neon.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_neon_number(9)
        True
        >>> is_neon_number(1)
        True
        >>> is_neon_number(0)
        True
        >>> is_neon_number(45)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    total = sum(int(d) for d in str(n * n))
    return bool(total == n)


def is_armstrong_number(n: int) -> bool:
    """Return ``True`` when *n* is an Armstrong (narcissistic) number.

    An Armstrong number is a number that is equal to the sum of its own
    digits each raised to the power of the number of digits.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an Armstrong number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_armstrong_number(153)
        True
        >>> is_armstrong_number(370)
        True
        >>> is_armstrong_number(371)
        True
        >>> is_armstrong_number(407)
        True
        >>> is_armstrong_number(123)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    digits = str(n)
    power = len(digits)
    total = sum(int(d) ** power for d in digits)
    return bool(total == n)


def is_automorphic_number(n: int) -> bool:
    """Return ``True`` when *n* is an automorphic number.

    An automorphic number is a number whose square ends with the same
    digits as the number itself. For example, 5^2 = 25 ends with 5,
    25^2 = 625 ends with 25.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an automorphic number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_automorphic_number(5)
        True
        >>> is_automorphic_number(6)
        True
        >>> is_automorphic_number(25)
        True
        >>> is_automorphic_number(76)
        True
        >>> is_automorphic_number(2)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    square = str(n * n)
    num_str = str(n)
    return square.endswith(num_str)
