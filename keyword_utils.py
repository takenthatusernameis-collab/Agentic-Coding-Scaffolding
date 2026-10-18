"""Utilities for Python keyword classification (wrapping :mod:`keyword`)."""

import keyword as _keyword


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
    """Run the keyword module's interactive ``main`` entry point."""
    return _keyword.main
