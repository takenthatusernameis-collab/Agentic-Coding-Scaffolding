"""AIFF-C audio file utilities wrapping the standard library :mod:`aifc`."""

from __future__ import annotations

import aifc as _aifc

__all__: list[str] = [
    "Error",
    "open",
]


Error = _aifc.Error
open = _aifc.open
