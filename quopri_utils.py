"""Quoted-printable encoding/decoding utilities wrapping stdlib quopri."""

from __future__ import annotations

import quopri
from typing import BinaryIO


def encode(input_bytes: bytes, quotetabs: bool = False, header: bool = False) -> bytes:
    return quopri.encodestring(input_bytes, quotetabs=quotetabs, header=header)


def decode(input_bytes: bytes, header: bool = False) -> bytes:
    return quopri.decodestring(input_bytes, header=header)


def encode_file(
    inp: BinaryIO, out: BinaryIO, quotetabs: bool = False, header: bool = False
) -> None:
    quopri.encode(inp, out, quotetabs=quotetabs, header=header)


def decode_file(inp: BinaryIO, out: BinaryIO, header: bool = False) -> None:
    quopri.decode(inp, out, header=header)


def isqp(b: int) -> bool:
    """Return ``True`` when byte *b* must be quoted in quoted-printable encoding.

    Delegates to :func:`quopri.needsquoting` with ``quotetabs=False`` and
    ``header=False``: the escape character ``=`` and every byte outside the
    printable ASCII range (0x20..0x7E) require quoting. Embedded spaces and
    tabs are not quoted unless they appear at a line end, and the header
    underscore is left untouched.

    Args:
        b: The byte ordinal to test.

    Returns:
        ``True`` if *b* must be quoted, ``False`` otherwise.

    Raises:
        TypeError: If *b* is not an int.
        ValueError: If *b* is not in the range 0..255.

    Example:
        >>> isqp(ord("="))
        True
        >>> isqp(ord("a"))
        False
    """
    if isinstance(b, bool) or not isinstance(b, int):
        raise TypeError("b must be an int")
    if not 0 <= b <= 0xFF:
        raise ValueError("b must be in range 0..255")
    return bool(quopri.needsquoting(bytes([b]), quotetabs=False, header=False))  # type: ignore[attr-defined]


__all__ = ["encode", "decode", "encode_file", "decode_file", "isqp"]
