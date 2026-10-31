"""Utilities for converting strings into URL-friendly slugs."""

import re
import unicodedata

__all__ = ["slugify", "is_slug", "deslugify", "truncate_slug"]


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


def truncate_slug(text: str, max_length: int, separator: str = "-", ellipsis: str = "...") -> str:
    """Truncate *text* (a slug) to at most *max_length* characters.

    Truncation happens on separator boundaries when possible; otherwise the slug
    is cut hard. *ellipsis* is appended when truncation occurs.

    Args:
        text: Slug to truncate.
        max_length: Maximum length of the returned string.
        separator: Separator between words.
        ellipsis: Suffix appended when truncated.

    Returns:
        Truncated slug.

    Raises:
        TypeError: If *text* is not a str or *max_length* is not an int.
        ValueError: If *max_length* is negative or *separator* is empty.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if isinstance(max_length, bool) or not isinstance(max_length, int):
        raise TypeError("max_length must be an int")
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty str")
    if len(text) <= max_length:
        return text
    if max_length <= len(ellipsis):
        return ellipsis[:max_length]
    limit = max_length - len(ellipsis)
    cut = text[:limit]
    idx = cut.rfind(separator)
    if idx > 0:
        cut = cut[:idx]
    return cut.rstrip(separator) + ellipsis
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
