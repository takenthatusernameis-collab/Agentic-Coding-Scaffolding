"""Decimal arithmetic utilities for precise decimal number operations.

This module provides helpers for performing arithmetic on ``decimal.Decimal``
values with explicit precision and rounding control, avoiding the binary
floating-point pitfalls of ``float`` arithmetic.
All functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any, Union

__all__: list[str] = [
    "to_decimal",
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "quantize",
    "compare",
    "abs_value",
    "negate",
    "is_positive",
    "is_negative",
    "is_zero",
]

Numeric = Union[int, float, str, Decimal]


def _to_decimal(value: Any) -> Decimal:
    """Coerce *value* to a ``Decimal`` or raise ``TypeError``/``ValueError``."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise TypeError(f"value must be a number, got {type(value).__name__}")
    if isinstance(value, (int, float, str)):
        try:
            return Decimal(value)
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError(f"could not convert {value!r} to Decimal: {exc}") from exc
    raise TypeError(f"value must be a number or numeric string, got {type(value).__name__}")


def to_decimal(value: Any) -> Decimal:
    """Convert *value* to a ``Decimal``.

    Args:
        value: An int, float, str, or Decimal to convert.

    Returns:
        The Decimal representation of *value*.

    Raises:
        TypeError: If *value`` is not a numeric type or numeric string.
        ValueError: If *value`` cannot be converted to a Decimal.

    Examples:
        >>> to_decimal("10.5")
        Decimal('10.5')
        >>> to_decimal(3)
        Decimal('3')
    """
    return _to_decimal(value)


def add(a: Any, b: Any) -> Decimal:
    """Return the sum of *a* and *b* as a Decimal.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The sum ``a + b`` as a Decimal.

    Raises:
        TypeError: If either operand is not numeric.
        ValueError: If either operand cannot be converted to a Decimal.

    Examples:
        >>> add("0.1", "0.2")
        Decimal('0.3')
    """
    return _to_decimal(a) + _to_decimal(b)


def subtract(a: Any, b: Any) -> Decimal:
    """Return the difference of *a* and *b* as a Decimal.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The difference ``a - b`` as a Decimal.
    """
    return _to_decimal(a) - _to_decimal(b)


def multiply(a: Any, b: Any) -> Decimal:
    """Return the product of *a* and *b* as a Decimal.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The product ``a * b`` as a Decimal.
    """
    return _to_decimal(a) * _to_decimal(b)


def divide(a: Any, b: Any) -> Decimal:
    """Return the quotient of *a* and *b* as a Decimal.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient ``a / b`` as a Decimal.

    Raises:
        ZeroDivisionError: If *b`` is zero.
    """
    dividend = _to_decimal(a)
    divisor = _to_decimal(b)
    if divisor == 0:
        raise ZeroDivisionError("division by zero")
    return dividend / divisor


def power(base: Any, exponent: Any) -> Decimal:
    """Return ``base ** exponent`` as a Decimal.

    Args:
        base: The base value.
        exponent: The exponent value.

    Returns:
        ``base ** exponent`` as a Decimal.
    """
    return _to_decimal(base) ** _to_decimal(exponent)


def quantize(value: Any, places: int = 2) -> Decimal:
    """Round *value* to *places* decimal places using ROUND_HALF_UP.

    Args:
        value: The number to round.
        places: The number of decimal places (non-negative).

    Returns:
        *value* rounded to *places* decimal places.

    Raises:
        TypeError: If *places`` is not an integer.
        ValueError: If *places`` is negative.

    Examples:
        >>> quantize("3.14159", 2)
        Decimal('3.14')
    """
    if isinstance(places, bool) or not isinstance(places, int):
        raise TypeError(f"places must be an integer, got {type(places).__name__}")
    if places < 0:
        raise ValueError("places must not be negative")
    return _to_decimal(value).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def compare(a: Any, b: Any) -> int:
    """Compare *a* and *b*, returning -1, 0, or 1.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        -1 if *a* < *b*, 0 if equal, 1 if *a* > *b*.
    """
    left = _to_decimal(a)
    right = _to_decimal(b)
    if left < right:
        return -1
    if left > right:
        return 1
    return 0


def abs_value(value: Any) -> Decimal:
    """Return the absolute value of *value* as a Decimal."""
    return abs(_to_decimal(value))


def negate(value: Any) -> Decimal:
    """Return the negation of *value* as a Decimal."""
    return -_to_decimal(value)


def is_positive(value: Any) -> bool:
    """Return ``True`` if *value`` is greater than zero."""
    return _to_decimal(value) > 0


def is_negative(value: Any) -> bool:
    """Return ``True`` if *value`` is less than zero."""
    return _to_decimal(value) < 0


def is_zero(value: Any) -> bool:
    """Return ``True`` if *value`` equals zero."""
    return _to_decimal(value) == 0
