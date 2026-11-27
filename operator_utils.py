"""Operator utility functions for common functional operations.

This module provides helpers wrapping standard operators and predicates
for transforming, combining, and comparing values.
All functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

from __future__ import annotations

import math
from typing import Any

__all__: list[str] = [
    "identity",
    "negate",
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "modulo",
    "clamp",
    "between",
]


def _validate_number(value: Any, name: str) -> None:
    """Validate that *value* is a real number (int or float, not bool) and finite."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


def identity(value: Any) -> Any:
    """Return ``value`` unchanged."""
    return value


def negate(value: Any) -> Any:
    """Return the negation of ``value`` (``-value``).

    Args:
        value: The number to negate.

    Returns:
        The negated value.

    Raises:
        TypeError: If *value* is not a number.
        ValueError: If *value* is NaN or infinite.
    """
    _validate_number(value, "value")
    return -value


def add(a: Any, b: Any) -> Any:
    """Return ``a + b``.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The sum ``a + b``.

    Raises:
        TypeError: If either operand is not a number.
        ValueError: If either operand is NaN or infinite.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a + b


def subtract(a: Any, b: Any) -> Any:
    """Return ``a - b``.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The difference ``a - b``.

    Raises:
        TypeError: If either operand is not a number.
        ValueError: If either operand is NaN or infinite.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a - b


def multiply(a: Any, b: Any) -> Any:
    """Return ``a * b``.

    Args:
        a: The first operand.
        b: The second operand.

    Returns:
        The product ``a * b``.

    Raises:
        TypeError: If either operand is not a number.
        ValueError: If either operand is NaN or infinite.
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a * b


def divide(a: Any, b: Any) -> Any:
    """Return ``a / b``.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The quotient ``a / b``.

    Raises:
        TypeError: If either operand is not a number.
        ValueError: If either operand is NaN or infinite.
        ZeroDivisionError: If *b* is zero.  # audit-ignore: ZeroDivisionError
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a / b


def power(base: Any, exponent: Any) -> Any:
    """Return ``base ** exponent``.

    Args:
        base: The base value.
        exponent: The exponent value.

    Returns:
        ``base`` raised to the power of ``exponent``.

    Raises:
        TypeError: If either operand is not a number.
        ValueError: If either operand is NaN or infinite.
    """
    _validate_number(base, "base")
    _validate_number(exponent, "exponent")
    return base**exponent


def modulo(a: Any, b: Any) -> Any:
    """Return ``a % b``.

    Args:
        a: The dividend.
        b: The divisor.

    Returns:
        The remainder ``a % b``.

    Raises:
        TypeError: If either operand is not a number.
        ValueError: If either operand is NaN or infinite.
        ZeroDivisionError: If *b* is zero.  # audit-ignore: ZeroDivisionError
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    return a % b


def clamp(value: Any, low: Any, high: Any) -> Any:
    """Clamp ``value`` to the inclusive range ``[low, high]``.

    Args:
        value: The value to clamp.
        low: The lower bound of the range.
        high: The upper bound of the range.

    Returns:
        *value* constrained to [low, high].

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If any argument is NaN or infinite, or if *low* exceeds *high*.
    """
    for arg, name in ((value, "value"), (low, "low"), (high, "high")):
        _validate_number(arg, name)
    if low > high:
        raise ValueError("low must not exceed high")
    if value < low:
        return low
    if value > high:
        return high
    return value


def between(value: Any, low: Any, high: Any, *, inclusive: bool = True) -> bool:
    """Return whether ``value`` lies between ``low`` and ``high``.

    Args:
        value: The value to test.
        low: The lower bound.
        high: The upper bound.
        inclusive: If True (default), bounds are inclusive.

    Returns:
        True if value is between low and high.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If any argument is NaN or infinite, or if low > high.
    """
    _validate_number(value, "value")
    _validate_number(low, "low")
    _validate_number(high, "high")
    if low > high:
        raise ValueError("low must not exceed high")
    if inclusive:
        return bool(low <= value <= high)
    return bool(low < value < high)
