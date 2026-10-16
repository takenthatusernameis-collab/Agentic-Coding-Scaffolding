"""Fraction arithmetic utilities for exact rational number operations.

This module provides helpers for performing arithmetic on
``fractions.Fraction`` values with exact precision, avoiding the binary
floating-point pitfalls of ``float`` arithmetic.
All functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Union

__all__: list[str] = [
    "to_fraction",
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "compare",
    "abs_value",
    "negate",
    "is_positive",
    "is_negative",
    "is_zero",
    "is_integer",
    "numerator",
    "denominator",
    "to_float",
    "from_float",
]

Numeric = Union[int, float, str, Fraction]


def _to_fraction(value: Any) -> Fraction:
    """Coerce *value* to a ``Fraction`` or raise ``TypeError``/``ValueError``."""
    if isinstance(value, Fraction):
        return value
    if isinstance(value, bool):
        raise TypeError(f"value must be a number, got {type(value).__name__}")
    if isinstance(value, (int, float, str)):
        try:
            return Fraction(value)
        except (ZeroDivisionError, ValueError, TypeError) as exc:
            raise ValueError(f"could not convert {value!r} to Fraction: {exc}") from exc
    raise TypeError(
        f"value must be a number or numeric string, got {type(value).__name__}"
    )


def to_fraction(value: Any) -> Fraction:
    """Convert *value* to a ``Fraction``.

    Args:
        value: An int, float, str, or Fraction to convert.

    Returns:
        The Fraction representation of *value*.

    Raises:
        TypeError: If *value`` is not a numeric type or numeric string.
        ValueError: If *value`` cannot be converted to a Fraction.

    Examples:
        >>> to_fraction("1/3")
        Fraction(1, 3)
        >>> to_fraction(0.5)
        Fraction(1, 2)
    """
    return _to_fraction(value)


def add(a: Any, b: Any) -> Fraction:
    """Return the sum of *a* and *b* as a Fraction.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The sum ``a + b`` as a Fraction.

    Raises:
        TypeError: If either operand is not numeric.
        ValueError: If either operand cannot be converted to a Fraction.

    Examples:
        >>> add("1/10", "2/10")
        Fraction(3, 10)
    """
    return _to_fraction(a) + _to_fraction(b)


def subtract(a: Any, b: Any) -> Fraction:
    """Return the difference of *a* and *b* as a Fraction.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The difference ``a - b`` as a Fraction.
    """
    return _to_fraction(a) - _to_fraction(b)


def multiply(a: Any, b: Any) -> Fraction:
    """Return the product of *a* and *b* as a Fraction.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The product ``a * b`` as a Fraction.
    """
    return _to_fraction(a) * _to_fraction(b)


def divide(a: Any, b: Any) -> Fraction:
    """Return the quotient of *a* and *b* as a Fraction.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient ``a / b`` as a Fraction.

    Raises:
        ZeroDivisionError: If *b`` is zero.
    """
    dividend = _to_fraction(a)
    divisor = _to_fraction(b)
    if divisor == 0:
        raise ZeroDivisionError("division by zero")
    return dividend / divisor


def power(base: Any, exponent: Any) -> Fraction:
    """Return ``base ** exponent`` as a Fraction.

    Args:
        base: The base value.
        exponent: The exponent value.

    Returns:
        ``base ** exponent`` as a Fraction.
    """
    result = _to_fraction(base) ** _to_fraction(exponent)
    if isinstance(result, float):
        return Fraction(result)
    return result


def compare(a: Any, b: Any) -> int:
    """Compare *a* and *b*, returning -1, 0, or 1.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        -1 if *a* < *b*, 0 if equal, 1 if *a* > *b*.
    """
    left = _to_fraction(a)
    right = _to_fraction(b)
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


def abs_value(value: Any) -> Fraction:
    """Return the absolute value of *value* as a Fraction."""
    return abs(_to_fraction(value))


def negate(value: Any) -> Fraction:
    """Return the negation of *value* as a Fraction."""
    return -_to_fraction(value)


def is_positive(value: Any) -> bool:
    """Return ``True`` if *value`` is greater than zero."""
    return _to_fraction(value) > 0


def is_negative(value: Any) -> bool:
    """Return ``True`` if *value`` is less than zero."""
    return _to_fraction(value) < 0


def is_zero(value: Any) -> bool:
    """Return ``True`` if *value`` equals zero."""
    return _to_fraction(value) == 0


def is_integer(value: Any) -> bool:
    """Return ``True`` if *value`` is a whole number (denominator is 1)."""
    return _to_fraction(value).denominator == 1


def numerator(value: Any) -> int:
    """Return the numerator of *value* in lowest terms."""
    return _to_fraction(value).numerator


def denominator(value: Any) -> int:
    """Return the denominator of *value* in lowest terms."""
    return _to_fraction(value).denominator


def to_float(value: Any) -> float:
    """Convert *value* to a ``float``."""
    return float(_to_fraction(value))


def from_float(value: Any) -> Fraction:
    """Convert *value* to an exact ``Fraction``.

    Args:
        value: A float or other numeric value to convert exactly.

    Returns:
        The exact Fraction representation of *value*.
    """
    return _to_fraction(value)
