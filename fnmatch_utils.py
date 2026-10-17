"""Utilities for filename pattern matching (wrapping :mod:`fnmatch`)."""

import fnmatch as _fnmatch


def match(name: str, pattern: str) -> bool:
    """Return True if *name* matches *pattern* (case-normalized on OS)."""
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    return _fnmatch.fnmatch(name, pattern)


def match_case(name: str, pattern: str) -> bool:
    """Case-sensitive version of :func:`match`."""
    if not isinstance(name, str):
        raise TypeError("name must be a str")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    return _fnmatch.fnmatchcase(name, pattern)


def filter_names(names: list[str], pattern: str) -> list[str]:
    """Return the subset of *names* matching *pattern*."""
    if not isinstance(names, (list, tuple)):
        raise TypeError("names must be a list or tuple")
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    return _fnmatch.filter(list(names), pattern)


def translate(pattern: str) -> str:
    """Translate a shell-style *pattern* to a regular expression."""
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a str")
    return _fnmatch.translate(pattern)
