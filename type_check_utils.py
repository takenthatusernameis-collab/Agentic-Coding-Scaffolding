"""Utilities for runtime type checking.

Provides lightweight predicates (``is_str``, ``is_int``, ...) and small
coercion helpers (``ensure_type``, ``coerce_to_str``). All functions are
hermetic and side-effect free.
"""

import dataclasses
import inspect
from collections.abc import Iterable, Mapping, Sequence
from typing import List

__all__: List[str] = [
    "is_str",
    "is_int",
    "is_float",
    "is_bool",
    "is_list",
    "is_dict",
    "is_tuple",
    "is_set",
    "is_frozenset",
    "is_none",
    "is_bytes",
    "is_numeric",
    "is_iterable",
    "is_callable",
    "is_protocol",
    "is_mapping",
    "is_sequence",
    "is_collection",
    "is_number",
    "is_object",
    "is_class",
    "is_dataclass",
    "is_instance",
    "is_type",
    "is_generator",
    "is_coroutine",
    "is_async_generator",
    "is_awaitable",
    "is_function",
    "is_method",
    "is_module",
    "is_namedtuple",
    "is_typeddict",
    "is_literal",
    "ensure_type",
    "coerce_to_str",
    "coerce_to_int",
    "coerce_to_float",
    "coerce_to_bool",
    "coerce_to_bytes",
]


def is_str(value: object) -> bool:
    """Return True if value is a string."""
    return isinstance(value, str)


def is_int(value: object) -> bool:
    """Return True if value is an int (excluding bool)."""
    return isinstance(value, int) and not isinstance(value, bool)


def is_float(value: object) -> bool:
    """Return True if value is a float."""
    return isinstance(value, float)


def is_bool(value: object) -> bool:
    """Return True if value is a bool."""
    return isinstance(value, bool)


def is_list(value: object) -> bool:
    """Return True if value is a list."""
    return isinstance(value, list)


def is_dict(value: object) -> bool:
    """Return True if value is a dict."""
    return isinstance(value, dict)


def is_tuple(value: object) -> bool:
    """Return True if value is a tuple."""
    return isinstance(value, tuple)


def is_set(value: object) -> bool:
    """Return True if value is a set."""
    return isinstance(value, set)


def is_frozenset(value: object) -> bool:
    """Return True if *value* is a :class:`frozenset`.

    A frozenset is an immutable hashable collection, distinct from the
    mutable :class:`set`. This helper reports whether *value* is a
    frozenset instance (a mutable set is not a frozenset, and vice versa).

    Args:
        value: The value to check.

    Returns:
        True if *value* is a frozenset, False otherwise.

    Examples:
        >>> is_frozenset(frozenset({1, 2, 3}))
        True
        >>> is_frozenset({1, 2, 3})
        False
        >>> is_frozenset([1, 2, 3])
        False
        >>> is_frozenset(42)
        False
    """
    return isinstance(value, frozenset)


def is_none(value: object) -> bool:
    """Return True if value is None."""
    return value is None


def is_bytes(value: object) -> bool:
    """Return True if value is bytes."""
    return isinstance(value, (bytes, bytearray))


