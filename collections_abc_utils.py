"""Utilities wrapping :mod:`collections.abc` abstract base classes.

>>> from collections_abc_utils import is_sequence, is_mapping, is_iterable, get_abc
>>> is_sequence([1, 2])
True
>>> is_mapping({"a": 1})
True
>>> is_iterable(42)
False
>>> get_abc("Sequence").__name__
'Sequence'
"""

from __future__ import annotations

import collections.abc as _cabc
from typing import Any

__all__ = [
    "get_abc",
    "is_async_generator",
    "is_async_iterable",
    "is_async_iterator",
    "is_awaitable",
    "is_callable",
    "is_collection",
    "is_container",
    "is_coroutine",
    "is_generator",
    "is_hashable",
    "is_iterable",
    "is_iterator",
    "is_mapping",
    "is_mutable_mapping",
    "is_mutable_sequence",
    "is_mutable_set",
    "is_reversible",
    "is_sequence",
    "is_set",
    "is_sized",
]


def _require_str(name: Any, label: str) -> str:
    if not isinstance(name, str):
        raise TypeError(f"{label} must be a string")
    return name


def get_abc(name: str) -> type:
    """Return the :mod:`collections.abc` ABC class with the given *name*.

    Args:
        name: Public ABC name (e.g. ``"Sequence"``, ``"Mapping"``).

    Returns:
        The ABC class.

    Raises:
        TypeError: If *name* is not a string.
        AttributeError: If *name* is not a public collections.abc attribute.
        ValueError: If *name* starts with ``_``.
    """
    _require_str(name, "name")
    if name.startswith("_"):
        raise ValueError("name must be a public collections.abc attribute")
    value = getattr(_cabc, name)
    if not isinstance(value, type):
        raise TypeError(f"collections.abc.{name} is not a class")
    return value


def is_awaitable(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Awaitable`."""
    return isinstance(obj, _cabc.Awaitable)


def is_coroutine(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Coroutine`."""
    return isinstance(obj, _cabc.Coroutine)


def is_async_iterable(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.AsyncIterable`."""
    return isinstance(obj, _cabc.AsyncIterable)


def is_async_iterator(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.AsyncIterator`."""
    return isinstance(obj, _cabc.AsyncIterator)


def is_async_generator(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.AsyncGenerator`."""
    return isinstance(obj, _cabc.AsyncGenerator)


def is_hashable(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Hashable`."""
    return isinstance(obj, _cabc.Hashable)


def is_iterable(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Iterable`."""
    return isinstance(obj, _cabc.Iterable)


def is_iterator(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Iterator`."""
    return isinstance(obj, _cabc.Iterator)


def is_generator(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Generator`."""
    return isinstance(obj, _cabc.Generator)


def is_reversible(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Reversible`."""
    return isinstance(obj, _cabc.Reversible)


def is_sized(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Sized`."""
    return isinstance(obj, _cabc.Sized)


def is_container(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Container`."""
    return isinstance(obj, _cabc.Container)


def is_collection(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Collection`."""
    return isinstance(obj, _cabc.Collection)


def is_callable(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Callable`."""
    return callable(obj)


def is_set(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Set`."""
    return isinstance(obj, _cabc.Set)


def is_mutable_set(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.MutableSet`."""
    return isinstance(obj, _cabc.MutableSet)


def is_mapping(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Mapping`."""
    return isinstance(obj, _cabc.Mapping)


def is_mutable_mapping(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.MutableMapping`."""
    return isinstance(obj, _cabc.MutableMapping)


def is_sequence(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.Sequence`."""
    return isinstance(obj, _cabc.Sequence)


def is_mutable_sequence(obj: Any) -> bool:
    """Return ``True`` if *obj* is an instance of :class:`collections.abc.MutableSequence`."""
    return isinstance(obj, _cabc.MutableSequence)
