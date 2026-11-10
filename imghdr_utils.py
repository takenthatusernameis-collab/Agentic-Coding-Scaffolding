"""Image format detection utilities wrapping the standard library :mod:`imghdr`."""

from __future__ import annotations

from typing import Any, Callable

try:
    import imghdr as _imghdr
    _IMGHDR_AVAILABLE = True
except Exception:
    _imghdr = None  # type: ignore[assignment]
    _IMGHDR_AVAILABLE = False

__all__: list[str] = [
    "what",
    "tests",
    "detect",
    "is_available",
    "is_image",
    "matching_formats",
    "read_header",
    "register_test",
    "supported_formats",
    "unregister_test",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`imghdr` module is available."""
    return _IMGHDR_AVAILABLE


tests: list[Callable[..., Any]] = list(getattr(_imghdr, "tests", [])) if _IMGHDR_AVAILABLE else []

if _IMGHDR_AVAILABLE:
    what = _imghdr.what

    def detect(file: Any, h: bytes | None = None) -> str | None:
        if h is None and hasattr(file, "read"):
            h = file.read(32)
            if hasattr(file, "seek"):
                try:
                    file.seek(0)
                except Exception:
                    pass
        return what(file, h)

    def is_image(file: Any, h: bytes | None = None) -> bool:
        return detect(file, h) is not None

    def matching_formats(file: Any, h: bytes | None = None) -> list[str]:
        result = detect(file, h)
        return [result] if result is not None else []

    def read_header(file: Any, h: bytes | None = None) -> bytes | None:
        del file
        return h

    def register_test(*args: Any, **kwargs: Any) -> None:
        del args, kwargs

    def unregister_test(*args: Any, **kwargs: Any) -> None:
        del args, kwargs

    def supported_formats() -> list[str]:
        return [
            "jpeg", "png", "gif", "tiff", "rgb", "pbm", "pgm", "ppm",
            "rast", "xbm", "bmp", "webp", "exr",
        ]
else:
    def what(*args: Any, **kwargs: Any) -> str | None:
        raise RuntimeError("imghdr module is not available")

    def detect(file: Any, h: bytes | None = None) -> str | None:
        del file, h
        raise RuntimeError("imghdr module is not available")

    def is_image(file: Any, h: bytes | None = None) -> bool:
        del file, h
        raise RuntimeError("imghdr module is not available")

    def matching_formats(file: Any, h: bytes | None = None) -> list[str]:
        del file, h
        raise RuntimeError("imghdr module is not available")

    def read_header(file: Any, h: bytes | None = None) -> bytes | None:
        del file, h
        raise RuntimeError("imghdr module is not available")

    def register_test(*args: Any, **kwargs: Any) -> None:
        del args, kwargs

    def unregister_test(*args: Any, **kwargs: Any) -> None:
        del args, kwargs

    def supported_formats() -> list[str]:
        return []
