"""Utility helper functions."""

from typing import Any, List, TypeVar

T = TypeVar("T")


def flatten(lst: List[List[T]]) -> List[T]:
    """Flatten a list of lists into a single list."""
    result: List[T] = []
    for item in lst:
        result.extend(item)
    return result


def chunk(lst: List[T], size: int) -> List[List[T]]:
    """Split a list into chunks of the specified size."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def unique(lst: List[T]) -> List[T]:
    """Return a list of unique elements preserving order."""
    seen: set = set()
    result: List[T] = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def is_empty(value: Any) -> bool:
    """Check if a value is considered empty."""
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, set, dict)):
        return len(value) == 0
    return False


def remove_none(lst: List[Any]) -> List[Any]:
    """Return a copy of lst with None values removed."""
    return [item for item in lst if item is not None]


def last(lst: List[T]) -> T:
    """Return the last element of a non-empty list."""
    if not lst:
        raise ValueError("List must not be empty")
    return lst[-1]


def first(lst: List[T]) -> T:
    """Return the first element of a non-empty list."""
    if not lst:
        raise ValueError("List must not be empty")
    return lst[0]
