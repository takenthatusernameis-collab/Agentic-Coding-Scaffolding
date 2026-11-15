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
    """Escape HTML special characters.

    Args:
        s: The string to escape.
        quote: When ``True`` (the default) the quote characters are escaped as
            well, so the result can be used inside an HTML attribute
            delimiter. When ``False`` only ``&``, ``<``, and ``>`` are
            replaced, matching :func:`html.escape` with ``quote=False``.

    Raises:
        TypeError: If ``s`` is not a string or ``quote`` is not a bool.

    Examples:
        >>> escape("<div>")
        '&lt;div&gt;'
        >>> escape('a "quoted" value', quote=False)
        'a "quoted" value'
    """
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")
    if not isinstance(quote, bool):
        raise TypeError(f"quote must be a bool, got {type(quote).__name__}")
    escaped = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if quote:
        escaped = escaped.replace('"', "&quot;").replace("'", "&#x27;")
    return escaped


def unescape(s: str) -> str:
    """Unescape HTML entities."""
    if not isinstance(s, str):
        raise TypeError(f"s must be a string, got {type(s).__name__}")
    import html

    return html.unescape(s)
