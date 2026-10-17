"""Identifier generation and validation utilities."""

from __future__ import annotations

import secrets
import string

_ALPHABET = string.ascii_letters + string.digits


def generate_id(length: int = 8) -> str:
    """Return a URL-safe random identifier of the given length.

    Args:
        length: Number of characters in the identifier. Must be positive.

    Returns:
        A random string of ``length`` characters drawn from letters and digits.

    Raises:
        TypeError: If ``length`` is not an integer.
        ValueError: If ``length`` is not positive.
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer")
    if length <= 0:
        raise ValueError("length must be greater than 0")
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def new_id() -> str:
    """Return a default-length (8 character) random identifier."""
    return generate_id()


def is_valid_id(value: str, length: int = 8) -> bool:
    """Return True if ``value`` is a valid identifier of the given length.

    Args:
        value: The identifier string to validate.
        length: The expected identifier length.

    Returns:
        True when ``value`` is a string of exactly ``length`` alphanumeric
        characters, False otherwise.
    """
    if not isinstance(value, str):
        return False
    if not isinstance(length, int) or isinstance(length, bool) or length <= 0:
        return False
    return len(value) == length and all(ch in _ALPHABET for ch in value)
