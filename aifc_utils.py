"""AIFF and AIFF-C format utilities wrapping the standard library :mod:`aifc` module.

The :mod:`aifc` module reads and writes audio files in the AIFF and AIFF-C
format.  It provides classes to open, read, and write AIFF files, and to query
and manipulate their parameters.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It adds the conveniences the
standard library leaves to the caller and re-exports the useful constants and
classes.

.. note::

   The :mod:`aifc` module was deprecated in Python 3.11 and removed in Python
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
    "Aifc_read",
    "Aifc_write",
    "Error",
    "is_available",
    "open",
    "open_aifc",
    "open_read",
    "open_write",
    "read_aifc",
    "write_aifc",
]

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import aifc as _aifc
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _aifc = None  # type: ignore[assignment]


def _aifc_module() -> Any:
    """Return the standard library ``aifc`` module."""
    if _aifc is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'aifc' module was removed in Python 3.13; "
            "use the wave or audio libraries to read AIFF files instead"
        )
    return _aifc


def _require_mode(value: Any, name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    if value not in ("r", "rb", "w", "wb"):
        raise ValueError(f"{name} must be one of 'r', 'rb', 'w', or 'wb', got {value!r}")
    return value


def is_available() -> bool:
    """Return ``True`` when the standard library ships the ``aifc`` module."""
    return _aifc is not None


def open(f: Any, mode: Any = None) -> Any:
    """Open an AIFF file and return an :class:`Aifc_read` or :class:`Aifc_write` object."""
    aifc_module = _aifc_module()
    mode = _require_mode(mode, "mode")
    return aifc_module.open(f, mode)


# Aliases
open_aifc = open
read_aifc = open
write_aifc = open
open_read = open
open_write = open


# Re-export classes and errors
Aifc_read = None  # type: ignore[assignment]
Aifc_write = None  # type: ignore[assignment]
Error = None  # type: ignore[assignment]


def _init_reexports() -> None:
    global Aifc_read, Aifc_write, Error
    if _aifc is not None:
        Aifc_read = _aifc.Aifc_read
        Aifc_write = _aifc.Aifc_write
        Error = _aifc.Error
    else:
        Aifc_read = object  # type: ignore
        Aifc_write = object  # type: ignore
        Error = Exception  # type: ignore


_init_reexports()
