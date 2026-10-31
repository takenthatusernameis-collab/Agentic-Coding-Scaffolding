"""Utilities for converting strings into URL-friendly slugs."""

import re
import unicodedata

__all__ = ["slugify", "is_slug", "deslugify"]


def slugify(text: str, separator: str = "-") -> str:
    """Convert *text* into a lowercase slug using *separator*.

    Args:
        text: Text to slugify.
        separator: Separator between words.

    Returns:
        Slugified string.

    Raises:
        TypeError: If *text* is not a str.
        ValueError: If *separator* is empty.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty str")
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    cleaned = re.sub(r"[^a-z0-9]+", separator, lowered)
    return cleaned.strip(separator)


def is_slug(text: str, separator: str = "-") -> bool:
    """Return True if *text* is already a valid slug."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not text:
        return False
    pattern = rf"^[a-z0-9]+({re.escape(separator)}[a-z0-9]+)*$"
    return bool(re.fullmatch(pattern, text))


def deslugify(text: str, separator: str = "-") -> str:
    """Convert a *slug* back into a title-cased phrase.

    Args:
        text: Slug to convert.
        separator: Separator between words.

    Returns:
        Title-cased phrase.

    Raises:
        TypeError: If *text* is not a str.
        ValueError: If *separator* is empty.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty str")
    return " ".join(part.capitalize() for part in text.split(separator) if part)
