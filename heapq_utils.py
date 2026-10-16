"""Heap queue utility functions.

This module provides helpers for heap queue operations using the standard library ``heapq`` module.
"""

from __future__ import annotations

import heapq
from typing import Any, Callable, Iterable, Iterator, List, Optional, TypeVar, cast

T = TypeVar("T")

__all__: list[str] = [
    "heapify",
    "heappush",
    "heappop",
    "heapreplace",
    "heappushpop",
    "merge",
    "nlargest",
    "nsmallest",
]


def heapify(items: list[Any]) -> None:
    """Transform list *items* into a heap, in-place, in linear time.

    Args:
        items: The list to turn into a heap.

    Raises:
        TypeError: If *items* is not a list.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    heapq.heapify(items)


def heappush(items: list[Any], item: Any) -> None:
    """Push the value *item* onto the heap *items*.

    Args:
        items: The heap list.
        item: The value to push.

    Raises:
        TypeError: If *items* is not a list.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    heapq.heappush(items, item)


def heappop(items: list[Any]) -> Any:
    """Pop and return the smallest item from the heap *items*.

    Args:
        items: The heap list.

    Returns:
        The smallest item.

    Raises:
        TypeError: If *items* is not a list.
        IndexError: If the heap is empty.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    return heapq.heappop(items)


def heapreplace(items: list[Any], item: Any) -> Any:
    """Pop and return the smallest item, then push *item*.

    The heap size stays the same.

    Args:
        items: The heap list.
        item: The value to push.

    Returns:
        The smallest item that was popped.

    Raises:
        TypeError: If *items* is not a list.
        IndexError: If the heap is empty.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    return heapq.heapreplace(items, item)


def heappushpop(items: list[Any], item: Any) -> Any:
    """Push *item* on the heap, then pop and return the smallest item.

    More efficient than ``heappush`` followed by ``heappop``.

    Args:
        items: The heap list.
        item: The value to push.

    Returns:
        The smallest item that was popped.

    Raises:
        TypeError: If *items* is not a list.
    """
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    return heapq.heappushpop(items, item)


def merge(
    *iterables: Iterable[T],
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False,
) -> Iterator[T]:
    """Merge multiple sorted inputs into a single sorted iterator.

    Args:
        *iterables: Sorted iterables to merge.
        key: Optional key function applied to each element.
        reverse: If True, inputs are merged in descending order.

    Returns:
        An iterator over the merged values.

    Raises:
        TypeError: If any argument is not iterable.
    """
    for it in iterables:
        if not isinstance(it, Iterable):
            raise TypeError("all arguments must be iterable")
    return heapq.merge(*iterables, key=cast(Any, key), reverse=reverse)


def nlargest(n: int, iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
    """Return the *n* largest elements from *iterable*.

    Args:
        n: Number of largest elements to return.
        iterable: The iterable to search.
        key: Optional key function applied to each element.

    Returns:
        A list of the *n* largest elements, in descending order.

    Raises:
        TypeError: If *iterable* is not iterable or *n* is not an int.
        ValueError: If *n* is negative.
    """
    if not isinstance(iterable, Iterable):
        raise TypeError("iterable must be iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return heapq.nlargest(n, iterable, key=cast(Any, key))


def nsmallest(n: int, iterable: Iterable[T], key: Optional[Callable[[T], Any]] = None) -> List[T]:
    """Return the *n* smallest elements from *iterable*.

    Args:
        n: Number of smallest elements to return.
        iterable: The iterable to search.
        key: Optional key function applied to each element.

    Returns:
        A list of the *n* smallest elements, in ascending order.

    Raises:
        TypeError: If *iterable* is not iterable or *n* is not an int.
        ValueError: If *n* is negative.
    """
    if not isinstance(iterable, Iterable):
        raise TypeError("iterable must be iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return heapq.nsmallest(n, iterable, key=cast(Any, key))
