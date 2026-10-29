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


def is_literal(tp):
    """Return ``True`` if ``tp`` is a :class:`typing.Literal` type."""
    try:
        from typing import Literal, get_origin

        origin = get_origin(tp)
        if origin is Literal:
            return True
    except Exception:
        pass
    # Python 3.8+
    try:
        import typing

        origin = getattr(tp, "__origin__", None)
        if origin is getattr(typing, "Literal", None):
            return True
    except Exception:
        pass
    # Python 3.9+ uses typing._LiteralGenericAlias
    try:
        from typing import _LiteralGenericAlias

        if isinstance(tp, _LiteralGenericAlias):
            return True
    except Exception:
        pass
    # Python 3.8 uses typing.LiteralMeta
    try:
        if isinstance(tp, type) and tp.__name__ == "Literal" and tp.__module__ == "typing":
            # This is the Literal class itself in some forms
            pass
    except Exception:
        pass
    return False


overload = _typing.overload
Final = _typing.Final
Literal = _typing.Literal
ClassVar = _typing.ClassVar
