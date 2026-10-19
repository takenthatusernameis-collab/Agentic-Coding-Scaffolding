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
    return bool(quopri.isqp(b))


__all__ = ["encode", "decode", "encode_file", "decode_file", "isqp"]
