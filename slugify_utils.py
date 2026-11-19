"""Utilities for converting strings into URL-friendly slugs."""

import re
import unicodedata
from typing import Iterable

__all__ = ["slugify", "is_slug", "deslugify", "truncate_slug", "slugify_many"]


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
    words = re.findall(r"[a-z0-9]+", lowered)
    return separator.join(words)


def is_slug(text: str, separator: str = "-") -> bool:
    """Return True if *text* is already a valid slug."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    if not text:
        return False
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty str")
    parts = text.split(separator)
    # No empty parts (no leading, trailing, or consecutive separators)
    if any(not part for part in parts):
        return False
    # All parts must be lowercase alphanumeric
    return all(part.isalnum() and part.lower() == part for part in parts)


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

    # Find the last separator position where prefix + ellipsis <= max_length
    # Search in the full text up to max_length - len(ellipsis) + len(separator)
    # to catch separators that start within the limit but end at or past it.
    search_limit = max_length - len(ellipsis) + len(separator)
    if search_limit > len(text):
        search_limit = len(text)

    idx = text.rfind(separator, 0, search_limit)
    while idx > 0:
        candidate = text[:idx] + ellipsis
        if len(candidate) <= max_length:
            # Strip any trailing separator substring from the prefix
            prefix = text[:idx]
            while prefix.endswith(separator):
                prefix = prefix[:-len(separator)]
            return prefix + ellipsis
        # Try earlier separator
        idx = text.rfind(separator, 0, idx)

    # No suitable separator found; hard cut
    hard_cut = text[:max_length - len(ellipsis)]
    while hard_cut.endswith(separator):
        hard_cut = hard_cut[:-len(separator)]
    return hard_cut + ellipsis


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


def slugify_many(texts: Iterable[str], separator: str = "-") -> list[str]:
    """Slugify each string in *texts*, returning a list of slugs.

    Args:
        texts: Iterable of strings to slugify.
        separator: Separator between words.

    Returns:
        List of slugified strings.

    Raises:
        TypeError: If *texts* is not iterable of str or *separator* is invalid.
    """
    if not isinstance(separator, str) or not separator:
        raise ValueError("separator must be a non-empty str")
    if not hasattr(texts, "__iter__") or isinstance(texts, (str, bytes)):
        raise TypeError("texts must be an iterable of str")
    result: list[str] = []
    for item in texts:
        if not isinstance(item, str):
            raise TypeError("texts must contain str values")
        result.append(slugify(item, separator))
    return result
