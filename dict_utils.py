"""Dictionary utility functions."""

from typing import Any, Dict, List, TypeVar

K = TypeVar("K")
V = TypeVar("V")

__all__ = [
    "K",
    "V",
    "contains_key",
    "contains_value",
    "deep_merge",
    "filter_dict",
    "flatten_dict",
    "has_key",
    "has_value",
    "invert_dict",
    "is_invertible","""
    "keys_equal",
    "merge",
    "omit_keys",
    "safe_get",
    "select_keys",
    "values_equal",
    "unflatten_dict",
]


def deep_merge(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge two dictionaries.

    Args:
        d1: Base dictionary.
        d2: Dictionary to merge into d1.

    Returns:
        Merged dictionary.
    """
    result = d1.copy()
    for key, value in d2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def merge(d1: Dict[K, V], d2: Dict[K, V]) -> Dict[K, V]:
    """Shallowly merge two dictionaries.

    Unlike :func:`deep_merge`, this performs a one-level merge: values from
    *d2* overwrite the corresponding values in *d1* for shared keys, without
    recursing into nested dictionaries.

    Args:
        d1: Base dictionary.
        d2: Dictionary whose entries override those in d1.

    Returns:
        New dictionary containing all entries from *d1* plus the entries from
        *d2* (with *d2* taking precedence on key conflicts).

    Raises:
        TypeError: If either argument is not a dict.

    Examples:
        >>> merge({"a": 1, "b": 2}, {"b": 3, "c": 4})
        {'a': 1, 'b': 3, 'c': 4}
        >>> merge({"a": {"x": 1}}, {"a": {"y": 2}})
        {'a': {'y': 2}}
    """
    if not isinstance(d1, dict):
        raise TypeError("d1 must be a dict")
    if not isinstance(d2, dict):
        raise TypeError("d2 must be a dict")
    result: Dict[K, V] = dict(d1)
    result.update(d2)
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten a nested dictionary into a single-level dictionary.

    Args:
        d: Dictionary to flatten.
        parent_key: Parent key prefix.
        sep: Separator between keys.

    Returns:
        Flattened dictionary.
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(d: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Unflatten a flat dictionary with keys containing separators.

    Args:
        d: Flattened dictionary.
        sep: Separator used in keys.

    Returns:
        Nested dictionary.
    """
    result: Dict[str, Any] = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def safe_get(d: Dict[Any, Any], *keys: Any, default: Any = None) -> Any:
    """Safely get a nested value from a dictionary.

    Args:
        d: Dictionary to search in.
        keys: Keys to traverse.
        default: Default value if not found.

    Returns:
        Value at the nested path or default.
    """
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def has_key(d: Dict[K, Any], key: K) -> bool:
    """Report whether *key* is present in *d*.

    Args:
        d: Dictionary to search in.
        key: Key to look for.

    Returns:
        ``True`` when *key* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> has_key({"a": 1, "b": 2}, "a")
        True
        >>> has_key({"a": 1, "b": 2}, "c")
        False
        >>> has_key({}, "a")
        False
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    return key in d


def contains_key(d: Dict[K, Any], key: K) -> bool:
    """Report whether *key* is present in *d*.

    This is an alias for :func:`has_key`, provided so the module offers a single
    ``contains_*`` naming convention alongside :func:`select_keys` and
    :func:`omit_keys`.

    Args:
        d: Dictionary to search in.
        key: Key to look for.

    Returns:
        ``True`` when *key* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> contains_key({"a": 1, "b": 2}, "a")
        True
        >>> contains_key({"a": 1, "b": 2}, "c")
        False
        >>> contains_key({}, "a")
        False
    """
    return has_key(d, key)


def has_value(d: Dict[Any, V], value: V) -> bool:
    """Report whether *value* is present in *d*.

    Args:
        d: Dictionary to search in.
        value: Value to look for.

    Returns:
        ``True`` when *value* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> has_value({"a": 1, "b": 2}, 1)
        True
        >>> has_value({"a": 1, "b": 2}, 3)
        False
        >>> has_value({}, 1)
        False
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    return value in d.values()


def contains_value(d: Dict[Any, V], value: V) -> bool:
    """Report whether *value* is present in *d*.

    This is an alias for :func:`has_value`, mirroring the
    :func:`contains_key` / :func:`has_key` pair.

    Args:
        d: Dictionary to search in.
        value: Value to look for.

    Returns:
        ``True`` when *value* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> contains_value({"a": 1, "b": 2}, 1)
        True
        >>> contains_value({"a": 1, "b": 2}, 3)
        False
        >>> contains_value({}, 1)
        False
    """
    return has_value(d, value)


def keys_equal(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> bool:
    """Report whether two dictionaries have the same set of keys.

    Only the keys are compared; values and key order are ignored.

    Args:
        d1: First dictionary.
        d2: Second dictionary.

    Returns:
        ``True`` when *d1* and *d2* contain the same keys, ``False`` otherwise.

    Raises:
        TypeError: If either argument is not a dict.

    Examples:
        >>> keys_equal({"a": 1, "b": 2}, {"a": 3, "b": 4})
        True
        >>> keys_equal({"a": 1}, {"a": 1, "b": 2})
        False
        >>> keys_equal({}, {})
        True
    """
    if not isinstance(d1, dict):
        raise TypeError("d1 must be a dict")
    if not isinstance(d2, dict):
        raise TypeError("d2 must be a dict")
    return set(d1) == set(d2)


def values_equal(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> bool:
    """Report whether two dictionaries have the same set of values.

    Only the values are compared; keys and value order are ignored.

    Args:
        d1: First dictionary.
        d2: Second dictionary.

    Returns:
        ``True`` when *d1* and *d2* contain the same values, ``False`` otherwise.

    Raises:
        TypeError: If either argument is not a dict.

    Examples:
        >>> values_equal({"a": 1, "b": 2}, {"c": 2, "d": 1})
        True
        >>> values_equal({"a": 1}, {"a": 1, "b": 2})
        False
        >>> values_equal({}, {})
        True
    """
    if not isinstance(d1, dict):
        raise TypeError("d1 must be a dict")
    if not isinstance(d2, dict):
        raise TypeError("d2 must be a dict")
    return set(d1.values()) == set(d2.values())


def invert_dict(d: Dict[K, V]) -> Dict[V, K]:
    """Invert a dictionary by swapping keys and values.

    Args:
        d: Dictionary to invert.

    Returns:
        Inverted dictionary.

    Raises:
        ValueError: If values are not unique.
    """
    if len(d.values()) != len(set(d.values())):
        raise ValueError("Cannot invert dictionary with duplicate values")
    return {v: k for k, v in d.items()}


def filter_dict(d: Dict[K, V], predicate: Any) -> Dict[K, V]:
    """Filter a dictionary based on a predicate.

    Args:
        d: Dictionary to filter.
        predicate: Function that takes (key, value) and returns bool.

    Returns:
        Filtered dictionary.
    """
    return {k: v for k, v in d.items() if predicate(k, v)}


def select_keys(d: Dict[K, V], keys: List[K]) -> Dict[K, V]:
    """Select a subset of keys from a dictionary.

    Args:
        d: Source dictionary.
        keys: Keys to select.

    Returns:
        New dictionary containing only the selected keys that exist in d.

    Raises:
        TypeError: If d is not a dict or keys is not a list.
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not isinstance(keys, list):
        raise TypeError("keys must be a list")
    return {k: d[k] for k in keys if k in d}


def omit_keys(d: Dict[K, V], keys: List[K]) -> Dict[K, V]:
    """Return a new dictionary excluding the given keys.

    Args:
        d: Source dictionary.
        keys: Keys to omit.

    Returns:
        New dictionary containing all keys except those in ``keys``.

    Raises:
        TypeError: If d is not a dict or keys is not a list.
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not isinstance(keys, list):
        raise TypeError("keys must be a list")
    key_set = set(keys)
    return {k: v for k, v in d.items() if k not in key_set}
