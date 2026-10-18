"""Utilities for simple lexical analysis (wrapping :mod:`shlex`)."""

import shlex as _shlex


def split(s, comments=False, posix=True):
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    return _shlex.split(s, comments=comments, posix=posix)


def quote(s):
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    return _shlex.quote(s)


def join(split_command):
    return _shlex.join(split_command)
