"""Utilities for pickle support registration (wrapping :mod:`copyreg`)."""

import copyreg as _copyreg


def add_extension(module, name, code):
    return _copyreg.add_extension(module, name, code)


def remove_extension(module, name, code):
    return _copyreg.remove_extension(module, name, code)


def clear_extension_cache():
    return _copyreg.clear_extension_cache()


def constructor(func):
    return _copyreg.constructor(func)


def dispatch_table():
    return _copyreg.dispatch_table


def pickle(type_, func, constructor=None):
    if constructor is None:
        return _copyreg.pickle(type_, func)
    return _copyreg.pickle(type_, func, constructor)
