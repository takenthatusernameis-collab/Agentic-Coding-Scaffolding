"""Cryptographically secure secrets and token utilities.

This module wraps the :mod:`secrets` standard library module to provide
cryptographically strong random values suitable for managing secrets such as
account authentication tokens, security tokens, and related secrets.
"""

from __future__ import annotations

import secrets
from typing import Sequence, TypeVar

__all__: list[str] = [
    "token_bytes",
    "token_hex",
    "token_urlsafe",
    "compare_digest",
    "randbelow",
    "randbits",
    "choice",
]

T = TypeVar("T")


def token_bytes(nbytes: int | None = None) -> bytes:
    """Return a random byte string containing cryptographically strong random bytes.

    Args:
        nbytes: The number of random bytes to return. Defaults to ``secrets.token_bytes()``
            if not provided (currently 32 bytes).

    Returns:
        A bytes object containing ``nbytes`` random bytes.

    Raises:
        ValueError: If ``nbytes`` is not a non-negative integer.
    """
    if nbytes is None:
        return secrets.token_bytes()
    if not isinstance(nbytes, int) or nbytes < 0:
        raise ValueError("nbytes must be a non-negative integer")
    return secrets.token_bytes(nbytes)


def token_hex(nbytes: int | None = None) -> str:
    """Return a random hexadecimal string containing cryptographically strong random bytes.

    Args:
        nbytes: The number of random bytes to convert to hexadecimal. Defaults to
            ``secrets.token_hex()`` if not provided (currently 16 bytes / 32 hex chars).

    Returns:
        A string of random hexadecimal characters.

    Raises:
        ValueError: If ``nbytes`` is not a non-negative integer.
    """
    if nbytes is None:
        return secrets.token_hex()
    if not isinstance(nbytes, int) or nbytes < 0:
        raise ValueError("nbytes must be a non-negative integer")
    return secrets.token_hex(nbytes)


def token_urlsafe(nbytes: int | None = None) -> str:
    """Return a random URL-safe text string containing cryptographically strong random bytes.

    Args:
        nbytes: The number of random bytes to encode. Defaults to
            ``secrets.token_urlsafe()`` if not provided.

    Returns:
        A URL-safe string of random characters.

    Raises:
        ValueError: If ``nbytes`` is not a non-negative integer.
    """
    if nbytes is None:
        return secrets.token_urlsafe()
    if not isinstance(nbytes, int) or nbytes < 0:
        raise ValueError("nbytes must be a non-negative integer")
    return secrets.token_urlsafe(nbytes)


def compare_digest(a: str | bytes, b: str | bytes) -> bool:
    """Return ``True`` if ``a`` and ``b`` are equal using a constant-time comparison.

    Args:
        a: First value to compare.
        b: Second value to compare.

    Returns:
        ``True`` if the values are equal, ``False`` otherwise. Values of mixed
        types (one ``str``, one ``bytes``) are never equal and return ``False``.
    """
    if isinstance(a, str) != isinstance(b, str):
        return False
    return secrets.compare_digest(a, b)  # type: ignore[arg-type]


def randbelow(n: int) -> int:
    """Return a random integer in the range [0, n).

    Args:
        n: The exclusive upper bound. Must be a positive integer.

    Returns:
        A random integer ``k`` such that ``0 <= k < n``.

    Raises:
        ValueError: If ``n`` is not a positive integer.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    return secrets.randbelow(n)


def randbits(k: int) -> int:
    """Return an integer with ``k`` random bits.

    Args:
        k: The number of random bits. Must be a non-negative integer.

    Returns:
        A non-negative integer with ``k`` random bits.

    Raises:
        ValueError: If ``k`` is not a non-negative integer.
    """
    if not isinstance(k, int) or k < 0:
        raise ValueError("k must be a non-negative integer")
    return secrets.randbits(k)


def choice(seq: Sequence[T]) -> T:
    """Return a randomly chosen element from a non-empty sequence.

    Args:
        seq: A non-empty sequence to choose an element from.

    Returns:
        A randomly chosen element from ``seq``.

    Raises:
        ValueError: If ``seq`` is empty.
    """
    if not seq:
        raise ValueError("seq must be a non-empty sequence")
    return secrets.choice(seq)
