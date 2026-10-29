"""Sun AU audio file utilities wrapping the standard library :mod:`sunau`."""

from __future__ import annotations

import sunau as _sunau

__all__: list[str] = [
    "Error",
    "open",
]


Error = _sunau.Error
open = _sunau.open
