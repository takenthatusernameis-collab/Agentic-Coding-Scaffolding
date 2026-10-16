"""Text wrapping utility functions."""

import textwrap
from typing import List


def wrap_text(text: str, width: int = 70) -> List[str]:
    """Wrap *text* into a list of lines no longer than *width*."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width < 1:
        raise ValueError("width must be at least 1")
    return textwrap.wrap(text, width=width)


def shorten_text(text: str, width: int, placeholder: str = "...") -> str:
    """Shorten *text* to fit within *width*, appending *placeholder* if trimmed."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width < 1:
        raise ValueError("width must be at least 1")
    if not isinstance(placeholder, str):
        raise TypeError("placeholder must be a string")
    return textwrap.shorten(text, width=width, placeholder=placeholder)


def dedent_text(text: str) -> str:
    """Remove common leading whitespace from every line of *text*."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return textwrap.dedent(text)


def indent_text(text: str, prefix: str) -> str:
    """Indent every line of *text* with *prefix*."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    return textwrap.indent(text, prefix)


def fill_text(text: str, width: int = 70) -> str:
    """Fill *text* so each line is no longer than *width*."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be an integer")
    if width < 1:
        raise ValueError("width must be at least 1")
    return textwrap.fill(text, width=width)
