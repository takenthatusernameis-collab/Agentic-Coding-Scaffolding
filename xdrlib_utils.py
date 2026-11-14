"""XDR encoding/decoding utilities wrapping the standard library :mod:`xdrlib`."""

from __future__ import annotations

from typing import Any, Type

__all__: list[str] = [
    "Error",
    "Packer",
    "Unpacker",
    "ConversionError",
    "is_available",
]

try:
    import xdrlib as _xdrlib

    _XDRLIB_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when xdrlib is unavailable
    _xdrlib = None  # type: ignore[assignment]
    _XDRLIB_AVAILABLE = False


def is_available() -> bool:
    """Return True if the standard library :mod:`xdrlib` module is available."""
    return _XDRLIB_AVAILABLE


Error: Type[BaseException]
ConversionError: Type[BaseException]
Packer: Any
Unpacker: Any

if _XDRLIB_AVAILABLE:
    _BaseError = getattr(_xdrlib, "Error", Exception)
    _BaseConversionError = getattr(_xdrlib, "ConversionError", _BaseError)

    class _Error(_BaseError):  # type: ignore[misc, valid-type]
        pass

    class _ConversionError(_BaseConversionError, _Error):  # type: ignore[misc, valid-type]
        pass

    Error = _Error
    ConversionError = _ConversionError
    Packer = _xdrlib.Packer
    Unpacker = _xdrlib.Unpacker
else:  # pragma: no cover - exercised when xdrlib is unavailable
    class _UnavailableError(Exception):
        pass

    class _UnavailableConversionError(_UnavailableError):
        pass

    class _UnavailablePacker:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("xdrlib module is not available")

    class _UnavailableUnpacker:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("xdrlib module is not available")

    Error = _UnavailableError
    ConversionError = _UnavailableConversionError
    Packer = _UnavailablePacker
    Unpacker = _UnavailableUnpacker
