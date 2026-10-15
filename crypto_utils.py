"""Cryptographic utility functions for hashing, token generation, and encoding."""

import base64
import hashlib
import secrets
from typing import List

__all__: List[str] = [
    "hash_string",
    "generate_token",
    "base64_encode",
    "base64_decode",
]


def hash_string(value: str, algorithm: str = "sha256") -> str:
    """Hash a string using the specified algorithm.

    Args:
        value: The string to hash.
        algorithm: The hashing algorithm to use (e.g., "sha256", "md5",
            "sha1", "sha512"). Defaults to "sha256".

    Returns:
        The hexadecimal digest of the hash.

    Raises:
        TypeError: If ``value`` is not a string.
        ValueError: If ``algorithm`` is not a supported hash algorithm.

    Examples:
        >>> isinstance(hash_string("hello"), str)
        True
        >>> len(hash_string("hello"))
        64
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    algo = algorithm.lower()
    try:
        hasher = hashlib.new(algo)
    except ValueError:
        raise ValueError(f"unsupported hash algorithm: {algorithm}")
    hasher.update(value.encode("utf-8"))
    return hasher.hexdigest()


def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure random hexadecimal token.

    Args:
        length: The number of bytes to generate. The resulting hex string
            will be ``2 * length`` characters long. Defaults to 32.

    Returns:
        A hexadecimal string token.

    Raises:
        TypeError: If ``length`` is not an integer.
        ValueError: If ``length`` is not positive.

    Examples:
        >>> isinstance(generate_token(), str)
        True
        >>> len(generate_token(16))
        32
    """
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer")
    if length <= 0:
        raise ValueError("length must be a positive integer")
    return secrets.token_hex(length)


def base64_encode(value: str) -> str:
    """Encode a string to base64.

    Args:
        value: The string to encode.

    Returns:
        The base64-encoded string.

    Raises:
        TypeError: If ``value`` is not a string.

    Examples:
        >>> base64_encode("hello")
        'aGVsbG8='
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    encoded = base64.b64encode(value.encode("utf-8"))
    return encoded.decode("ascii")


def base64_decode(value: str) -> str:
    """Decode a base64-encoded string.

    Args:
        value: The base64-encoded string to decode.

    Returns:
        The decoded string.

    Raises:
        TypeError: If ``value`` is not a string.
        ValueError: If ``value`` is not valid base64.

    Examples:
        >>> base64_decode("aGVsbG8=")
        'hello'
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    try:
        decoded = base64.b64decode(value, validate=True)
    except Exception as exc:
        raise ValueError("invalid base64 string") from exc
    return decoded.decode("utf-8")
