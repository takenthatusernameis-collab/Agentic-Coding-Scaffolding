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
    "array_to_list",
    "array_from_list",
    "array_extend_from_list",
    "array_remove_first",
]


def _require_array(arr: object, name: str) -> array:
    if not isinstance(arr, array):
        raise TypeError(f"{name} must be an array, got {type(arr).__name__}")
    return arr


def _require_str(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_list(value: object, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list, got {type(value).__name__}")
    return value


def _require_int(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def array_create(typecode: str, initial: Iterable[Any] | None = None) -> array:
    """Create a new array with the given typecode."""
    _require_str(typecode, "typecode")
    if initial is None:
        return array(typecode)
    if isinstance(initial, str):
        raise TypeError("initial must not be a string")
    try:
        iter(initial)
    except TypeError:
        raise TypeError(f"initial must be iterable, got {type(initial).__name__}")
    return array(typecode, initial)


def array_fromlist(typecode: str, lst: list[Any]) -> array:
    """Create an array from a list."""
    _require_str(typecode, "typecode")
    _require_list(lst, "lst")
    return array(typecode, lst)


def array_tolist(arr: array) -> list[Any]:
    """Convert an array to a list."""
    _require_array(arr, "arr")
    return list(arr)


def array_append(arr: array, item: Any) -> None:
    """Append an item to the array."""
    _require_array(arr, "arr")
    arr.append(item)


def array_extend(arr: array, iterable: Iterable[Any]) -> None:
    """Extend array with items from iterable."""
    _require_array(arr, "arr")
    if isinstance(iterable, str):
        raise TypeError("iterable must not be a string")
    try:
        iter(iterable)
    except TypeError:
        raise TypeError(f"iterable must be iterable, got {type(iterable).__name__}")
    arr.extend(iterable)


def array_insert(arr: array, index: int, item: Any) -> None:
    """Insert item at index in array."""
    _require_array(arr, "arr")
    _require_int(index, "index")
    arr.insert(index, item)


def array_pop(arr: array, index: int = -1) -> Any:
    """Remove and return item at index."""
    _require_array(arr, "arr")
    _require_int(index, "index")
    return arr.pop(index)


def array_remove(arr: array, item: Any) -> None:
    """Remove first occurrence of item from array."""
    _require_array(arr, "arr")
    arr.remove(item)


def array_reverse(arr: array) -> None:
    """Reverse array in place."""
    _require_array(arr, "arr")
    arr.reverse()


def array_buffer_info(arr: array) -> tuple[int, int]:
    """Return (address, length) of the buffer used by array."""
    _require_array(arr, "arr")
    return arr.buffer_info()


def array_byteswap(arr: array) -> None:
    """Swap bytes in place if array is not single byte."""
    _require_array(arr, "arr")
    arr.byteswap()


def array_count(arr: array, item: Any) -> int:
    """Count occurrences of item in array."""
    _require_array(arr, "arr")
    return arr.count(item)


def array_index(arr: array, item: Any, start: int = 0, stop: int | None = None) -> int:
    """Return index of first occurrence of item."""
    _require_array(arr, "arr")
    _require_int(start, "start")
    if stop is not None:
        _require_int(stop, "stop")
        return arr.index(item, start, stop)
    return arr.index(item, start)


def array_to_list(arr: array) -> list[Any]:
    """Return a list view of the elements of *arr*.

    Args:
        arr: The array to convert.

    Returns:
        A list containing the elements of *arr* in order.

    Raises:
        TypeError: If *arr* is not an array.

    Examples:
        >>> array_to_list(array("i", [1, 2, 3]))
        [1, 2, 3]
        >>> array_to_list(array("i"))
        []
    """
    _require_array(arr, "arr")
    return arr.tolist()


def array_from_list(arr_type: str, values: list[Any]) -> array:
    """Create an array of the given typecode from *values*.

    Args:
        arr_type: The typecode of the new array (e.g. ``"i"`` for signed int).
        values: The list of values to load into the array.

    Returns:
        A new array holding the elements of *values*.

    Raises:
        TypeError: If *arr_type* is not a string or *values* is not a list.

    Examples:
        >>> array_from_list("i", [1, 2, 3]).tolist()
        [1, 2, 3]
        >>> array_from_list("f", [1.0, 2.5]).tolist()
        [1.0, 2.5]
    """
    if not isinstance(arr_type, str):
        raise TypeError("arr_type must be a str")
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    return array(arr_type, values)


def array_extend_from_list(arr: array, values: list[Any]) -> None:
    """Extend *arr* with the elements of *values*.

    Args:
        arr: The array to extend in place.
        values: The list of values to append to *arr*.

    Raises:
        TypeError: If *arr* is not an array or *values* is not a list.

    Examples:
        >>> a = array("i", [1, 2])
        >>> array_extend_from_list(a, [3, 4])
        >>> a.tolist()
        [1, 2, 3, 4]
    """
    _require_array(arr, "arr")
    if not isinstance(values, list):
        raise TypeError("values must be a list")
    arr.extend(values)


def array_remove_first(arr: array, item: Any) -> None:
    """Remove the first occurrence of *item* from *arr*.

    Args:
        arr: The array to modify in place.
        item: The value to remove.

    Raises:
        TypeError: If *arr* is not an array.
        ValueError: If *item* is not present in *arr*.

    Examples:
        >>> a = array("i", [1, 2, 1])
        >>> array_remove_first(a, 1)
        >>> a.tolist()
        [2, 1]
    """
    _require_array(arr, "arr")
    arr.remove(item)
