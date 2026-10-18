"""Utilities wrapping :mod:`abc` for abstract base classes."""

import abc as _abc


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
