"""Cgitb utilities wrapping the standard library :mod:`cgitb`."""

from __future__ import annotations

import cgitb as _cgitb
from typing import Any

__all__: list[str] = [
    "enable",
    "disable",
    "reset",
    "lookup",
    "scanvars",
    "handler",
    "text",
    "html",
    "small",
    "strong",
    "grey",
    "pink",
    "blue",
    "is_available",
]

enable = _cgitb.enable
reset = getattr(_cgitb, "reset", lambda: None)
lookup = getattr(_cgitb, "lookup", lambda *a, **k: None)
scanvars = getattr(_cgitb, "scanvars", lambda *a, **k: ([], []))
handler = getattr(_cgitb, "handler", lambda *a, **k: None)
text = getattr(_cgitb, "text", lambda *a, **k: "")
html = getattr(_cgitb, "html", lambda *a, **k: "")
small = getattr(_cgitb, "small", lambda x: f"<small>{x}</small>")
strong = getattr(_cgitb, "strong", lambda x: f"<strong>{x}</strong>")
grey = getattr(_cgitb, "grey", lambda x: f"<span style='color: gray'>{x}</span>")
pink = getattr(_cgitb, "pink", lambda x: f"<span style='color: pink'>{x}</span>")
blue = getattr(_cgitb, "blue", lambda x: f"<span style='color: blue'>{x}</span>")


def disable() -> None:
    if hasattr(_cgitb, "disable"):
        return _cgitb.disable()
    import sys

    sys.excepthook = sys.__excepthook__


def is_available() -> bool:
    """Return True if the standard library :mod:`cgitb` module is available."""
    return True
