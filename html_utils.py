"""HTML utility functions for escaping, unescaping, and sanitizing HTML.

This module provides utilities for working with HTML content using the
standard library :mod:`html` module: escaping special characters for safe
insertion into HTML, unescaping HTML entities back to their original
characters, and stripping HTML tags from markup.
"""

from __future__ import annotations

import html
import re
from typing import Union

__all__: list[str] = [
    "escape_html",
    "unescape_html",
    "strip_tags",
    "escape_attribute",
]

_TAG_RE = re.compile(r"<[^>]*>")


def escape_html(text: Union[str, None]) -> str:
    """Escape HTML special characters in ``text``.

    Converts ``&``, ``<``, ``>``, ``"``, and ``'`` to their corresponding
    HTML entities so the text can be safely inserted into an HTML document.

    Args:
        text: The text to escape. ``None`` is treated as an empty string.

    Returns:
        The escaped HTML-safe string.

    Raises:
        TypeError: If ``text`` is not a string or ``None``.

    Examples:
        >>> escape_html("<script>alert('xss')</script>")
        '&lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;'
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        raise TypeError("text must be a string or None")
    return html.escape(text, quote=True)


def unescape_html(text: str) -> str:
    """Unescape HTML entities in ``text`` back to their original characters.

    Converts named and numeric character references (e.g. ``&amp;``,
    ``&#60;``, ``&#x3c;``) back to ``&``, ``<``, etc.

    Args:
        text: The HTML-escaped text to unescape.

    Returns:
        The unescaped string.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> unescape_html("&lt;div&gt;")
        '<div>'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return html.unescape(text)


def strip_tags(html_content: str) -> str:
    """Remove all HTML tags from ``html_content``.

    Strips anything matching ``<...>`` from the input, leaving only the
    text content. HTML entities are not decoded; use :func:`unescape_html`
    on the result if entity decoding is desired.

    Args:
        html_content: The HTML string to strip tags from.

    Returns:
        The text content with all tags removed.

    Raises:
        TypeError: If ``html_content`` is not a string.

    Examples:
        >>> strip_tags("<p>Hello <b>world</b>!</p>")
        'Hello world!'
    """
    if not isinstance(html_content, str):
        raise TypeError("html_content must be a string")
    return _TAG_RE.sub("", html_content)


def escape_attribute(value: Union[str, None]) -> str:
    """Escape ``value`` for safe use inside an HTML attribute.

    Like :func:`escape_html`, but intended for attribute values where both
    double and single quotes must be escaped to prevent breaking out of the
    attribute delimiter.

    Args:
        value: The attribute value to escape. ``None`` is treated as an
            empty string.

    Returns:
        The attribute-value-escaped string.

    Raises:
        TypeError: If ``value`` is not a string or ``None``.

    Examples:
        >>> escape_attribute('onload="alert(1)"')
        'onload=&quot;alert(1)&quot;'
    """
    if value is None:
        return ""
    if not isinstance(value, str):
        raise TypeError("value must be a string or None")
    return html.escape(value, quote=True)
