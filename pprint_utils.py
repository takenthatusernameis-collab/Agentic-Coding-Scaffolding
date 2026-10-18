"""Utilities for pretty-printing (wrapping :mod:`pprint`)."""

import pprint as _pprint


def pformat(obj, indent=1, width=80, depth=None, compact=False, sort_dicts=True):
    return _pprint.pformat(
        obj, indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts
    )


def pprint(obj, stream=None, indent=1, width=80, depth=None, compact=False, sort_dicts=True):
    return _pprint.pprint(
        obj, stream=stream, indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts
    )


def isreadable(obj):
    return _pprint.isreadable(obj)


def isrecursive(obj):
    return _pprint.isrecursive(obj)


def saferepr(obj):
    return _pprint.saferepr(obj)
