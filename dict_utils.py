"""Dictionary utility functions."""

from typing import Any, Dict, List, TypeVar

K = TypeVar("K")
V = TypeVar("V")


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
