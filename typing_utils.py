"""Utilities for working with type hints (wrapping :mod:`typing`)."""

import typing as _typing


def get_type_hints(obj, globalns=None, localns=None, include_extras=False):
    """Return a dictionary containing type hints for a function, method, or module.

    See :func:`typing.get_type_hints`.
    """
    return _typing.get_type_hints(
        obj, globalns=globalns, localns=localns, include_extras=include_extras
    )


def get_origin(tp):
    """Return the unsubscripted generic type of ``tp``, or ``None`` if unsupported.

    See :func:`typing.get_origin`.
    """
    return _typing.get_origin(tp)


def get_args(tp):
    """Return the type arguments of ``tp`` as a tuple, or an empty tuple if unsupported.

    See :func:`typing.get_args`.
    """
    return _typing.get_args(tp)


def is_typeddict(tp):
    """Return ``True`` if ``tp`` is a :class:`typing.TypedDict` meta-class or instance.

    See :func:`typing.is_typeddict`.
    """
    return _typing.is_typeddict(tp)


overload = _typing.overload
Final = _typing.Final
Literal = _typing.Literal
ClassVar = _typing.ClassVar
