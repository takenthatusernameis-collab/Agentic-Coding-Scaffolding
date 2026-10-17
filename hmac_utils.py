"""HMAC-based message authentication utilities.

This module provides utilities for computing HMAC signatures using the
standard library :mod:`hmac` and :mod:`hashlib` modules. It supports multiple
hash algorithms (MD5, SHA1, SHA256, SHA512), constant-time signature
verification, and a generic ``hmac_new`` entry point that accepts any of the
supported algorithms.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Union

__all__: list[str] = [
    "hmac_md5",
    "hmac_sha1",
    "hmac_sha256",
    "hmac_sha512",
    "hmac_new",
    "sign",
    "verify",
    "compare_digest",
]

_ALGORITHMS: tuple[str, ...] = ("md5", "sha1", "sha256", "sha512")


def _normalize_input(data: Union[str, bytes]) -> bytes:
    """Normalize input to bytes."""
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be str or bytes")


def _normalize_key(key: Union[str, bytes]) -> bytes:
    """Normalize key to bytes."""
    if isinstance(key, str):
        return key.encode("utf-8")
    if isinstance(key, bytes):
        return key
    raise TypeError("key must be str or bytes")


def _hmac(data: Union[str, bytes], key: Union[str, bytes], algorithm: str) -> str:
    """Compute the HMAC digest of *data* using *key* and *algorithm*."""
    if algorithm not in _ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    message = _normalize_input(data)
    secret = _normalize_key(key)
    return hmac.new(secret, message, getattr(hashlib, algorithm)).hexdigest()


def hmac_md5(data: Union[str, bytes], key: Union[str, bytes]) -> str:
    """Compute the HMAC-MD5 digest of *data* using *key*.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.

    Returns:
        Hexadecimal HMAC-MD5 digest.

    Raises:
        TypeError: If *data* or *key* is not str or bytes.
    """
    return _hmac(data, key, "md5")


def hmac_sha1(data: Union[str, bytes], key: Union[str, bytes]) -> str:
    """Compute the HMAC-SHA1 digest of *data* using *key.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.

    Returns:
        Hexadecimal HMAC-SHA1 digest.

    Raises:
        TypeError: If *data* or *key* is not str or bytes.
    """
    return _hmac(data, key, "sha1")


def hmac_sha256(data: Union[str, bytes], key: Union[str, bytes]) -> str:
    """Compute the HMAC-SHA256 digest of *data* using *key*.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.

    Returns:
        Hexadecimal HMAC-SHA256 digest.

    Raises:
        TypeError: If *data* or *key* is not str or bytes.
    """
    return _hmac(data, key, "sha256")


def hmac_sha512(data: Union[str, bytes], key: Union[str, bytes]) -> str:
    """Compute the HMAC-SHA512 digest of *data* using *key*.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.

    Returns:
        Hexadecimal HMAC-SHA512 digest.

    Raises:
        TypeError: If *data* or *key* is not str or bytes.
    """
    return _hmac(data, key, "sha512")


def hmac_new(
    data: Union[str, bytes],
    key: Union[str, bytes],
    algorithm: str = "sha256",
) -> str:
    """Compute the HMAC digest of *data* using *key* and *algorithm*.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512).
            Defaults to "sha256".

    Returns:
        Hexadecimal HMAC digest.

    Raises:
        TypeError: If *data* or *key* is not str or bytes.
        ValueError: If *algorithm* is not supported.
    """
    return _hmac(data, key, algorithm)


def sign(
    data: Union[str, bytes],
    key: Union[str, bytes],
    algorithm: str = "sha256",
) -> str:
    """Sign *data* with *key* using *algorithm*, returning the HMAC digest.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512).
            Defaults to "sha256".

    Returns:
        Hexadecimal HMAC signature.

    Raises:
        TypeError: If *data* or *key* is not str or bytes.
        ValueError: If *algorithm* is not supported.
    """
    return _hmac(data, key, algorithm)


def verify(
    data: Union[str, bytes],
    key: Union[str, bytes],
    signature: str,
    algorithm: str = "sha256",
) -> bool:
    """Verify *signature* against the HMAC of *data* using *key* and *algorithm.

    Uses a constant-time comparison to avoid timing attacks.

    Args:
        data: Input string or bytes.
        key: Secret key as a string or bytes.
        signature: Hexadecimal HMAC signature to verify.
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512).
            Defaults to "sha256".

    Returns:
        True if the signature matches, False otherwise.

    Raises:
        TypeError: If *data*, *key*, or *signature* is not a string/bytes.
        ValueError: If *algorithm* is not supported.
    """
    expected = _hmac(data, key, algorithm)
    return compare_digest(signature, expected)


def compare_digest(a: str, b: str) -> bool:
    """Return True if *a* and *b* are equal using a constant-time comparison.

    Args:
        a: First string to compare.
        b: Second string to compare.

    Returns:
        True if the strings are equal, False otherwise.

    Raises:
        TypeError: If either argument is not a string.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return hmac.compare_digest(a, b)
