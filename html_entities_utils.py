"""HTML entity utilities wrapping the standard library html.entities module.

Provides helpers for working with HTML entities.
"""

import html.entities as entities
from typing import Dict

__all__ = [
    "name2codepoint",
    "codepoint2name",
    "html5",
    "entitydefs",
    "escape",
    "unescape",
    "is_available",
]


def is_available() -> bool:
    """Return True if html.entities is available."""
    return True


name2codepoint: Dict[str, int] = entities.name2codepoint
codepoint2name: Dict[int, str] = entities.codepoint2name
html5: Dict[str, str] = getattr(entities, "html5", {})
entitydefs: Dict[str, str] = getattr(entities, "entitydefs", {})


def escape(s: str, quote: bool = True) -> str:
    """Escape HTML special characters."""
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")
    if not isinstance(quote, bool):
        raise TypeError(f"quote must be a bool, got {type(quote).__name__}")
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def unescape(s: str) -> str:
    """Unescape HTML entities."""
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")
    import html

    return html.unescape(s)
