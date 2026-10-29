"""XDR encoding/decoding utilities wrapping the standard library :mod:`xdrlib`."""

from __future__ import annotations

import xdrlib as _xdrlib

__all__: list[str] = [
    "Error",
    "Packer",
    "Unpacker",
    "ConversionError",
]


Error = getattr(_xdrlib, "Error", Exception)
ConversionError = getattr(_xdrlib, "ConversionError", Error)
Packer = _xdrlib.Packer
Unpacker = _xdrlib.Unpacker
