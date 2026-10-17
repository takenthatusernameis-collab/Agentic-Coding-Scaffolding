"""Array utility functions wrapping the standard library 'array' module."""

from __future__ import annotations

from array import array
from typing import Any, Iterable

__all__: list[str] = [
    "array_create",
    "array_fromlist",
    "array_tolist",
    "array_append",
    "array_extend",
    "array_insert",
    "array_pop",
    "array_remove",
    "array_reverse",
    "array_buffer_info",
    "array_byteswap",
    "array_count",
    "array_index",
]


def array_create(typecode: str, initial: Iterable[Any] | None = None) -> array:
    """Create a new array with the given typecode."""
    if initial is None:
        return array(typecode)
    return array(typecode, initial)


def array_fromlist(typecode: str, lst: list[Any]) -> array:
    """Create an array from a list."""
    return array(typecode, lst)


def array_tolist(arr: array) -> list[Any]:
    """Convert an array to a list."""
    return list(arr)


def array_append(arr: array, item: Any) -> None:
    """Append an item to the array."""
    arr.append(item)


def array_extend(arr: array, iterable: Iterable[Any]) -> None:
    """Extend array with items from iterable."""
    arr.extend(iterable)


def array_insert(arr: array, index: int, item: Any) -> None:
    """Insert item at index in array."""
    arr.insert(index, item)


def array_pop(arr: array, index: int = -1) -> Any:
    """Remove and return item at index."""
    return arr.pop(index)


def array_remove(arr: array, item: Any) -> None:
    """Remove first occurrence of item from array."""
    arr.remove(item)


def array_reverse(arr: array) -> None:
    """Reverse array in place."""
    arr.reverse()


def array_buffer_info(arr: array) -> tuple[int, int]:
    """Return (address, length) of the buffer used by array."""
    return arr.buffer_info()


def array_byteswap(arr: array) -> None:
    """Swap bytes in place if array is not single byte."""
    arr.byteswap()


def array_count(arr: array, item: Any) -> int:
    """Count occurrences of item in array."""
    return arr.count(item)


def array_index(arr: array, item: Any, start: int = 0, stop: int | None = None) -> int:
    """Return index of first occurrence of item."""
    if stop is None:
        return arr.index(item, start)
    return arr.index(item, start, stop)
