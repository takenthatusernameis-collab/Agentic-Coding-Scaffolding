"""Number utility functions."""

from typing import Union

Number = Union[int, float]


def clamp(value: Number, minimum: Number, maximum: Number) -> Number:
    """Clamp a value to a closed interval [minimum, maximum]."""
    if minimum > maximum:
        raise ValueError("minimum must not exceed maximum")
    return max(minimum, min(maximum, value))


def round_to(value: float, places: int = 0) -> float:
    """Round a value to the given number of decimal places."""
    return round(value, places)


def is_integer(value: Number) -> bool:
    """Return True if the value is integral."""
    return isinstance(value, int) or float(value).is_integer()


def format_number(value: Number, precision: int = 2) -> str:
    """Format a number with thousands separators and fixed decimals."""
    return f"{value:,.{precision}f}"


def percentage(part: Number, total: Number, precision: int = 1) -> str:
    """Return part as a percentage of total formatted as string."""
    if total == 0:
        return "0.0%"
    return f"{(part / total) * 100:.{precision}f}%"
