"""Regular expression compile utilities wrapping the standard library
:mod:`sre_compile` module.

The :mod:`sre_compile` module compiles regular expression patterns into the
internal code representation used by the :mod:`re` engine. This wrapper
provides a validated, consistent interface with typed accessors and input
validation, and degrades gracefully when the module is unavailable.

The wrapper only reads from the standard library and never writes to the
filesystem.
"""

from __future__ import annotations

import warnings
from typing import Any

__all__ = [
    "compile_pattern",
    "is_available",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import sre_compile as _sre_compile
except Exception:  # pragma: no cover
    _sre_compile = None  # type: ignore[assignment]


def _sre_compile_module() -> Any:
    """Return the standard library ``sre_compile`` module."""
    if _sre_compile is None:  # pragma: no cover
        raise RuntimeError(
            "the standard library 'sre_compile' module is not available"
        )
    return _sre_compile


def is_available() -> bool:
    """Report whether the interpreter ships the standard library module."""
    return _sre_compile is not None


def compile_pattern(pattern: Any, flags: int = 0) -> Any:
    """Compile a pattern using :func:`sre_compile.compile`."""
    if not isinstance(flags, int):
        raise TypeError(f"flags must be int, got {type(flags).__name__}")
    mod = _sre_compile_module()
    return mod.compile(pattern, flags)
