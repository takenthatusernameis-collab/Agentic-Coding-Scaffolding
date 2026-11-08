"""Deque utilities wrapping the standard library collections.deque."""

from collections import deque
from typing import Any, Iterable, List, Optional


def create_deque(iterable: Optional[Iterable[Any]] = None, maxlen: Optional[int] = None) -> deque:
    """Create a new deque."""
    if iterable is None:
        return deque(maxlen=maxlen)
    return deque(iterable, maxlen=maxlen)


def append_left(d: deque, x: Any) -> None:
    """Append x to the left of deque d."""
    d.appendleft(x)


def append_right(d: deque, x: Any) -> None:
    """Append x to the right of deque d."""
    d.append(x)


def pop_left(d: deque) -> Any:
    """Remove and return an element from the left of deque d."""
    return d.popleft()


def pop_right(d: deque) -> Any:
    """Remove and return an element from the right of deque d."""
    return d.pop()


def extend_left(d: deque, iterable: Iterable[Any]) -> None:
    """Extend the left side of deque d with elements from iterable."""
    d.extendleft(iterable)


def extend_right(d: deque, iterable: Iterable[Any]) -> None:
    """Extend the right side of deque d with elements from iterable."""
    d.extend(iterable)


def rotate_deque(d: deque, n: int = 1) -> None:
    """Rotate the deque n steps to the right."""
    d.rotate(n)


def clear_deque(d: deque) -> None:
    """Remove all elements from deque."""
    d.clear()


def deque_to_list(d: deque) -> List[Any]:
    """Convert deque to list."""
    return list(d)


def count_in_deque(d: deque, x: Any) -> int:
    """Count occurrences of x in deque."""
    return d.count(x)


def has_in_deque(d: deque, x: Any) -> bool:
    """Return True if deque d contains x at least once.

    Args:
        d: A deque to search.
        x: The value to look for.

    Returns:
        True if x occurs at least once in d, False otherwise.

    Examples:
        >>> d = create_deque([1, 2, 1, 3, 1])
        >>> has_in_deque(d, 1)
        True
        >>> has_in_deque(d, 9)
        False
    """
    return count_in_deque(d, x) > 0


def index_in_deque(
    d: deque, value: Any, start: int = 0, stop: Optional[int] = None
) -> int:
    """Return the index of the first occurrence of value in deque d.

    Args:
        d: A deque to search.
        value: The value to locate.
        start: Index to start searching from (inclusive). Defaults to 0.
        stop: Index to stop searching before (exclusive). Defaults to the
            length of the deque.

    Returns:
        The 0-based index of the first matching element.

    Raises:
        ValueError: If value is not found in the specified range.

    Examples:
        >>> d = create_deque([1, 2, 3, 2])
        >>> index_in_deque(d, 2)
        1
        >>> index_in_deque(d, 2, 2)
        3
    """
    if stop is None:
        return d.index(value, start)
    return d.index(value, start, stop)


def find_index_in_deque(
    d: deque, value: Any, start: int = 0, stop: Optional[int] = None
) -> Optional[int]:
    """Return the index of the first occurrence of value in deque d, or None.

    A non-raising companion to :func:`index_in_deque`.

    Args:
        d: A deque to search.
        value: The value to locate.
        start: Index to start searching from (inclusive). Defaults to 0.
        stop: Index to stop searching before (exclusive). Defaults to the
            length of the deque.

    Returns:
        The 0-based index of the first matching element, or None if value is
        not found in the specified range.

    Examples:
        >>> d = create_deque([1, 2, 3, 2])
        >>> find_index_in_deque(d, 2)
        1
        >>> find_index_in_deque(d, 9) is None
        True
        >>> find_index_in_deque(d, 2, 2)
        3
    """
    try:
        return index_in_deque(d, value, start, stop)
    except ValueError:
        return None


def remove_from_deque(d: deque, value: Any) -> None:
    """Remove first occurrence of value."""
    d.remove(value)


def peek_left(d: deque) -> Any:
    """Return the leftmost element of deque d without removing it.

    Args:
        d: A deque to peek into.

    Returns:
        The leftmost element.

    Raises:
        IndexError: If the deque is empty.

    Examples:
        >>> d = create_deque([1, 2, 3])
        >>> peek_left(d)
        1
        >>> d == create_deque([1, 2, 3])
        True
    """
    if not d:
        raise IndexError("peek from an empty deque")
    return d[0]


def peek_right(d: deque) -> Any:
    """Return the rightmost element of deque d without removing it.

    Args:
        d: A deque to peek into.

    Returns:
        The rightmost element.

    Raises:
        IndexError: If the deque is empty.

    Examples:
        >>> d = create_deque([1, 2, 3])
        >>> peek_right(d)
        3
        >>> d == create_deque([1, 2, 3])
        True
    """
    if not d:
        raise IndexError("peek from an empty deque")
    return d[-1]


def reverse_deque(d: deque) -> None:
    """Reverse the deque in place."""
    d.reverse()


def size(d: deque) -> int:
    """Return the number of elements in deque d.

    Args:
        d: A deque to measure.

    Returns:
        The number of elements in d.

    Examples:
        >>> d = create_deque()
        >>> size(d)
        0
        >>> append_right(d, 1)
        >>> size(d)
        1
        >>> append_right(d, 2)
        >>> size(d)
        2
    """
    return len(d)


def is_empty(d: deque) -> bool:
    """Return True when deque d contains no elements.

    Args:
        d: A deque to inspect.

    Returns:
        True if d is empty, False otherwise.

    Examples:
        >>> d = create_deque()
        >>> is_empty(d)
        True
        >>> append_right(d, 1)
        >>> is_empty(d)
        False
    """
    return len(d) == 0


def has_items(d: deque) -> bool:
    """Return True when deque d contains at least one element.

    Args:
        d: A deque to inspect.

    Returns:
        True if d is non-empty, False otherwise.

    Examples:
        >>> d = create_deque()
        >>> has_items(d)
        False
        >>> append_right(d, 1)
        >>> has_items(d)
        True
    """
    return len(d) > 0


__all__ = [
    "create_deque",
    "append_left",
    "append_right",
    "pop_left",
    "pop_right",
    "extend_left",
    "extend_right",
    "rotate_deque",
    "clear_deque",
    "deque_to_list",
    "count_in_deque",
    "has_in_deque",
    "index_in_deque",
    "find_index_in_deque",
    "peek_left",
    "peek_right",
    "remove_from_deque",
    "reverse_deque",
    "size",
    "is_empty",
    "has_items",
]
