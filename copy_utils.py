"""Copy utilities for duplicating Python objects and mappings.

This module wraps the standard library :mod:`copy` module with input
validation and convenience helpers for shallow and deep copying of objects
and dictionaries. All functions raise ``TypeError`` or ``ValueError`` on
invalid arguments.
"""

from __future__ import annotations

import copy as _copy
from typing import Any, Dict, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

__all__: list[str] = [
    "shallow_copy",
    "deep_copy",
    "copy_dict",
    "deep_copy_dict",
    "merge_copy",
    "is_same_object",
]


def shallow_copy(obj: T) -> T:
    """Return a shallow copy of *obj*.

    Args:
        obj: The object to copy.

    Returns:
        A new object that is a shallow copy of *obj*.

    Raises:
        TypeError: If *obj* cannot be copied.
    """
    try:
        return _copy.copy(obj)  # type: ignore[return-value]
    except TypeError as exc:
        raise TypeError(f"object of type {type(obj).__name__} cannot be shallow copied") from exc


def deep_copy(obj: T) -> T:
    """Return a deep copy of *obj*.

    Args:
        obj: The object to copy.

    Returns:
        A new object that is a deep copy of *obj*.

    Raises:
        TypeError: If *obj* cannot be deep copied.
    """
    try:
        return _copy.deepcopy(obj)  # type: ignore[return-value]
    except TypeError as exc:
        raise TypeError(f"object of type {type(obj).__name__} cannot be deep copied") from exc


def copy_dict(mapping: Dict[K, V]) -> Dict[K, V]:
    """Return a shallow copy of *mapping*.

    Args:
        mapping: The dictionary to copy.

    Returns:
        A new dictionary with the same keys and values as *mapping*.

    Raises:
        TypeError: If *mapping* is not a dictionary.
    """
    if not isinstance(mapping, dict):
        raise TypeError(f"mapping must be a dict, got {type(mapping).__name__}")
    return dict(mapping)


def deep_copy_dict(mapping: Dict[K, V]) -> Dict[K, V]:
    """Return a deep copy of *mapping*.

    Args:
        mapping: The dictionary to copy.

    Returns:
        A new dictionary with deeply copied keys and values.

    Raises:
        TypeError: If *mapping* is not a dictionary.
    """
    if not isinstance(mapping, dict):
        raise TypeError(f"mapping must be a dict, got {type(mapping).__name__}")
    return _copy.deepcopy(mapping)


def merge_copy(*mappings: Dict[K, V]) -> Dict[K, V]:
    """Return a new dictionary merging *mappings*, later ones taking precedence.

    The input mappings are not mutated.

    Args:
        *mappings: Dictionaries to merge.

    Returns:
        A new merged dictionary.

    Raises:
        TypeError: If any argument is not a dictionary.
    """
    for mapping in mappings:
        if not isinstance(mapping, dict):
            raise TypeError(
                f"all arguments must be dicts, got {type(mapping).__name__}"
            )
    result: Dict[K, V] = {}
    for mapping in mappings:
        result.update(mapping)
    return result


def is_same_object(a: Any, b: Any) -> bool:
    """Return True if *a* and *b* are the same object (identity check).

    Args:
        a: The first object.
        b: The second object.

    Returns:
        True if *a* is *b*, False otherwise.
    """
    return a is b
