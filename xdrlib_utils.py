"""XDR encoding/decoding utilities wrapping the standard library :mod:`xdrlib`."""

from __future__ import annotations

from typing import Any

try:
    import xdrlib as _xdrlib
    _XDRLIB_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when xdrlib is unavailable
    _xdrlib = None  # type: ignore[assignment]
    _XDRLIB_AVAILABLE = False

__all__: list[str] = [
    "Error",
    "Packer",
    "Unpacker",
    "ConversionError",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`xdrlib` module is available."""
    return _XDRLIB_AVAILABLE


if _XDRLIB_AVAILABLE:
    Error = getattr(_xdrlib, "Error", Exception)
    ConversionError = getattr(_xdrlib, "ConversionError", Error)
    Packer = _xdrlib.Packer
    Unpacker = _xdrlib.Unpacker
else:  # pragma: no cover - exercised when xdrlib is unavailable
    class Error(Exception):  # type: ignore[no-redef]
        pass

    class ConversionError(Error):  # type: ignore[no-redef]
        pass

    class Packer:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("xdrlib module is not available")

    class Unpacker:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("xdrlib module is not available")