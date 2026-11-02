"""Data utility functions."""

import copy
from typing import Any, Dict, Iterable, List, Set, TypeVar

K = TypeVar("K")
V = TypeVar("V")
__all__ = [
    "K",
    "V",
    "deep_copy",
    "del_nested",
    "flatten_dict",
    "get_nested",
    "invert_dict",
    "merge_dicts",
    "omit",
    "pick",
    "set_nested",
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


def get_nested(d: Dict[str, Any], path: str, default: Any = None, sep: str = ".") -> Any:
    """Return the value at a dot-separated path in a nested dictionary.

    Traverses *d* using the segments of *path* split on *sep*. When a segment
    is missing or an intermediate value is not a dictionary, *default* is
    returned instead of raising.

    Args:
        d: The dictionary to traverse.
        path: A dot-separated key path, e.g. ``"a.b.c"``.
        default: Value returned when *path* does not exist in *d*.
        sep: Separator between path segments (default: ``"."``).

    Returns:
        The value stored at *path*, or *default* when the path is absent.

    Raises:
        TypeError: If *d* is not a dictionary or *path* is not a string.

    Examples:
        >>> get_nested({"a": {"b": 1}}, "a.b")
        1
        >>> get_nested({"a": {"b": {"c": 3}}}, "a.b.c")
        3
        >>> get_nested({"a": {"b": 1}}, "a.c", default=0)
        0
        >>> get_nested({"a": 1}, "a.b", default="missing")
        'missing'
        >>> get_nested({}, "a.b", default="missing")
        'missing'
    """
    if not isinstance(d, dict):
        raise TypeError(f"d must be a dict, got {type(d).__name__}")
    if not isinstance(path, str):
        raise TypeError(f"path must be a string, got {type(path).__name__}")
    current: Any = d
    for segment in path.split(sep):
        if not isinstance(current, dict) or segment not in current:
            return default
        current = current[segment]
    return current


def set_nested(d: Dict[str, Any], path: str, value: Any, sep: str = ".") -> Dict[str, Any]:
    """Set a value at a dot-separated path in a nested dictionary.

    Creates intermediate dictionaries as needed along the path. If an
    intermediate value exists but is not a dictionary, it will be replaced
    with a new dictionary so that the assignment can proceed.

    Args:
        d: The dictionary to modify.
        path: A dot-separated key path, e.g. ``"a.b.c"``.
        value: The value to set.
        sep: Separator between path segments (default: ``"."``).

    Returns:
        The modified dictionary (same object, mutated).

    Raises:
        TypeError: If *d* is not a dictionary or *path* is not a string.
        ValueError: If *path* is empty.

    Examples:
        >>> d = {}
        >>> set_nested(d, "a.b.c", 1)
        {'a': {'b': {'c': 1}}}
        >>> set_nested(d, "a.b.d", 2)
        {'a': {'b': {'c': 1, 'd': 2}}}
    """
    if not isinstance(d, dict):
        raise TypeError(f"d must be a dict, got {type(d).__name__}")
    if not isinstance(path, str):
        raise TypeError(f"path must be a string, got {type(path).__name__}")
    segments = path.split(sep)
    if not segments or segments == [""]:
        raise ValueError("path must not be empty")
    current: Dict[str, Any] = d
    for segment in segments[:-1]:
        if segment not in current or not isinstance(current[segment], dict):
            current[segment] = {}
        current = current[segment]
    current[segments[-1]] = value
    return d


def del_nested(d: Dict[str, Any], path: str, sep: str = ".") -> bool:
    """Delete the value at a dot-separated path in a nested dictionary.

    Traverses *d* using the segments of *path* split on *sep* and removes the
    final key if it exists. Returns True when a key was deleted, False when
    the path does not exist or an intermediate value is not a dictionary.

    Args:
        d: The dictionary to modify.
        path: A dot-separated key path, e.g. ``"a.b.c"``.
        sep: Separator between path segments (default: ``"."``).

    Returns:
        True when a key was deleted, False when the path is absent.

    Raises:
        TypeError: If *d* is not a dictionary or *path* is not a string.
        ValueError: If *path* is empty.

    Examples:
        >>> d = {"a": {"b": 1}}
        >>> del_nested(d, "a.b")
        True
        >>> d
        {'a': {}}
        >>> del_nested(d, "a.c")
        False
        >>> del_nested({}, "a.b")
        False
    """
    if not isinstance(d, dict):
        raise TypeError(f"d must be a dict, got {type(d).__name__}")
    if not isinstance(path, str):
        raise TypeError(f"path must be a string, got {type(path).__name__}")
    segments = path.split(sep)
    if not path or not any(segments):
        raise ValueError("path must not be empty")
    current: Dict[str, Any] = d
    for segment in segments[:-1]:
        if segment not in current or not isinstance(current[segment], dict):
            return False
        current = current[segment]
    if segments[-1] not in current:
        return False
    del current[segments[-1]]
    return True