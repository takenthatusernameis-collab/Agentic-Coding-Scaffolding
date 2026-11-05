"""Image format detection utilities wrapping the standard library :mod:`imghdr`."""

from __future__ import annotations

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


if _IMGHDR_AVAILABLE:
    what = _imghdr.what
    tests = getattr(_imghdr, "tests", [])
    def detect(file, h=None):  # type: ignore[no-untyped-def]
        if h is None and hasattr(file, "read"):
            h = file.read(32)
            if hasattr(file, "seek"):
                try:
                    file.seek(0)
                except Exception:
                    pass
        return what(file, h)
    is_image = lambda file, h=None: detect(file, h) is not None  # type: ignore[no-untyped-def]
    matching_formats = lambda file, h=None: [detect(file, h)] if detect(file, h) is not None else []  # type: ignore[no-untyped-def]
    read_header = lambda file, h=None: h  # type: ignore[no-untyped-def]
    register_test = getattr(_imghdr, "tests", []).append if False else (lambda *args, **kwargs: None)  # type: ignore[no-untyped-def]
    unregister_test = lambda *args, **kwargs: None  # type: ignore[no-untyped-def]
    supported_formats = lambda: ["jpeg", "png", "gif", "tiff", "rgb", "pbm", "pgm", "ppm", "rast", "xbm", "bmp", "webp", "exr"]  # type: ignore[no-untyped-def]
else:
    def what(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("imghdr module is not available")
    tests = []
    def detect(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("imghdr module is not available")
    def is_image(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("imghdr module is not available")
    def matching_formats(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("imghdr module is not available")
    def read_header(*args, **kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("imghdr module is not available")
    def register_test(*args, **kwargs):  # type: ignore[no-untyped-def]
        pass
    def unregister_test(*args, **kwargs):  # type: ignore[no-untyped-def]
        pass
    def supported_formats():  # type: ignore[no-untyped-def]
        return []
