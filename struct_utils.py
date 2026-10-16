"""Binary struct packing and unpacking utilities.

This module provides utilities for converting between Python values and
binary :mod:`struct` format representations, with configurable byte order,
input validation, and helpers for calculating the size of a format string
and validating format strings. All functions wrap the standard library
:mod:`struct` module and raise :class:`TypeError` or :class:`ValueError`
on invalid input.
"""

from __future__ import annotations

import struct
from typing import Any, Tuple, Union

__all__: list[str] = [
    "pack",
    "unpack",
    "pack_into",
    "unpack_from",
    "calcsize",
    "is_valid_format",
]


def _require_string(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _validate_format(fmt: str) -> str:
    """Validate ``fmt`` as a :mod:`struct` format string and return it.

    Raises:
        TypeError: If ``fmt`` is not a string.
        ValueError: If ``fmt`` is not a valid struct format string.
    """
    _require_string(fmt, "fmt")
    try:
        struct.calcsize(fmt)
    except struct.error as exc:
        raise ValueError(f"invalid struct format string: {exc}") from exc
    return fmt


def pack(fmt: str, *values: Any) -> bytes:
    """Pack ``values`` according to ``fmt`` and return the resulting bytes.

    Args:
        fmt: A :mod:`struct` format string (e.g. ``"<iif"``).
        values: The values to pack, matching the format specifiers.

    Returns:
        The packed binary data as a :class:`bytes` object.

    Raises:
        TypeError: If ``fmt`` is not a string.
        ValueError: If ``fmt`` is invalid or the values do not match the format.

    Examples:
        >>> pack("<B", 65)
        b'A'
        >>> pack(">I", 0x41424344)
        b'ABCD'
    """
    _validate_format(fmt)
    try:
        return struct.pack(fmt, *values)
    except struct.error as exc:
        raise ValueError(f"failed to pack values for format {fmt!r}: {exc}") from exc


def unpack(fmt: str, buffer: Union[bytes, bytearray]) -> Tuple[Any, ...]:
    """Unpack ``buffer`` according to ``fmt`` and return the resulting values.

    Args:
        fmt: A :mod:`struct` format string.
        buffer: The binary data to unpack. Its length must match
            :func:`calcsize` for ``fmt``.

    Returns:
        A tuple of unpacked values.

    Raises:
        TypeError: If ``fmt`` is not a string or ``buffer`` is not bytes/bytearray.
        ValueError: If ``fmt`` is invalid or the buffer size is incorrect.

    Examples:
        >>> unpack("<B", b'A')
        (65,)
    """
    _validate_format(fmt)
    if not isinstance(buffer, (bytes, bytearray)):
        raise TypeError("buffer must be bytes or bytearray")
    try:
        return struct.unpack(fmt, buffer)
    except struct.error as exc:
        raise ValueError(f"failed to unpack buffer for format {fmt!r}: {exc}") from exc


def pack_into(fmt: str, buffer: bytearray, offset: int, *values: Any) -> None:
    """Pack ``values`` into ``buffer`` at ``offset`` according to ``fmt``.

    Args:
        fmt: A :mod:`struct` format string.
        buffer: A mutable :class:`bytearray` to pack into.
        offset: The byte offset in ``buffer`` to start writing at.
        values: The values to pack, matching the format specifiers.

    Raises:
        TypeError: If ``fmt`` is not a string, ``buffer`` is not a bytearray,
            or ``offset`` is not an integer.
        ValueError: If ``fmt`` is invalid, ``offset`` is negative, or there is
            not enough room in ``buffer``.

    Examples:
        >>> buf = bytearray(4)
        >>> pack_into(">I", buf, 0, 0x41424344)
        >>> buf
        bytearray(b'ABCD')
    """
    _validate_format(fmt)
    if not isinstance(buffer, bytearray):
        raise TypeError("buffer must be a bytearray")
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise TypeError("offset must be an integer")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    try:
        struct.pack_into(fmt, buffer, offset, *values)
    except struct.error as exc:
        raise ValueError(f"failed to pack into buffer for format {fmt!r}: {exc}") from exc


def unpack_from(fmt: str, buffer: Union[bytes, bytearray], offset: int = 0) -> Tuple[Any, ...]:
    """Unpack values from ``buffer`` starting at ``offset`` according to ``fmt``.

    Args:
        fmt: A :mod:`struct` format string.
        buffer: The binary data to unpack from.
        offset: The byte offset to start reading from. Defaults to 0.

    Returns:
        A tuple of unpacked values.

    Raises:
        TypeError: If ``fmt`` is not a string, ``buffer`` is not bytes/bytearray,
            or ``offset`` is not an integer.
        ValueError: If ``fmt`` is invalid, ``offset`` is negative, or there is
            not enough data in ``buffer``.

    Examples:
        >>> unpack_from(">I", b'ABCD', 0)
        (1094861636,)
    """
    _validate_format(fmt)
    if not isinstance(buffer, (bytes, bytearray)):
        raise TypeError("buffer must be bytes or bytearray")
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise TypeError("offset must be an integer")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    try:
        return struct.unpack_from(fmt, buffer, offset)
    except struct.error as exc:
        raise ValueError(f"failed to unpack from buffer for format {fmt!r}: {exc}") from exc


def calcsize(fmt: str) -> int:
    """Return the size in bytes of a value described by ``fmt``.

    Args:
        fmt: A :mod:`struct` format string.

    Returns:
        The number of bytes required to pack ``fmt``.

    Raises:
        TypeError: If ``fmt`` is not a string.
        ValueError: If ``fmt`` is invalid.

    Examples:
        >>> calcsize("<h")
        2
        >>> calcsize(">I")
        4
    """
    return struct.calcsize(_validate_format(fmt))


def is_valid_format(fmt: str) -> bool:
    """Return True if ``fmt`` is a valid :mod:`struct` format string.

    Args:
        fmt: The format string to validate.

    Returns:
        True if ``fmt`` is a valid struct format string, False otherwise.

    Examples:
        >>> is_valid_format("<h")
        True
        >>> is_valid_format("!!invalid!!")
        False
    """
    if not isinstance(fmt, str):
        return False
    try:
        struct.calcsize(fmt)
        return True
    except struct.error:
        return False