def is_numeric(value: object) -> bool:
    """Return True if value is int or float (excluding bool)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_iterable(value: object) -> bool:
    """Return True if value is iterable but not a string."""
    if isinstance(value, str):
        return False
    return isinstance(value, Iterable)


def is_callable(value: object) -> bool:
    """Return True if value is callable."""
    return callable(value)


def is_protocol(value: object) -> bool:
    """Return True if *value* is a :class:`typing.Protocol` class.

    A Protocol is a class created with :class:`typing.Protocol` (or
    :func:`typing.runtime_checkable`) that defines a structural interface.
    This helper reports whether *value* is such a class, distinguishing it
    from ordinary classes and built-in types.

    Args:
        value: The value to check.

    Returns:
        True if *value* is a Protocol class, False otherwise.

    Raises:
        TypeError: If *value* is not a class.

    Examples:
        >>> from typing import Protocol, runtime_checkable
        >>> class MyProtocol(Protocol):
        ...     def do(self) -> None: ...
        >>> is_protocol(MyProtocol)
        True
        >>> is_protocol(int)
        False
        >>> is_protocol("not a class")
        Traceback (most recent call last):
        ...
        TypeError: value must be a class, got str
    """
    if not isinstance(value, type):
        raise TypeError(f"value must be a class, got {type(value).__name__}")
    return bool(getattr(value, "_is_protocol", False))


def is_mapping(value: object) -> bool:
    """Return True if value is a mapping (dict-like)."""
    if isinstance(value, str):
        return False
    return isinstance(value, Mapping)


def is_sequence(value: object) -> bool:
    """Return True if value is a sequence but not a string."""
    if isinstance(value, str):
        return False
    return isinstance(value, Sequence)


def is_collection(value: object) -> bool:
    """Return True if value is a collection (sized iterable) but not a string."""
    if isinstance(value, str):
        return False
    from collections.abc import Collection

    return isinstance(value, Collection)


def is_number(value: object) -> bool:
    """Return True if value is int or float (excluding bool)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_object(value: object) -> bool:
    """Return True if value is an instance of object (always true in normal cases)."""
    return isinstance(value, object)


def is_class(value: object) -> bool:
    """Return True if value is a class."""
    return isinstance(value, type)


def is_dataclass(value: object) -> bool:
    """Return True if value is a dataclass instance or class."""
    if isinstance(value, type):
        return dataclasses.is_dataclass(value)
    return dataclasses.is_dataclass(value)


def is_instance(value: object, cls: type) -> bool:
    """Return True if value is an instance of cls."""
    return isinstance(value, cls)


def is_type(value: object) -> bool:
    """Return True if value is a type."""
    return isinstance(value, type)


def is_generator(value: object) -> bool:
    """Return True if value is a generator."""
    import types

    return isinstance(value, types.GeneratorType)


def is_coroutine(value: object) -> bool:
    """Return True if value is a coroutine."""
    import types

    return isinstance(value, types.CoroutineType)


def is_async_generator(value: object) -> bool:
    """Return True if value is an async generator."""
    import types

    return isinstance(value, types.AsyncGeneratorType)


def is_awaitable(value: object) -> bool:
    """Return True if *value* is awaitable.

    An awaitable is an object that can be used in an ``await`` expression.
    This includes coroutines, objects with an ``__await__`` method,
    and certain futures in some contexts. The check is consistent with
    :func:`inspect.isawaitable`.

    Args:
        value: The value to check.

    Returns:
        True if *value* is awaitable, False otherwise.

    Examples:
        >>> import asyncio
        >>> async def f():
        ...     return 1
        >>> is_awaitable(f())
        True
        >>> is_awaitable(42)
        False
    """
    return inspect.isawaitable(value)


def is_function(value: object) -> bool:
    """Return True if value is a function (not method)."""
    return inspect.isfunction(value)


def is_method(value: object) -> bool:
    """Return True if value is a method."""
    return inspect.ismethod(value)


def is_module(value: object) -> bool:
    """Return True if *value* is a module.

    A module is any object whose type is :class:`types.ModuleType` (for
    example the :mod:`sys` or :mod:`os` modules). This helper distinguishes
    modules from classes, functions, and ordinary objects.

    Args:
        value: The value to check.

    Returns:
        True if *value* is a module, False otherwise.

    Examples:
        >>> import sys
        >>> is_module(sys)
        True
        >>> is_module(42)
        False
        >>> is_module(len)
        False
    """
    import types

    return isinstance(value, types.ModuleType)


