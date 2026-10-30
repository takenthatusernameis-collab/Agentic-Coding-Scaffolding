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


def is_perfect_number(n: int) -> bool:
    """Return ``True`` when *n* is a perfect number.

    A perfect number is a positive integer that equals the sum of its proper
    divisors (the divisors excluding the number itself). The smallest perfect
    number is 6 (= 1 + 2 + 3); the next are 28, 496, and 8128.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a perfect number, ``False`` otherwise. Numbers
        below 2 are never perfect.

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
    if n < 2:
        return False
    total = 0
    candidate = 1
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate and other != n:
                total += other
        candidate += 1
    return total == n
