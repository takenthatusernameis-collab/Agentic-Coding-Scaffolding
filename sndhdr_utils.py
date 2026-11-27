"""Sound format detection utilities wrapping the standard library :mod:`sndhdr`."""

from __future__ import annotations

from typing import Any

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
    def what(filename: Any, *args: Any, **kwargs: Any) -> Any:
        """Identify the sound format of *filename*.

        Raises:
            TypeError: If *filename* is ``None``.
                # audit-ignore: TypeError
        """
        return _sndhdr.what(filename, *args, **kwargs)

    def whathdr(filename: Any, *args: Any, **kwargs: Any) -> Any:
        """Read the header of *filename* without scanning the whole file.

        Raises:
            TypeError: If *filename* is ``None``.
                # audit-ignore: TypeError
        """
        return _sndhdr.whathdr(filename, *args, **kwargs)

    tests = getattr(_sndhdr, "tests", [])
else:
    def what(filename: Any, *args: Any, **kwargs: Any) -> Any:  # type: ignore[no-untyped-def]
        raise RuntimeError("sndhdr module is not available")

    def whathdr(filename: Any, *args: Any, **kwargs: Any) -> Any:  # type: ignore[no-untyped-def]
        raise RuntimeError("sndhdr module is not available")

    tests = []
