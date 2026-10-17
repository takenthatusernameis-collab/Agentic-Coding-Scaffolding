"""Locale utility functions for working with locale identifiers and language tags."""

from __future__ import annotations

__all__ = [
    "normalize_locale",
    "language_code",
    "region_code",
    "is_valid_locale",
]


def normalize_locale(value: str) -> str:
    """Normalize a locale string to ``language_REGION`` form."""
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    parts = value.replace("-", "_").split("_")
    language = parts[0].lower() if parts and parts[0] else ""
    region = parts[1].upper() if len(parts) > 1 and parts[1] else ""
    return f"{language}_{region}" if region else language


def language_code(value: str) -> str:
    """Extract the language code from a locale string."""
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    return value.replace("-", "_").split("_")[0].lower()


def region_code(value: str) -> str:
    """Extract the region code from a locale string."""
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    parts = value.replace("-", "_").split("_")
    return parts[1].upper() if len(parts) > 1 else ""


def is_valid_locale(value: str) -> bool:
    """Return True if value looks like a valid locale identifier."""
    if not isinstance(value, str):
        return False
    parts = value.replace("-", "_").split("_")
    if not parts or not parts[0].isalpha() or len(parts[0]) not in (2, 3):
        return False
    if len(parts) > 1 and (not parts[1].isalpha() or len(parts[1]) not in (2, 3)):
        return False
    return True
