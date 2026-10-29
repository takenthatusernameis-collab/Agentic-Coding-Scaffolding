"""Type introspection utilities."""

from __future__ import annotations

import sys
import typing
from typing import Any, List, Literal, Union, get_args, get_origin

__all__: List[str] = [
    "is_optional",
    "is_union",
    "is_literal",
    "is_generic",
    "get_type_args",
    "type_name",
    "is_subclass_safe",
]


def _is_optional_type(tp: Any) -> bool:
    origin = get_origin(tp)
    args = get_args(tp)
    if origin is Union:
        return type(None) in args
    if sys.version_info >= (3, 10):
        from types import UnionType

        if isinstance(tp, UnionType):
            return type(None) in args
    return False


def is_optional(tp: Any) -> bool:
    """Return True if the type is Optional[T] (Union[T, None])."""
    if tp is type(None):
        return True
    return _is_optional_type(tp)


def is_union(tp: Any) -> bool:
    """Return True if the type is a Union."""
    origin = get_origin(tp)
    if origin is Union:
        return True
    if sys.version_info >= (3, 10):
        from types import UnionType

        if isinstance(tp, UnionType):
            return True
    return False


def is_literal(tp: Any) -> bool:
    """Return True if the type is a Literal."""
    origin = get_origin(tp)
    if origin is Literal:
        return True
    if sys.version_info >= (3, 8):
        try:
            # In Python 3.8+, Literal is from typing
            if getattr(tp, "__origin__", None) is Literal:
                return True
        except Exception:
            pass
    # Fallback for some Python versions
    try:
        _LiteralGenericAlias = getattr(typing, "_LiteralGenericAlias", None)
        if _LiteralGenericAlias is not None and isinstance(tp, _LiteralGenericAlias):
            return True
    except Exception:
        pass
    return False


def is_generic(tp: Any) -> bool:
    """Return True if the type is a generic alias (e.g., List[int])."""
    origin = get_origin(tp)
    if origin is not None:
        return True
    if hasattr(tp, "__origin__") and getattr(tp, "__origin__") is not None:
        return True
    return False


def get_type_args(tp: Any) -> tuple[Any, ...]:
    """Return the type arguments of a generic type, if any."""
    return get_args(tp)


def type_name(tp: Any) -> str:
    """Return a human-readable name for a type."""
    if tp is None:
        return "None"
    origin = get_origin(tp)
    if origin is not None:
        args_list: List[str] = []
        for a in get_args(tp):
            args_list.append(type_name(a))
        args_str = ", ".join(args_list)
        origin_name = getattr(origin, "__name__", str(origin))
        if args_str:
            return f"{origin_name}[{args_str}]"
        return str(origin_name)
    if hasattr(tp, "__name__"):
        name = getattr(tp, "__name__")
        return str(name)
    return str(tp)


def is_subclass_safe(cls: Any, base: Any) -> bool:
    """Safely check subclass relationship without raising TypeError."""
    try:
        return issubclass(cls, base)
    except Exception:
        return False
