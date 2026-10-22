"""Sound format detection utilities wrapping the standard library :mod:`sndhdr` module.

The :mod:`sndhdr` module recognizes a sound file format from the first bytes of
a file or a byte stream.  It reads a small header, compares it against the
magic number of every format it knows, and returns a ``SndHeaders`` namedtuple
describing the file.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.

.. note::

   The :mod:`sndhdr` module was deprecated in Python 3.11 and removed in Python
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
    "SndHeaders",
    "is_available",
    "what",
    "whathdr",
]

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import sndhdr as _sndhdr
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _sndhdr = None  # type: ignore[assignment]


def is_available() -> bool:
    """Return whether the standard library ``sndhdr`` module is available."""
    return _sndhdr is not None


def _require_available() -> Any:
    if _sndhdr is None:  # pragma: no cover - depends on interpreter
        raise RuntimeError(
            "the standard library 'sndhdr' module is not available on this "
            "interpreter; use a Python 3.12 or older interpreter"
        )
    return _sndhdr


def what(filename: PathLike) -> Any:
    """Guess the type of a sound file."""
    if not isinstance(filename, (str, os.PathLike)):
        raise TypeError("filename must be a str or path-like object")
    return _require_available().what(filename)


def whathdr(filename: PathLike) -> Any:
    """Recognize a sound file header."""
    if not isinstance(filename, (str, os.PathLike)):
        raise TypeError("filename must be a str or path-like object")
    return _require_available().whathdr(filename)


SndHeaders = None  # type: ignore[assignment]
if _sndhdr is not None:  # pragma: no cover - depends on interpreter
    SndHeaders = _sndhdr.SndHeaders