"""Type introspection utilities."""

from __future__ import annotations

import sys
import typing
from typing import Any, Callable, Dict, List, Literal, Tuple, Union, get_args, get_origin

__all__: List[str] = [
    "is_optional",
    "is_union",
    "is_literal",
    "is_generic",
    "get_type_args",
    "type_name",
    "is_subclass_safe",
    "is_type_var",
    "is_class_var",
    "is_none_type",
    "is_any",
    "unwrap_optional",
    "is_callable",
    "is_tuple",
    "is_list_type",
    "is_dict_type",
    "get_origin_name",
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


def is_type_var(tp: Any) -> bool:
    """Return True if *tp* is a typing.TypeVar."""
    return isinstance(tp, typing.TypeVar)


def is_class_var(tp: Any) -> bool:
    """Return True if *tp* is a typing.ClassVar."""
    origin = get_origin(tp)
    if origin is typing.ClassVar:
        return True
    return tp is typing.ClassVar


def is_none_type(tp: Any) -> bool:
    """Return True if *tp* is NoneType."""
    return tp is type(None) or tp is None


def is_any(tp: Any) -> bool:
    """Return True if *tp* is typing.Any."""
    return tp is Any


def unwrap_optional(tp: Any) -> Any:
    """Return the inner type of Optional[...], else return tp unchanged."""
    if not is_optional(tp):
        return tp
    args = get_args(tp)
    # Filter out None
    non_none = [a for a in args if a is not type(None)]
    if len(non_none) == 1:
        return non_none[0]
    # If multiple non-None (shouldn't happen for Optional), return Union of them
    if len(non_none) > 1:
        return Union[tuple(non_none)]  # type: ignore[misc]
    return tp


def is_callable(tp: Any) -> bool:
    """Return True if *tp* is a Callable type."""
    origin = get_origin(tp)
    if origin is Callable:
        return True
    if tp is Callable:
        return True
    return False


def is_tuple(tp: Any) -> bool:
    """Return True if *tp* is a Tuple type."""
    origin = get_origin(tp)
    if origin is tuple or origin is Tuple:
        return True
    if tp is tuple or tp is Tuple:
        return True
    return False


def is_list_type(tp: Any) -> bool:
    """Return True if *tp* is a List type."""
    origin = get_origin(tp)
    if origin is list or origin is List:
        return True
    if tp is list or tp is List:
        return True
    return False


def is_dict_type(tp: Any) -> bool:
    """Return True if *tp* is a Dict type."""
    origin = get_origin(tp)
    if origin is dict or origin is Dict:
        return True
    if tp is dict or tp is Dict:
        return True
    return False


def get_origin_name(tp: Any) -> str:
    """Return the name of the origin of a generic type."""
    origin = get_origin(tp)
    if origin is None:
        if hasattr(tp, "__name__"):
            return str(getattr(tp, "__name__"))
        return str(tp)
    if hasattr(origin, "__name__"):
        return str(getattr(origin, "__name__"))
    return str(origin)
