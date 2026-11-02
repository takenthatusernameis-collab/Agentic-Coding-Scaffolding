"""Data utility functions."""

import copy
from typing import Any, Dict, Iterable, List, Set, TypeVar

K = TypeVar("K")
V = TypeVar("V")
__all__ = [
    "K",
    "V",
    "deep_copy",
    "flatten_dict",
    "merge_dicts",
    "omit",
    "pick",
    "invert_dict",
]



def deep_copy(obj: Any) -> Any:
    """Create a deep copy of an object."""
    try:
        return copy.deepcopy(obj)
    except Exception:
        return copy.copy(obj)


def merge_dicts(*dicts: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merge multiple dictionaries, later values override earlier ones."""
    result: Dict[Any, Any] = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def pick(d: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    """Return a new dict with only specified keys."""
    key_set: Set[K] = set(keys)
    return {k: d[k] for k in d if k in key_set}


def omit(d: Dict[K, V], keys: Iterable[K]) -> Dict[K, V]:
    """Return a new dict without specified keys."""
    key_set: Set[K] = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dict to dot-notation keys."""
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def invert_dict(d: Dict[K, V]) -> Dict[V, K]:
    """Return a new dictionary with keys and values swapped.

    Args:
        d: The dictionary to invert.

    Returns:
        A new dictionary mapping each value of *d* to its key.

    Raises:
        TypeError: If *d* is not a dictionary.
        ValueError: If *d* contains duplicate values, since the inverse would
            be ambiguous.

    Examples:
        >>> invert_dict({"a": 1, "b": 2})
        {1: 'a', 2: 'b'}
        >>> invert_dict({})
        {}
    """
    if not isinstance(d, dict):
        raise TypeError(f"d must be a dict, got {type(d).__name__}")
    inverted: Dict[V, K] = {}
    for key, value in d.items():
        if value in inverted:
            raise ValueError(f"cannot invert dict with duplicate value: {value!r}")
        inverted[value] = key
    return inverted
