"""Utilities for Python keyword classification (wrapping :mod:`keyword`)."""

import keyword as _keyword

__all__ = [
    "is_keyword",
    "is_soft_keyword",
    "kwlist",
    "main",
    "softkwlist",
]


def is_keyword(word):
    """Return ``True`` if ``word`` is a Python keyword."""
    if not isinstance(word, str):
        raise TypeError("word must be a str")
    return _keyword.iskeyword(word)


def is_soft_keyword(word):
    """Return ``True`` if ``word`` is a Python soft keyword."""
    if not isinstance(word, str):
        raise TypeError("word must be a str")
    return _keyword.issoftkeyword(word)


def kwlist():
    """Return a copy of the list of Python keywords."""
    return list(_keyword.kwlist)


def softkwlist():
    """Return a copy of the list of Python soft keywords."""
    return list(_keyword.softkwlist)


def main():
    """Return the ``keyword`` module's ``main`` entry point if available.

    The standard library removed ``keyword.main`` in Python 3.12, so this
    returns ``None`` on current interpreters instead of raising.
    """
    return getattr(_keyword, "main", None)
