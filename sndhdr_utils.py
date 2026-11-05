"""Sound format detection utilities wrapping the standard library :mod:`sndhdr`."""

from __future__ import annotations

try:
    import sndhdr as _sndhdr
    _SNDHDR_AVAILABLE = True
except Exception:
    _sndhdr = None  # type: ignore[assignment]
    _SNDHDR_AVAILABLE = False

__all__: list[str] = [
    "what",
    "whathdr",
    "tests",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`sndhdr` module is available."""
    return _SNDHDR_AVAILABLE


if _SNDHDR_AVAILABLE:
    what = _sndhdr.what
    whathdr = _sndhdr.whathdr
    tests = getattr(_sndhdr, "tests", [])
else:
    def what(filename):  # type: ignore[no-untyped-def]
        raise RuntimeError("sndhdr module is not available")

    def whathdr(filename):  # type: ignore[no-untyped-def]
        raise RuntimeError("sndhdr module is not available")

    tests = []
