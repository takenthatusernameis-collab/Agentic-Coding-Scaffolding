"""Tree and nested structure utilities for working with nested dict/list data."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def get_nested(d: Dict[str, Any] | Any, keys: Iterable[str | int], default: Any = None) -> Any:
    """Safely get a value from a nested structure using a key path.

    Args:
        d: The nested dictionary/list structure to traverse.
        keys: An iterable of keys/indexes representing the path.
        default: The default value to return if the path is missing.

    Returns:
        The value at the path, or default if not found.

    Examples:
        >>> get_nested({"a": {"b": {"c": 1}}}, ["a", "b", "c"])
        1
        >>> get_nested({"a": {"b": 2}}, ["a", "x"], default="missing")
        'missing'
        >>> get_nested({"a": [1, 2, 3]}, ["a", 1])
        2
    """
    try:
        result: Any = d
        for key in keys:
            result = result[key]  # type: ignore[index]
        return result
    except (KeyError, IndexError, TypeError):
        return default


def set_nested(d: Dict[str, Any], keys: Iterable[str | int], value: Any) -> Dict[str, Any]:
    """Set a value in a nested dict, creating intermediate dicts as needed.

    Args:
        d: The root dictionary to modify.
        keys: An iterable of keys representing the path.
        value: The value to set.

    Returns:
        The modified dictionary (same object, mutated).

    Examples:
        >>> d = {}
        >>> set_nested(d, ["a", "b", "c"], 1)
        {'a': {'b': {'c': 1}}}
        >>> set_nested(d, ["a", "b", "d"], 2)
        {'a': {'b': {'c': 1, 'd': 2}}}
    """
    keys_list = list(keys)
    if not keys_list:
        return d

    current: Any = d
    for key in keys_list[:-1]:
        if key not in current or not isinstance(current[key], dict):  # type: ignore[index]
            current[key] = {}  # type: ignore[index]
        current = current[key]  # type: ignore[index]
    current[keys_list[-1]] = value  # type: ignore[index]
    return d


def delete_nested(d: Dict[str, Any], keys: Iterable[str | int]) -> bool:
    """Delete a value at a nested path.

    Args:
        d: The root dictionary to modify.
        keys: An iterable of keys representing the path.

    Returns:
        True if the value was deleted, False if the path doesn't exist.

    Examples:
        >>> d = {"a": {"b": {"c": 1}}}
        >>> delete_nested(d, ["a", "b", "c"])
        True
        >>> delete_nested(d, ["a", "x"])
        False
    """
    keys_list = list(keys)
    if not keys_list:
        return False

    current: Any = d
    path: List[Any] = []
    for key in keys_list[:-1]:
        path.append((current, key))
        if not isinstance(current, dict) or key not in current:  # type: ignore[index]
            return False
        current = current[key]  # type: ignore[index]

    last_key = keys_list[-1]
    if not isinstance(current, dict) or last_key not in current:  # type: ignore[index]
        return False
    del current[last_key]  # type: ignore[index]
    return True


def flatten_tree(d: Dict[str, Any] | Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten a nested dictionary into a flat dictionary with compound keys.

    Args:
        d: The nested dictionary to flatten.
        parent_key: The base key for nested items.
        sep: The separator between keys.

    Returns:
        A flat dictionary.

    Examples:
        >>> flatten_tree({"a": {"b": {"c": 1, "d": 2}}, "e": 3})
        {'a.b.c': 1, 'a.b.d': 2, 'e': 3}
    """
    items: List[Tuple[str, Any]] = []
    if isinstance(d, dict):
        for key, value in d.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else str(key)
            items.extend(flatten_tree(value, new_key, sep).items())
        return dict(items)
    else:
        if parent_key == "":
            return {"": d}
        return {parent_key: d}


def unflatten_tree(flat: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Unflatten a flat dictionary with compound keys back to a nested structure.

    Args:
        flat: A flat dictionary with keys joined by sep.
        sep: The separator used in keys.

    Returns:
        A nested dictionary.

    Examples:
        >>> unflatten_tree({"a.b.c": 1, "a.b.d": 2, "e": 3})
        {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
    """
    result: Dict[str, Any] = {}
    for key, value in flat.items():
        parts = key.split(sep) if sep and sep in key else [key] if key else []
        current = result
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        if parts:
            current[parts[-1]] = value
        else:
            result = value  # type: ignore[assignment]
    return result


def map_tree(func: Callable[[Any], Any], tree: Any) -> Any:
    """Recursively apply a function to all leaf values in a tree structure.

    Dict values and list elements are treated as branches. Non-container
    values (or leaf nodes) have func applied.

    Args:
        func: The function to apply to leaf values.
        tree: The tree structure to traverse.

    Returns:
        A new tree structure with func applied to all leaves.

    Examples:
        >>> map_tree(lambda x: x * 2, {"a": {"b": 1}, "c": [2, 3]})
        {'a': {'b': 2}, 'c': [4, 6]}
    """
    if isinstance(tree, dict):
        return {k: map_tree(func, v) for k, v in tree.items()}
    elif isinstance(tree, list):
        return [map_tree(func, item) for item in tree]
    elif isinstance(tree, tuple):
        return tuple(map_tree(func, item) for item in tree)
    else:
        return func(tree)


def filter_tree(pred: Callable[[Any], bool], tree: Any) -> Any:
    """Recursively filter a tree structure based on a predicate.

    The predicate is applied to values. For dicts, only key-value pairs
    where pred(value) is True (or based on leaf logic) are kept? This
    implementation keeps nodes where the transformed/considered value passes;
    for nested structures, it recursively filters and drops empty containers
    when appropriate.

    Args:
        pred: The predicate function returning True for values to keep.
        tree: The tree structure to filter.

    Returns:
        A filtered tree structure.

    Examples:
        >>> filter_tree(lambda x: x > 1, {"a": 1, "b": 2, "c": {"d": 3, "e": 0}})
        {'b': 2, 'c': {'d': 3}}
    """
    if isinstance(tree, dict):
        result: Dict[str, Any] = {}
        for k, v in tree.items():
            filtered = filter_tree(pred, v)
            # Keep if filtered is not empty container or if it's a truthy leaf that passed
            if isinstance(filtered, (dict, list, tuple)):
                if filtered:  # non-empty
                    result[k] = filtered
            elif pred(v) if False else True:  # always keep if leaf passes pred? better check
                pass  # handle below
            # simpler: if the original v becomes filtered, keep based on whether useful
            # but easier logic: apply pred to leaf; for containers, recurse and keep if non-empty
            if isinstance(v, (dict, list, tuple)):
                if filtered:
                    result[k] = filtered
            else:
                if pred(v):
                    result[k] = v
        return result
    elif isinstance(tree, list):
        result_list = []
        for item in tree:
            filtered = filter_tree(pred, item)
            if isinstance(filtered, (dict, list, tuple)):
                if filtered:
                    result_list.append(filtered)
            else:
                if pred(item):
                    result_list.append(item)
        return result_list
    elif isinstance(tree, tuple):
        result_list = []
        for item in tree:
            filtered = filter_tree(pred, item)
            if isinstance(filtered, (dict, list, tuple)):
                if filtered:
                    result_list.append(filtered)
            else:
                if pred(item):
                    result_list.append(item)
        return tuple(result_list)
    else:
        return tree if pred(tree) else None  # type: ignore[return-value]
