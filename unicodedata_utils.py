"""Unicodedata utility functions wrapping the standard library 'unicodedata' module."""

from __future__ import annotations

import unicodedata
from typing import Literal

__all__: list[str] = [
    "unicodedata_lookup",
    "unicodedata_name",
    "unicodedata_normalize",
    "unicodedata_category",
    "unicodedata_bidirectional",
    "unicodedata_combining",
    "unicodedata_east_asian_width",
    "unicodedata_mirrored",
    "unicodedata_decimal",
    "unicodedata_digit",
    "unicodedata_numeric",
]


def unicodedata_lookup(name: str) -> str:
    """Look up a character by its name."""
    return unicodedata.lookup(name)


def unicodedata_name(char: str, default: str | None = None) -> str:
    """Return the name of a character."""
    if default is None:
        return unicodedata.name(char)
    return unicodedata.name(char, default)


def unicodedata_normalize(form: Literal["NFC","NFD","NFKC","NFKD"], unistr: str) -> str:
    """Return the normal form of a Unicode string."""
    return unicodedata.normalize(form, unistr)


def unicodedata_category(char: str) -> str:
    """Return the general category of a character."""
    return unicodedata.category(char)


def unicodedata_bidirectional(char: str) -> str:
    """Return the bidirectional class of a character."""
    return unicodedata.bidirectional(char)


def unicodedata_combining(char: str) -> int:
    """Return the combining class of a character."""
    return unicodedata.combining(char)


def unicodedata_east_asian_width(char: str) -> str:
    """Return the east asian width of a character."""
    return unicodedata.east_asian_width(char)


def unicodedata_mirrored(char: str) -> int:
    """Return whether a character is mirrored."""
    return unicodedata.mirrored(char)


def unicodedata_decimal(char: str, default: int | None = None) -> int:
    """Return the decimal value of a character."""
    if default is None:
        return unicodedata.decimal(char)
    return unicodedata.decimal(char, default)


def unicodedata_digit(char: str, default: int | None = None) -> int:
    """Return the digit value of a character."""
    if default is None:
        return unicodedata.digit(char)
    return unicodedata.digit(char, default)


def unicodedata_numeric(char: str, default: float | None = None) -> float:
    """Return the numeric value of a character."""
    if default is None:
        return unicodedata.numeric(char)
    return unicodedata.numeric(char, default)
