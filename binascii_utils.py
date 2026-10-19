"""Binary-to-ASCII encoding and decoding utilities (wrapping :mod:`binascii`).

This module provides helpers for converting between binary data and various
ASCII encodings using the standard library :mod:`binascii` module, including
hexadecimal, Base64, UUencode, and quoted-printable encodings, as well as
CRC32, Adler32, and CRC-HQX checksums.
"""

from __future__ import annotations

import binascii as _binascii
import zlib
from typing import Union

__all__: list[str] = [
    "hexlify",
    "unhexlify",
    "b2a_base64",
    "a2b_base64",
    "b2a_uu",
    "a2b_uu",
    "b2a_qp",
    "a2b_qp",
    "crc32",
    "adler32",
    "crc_hqx",
]

_Data = Union[str, bytes]


def _to_bytes(data: _Data) -> bytes:
    """Normalize *data* to bytes, raising ``TypeError`` for unsupported types."""
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be str or bytes")


def hexlify(data: _Data) -> str:
    """Return the hexadecimal representation of *data* as a string.

    Args:
        data: Input string or bytes.

    Returns:
        Lowercase hexadecimal string representation of *data*.

    Raises:
        TypeError: If *data* is not str or bytes.
    """
    return _binascii.hexlify(_to_bytes(data)).decode("ascii")


def unhexlify(data: _Data) -> bytes:
    """Return the binary data represented by the hexadecimal string *data*.

    Args:
        data: Hexadecimal string or bytes.

    Returns:
        Binary representation of *data*.

    Raises:
        TypeError: If *data* is not str or bytes.
        ValueError: If *data* is not valid hexadecimal data.
    """
    return _binascii.unhexlify(_to_bytes(data))


def b2a_base64(data: _Data) -> str:
    """Return the Base64-encoded representation of *data* as a string.

    Args:
        data: Input string or bytes.

    Returns:
        Base64-encoded ASCII string with a trailing newline.

    Raises:
        TypeError: If *data* is not str or bytes.
    """
    return _binascii.b2a_base64(_to_bytes(data)).decode("ascii")


def a2b_base64(data: _Data) -> bytes:
    """Return the binary data represented by the Base64 string *data*.

    Args:
        data: Base64-encoded string or bytes.

    Returns:
        Decoded binary data.

    Raises:
        TypeError: If *data* is not str or bytes.
        ValueError: If *data* is not valid Base64 data.
    """
    return _binascii.a2b_base64(_to_bytes(data))


def b2a_uu(data: _Data) -> str:
    """Return the UUencode representation of *data* as a string.

    Args:
        data: Input string or bytes.

    Returns:
        UUencode-encoded ASCII string.

    Raises:
        TypeError: If *data* is not str or bytes.
    """
    return _binascii.b2a_uu(_to_bytes(data)).decode("ascii")


def a2b_uu(data: _Data) -> bytes:
    """Return the binary data represented by the UUencode string *data*.

    Args:
        data: UUencode-encoded string or bytes.

    Returns:
        Decoded binary data.

    Raises:
        TypeError: If *data* is not str or bytes.
        ValueError: If *data* is not valid UUencode data.
    """
    return _binascii.a2b_uu(_to_bytes(data))


def b2a_qp(data: _Data) -> str:
    """Return the quoted-printable representation of *data* as a string.

    Args:
        data: Input string or bytes.

    Returns:
        Quoted-printable-encoded ASCII string.

    Raises:
        TypeError: If *data* is not str or bytes.
    """
    return _binascii.b2a_qp(_to_bytes(data)).decode("ascii")


def a2b_qp(data: _Data) -> bytes:
    """Return the binary data represented by the quoted-printable string *data*.

    Args:
        data: Quoted-printable-encoded string or bytes.

    Returns:
        Decoded binary data.

    Raises:
        TypeError: If *data* is not str or bytes.
        ValueError: If *data* is not valid quoted-printable data.
    """
    return _binascii.a2b_qp(_to_bytes(data))


def crc32(data: _Data) -> int:
    """Return the CRC32 checksum of *data* as an unsigned 32-bit integer.

    Args:
        data: Input string or bytes.

    Returns:
        CRC32 checksum of *data*.

    Raises:
        TypeError: If *data* is not str or bytes.
    """
    return _binascii.crc32(_to_bytes(data)) & 0xFFFFFFFF


def adler32(data: _Data) -> int:
    """Return the Adler32 checksum of *data* as an unsigned 32-bit integer.

    Args:
        data: Input string or bytes.

    Returns:
        Adler32 checksum of *data*.

    Raises:
        TypeError: If *data* is not str or bytes.
    """
    return zlib.adler32(_to_bytes(data)) & 0xFFFFFFFF


def crc_hqx(data: _Data, value: int = 0) -> int:
    """Return the CRC-HQX checksum of *data* with the given initial *value*.

    Args:
        data: Input string or bytes.
        value: Initial CRC value (defaults to 0).

    Returns:
        CRC-HQX checksum of *data*.

    Raises:
        TypeError: If *data* is not str or bytes or *value* is not an int.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an int")
    return _binascii.crc_hqx(_to_bytes(data), value)