def is_namedtuple(value: object) -> bool:
    """Return True if *value* is a namedtuple class or instance.

    A namedtuple is a subclass of :class:`tuple` produced by
    :func:`collections.namedtuple` that exposes named fields. This helper
    detects both the class itself and instances of such a class by checking
    for the ``_fields`` attribute (a tuple of field names) that
    :func:`collections.namedtuple` attaches.

    Args:
        value: The value to check.

    Returns:
        True if *value* is a namedtuple class or instance, False otherwise.

    Examples:
        >>> from collections import namedtuple
        >>> Point = namedtuple("Point", ["x", "y"])
        >>> is_namedtuple(Point)
        True
        >>> is_namedtuple(Point(1, 2))
        True
        >>> is_namedtuple((1, 2))
        False
    """
    if isinstance(value, type):
        return issubclass(value, tuple) and isinstance(getattr(value, "_fields", None), tuple)
    return isinstance(value, tuple) and isinstance(
        getattr(type(value), "_fields", None), tuple
    )


def is_typeddict(value: object) -> bool:
    """Return True if *value* is a TypedDict class or instance.

    TypedDict classes are created via :class:`typing.TypedDict` and are
    dict subclasses with type annotations describing their keys. This
    helper detects TypedDict classes (by checking for the
    ``__annotations__`` attribute and that the class is a dict subclass)
    and instances of TypedDict classes.

    Args:
        value: The value to check.

    Returns:
        True if *value* is a TypedDict class or instance, False otherwise.

    Examples:
        >>> from typing import TypedDict
        >>> class Point(TypedDict):
        ...     x: int
        ...     y: int
        >>> is_typeddict(Point)
        True
        >>> is_typeddict({"x": 1, "y": 2})
        False
    """
    if isinstance(value, type):
        if not issubclass(value, dict):
            return False
        # TypedDict classes have __annotations__ and are typically
        # created by typing.TypedDict (metaclass _TypedDictMeta)
        if not hasattr(value, "__annotations__"):
            return False
        # Exclude regular dict subclasses that just happen to have annotations
        # TypedDict from typing has specific characteristics
        try:
            # Check if it's from typing.TypedDict
            module = getattr(value, "__module__", "")
            if module == "typing" and value.__name__ == "TypedDict":
                pass  # This shouldn't happen as TypedDict is a function/class in typing
        except Exception:
            pass
        # Check for TypedDict markers
        # or we can check the metaclass
        if hasattr(value, "__required_keys__") or hasattr(value, "__optional_keys__"):
            return True
        # Fallback: if it's a dict subclass with annotations and not a regular class
        # that just happens to inherit from dict, it's likely a TypedDict
        # But be more specific - check if it's created by TypedDict mechanism
        mro = getattr(value, "__mro__", [])
        for cls in mro:
            if cls.__name__ == "TypedDict" and getattr(cls, "__module__", "") == "typing":
                return True
        # Also check using typing.is_typeddict if available
        try:
            import typing

            if hasattr(typing, "is_typeddict"):
                return typing.is_typeddict(value)
        except Exception:
            pass
        return False
    # For instances, check if the instance's type is a TypedDict
    return is_typeddict(type(value))


def is_literal(value: object) -> bool:
    """Return True if *value* is a Literal type."""
    try:
        import typing
        from typing import get_origin

        origin = get_origin(value)
        if origin is getattr(typing, "Literal", None):
            return True
    except Exception:
        pass
    try:
        import typing as _typing

        _lit_alias = getattr(_typing, "_LiteralGenericAlias", None)
        if _lit_alias is not None and isinstance(value, _lit_alias):
            return True
    except Exception:
        pass
    # In some Python versions
    try:
        from typing import get_origin

        import typing_extensions

        origin = get_origin(value)
        if origin is getattr(typing_extensions, "Literal", None):
            return True
    except Exception:
        pass
    return False


def ensure_type(value: object, expected_type: object, name: str = "value") -> object:
    """Ensure value is of expected_type, raising TypeError otherwise.

    *expected_type* may be a single type or a tuple of types, mirroring
    :func:`isinstance`.

    Args:
        value: The value to check.
        expected_type: The expected type (or tuple of types).
        name: Name used in the error message.

    Returns:
        The value unchanged if type matches.

    Raises:
        TypeError: If value is not an instance of expected_type.
    """
    if not isinstance(expected_type, (type, tuple)):
        raise TypeError(
            f"expected_type must be a type or tuple of types, "
            f"got {type(expected_type).__name__}"
        )
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            expected_name = " or ".join(t.__name__ for t in expected_type)
        else:
            expected_name = expected_type.__name__
        raise TypeError(
            f"{name} must be of type {expected_name}, "
            f"got {type(value).__name__}"
        )
    return value


