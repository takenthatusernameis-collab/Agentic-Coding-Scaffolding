"""Utilities for Python keyword classification (wrapping :mod:`keyword`)."""

import keyword as _keyword


def is_keyword(word):
    if not isinstance(word, str):
        raise TypeError("word must be a str")
    return _keyword.iskeyword(word)


def is_soft_keyword(word):
    if not isinstance(word, str):
        raise TypeError("word must be a str")
    return _keyword.issoftkeyword(word)


def kwlist():
    return list(_keyword.kwlist)


def softkwlist():
    return list(_keyword.softkwlist)


def main():
    return _keyword.main
""" content">
"""Tests for keyword_utils."""

import keyword_utils


def test_is_keyword():
    assert keyword_utils.is_keyword("if") is True
    assert keyword_utils.is_keyword("foo") is False


def test_is_soft_keyword():
    assert keyword_utils.is_soft_keyword("match") is True
    assert keyword_utils.is_soft_keyword("if") is False


def test_kwlist():
    assert "def" in keyword_utils.kwlist()


def test_type_error():
    try:
        keyword_utils.is_keyword(123)
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")
""" filePath="/home/runner/work/Agentic-Coding-Scaffolding/Agentic-Coding-Scaffolding/keyword_utils.py"