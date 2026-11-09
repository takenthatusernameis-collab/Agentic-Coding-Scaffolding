"""Dictionary utility functions."""

from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")

__all__ = [
    "K",
    "V",
    "contains_all_keys",
    "contains_all_values",
    "contains_any_key",
    "contains_any_value",
    "contains_key",
    "contains_value",
    "count_all_keys",
    "count_all_values",
    "count_where",
    "deep_merge",
    "filter_dict",
    "all_where",
    "find_where",
    "flatten_dict",
    "has_all_keys",
    "has_all_values",
    "has_any_key",
    "has_any_value",
    "has_key",
    "has_value",
    "has_where",
    "invert_dict",
    "is_invertible",
    "keys_equal",
    "merge",
    "none_where",
    "omit_keys",
    "safe_get",
    "select_keys",
    "values_equal",
    "unflatten_dict",
]


def deep_merge(d1: Dict[Any, Any], d2: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge two dictionaries.

    Unlike :func:`merge`, this recurses into nested dictionaries when both
    sides have a ``dict`` value for the same key.

    Args:
        d1: Base dictionary.
        d2: Dictionary to merge into d1.

    Returns:
        Merged dictionary.

    Raises:
        TypeError: If either argument is not a dict.
    """
    if not isinstance(d1, dict):
        raise TypeError("d1 must be a dict")
    if not isinstance(d2, dict):
        raise TypeError("d2 must be a dict")
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


def is_invertible(d: Dict[K, V]) -> bool:
    """Report whether *d* can be inverted without losing information.

    A dictionary is invertible when all of its values are distinct, so that
    swapping keys and values produces a one-to-one mapping. This is the
    boolean companion to :func:`invert_dict`, which raises ``ValueError``
    when the dictionary is not invertible.

    Args:
        d: Dictionary to check.

    Returns:
        ``True`` when every value in *d* is unique, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> is_invertible({"a": 1, "b": 2})
        True
        >>> is_invertible({"a": 1, "b": 1})
        False
        >>> is_invertible({})
        True
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    values = list(d.values())
    return len(values) == len(set(values))


def filter_dict(d: Dict[K, V], predicate: Any) -> Dict[K, V]:
    """Filter a dictionary based on a predicate.

    Args:
        d: Dictionary to filter.
        predicate: Function that takes (key, value) and returns bool.

    Returns:
        Filtered dictionary.
    """
    return {k: v for k, v in d.items() if predicate(k, v)}

def count_where(d: Dict[K, V], predicate: Callable[[K, V], bool]) -> int:
    """Count items in *d* for which *predicate(key, value)* returns ``True``.

    Args:
        d: Dictionary to inspect.
        predicate: Function that takes ``(key, value)`` and returns ``bool``.

    Returns:
        The number of items matching *predicate*.

    Raises:
        TypeError: If *d* is not a dict or *predicate* is not callable.

    Examples:
        >>> count_where({"a": 1, "b": 2, "c": 3}, lambda k, v: v % 2 == 1)
        2
        >>> count_where({"a": 1, "b": 2}, lambda k, v: v > 10)
        0
        >>> count_where({}, lambda k, v: True)
        0
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return sum(1 for k, v in d.items() if predicate(k, v))


def has_where(d: Dict[K, V], predicate: Callable[[K, V], bool]) -> bool:
    """Report whether any item in *d* satisfies *predicate(key, value)*.

    This is the boolean companion to :func:`count_where`.

    Args:
        d: Dictionary to inspect.
        predicate: Function that takes ``(key, value)`` and returns ``bool``.

    Returns:
        ``True`` when at least one item matches, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict or *predicate* is not callable.

    Examples:
        >>> has_where({"a": 1, "b": 2}, lambda k, v: v > 1)
        True
        >>> has_where({"a": 1, "b": 2}, lambda k, v: v > 10)
        False
        >>> has_where({}, lambda k, v: True)
        False
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return any(predicate(k, v) for k, v in d.items())


def find_where(
    d: Dict[K, V], predicate: Callable[[K, V], bool]
) -> Optional[Tuple[K, V]]:
    """Find the first item in *d* satisfying *predicate(key, value)*.

    Iteration follows the dictionary's insertion order.

    Args:
        d: Dictionary to inspect.
        predicate: Function that takes ``(key, value)`` and returns ``bool``.

    Returns:
        The first matching ``(key, value)`` tuple, or ``None`` if no item
        matches.

    Raises:
        TypeError: If *d* is not a dict or *predicate* is not callable.

    Examples:
        >>> find_where({"a": 1, "b": 2, "c": 3}, lambda k, v: v > 1)
        ('b', 2)
        >>> find_where({"a": 1, "b": 2}, lambda k, v: v > 10) is None
        True
        >>> find_where({}, lambda k, v: True) is None
        True
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    for k, v in d.items():
        if predicate(k, v):
            return (k, v)
    return None


def all_where(d: Dict[K, V], predicate: Callable[[K, V], bool]) -> bool:
    """Report whether every item in *d* satisfies *predicate(key, value)*.

    Vacuously ``True`` for an empty dictionary, matching Python ``all`` semantics.

    Args:
        d: Dictionary to inspect.
        predicate: Function that takes ``(key, value)`` and returns ``bool``.

    Returns:
        ``True`` when all items match (or *d* is empty), ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict or *predicate* is not callable.

    Examples:
        >>> all_where({"a": 2, "b": 4}, lambda k, v: v % 2 == 0)
        True
        >>> all_where({"a": 2, "b": 3}, lambda k, v: v % 2 == 0)
        False
        >>> all_where({}, lambda k, v: False)
        True
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return all(predicate(k, v) for k, v in d.items())


def none_where(d: Dict[K, V], predicate: Callable[[K, V], bool]) -> bool:
    """Report whether no item in *d* satisfies *predicate(key, value)*.

    This is the negation companion to :func:`has_where`. An empty dictionary
    returns ``True``.

    Args:
        d: Dictionary to inspect.
        predicate: Function that takes ``(key, value)`` and returns ``bool``.

    Returns:
        ``True`` when no items match (or *d* is empty), ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict or *predicate* is not callable.

    Examples:
        >>> none_where({"a": 1, "b": 3}, lambda k, v: v % 2 == 0)
        True
        >>> none_where({"a": 1, "b": 2}, lambda k, v: v % 2 == 0)
        False
        >>> none_where({}, lambda k, v: True)
        True
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return not any(predicate(k, v) for k, v in d.items())



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


def has_all_keys(d: Dict[Any, Any], keys: Any) -> bool:
    """Report whether all of *keys* are present in *d*.

    This is the boolean companion to :func:`count_all_keys`; it reports
    whether every key in *keys* is present in *d*, short-circuiting on
    the first missing key.

    Args:
        d: Dictionary to search in.
        keys: Iterable of keys to look for.

    Returns:
        ``True`` when every key in *keys* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> has_all_keys({"a": 1, "b": 2}, ["a", "b"])
        True
        >>> has_all_keys({"a": 1, "b": 2}, ["a", "c"])
        False
        >>> has_all_keys({}, [])
        True
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    return all(k in d for k in keys)


def contains_all_keys(d: Dict[Any, Any], keys: Any) -> bool:
    """Alias for :func:`has_all_keys`."""
    return has_all_keys(d, keys)


def count_all_keys(d: Dict[Any, Any], keys: Any) -> int:
    """Return the number of keys from *keys* that are present in *d*.

    This is the integer companion to :func:`has_all_keys` and
    :func:`has_any_key`; it reports how many of the given *keys* are present
    in *d*. Keys that appear more than once in *keys* are counted once per
    occurrence.

    Args:
        d: Dictionary to search in.
        keys: Iterable of keys to look for.

    Returns:
        The count of keys from *keys* that are present in *d*.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> count_all_keys({"a": 1, "b": 2}, ["a", "b"])
        2
        >>> count_all_keys({"a": 1, "b": 2}, ["a", "c"])
        1
        >>> count_all_keys({}, [])
        0
        >>> count_all_keys({"a": 1, "b": 2}, ["a", "a", "b"])
        3
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    return sum(1 for k in keys if k in d)


def has_any_key(d: Dict[Any, Any], keys: Any) -> bool:
    """Report whether at least one of *keys* is present in *d*.

    This is the boolean companion to :func:`count_all_keys`; it reports
    whether at least one key in *keys* is present in *d*, short-circuiting
    on the first match.

    Args:
        d: Dictionary to search in.
        keys: Iterable of keys to look for.

    Returns:
        ``True`` when at least one key in *keys* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> has_any_key({"a": 1, "b": 2}, ["a", "c"])
        True
        >>> has_any_key({"a": 1, "b": 2}, ["c", "d"])
        False
        >>> has_any_key({}, [])
        False
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    return any(k in d for k in keys)


def contains_any_key(d: Dict[Any, Any], keys: Any) -> bool:
    """Alias for :func:`has_any_key`."""
    return has_any_key(d, keys)


def has_all_values(d: Dict[Any, Any], values: Any) -> bool:
    """Report whether all of *values* are present in *d*.

    This is the boolean companion to :func:`count_all_values`; it reports
    whether every value in *values* is present in *d*, short-circuiting on
    the first missing value.

    Args:
        d: Dictionary to search in.
        values: Iterable of values to look for.

    Returns:
        ``True`` when every value in *values* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> has_all_values({"a": 1, "b": 2}, [1, 2])
        True
        >>> has_all_values({"a": 1, "b": 2}, [1, 3])
        False
        >>> has_all_values({}, [])
        True
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    d_values = d.values()
    return all(v in d_values for v in values)


def contains_all_values(d: Dict[Any, Any], values: Any) -> bool:
    """Alias for :func:`has_all_values`."""
    return has_all_values(d, values)


def count_all_values(d: Dict[Any, Any], values: Any) -> int:
    """Return the number of values from *values* that are present in *d*.

    Each element of *values* is checked against the dictionary's values;
    duplicates in *values* are counted separately, so the result can exceed
    the number of distinct values in *d*. An empty *values* iterable yields
    ``0``.

    Args:
        d: Dictionary to search in.
        values: Iterable of values to look for.

    Returns:
        The number of elements of *values* that are present in *d*.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> count_all_values({"a": 1, "b": 2}, [1, 2])
        2
        >>> count_all_values({"a": 1, "b": 2}, [1, 3])
        1
        >>> count_all_values({}, [])
        0
        >>> count_all_values({"a": 1, "b": 2}, [1, 1, 2])
        3
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    d_values = d.values()
    return sum(1 for v in values if v in d_values)


def has_any_value(d: Dict[Any, Any], values: Any) -> bool:
    """Report whether at least one of *values* is present in *d*.

    This is the boolean companion to :func:`count_all_values`; it reports
    whether any value in *values* is present in *d*, short-circuiting on
    the first match.

    Args:
        d: Dictionary to search in.
        values: Iterable of values to look for.

    Returns:
        ``True`` when at least one value in *values* is present in *d*, ``False`` otherwise.

    Raises:
        TypeError: If *d* is not a dict.

    Examples:
        >>> has_any_value({"a": 1, "b": 2}, [1, 3])
        True
        >>> has_any_value({"a": 1, "b": 2}, [3, 4])
        False
        >>> has_any_value({}, [])
        False
    """
    if not isinstance(d, dict):
        raise TypeError("d must be a dict")
    d_values = d.values()
    return any(v in d_values for v in values)


def contains_any_value(d: Dict[Any, Any], values: Any) -> bool:
    """Alias for :func:`has_any_value`."""
    return has_any_value(d, values)
