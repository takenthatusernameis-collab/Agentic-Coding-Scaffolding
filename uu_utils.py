"""Uuencode utilities wrapping the standard library ``uu``."""

from __future__ import annotations

import io
import uu
from pathlib import Path

__all__ = ["uu_encode", "uu_decode"]


def uu_encode(data, out_path):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"data must be bytes, got {type(data).__name__}")
    if not isinstance(out_path, (str, Path)):
        raise TypeError(f"out_path must be str or Path, got {type(out_path).__name__}")
    with open(out_path, "wb") as f:
        uu.encode(io.BytesIO(bytes(data)), f)


def uu_decode(in_path, out_path=None):
    if not isinstance(in_path, (str, Path)):
        raise TypeError(f"in_path must be str or Path, got {type(in_path).__name__}")
    if out_path is not None and not isinstance(out_path, (str, Path)):
        raise TypeError(f"out_path must be str or Path or None, got {type(out_path).__name__}")
    buf = io.BytesIO()
    uu.decode(str(in_path), buf if out_path is None else str(out_path))
    if out_path is None:
        buf.seek(0)
        return buf.read()
    with open(out_path, "rb") as f:
        return f.read()
