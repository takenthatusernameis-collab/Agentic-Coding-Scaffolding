"""Utilities for simple lexical analysis (wrapping :mod:`shlex`)."""

import shlex as _shlex

__all__ = [
    "join",
    "quote",
    "split",
]


def split(s, comments=False, posix=True):
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    return _shlex.split(s, comments=comments, posix=posix)


def quote(s):
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    return _shlex.quote(s)


def join(split_command):
    if not isinstance(split_command, (list, tuple)):
        raise TypeError("split_command must be a list or tuple")
    if not all(isinstance(item, str) for item in split_command):
        raise TypeError("split_command items must be str")
    return _shlex.join(split_command)
