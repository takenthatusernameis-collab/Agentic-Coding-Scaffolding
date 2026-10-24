"""Utilities for converting strings into URL-friendly slugs."""

import re
import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """Convert *text* into a lowercase slug using *separator*."""
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
