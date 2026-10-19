"""Utilities for command line option parsing (wrapping :mod:`getopt`)."""

import getopt as _getopt


def getopt(args, shortopts, longopts=()):
    if not isinstance(args, (list, tuple)):
        raise TypeError("args must be a list or tuple")
    if not isinstance(shortopts, str):
        raise TypeError("shortopts must be a str")
    return _getopt.getopt(args, shortopts, longopts)


def gnu_getopt(args, shortopts, longopts=()):
    if not isinstance(args, (list, tuple)):
        raise TypeError("args must be a list or tuple")
    if not isinstance(shortopts, str):
        raise TypeError("shortopts must be a str")
    return _getopt.gnu_getopt(args, shortopts, longopts)


GetoptError = _getopt.GetoptError
