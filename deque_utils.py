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


def remove_from_deque(d: deque, value: Any) -> None:
    """Remove first occurrence of value."""
    d.remove(value)


def reverse_deque(d: deque) -> None:
    """Reverse the deque in place."""
    d.reverse()


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
    "remove_from_deque",
    "reverse_deque",
]
