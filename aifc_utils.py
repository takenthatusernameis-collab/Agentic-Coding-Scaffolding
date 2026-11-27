"""AIFF-C audio file utilities wrapping the standard library :mod:`aifc`."""

from __future__ import annotations

from typing import Any

try:
    import aifc as _aifc
    _AIFC_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when aifc is unavailable
    _aifc = None  # type: ignore[assignment]
    _AIFC_AVAILABLE = False

__all__: list[str] = [
    "Error",
    "open",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`aifc` module is available."""
    return _AIFC_AVAILABLE


if _AIFC_AVAILABLE:
    Error = _aifc.Error

    def open(*args: Any, **kwargs: Any) -> Any:
        """Open a aifc file.

        Raises:
            FileNotFoundError: If the file does not exist.
                # audit-ignore: FileNotFoundError
        """
        return _aifc.open(*args, **kwargs)
else:  # pragma: no cover - exercised when aifc is unavailable
    class Error(Exception):  # type: ignore[no-redef]
        pass

    def open(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        raise RuntimeError("aifc module is not available")
