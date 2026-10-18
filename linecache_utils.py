"""Utilities for reading source lines (wrapping :mod:`linecache`)."""

import linecache as _linecache


def getline(filename, lineno, module_globals=None):
    if not isinstance(filename, str):
        raise TypeError("filename must be a str")
    if not isinstance(lineno, int):
        raise TypeError("lineno must be an int")
    return _linecache.getline(filename, lineno, module_globals)


def getlines(filename, module_globals=None):
    if not isinstance(filename, str):
        raise TypeError("filename must be a str")
    return _linecache.getlines(filename, module_globals)


def checkcache(filename=None):
    return _linecache.checkcache(filename)


def updatecache(filename, module_globals=None):
    if not isinstance(filename, str):
        raise TypeError("filename must be a str")
    return _linecache.updatecache(filename, module_globals)


def lazycache(filename, module_globals):
    if not isinstance(filename, str):
        raise TypeError("filename must be a str")
    return _linecache.lazycache(filename, module_globals)


def clearcache():
    return _linecache.clearcache()
