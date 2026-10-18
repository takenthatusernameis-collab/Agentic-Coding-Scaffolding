"""Operator utility functions for common functional operations.

This module provides helpers wrapping standard operators and predicates
for transforming, combining, and comparing values.
"""

from __future__ import annotations

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


def identity(value: Any) -> Any:
    """Return ``value`` unchanged."""
    return value


def negate(value: Any) -> Any:
    """Return the negation of ``value`` (``-value``)."""
    return -value


def add(a: Any, b: Any) -> Any:
    """Return ``a + b``."""
    return a + b


def subtract(a: Any, b: Any) -> Any:
    """Return ``a - b``."""
    return a - b


def multiply(a: Any, b: Any) -> Any:
    """Return ``a * b``."""
    return a * b


def divide(a: Any, b: Any) -> Any:
    """Return ``a / b``."""
    return a / b


def power(base: Any, exponent: Any) -> Any:
    """Return ``base ** exponent``."""
    return base**exponent


def modulo(a: Any, b: Any) -> Any:
    """Return ``a % b``."""
    return a % b


def clamp(value: Any, low: Any, high: Any) -> Any:
    """Clamp ``value`` to the inclusive range ``[low, high]``."""
    if value < low:
        return low
    if value > high:
        return high
    return value


def between(value: Any, low: Any, high: Any, *, inclusive: bool = True) -> bool:
    """Return whether ``value`` lies between ``low`` and ``high``."""
    if inclusive:
        return bool(low <= value <= high)
    return bool(low < value < high)
