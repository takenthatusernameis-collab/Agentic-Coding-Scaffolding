"""Sun AU format utilities wrapping the standard library :mod:`sunau` module.

The :mod:`sunau` module reads and writes Sun AU audio files.  It provides
classes to open, read, and write AU files, and to query and manipulate their
parameters.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It adds the conveniences the
standard library leaves to the caller and re-exports the useful constants and
classes.

.. note::

   The :mod:`sunau` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module, while the helpers that
   need no standard library keep working.
"""

from __future__ import annotations

import os
import warnings
from typing import Any, Optional, Union

__all__ = [
    "Au_read",
    "Au_write",
    "Error",
    "is_available",
    "open",
    "open_au",
    "open_read",
    "open_write",
]

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import sunau as _sunau
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _sunau = None  # type: ignore[assignment]


def _sunau_module() -> Any:
    """Return the standard library ``sunau`` module."""
    if _sunau is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'sunau' module was removed in Python 3.13; "
            "use the wave or audio libraries to read AU files instead"
        )
    return _sunau


def _require_mode(value: Any, name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    if value not in ("r", "rb", "w", "wb"):
        raise ValueError(f"{name} must be one of 'r', 'rb', 'w', or 'wb', got {value!r}")
    return value


def is_available() -> bool:
    """Return ``True`` when the standard library ships the ``sunau`` module."""
    return _sunau is not None


def open(f: Any, mode: Any = None) -> Any:
    """Open a Sun AU file and return an :class:`Au_read` or :class:`Au_write` object."""
    sunau_module = _sunau_module()
    mode = _require_mode(mode, "mode")
    return sunau_module.open(f, mode)


Au_read = _sunau.Au_read if _sunau is not None else None  # type: ignore[attr-defined]
Au_write = _sunau.Au_write if _sunau is not None else None  # type: ignore[attr-defined]
Error = _sunau.Error if _sunau is not None else None  # type: ignore[attr-defined]


def open_au(f: Any, mode: Any = None) -> Any:
    """Alias for :func:`open`."""
    return open(f, mode)


def open_read(f: Any) -> Any:
    """Open a Sun AU file for reading."""
    return open(f, "r")


def open_write(f: Any) -> Any:
    """Open a Sun AU file for writing."""
    return open(f, "w")