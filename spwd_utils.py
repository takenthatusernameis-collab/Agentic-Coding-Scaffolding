"""Shadow password database utilities wrapping the standard library :mod:`spwd`."""

from __future__ import annotations

try:
    import spwd as _spwd
    _SPWD_AVAILABLE = True
except Exception:
    _spwd = None  # type: ignore[assignment]
    _SPWD_AVAILABLE = False

__all__: list[str] = [
    "getspnam",
    "getspall",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`spwd` module is available."""
    return _SPWD_AVAILABLE


if _SPWD_AVAILABLE:
    getspnam = _spwd.getspnam
    getspall = _spwd.getspall
else:
    def getspnam(name):  # type: ignore[no-untyped-def]
        if not isinstance(name, str):
            raise TypeError("name must be a str")
        raise RuntimeError("spwd module is not available")

    def getspall():  # type: ignore[no-untyped-def]
        raise RuntimeError("spwd module is not available")
