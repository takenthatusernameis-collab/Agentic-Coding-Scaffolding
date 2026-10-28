"""Utilities for runtime type checking."""


def is_str(value: object) -> bool:
    """Return True if value is a string."""
    return isinstance(value, str)


def is_int(value: object) -> bool:
    """Return True if value is an int (excluding bool)."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_float(value: object) -> bool:
    """Return True if value is a float."""
    return isinstance(value, float)


def is_bool(value: object) -> bool:
    """Return True if value is a bool."""
    return isinstance(value, bool)


def is_list(value: object) -> bool:
    """Return True if value is a list."""
    return isinstance(value, list)


def is_dict(value: object) -> bool:
    """Return True if value is a dict."""
    return isinstance(value, dict)


def is_tuple(value: object) -> bool:
    """Return True if value is a tuple."""
    return isinstance(value, tuple)


def is_set(value: object) -> bool:
    """Return True if value is a set."""
    return isinstance(value, set)


def is_none(value: object) -> bool:
    """Return True if value is None."""
    return value is None


def is_numeric(value: object) -> bool:
    """Return True if value is int or float (excluding bool)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_iterable(value: object) -> bool:
    """Return True if value is iterable but not a string."""
    if isinstance(value, str):
        return False
    try:
        iter(value)
        return True
    except TypeError:
        return False


def is_callable(value: object) -> bool:
    """Return True if value is callable."""
    return callable(value)


def ensure_type(value: object, expected_type: type, name: str = "value") -> object:
    """Ensure value is of expected_type, raising TypeError otherwise.

    Args:
        value: The value to check.
        expected_type: The expected type.
        name: Name used in the error message.

    Returns:
        The value unchanged if type matches.

    Raises:
        TypeError: If value is not an instance of expected_type.
    """
    if not isinstance(value, expected_type):
        raise TypeError(
            f"{name} must be of type {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )
    return value


def coerce_to_str(value: object) -> str:
    """Convert value to string."""
    return str(value)
