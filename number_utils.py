"""Number utility functions."""

from __future__ import annotations

from typing import List, Union

Number = Union[int, float]

__all__: List[str] = [
    "clamp",
    "round_to",
    "is_integer",
    "format_number",
    "percentage",
    "lerp",
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
