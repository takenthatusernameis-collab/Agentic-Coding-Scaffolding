"""UUencode and UUdecode utilities wrapping the standard library :mod:`uu`."""

from __future__ import annotations

import io as _io
import uu as _uu
from typing import Any

__all__: list[str] = [
    "Error",
    "encode",
    "decode",
    "encode_file",
    "decode_file",
]


Error = _uu.Error


def encode(in_file: Any, out_file: Any, name: str | None = None, mode: int | None = None, backtick: bool = False) -> None:
    if name is None:
        name = "-"
    if mode is None:
        mode = 0o666
    try:
        _uu.encode(in_file, out_file, name, mode, backtick=backtick)
    except Exception:
        # Try different calling convention for compatibility
        _uu.encode(in_file, out_file, name, mode)


def decode(in_file: Any, out_file: Any | None = None, mode: int | None = None, quiet: int = 0) -> None:
    if mode is None:
        mode = 0o666
    try:
        _uu.decode(in_file, out_file, mode, quiet)
    except Exception:
        _uu.decode(in_file, out_file, mode)


def encode_file(in_file: Any, out_file: Any, name: str = "-", mode: int = 0o666, backtick: bool = False) -> None:
    encode(in_file, out_file, name, mode, backtick)


def decode_file(in_file: Any, out_file: Any | None = None, mode: int = 0o666, quiet: int = 0) -> None:
    decode(in_file, out_file, mode, quiet)
