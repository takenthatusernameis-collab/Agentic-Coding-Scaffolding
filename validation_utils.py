"""Validation utility functions for common input validation tasks."""

import re
from typing import Any, Union


def is_email(email: Any) -> bool:
    """
    Check if a string is a valid email address (basic RFC-like validation).

    Args:
        email: The email string to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    if not isinstance(email, str) or not email:
        return False

    email = email.strip()
    if not email:
        return False
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(pattern.match(email))


def is_numeric(value: Any) -> bool:
    """
    Check if a value is numeric (int, float, or string representing a number).

    Args:
        value: The value to check.

    Returns:
        True if the value is numeric, False otherwise.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
    return False


def is_integer(value: Any) -> bool:
    """
    Check if a value is an integer (or string representing an integer).

    Args:
        value: The value to check.

    Returns:
        True if the value is an integer, False otherwise.
    """
    if isinstance(value, bool):
        return False
    if isinstance(value, int) and not isinstance(value, bool):
        return True
    if isinstance(value, float):
        return value.is_integer()
    if isinstance(value, str):
        if re.match(r"^[-+]?\d+$", value.strip()):
            return True
        return False
    return False


def is_alphanumeric(value: Any) -> bool:
    """
    Check if a string contains only alphanumeric characters.

    Args:
        value: The value to check.

    Returns:
        True if the string is alphanumeric, False otherwise.
    """
    if not isinstance(value, str):
        return False
    if not value:
        return False
    return bool(re.match(r"^[a-zA-Z0-9]+$", value))


def is_boolean_string(value: Any) -> bool:
    """
    Check if a string represents a boolean value.

    Args:
        value: The value to check.

    Returns:
        True if the string is a boolean string, False otherwise.
    """
    if not isinstance(value, str):
        return False
    return value.strip().lower() in ("true", "false", "1", "0")


def is_none_or_empty(value: Any) -> bool:
    """
    Check if a value is None or empty.

    Args:
        value: The value to check.

    Returns:
        True if the value is None or empty, False otherwise.
    """
    if value is None:
        return True
    if isinstance(value, str):
        return len(value) == 0
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) == 0
    return False


def min_length(value: Any, length: int) -> bool:
    """
    Check if a value has at least the minimum length.

    Args:
        value: The value to check (string, list, etc.).
        length: The minimum required length.

    Returns:
        True if the value meets the minimum length, False otherwise.
    """
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if isinstance(value, str):
        return len(value) >= length
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) >= length
    return False


def max_length(value: Any, length: int) -> bool:
    """
    Check if a value has at most the maximum length.

    Args:
        value: The value to check (string, list, etc.).
        length: The maximum allowed length.

    Returns:
        True if the value meets the maximum length, False otherwise.
    """
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if isinstance(value, str):
        return len(value) <= length
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) <= length
    return False


def matches_regex(value: Any, pattern: Union[str, re.Pattern], flags: int = 0) -> bool:
    """
    Check if a string matches a regular expression pattern.

    Args:
        value: The string to check.
        pattern: The regex pattern (string or compiled Pattern).
        flags: Regex flags (optional).

    Returns:
        True if the string matches the pattern, False otherwise.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    if isinstance(pattern, re.Pattern):
        return bool(pattern.match(value))
    elif isinstance(pattern, str):
        try:
            compiled = re.compile(pattern, flags)
            return bool(compiled.match(value))
        except re.error:
            raise ValueError("invalid regex pattern")
    else:
        raise TypeError("pattern must be a string or re.Pattern")


def is_valid_hostname(hostname: Any) -> bool:
    """
    Check if a string is a valid hostname (basic validation).

    Args:
        hostname: The hostname string to validate.

    Returns:
        True if the hostname is valid, False otherwise.
    """
    if not isinstance(hostname, str) or not hostname:
        return False
    hostname = hostname.strip()
    if not hostname:
        return False
    if hostname.endswith(".") or hostname.endswith(".."):
        return False
    if len(hostname) > 253:
        return False
    if hostname.startswith("-") or hostname.endswith("-"):
        return False
    labels = hostname.split(".")
    for label in labels:
        if not label:
            return False
        if len(label) > 63:
            return False
        if not re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$", label):
            return False
    return True