def coerce_to_str(value: object) -> str:
    """Convert value to string.

    Args:
        value: The value to convert.

    Returns:
        The string representation of *value*.

    Examples:
        >>> coerce_to_str(123)
        '123'
        >>> coerce_to_str([1, 2])
        '[1, 2]'
    """
    return str(value)


def coerce_to_int(value: object) -> int:
    """Convert *value* to an int.

    Accepts ints (including bools, which are converted to ``0``/``1``),
    floats, and numeric strings; raises ``TypeError`` for unsupported
    types and ``ValueError`` for strings that do not parse as an integer.

    Args:
        value: The value to convert.

    Returns:
        The integer representation of *value*.

    Raises:
        TypeError: If *value* cannot be converted to an int.
        ValueError: If *value* is a string that is not a valid integer.

    Examples:
        >>> coerce_to_int(123)
        123
        >>> coerce_to_int("456")
        456
        >>> coerce_to_int(True)
        1
    """
    if isinstance(value, bool) or isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        return int(value)
    raise TypeError(
        f"cannot coerce {type(value).__name__} to int"
    )


def coerce_to_float(value: object) -> float:
    """Convert *value* to a float.

    Accepts ints (including bools, which are converted to ``0.0``/``1.0``),
    floats, and numeric strings; raises ``TypeError`` for unsupported
    types and ``ValueError`` for strings that do not parse as a float.

    Args:
        value: The value to convert.

    Returns:
        The float representation of *value*.

    Raises:
        TypeError: If *value* cannot be converted to a float.
        ValueError: If *value* is a string that is not a valid float.

    Examples:
        >>> coerce_to_float(123)
        123.0
        >>> coerce_to_float("4.56")
        4.56
        >>> coerce_to_float(True)
        1.0
    """
    if isinstance(value, bool) or isinstance(value, int):
        return float(value)
    if isinstance(value, float):
        return value
    if isinstance(value, str):
        return float(value)
    raise TypeError(
        f"cannot coerce {type(value).__name__} to float"
    )


def coerce_to_bool(value: object) -> bool:
    """Convert *value* to a bool.

    Accepts bools, ints, floats, and common truthy/falsy strings
    (``"true"``, ``"false"``, ``"1"``, ``"0"``, ``"yes"``, ``"no"``);
    raises ``TypeError`` for unsupported types and ``ValueError`` for
    strings that do not parse as a bool.

    Args:
        value: The value to convert.

    Returns:
        The bool representation of *value*.

    Raises:
        TypeError: If *value* cannot be converted to a bool.
        ValueError: If *value* is a string that is not a valid bool.

    Examples:
        >>> coerce_to_bool(True)
        True
        >>> coerce_to_bool("false")
        False
        >>> coerce_to_bool(1)
        True
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, float):
        return value != 0.0
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "1", "yes", "y", "on"):
            return True
        if lowered in ("false", "0", "no", "n", "off"):
            return False
        raise ValueError(f"cannot coerce {value!r} to bool")
    raise TypeError(
        f"cannot coerce {type(value).__name__} to bool"
    )


def coerce_to_bytes(value: object) -> bytes:
    """Convert *value* to bytes.

    Accepts :class:`str` (encoded as UTF-8), :class:`bytes`, and
    :class:`bytearray`; raises :exc:`TypeError` for unsupported types.

    Args:
        value: The value to convert.

    Returns:
        The bytes representation of *value*.

    Raises:
        TypeError: If *value* cannot be converted to bytes.

    Examples:
        >>> coerce_to_bytes("hello")
        b'hello'
        >>> coerce_to_bytes(b"world")
        b'world'
        >>> coerce_to_bytes(bytearray(b"!"))
        b'!'
    """
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, (bytes, bytearray)):
        return bytes(value)
    raise TypeError(
        f"cannot coerce {type(value).__name__} to bytes"
    )
