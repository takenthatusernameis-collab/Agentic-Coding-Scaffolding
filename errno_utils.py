"""Utilities for system error numbers (wrapping :mod:`errno`)."""

import errno as _errno
import os as _os


def errorcode(code):
    return _errno.errorcode.get(code)


def strerror(code):
    return _os.strerror(code)


def is_errno(code, name):
    return getattr(_errno, name, None) == code
