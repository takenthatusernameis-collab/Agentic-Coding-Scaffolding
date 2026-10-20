"""Ambiguous indentation detection utilities wrapping the standard library :mod:`tabnanny` module.

The :mod:`tabnanny` module scans Python source files for ambiguous indentation,
that is, a mix of tabs and spaces that makes a program hard to read or that
changes the meaning of a program depending on how the indentation is
interpreted.  This wrapper validates every argument before the standard library
is reached, so a caller gets a clear :class:`TypeError` instead of an opaque
failure.  It also re-exports :class:`NannyNag`, the exception raised when
ambiguous indentation is found.

The module is pure computation, so it works on every platform and never
touches the network or a subprocess.  It only reads the files the caller points
it at.
"""

from __future__ import annotations

import os as _os
import tabnanny as _tabnanny

__all__: list[str] = [
    "NannyNag",
    "check",
    "process_tokens",
]

#: The exception raised by :mod:`tabnanny` when ambiguous indentation is found.
NannyNag = _tabnanny.NannyNag


def check(path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes]) -> None:
    """Check *path* (a file or a directory) for ambiguous indentation.

    Args:
        path: The file or directory to check.

    Raises:
        TypeError: If *path* is not a path-like object.
        NannyNag: If *path* contains ambiguous indentation.
    """
    if not isinstance(path, (str, bytes, _os.PathLike)):
        raise TypeError(f"path must be a path-like object, got {type(path).__name__}")
    _tabnanny.check(path)


def process_tokens(tokens) -> None:
    """Process *tokens* and raise :class:`NannyNag` on ambiguous indentation.

    Args:
        tokens: An iterable of tokens as produced by :mod:`tokenize`.

    Raises:
        TypeError: If *tokens* is not iterable.
        NannyNag: If the tokens contain ambiguous indentation.
    """
    try:
        iterator = iter(tokens)
    except TypeError:
        raise TypeError(f"tokens must be iterable, got {type(tokens).__name__}") from None
    _tabnanny.process_tokens(iterator)
