"""Sun AU audio file utilities wrapping the standard library :mod:`sunau`."""

from __future__ import annotations

from typing import Any

try:
    import sunau as _sunau
    _SUNAU_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when sunau is unavailable
    _sunau = None  # type: ignore[assignment]
    _SUNAU_AVAILABLE = False

__all__: list[str] = [
    "Error",
    "open",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`sunau` module is available."""
    return _SUNAU_AVAILABLE


if _SUNAU_AVAILABLE:
    Error = _sunau.Error
    open = _sunau.open
else:  # pragma: no cover - exercised when sunau is unavailable
    class Error(Exception):  # type: ignore[no-redef]
        pass

    def open(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        raise RuntimeError("sunau module is not available")
