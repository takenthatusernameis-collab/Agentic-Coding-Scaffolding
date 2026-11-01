"""Utilities wrapping :mod:`abc` for abstract base classes."""

import abc as _abc

__all__ = [
    "ABC",
    "ABCMeta",
    "abstractmethod",
    "abstractclassmethod",
    "abstractstaticmethod",
    "abstractproperty",
    "get_cache_token",
    "update_abstractmethods",
    "is_abstract",
]


def ABC():
    return _abc.ABC

def ABCMeta():
    return _abc.ABCMeta


def abstractmethod(func):
    return _abc.abstractmethod(func)


def abstractclassmethod(func):
    return _abc.abstractclassmethod(func)


def abstractstaticmethod(func):
    return _abc.abstractstaticmethod(func)


def abstractproperty(func):
    return _abc.abstractproperty(func)


def get_cache_token():
    return _abc.get_cache_token()


def update_abstractmethods(cls):
    return _abc.update_abstractmethods(cls)


def is_abstract(obj):
    """Return True if *obj* is an abstract class with unimplemented methods.

    Args:
        obj: Any object, typically a class.

    Returns:
        bool: True when ``obj`` exposes a non-empty ``__abstractmethods__``
        attribute, False otherwise.
    """
    abstractmethods = getattr(obj, "__abstractmethods__", None)
    return bool(abstractmethods)
