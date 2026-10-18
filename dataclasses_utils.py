"""Dataclass utilities.

This module provides utilities for working with Python :mod:`dataclasses`,
including helpers to check for dataclasses, convert dataclasses to
dictionaries/tuples with validation, inspect fields, and access field
metadata. All functions wrap the standard library :mod:`dataclasses`
module and raise :class:`TypeError` or :class:`ValueError` on invalid
input.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Callable, Dict, Iterable, List, Tuple, TypeVar, Union

__all__: list[str] = [
    "is_dataclass",
    "fields",
    "asdict",
    "astuple",
    "replace",
    "make_dataclass",
    "field",
    "MISSING",
    "dataclass_fields",
    "is_dataclass_instance",
    "to_dict",
    "to_tuple",
    "get_field_names",
    "get_field_default",
    "has_field",
]

T = TypeVar("T")
KT = TypeVar("KT")
VT = TypeVar("VT")


def _require_type(obj: Any, name: str, cls: Union[type, Tuple[type, ...]]) -> Any:
    if not isinstance(obj, cls):
        type_names = (
            cls.__name__
            if isinstance(cls, type)
            else " or ".join(c.__name__ for c in cls)
        )
        raise TypeError(f"{name} must be of type {type_names}")
    return obj


def is_dataclass(obj: Any) -> bool:
    """Return ``True`` if ``obj`` is a dataclass class or dataclass instance.

    This is a thin wrapper around :func:`dataclasses.is_dataclass` with
    additional input validation not strictly required, but consistent with
    the project's style.

    Args:
        obj: The object to test.

    Returns:
        ``True`` if the object is a dataclass, ``False`` otherwise.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> is_dataclass(Point)
        True
        >>> is_dataclass(Point(1, 2))
        True
        >>> is_dataclass("not a dataclass")
        False
    """
    # No type restriction needed; is_dataclass accepts any object.
    return dataclasses.is_dataclass(obj)


def is_dataclass_instance(obj: Any) -> bool:
    """Return ``True`` if ``obj`` is a dataclass instance.

    Args:
        obj: The object to test.

    Returns:
        ``True`` if ``obj`` is an instance of a dataclass, ``False`` otherwise.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> is_dataclass_instance(Point(1, 2))
        True
        >>> is_dataclass_instance(Point)
        False
    """
    return dataclasses.is_dataclass(obj) and not isinstance(obj, type)


def fields(class_or_instance: Any) -> Tuple[dataclasses.Field[Any], ...]:
    """Return a tuple of ``Field`` objects for a dataclass.

    Args:
        class_or_instance: A dataclass class or dataclass instance.

    Returns:
        A tuple of :class:`dataclasses.Field` objects.

    Raises:
        TypeError: If ``class_or_instance`` is not a dataclass or a
            dataclass instance.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> len(fields(Point))
        2
    """
    if not dataclasses.is_dataclass(class_or_instance):
        raise TypeError("class_or_instance must be a dataclass or dataclass instance")
    return dataclasses.fields(class_or_instance)


def dataclass_fields(class_or_instance: Any) -> Tuple[dataclasses.Field[Any], ...]:
    """Return fields for a dataclass (alias for :func:`fields`)."""
    return fields(class_or_instance)


_DictFactory = Callable[[Iterable[Tuple[Any, Any]]], Dict[Any, Any]]


def asdict(obj: Any, *, dict_factory: _DictFactory = dict) -> Dict[Any, Any]:
    """Convert a dataclass instance to a dictionary.

    Args:
        obj: A dataclass instance to convert.
        dict_factory: A factory function to create the result dictionary
            (defaults to :class:`dict`).

    Returns:
        A dictionary representation of the dataclass instance.

    Raises:
        TypeError: If ``obj`` is not a dataclass instance.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> asdict(Point(1, 2))
        {'x': 1, 'y': 2}
    """
    if not dataclasses.is_dataclass(obj) or isinstance(obj, type):
        raise TypeError("obj must be a dataclass instance")
    return dataclasses.asdict(obj, dict_factory=dict_factory)


def to_dict(obj: Any, *, dict_factory: _DictFactory = dict) -> Dict[Any, Any]:
    """Convert a dataclass instance to a dictionary (alias for :func:`asdict`)."""
    return asdict(obj, dict_factory=dict_factory)


_TupleFactory = Callable[[Iterable[Any]], Tuple[Any, ...]]


def astuple(obj: Any, *, tuple_factory: _TupleFactory = tuple) -> Tuple[Any, ...]:
    """Convert a dataclass instance to a tuple.

    Args:
        obj: A dataclass instance to convert.
        tuple_factory: A factory function to create the result tuple
            (defaults to :class:`tuple`).

    Returns:
        A tuple representation of the dataclass instance.

    Raises:
        TypeError: If ``obj`` is not a dataclass instance.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> astuple(Point(1, 2))
        (1, 2)
    """
    if not dataclasses.is_dataclass(obj) or isinstance(obj, type):
        raise TypeError("obj must be a dataclass instance")
    return dataclasses.astuple(obj, tuple_factory=tuple_factory)


def to_tuple(obj: Any, *, tuple_factory: _TupleFactory = tuple) -> Tuple[Any, ...]:
    """Convert a dataclass instance to a tuple (alias for :func:`astuple`)."""
    return astuple(obj, tuple_factory=tuple_factory)


def replace(obj: Any, **changes: Any) -> Any:
    """Return a new object replacing specified fields with new values.

    Args:
        obj: A dataclass instance.
        **changes: Field names and their new values.

    Returns:
        A new instance with the specified fields replaced.

    Raises:
        TypeError: If ``obj`` is not a dataclass instance.
        ValueError: If any field in ``changes`` is not a valid field name.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> replace(Point(1, 2), x=3)
        Point(x=3, y=2)
    """
    if not dataclasses.is_dataclass(obj) or isinstance(obj, type):
        raise TypeError("obj must be a dataclass instance")
    return dataclasses.replace(obj, **changes)


def make_dataclass(
    cls_name: str,
    fields: Iterable[Union[str, Tuple[str, type], Tuple[str, type, Any]]],
    *,
    bases: Tuple[type, ...] = (),
    namespace: Dict[str, Any] | None = None,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    match_args: bool = True,
    kw_only: bool = False,
    slots: bool = False,
) -> type:
    """Create a new dataclass dynamically.

    This is a wrapper around :func:`dataclasses.make_dataclass` with input
    validation.

    Args:
        cls_name: Name of the new dataclass.
        fields: Field specifications.
        bases: Base classes for the new dataclass.
        namespace: Namespace dictionary for the class body.
        init: Whether to generate ``__init__``.
        repr: Whether to generate ``__repr__``.
        eq: Whether to generate ``__eq__``.
        order: Whether to generate ordering methods.
        unsafe_hash: Whether to force ``__hash__`` generation.
        frozen: Whether the dataclass is immutable.
        match_args: Whether to generate ``__match_args__``.
        kw_only: Whether fields are keyword-only.
        slots: Whether to generate ``__slots__``.

    Returns:
        The newly created dataclass type.

    Raises:
        TypeError: If arguments have incorrect types.
        ValueError: If field specifications are invalid.

    Examples:
        >>> Point = make_dataclass('Point', [('x', int), ('y', int)])
        >>> Point(x=1, y=2)
        Point(x=1, y=2)
    """
    _require_type(cls_name, "cls_name", str)
    if not isinstance(fields, Iterable):
        raise TypeError("fields must be iterable")
    if not isinstance(bases, tuple):
        raise TypeError("bases must be a tuple")
    if namespace is not None and not isinstance(namespace, dict):
        raise TypeError("namespace must be a dict or None")
    try:
        return dataclasses.make_dataclass(
            cls_name,
            list(fields),
            bases=bases,
            namespace=namespace,
            init=init,
            repr=repr,
            eq=eq,
            order=order,
            unsafe_hash=unsafe_hash,
            frozen=frozen,
            match_args=match_args,
            kw_only=kw_only,
            slots=slots,
        )
    except (TypeError, ValueError):
        raise


# Re-export field and MISSING for convenience
field = dataclasses.field
MISSING = dataclasses.MISSING


def get_field_names(class_or_instance: Any) -> List[str]:
    """Return a list of field names for a dataclass.

    Args:
        class_or_instance: A dataclass class or dataclass instance.

    Returns:
        A list of field names as strings.

    Raises:
        TypeError: If ``class_or_instance`` is not a dataclass.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> get_field_names(Point)
        ['x', 'y']
    """
    if not dataclasses.is_dataclass(class_or_instance):
        raise TypeError("class_or_instance must be a dataclass or dataclass instance")
    return [f.name for f in dataclasses.fields(class_or_instance)]


def get_field_default(class_or_instance: Any, field_name: str) -> Any:
    """Return the default value for a field.

    Args:
        class_or_instance: A dataclass class or dataclass instance.
        field_name: Name of the field.

    Returns:
        The default value of the field, or ``dataclasses.MISSING`` if no
        default is provided.

    Raises:
        TypeError: If ``class_or_instance`` is not a dataclass.
        KeyError: If the field does not exist.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int = 0
        >>> get_field_default(Point, 'y')
        0
        >>> get_field_default(Point, 'x') is MISSING
        True
    """
    _require_type(field_name, "field_name", str)
    if not dataclasses.is_dataclass(class_or_instance):
        raise TypeError("class_or_instance must be a dataclass or dataclass instance")
    for f in dataclasses.fields(class_or_instance):
        if f.name == field_name:
            return f.default if f.default is not dataclasses.MISSING else dataclasses.MISSING
    raise KeyError(f"field '{field_name}' not found")


def has_field(class_or_instance: Any, field_name: str) -> bool:
    """Return ``True`` if the dataclass has the specified field.

    Args:
        class_or_instance: A dataclass class or dataclass instance.
        field_name: Name of the field to check for.

    Returns:
        ``True`` if the field exists, ``False`` otherwise.

    Raises:
        TypeError: If ``class_or_instance`` is not a dataclass or if
            ``field_name`` is not a string.

    Examples:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        >>> has_field(Point, 'x')
        True
        >>> has_field(Point, 'z')
        False
    """
    _require_type(field_name, "field_name", str)
    if not dataclasses.is_dataclass(class_or_instance):
        raise TypeError("class_or_instance must be a dataclass or dataclass instance")
    return any(f.name == field_name for f in dataclasses.fields(class_or_instance))
