"""Base64 and hexadecimal encoding/decoding utilities.

This module provides utilities for encoding and decoding data using Base64
(standard and URL-safe alphabets) and hexadecimal representations, with input
validation and helpers for checking whether a string is valid Base64 or hex.
All functions operate on :class:`str` or :class:`bytes` and raise
:class:`TypeError` or :class:`ValueError` on invalid input.
"""

from __future__ import annotations

import base64
import binascii
from typing import Union

__all__: list[str] = [
    "base64_encode",
    "base64_decode",
    "base64_encode_bytes",
    "base64_decode_bytes",
    "hex_encode",
    "hex_decode",
    "is_valid_base64",
    "is_valid_hex",
]


def _to_bytes(data: Union[str, bytes]) -> bytes:
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be a string or bytes")


def base64_encode(data: Union[str, bytes], urlsafe: bool = False) -> str:
    """Encode ``data`` as a Base64 string.

    Args:
        data: The string or bytes to encode.
        urlsafe: If True, use the URL-safe Base64 alphabet (``-`` and ``_``
            instead of ``+`` and ``/``). Defaults to False.

    Returns:
        The Base64-encoded ASCII string.

    Raises:
        TypeError: If ``data`` is not a string or bytes.

    Examples:
        >>> base64_encode("hello")
        'aGVsbG8='
        >>> base64_encode("hello", urlsafe=True)
        'aGVsbG8='
    """
    encoded = (
        base64.urlsafe_b64encode(_to_bytes(data))
        if urlsafe
        else base64.b64encode(_to_bytes(data))
    )
    return encoded.decode("ascii")


def base64_decode(encoded: str, urlsafe: bool = False) -> str:
    """Decode a Base64-encoded string back to a UTF-8 string.

    Args:
        encoded: The Base64-encoded string to decode.
        urlsafe: If True, interpret ``encoded`` using the URL-safe alphabet.
            Defaults to False.

    Returns:
        The decoded UTF-8 string.

    Raises:
        TypeError: If ``encoded`` is not a string.
        ValueError: If ``encoded`` is not valid Base64.
        UnicodeDecodeError: If the decoded bytes are not valid UTF-8.

    Examples:
        >>> base64_decode("aGVsbG8=")
        'hello'
    """
    if not isinstance(encoded, str):
        raise TypeError("encoded must be a string")
    encoded_bytes = encoded.encode("ascii")
    try:
        decoded = (
            base64.urlsafe_b64decode(encoded_bytes)
            if urlsafe
            else base64.b64decode(encoded_bytes)
        )
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid base64 data: {exc}") from exc
    return decoded.decode("utf-8")


def base64_encode_bytes(data: Union[str, bytes]) -> bytes:
    """Encode ``data`` as Base64 bytes.

    Args:
        data: The string or bytes to encode.

    Returns:
        The Base64-encoded bytes.

    Raises:
        TypeError: If ``data`` is not a string or bytes.

    Examples:
        >>> base64_encode_bytes("hello")
        b'aGVsbG8='
    """
    return base64.b64encode(_to_bytes(data))


def base64_decode_bytes(encoded: Union[str, bytes]) -> bytes:
    """Decode a Base64-encoded string or bytes back to raw bytes.

    Args:
        encoded: The Base64-encoded data to decode.

    Returns:
        The decoded bytes.

    Raises:
        TypeError: If ``encoded`` is not a string or bytes.
        ValueError: If ``encoded`` is not valid Base64.

    Examples:
        >>> base64_decode_bytes("aGVsbG8=")
        b'hello'
    """
    if isinstance(encoded, str):
        encoded_bytes = encoded.encode("ascii")
    elif isinstance(encoded, bytes):
        encoded_bytes = encoded
    else:
        raise TypeError("encoded must be a string or bytes")
    try:
        return base64.b64decode(encoded_bytes)
    except (binascii.Error, ValueError) as exc:
        raise ValueError(f"invalid base64 data: {exc}") from exc


def hex_encode(data: Union[str, bytes]) -> str:
    """Encode ``data`` as a lowercase hexadecimal string.

    Args:
        data: The string or bytes to encode.

    Returns:
        The lowercase hexadecimal-encoded string.

    Raises:
        TypeError: If ``data`` is not a string or bytes.

    Examples:
        >>> hex_encode("hello")
        '68656c6c6f'
    """
    return _to_bytes(data).hex()


def hex_decode(encoded: str) -> str:
    """Decode a hexadecimal-encoded string back to a UTF-8 string.

    Args:
        encoded: The hexadecimal-encoded string to decode.

    Returns:
        The decoded UTF-8 string.

    Raises:
        TypeError: If ``encoded`` is not a string.
        ValueError: If ``encoded`` is not valid hexadecimal or the decoded
            bytes are not valid UTF-8.

    Examples:
        >>> hex_decode("68656c6c6f")
        'hello'
    """
    if not isinstance(encoded, str):
        raise TypeError("encoded must be a string")
    try:
        decoded = bytes.fromhex(encoded)
    except ValueError as exc:
        raise ValueError(f"invalid hexadecimal data: {exc}") from exc
    return decoded.decode("utf-8")


def is_valid_base64(encoded: str, urlsafe: bool = False) -> bool:
    """Return True if ``encoded`` is valid Base64 data.

    Args:
        encoded: The string to validate.
        urlsafe: If True, validate against the URL-safe alphabet.
            Defaults to False.

    Returns:
        True if ``encoded`` is valid Base64, False otherwise.

    Examples:
        >>> is_valid_base64("aGVsbG8=")
        True
        >>> is_valid_base64("not valid base64!!!")
        False
    """
    if not isinstance(encoded, str):
        return False
    try:
        base64_decode(encoded, urlsafe=urlsafe)
        return True
    except (TypeError, ValueError, UnicodeDecodeError):
        return False


def is_valid_hex(encoded: str) -> bool:
    """Return True if ``encoded`` is valid hexadecimal data.

    Args:
        encoded: The string to validate.

    Returns:
        True if ``encoded`` is valid hexadecimal, False otherwise.

    Examples:
        >>> is_valid_hex("68656c6c6f")
        True
        >>> is_valid_hex("zzzz")
        False
    """
    if not isinstance(encoded, str):
        return False
    try:
        bytes.fromhex(encoded)
        return True
    except ValueError:
        return False
