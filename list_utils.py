"""Advanced list utility functions for common manipulation tasks."""

from typing import Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")
K = TypeVar("K")

__all__: List[str] = [
    "partition",
    "group_by",
    "safe_get",
    "find",
    "drop",
    "take",
    "intersperse",
    "chunks",
]


def partition(lst: List[T], predicate: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
    """Split a list into two lists based on a predicate.

    Args:
        lst: The list to partition.
        predicate: A function that returns ``True`` for elements that should
            be in the first result list.

    Returns:
        A tuple of ``(matching, non_matching)`` lists.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> partition([1, 2, 3, 4], lambda x: x % 2 == 0)
        ([2, 4], [1, 3])
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    matching: List[T] = []
    non_matching: List[T] = []
    for item in lst:
        if predicate(item):
            matching.append(item)
        else:
            non_matching.append(item)
    return matching, non_matching


def group_by(lst: List[T], key_func: Callable[[T], K]) -> dict:
    """Group elements of a list into a dict by key function.

    Args:
        lst: The list to group.
        key_func: A function that extracts a grouping key from each element.

    Returns:
        A dict mapping each key to the list of elements that produced it,
        preserving insertion order of first occurrence.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> result = group_by(["a", "b", "c"], lambda s: len(s))
        >>> result == {1: ["a", "b", "c"]}
        True
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    result: dict = {}
    for item in lst:
        key = key_func(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result


def safe_get(lst: List[T], index: int, default: Optional[T] = None) -> Optional[T]:
    """Safely retrieve an element by index, returning a default on out-of-range.

    Args:
        lst: The list to index into.
        index: The index to retrieve. Supports negative indexing.
        default: The value to return if the index is out of range.
            Defaults to ``None``.

    Returns:
        The element at ``index``, or ``default`` if the index is out of range.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> safe_get([1, 2, 3], 0)
        1
        >>> safe_get([1, 2, 3], 10, default=0)
        0
        >>> safe_get([1, 2, 3], -1)
        3
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    try:
        return lst[index]
    except IndexError:
        return default


def find(lst: List[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Return the first element in the list that satisfies the predicate.

    Args:
        lst: The list to search.
        predicate: A function that returns ``True`` for the desired element.

    Returns:
        The first matching element, or ``None`` if no element matches.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> find([1, 2, 3], lambda x: x > 2)
        3
        >>> find([1, 2, 3], lambda x: x > 5)

    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    for item in lst:
        if predicate(item):
            return item
    return None


def drop(lst: List[T], n: int) -> List[T]:
    """Drop the first ``n`` elements from a list and return the rest.

    Args:
        lst: The list to truncate.
        n: The number of elements to drop from the front.

    Returns:
        A new list with the first ``n`` elements removed.
        If ``n`` exceeds the list length, returns an empty list.

    Raises:
        TypeError: If ``lst`` is not a list or ``n`` is not an integer.
        ValueError: If ``n`` is negative.

    Examples:
        >>> drop([1, 2, 3, 4, 5], 2)
        [3, 4, 5]
        >>> drop([1, 2, 3], 5)
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return lst[n:]


def take(lst: List[T], n: int) -> List[T]:
    """Take the first ``n`` elements from a list and return them.

    Args:
        lst: The list to take elements from.
        n: The number of elements to take from the front.

    Returns:
        A new list containing the first ``n`` elements.
        If ``n`` exceeds the list length, returns the whole list.

    Raises:
        TypeError: If ``lst`` is not a list or ``n`` is not an integer.
        ValueError: If ``n`` is negative.

    Examples:
        >>> take([1, 2, 3, 4, 5], 3)
        [1, 2, 3]
        >>> take([1, 2, 3], 10)
        [1, 2, 3]
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    return lst[:n]


def intersperse(lst: List[T], separator: T) -> List[T]:
    """Insert a separator between each pair of adjacent elements in a list.

    Args:
        lst: The list to intersperse.
        separator: The value to insert between each element.

    Returns:
        A new list with the separator inserted between every pair of
        adjacent elements. Returns an empty list if ``lst`` is empty.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> intersperse([1, 2, 3], 0)
        [1, 0, 2, 0, 3]
        >>> intersperse(["a", "b"], "-")
        ['a', '-', 'b']
        >>> intersperse([], "-")
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not lst:
        return []
    result: List[T] = [lst[0]]
    for item in lst[1:]:
        result.append(separator)
        result.append(item)
    return result


def chunks(lst: List[T], size: int) -> List[List[T]]:
    """Split a list into consecutive chunks of a given size.

    Args:
        lst: The list to split into chunks.
        size: The maximum size of each chunk (must be a positive integer).

    Returns:
        A list of chunks. The last chunk may be shorter than ``size`` if
        the list length is not divisible by ``size``. Returns an empty list
        if ``lst`` is empty.

    Raises:
        TypeError: If ``lst`` is not a list or ``size`` is not an integer
            (bool is rejected).
        ValueError: If ``size`` is not positive.

    Examples:
        >>> chunks([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunks([1, 2, 3], 1)
        [[1], [2], [3]]
        >>> chunks([], 3)
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an integer")
    if size < 1:
        raise ValueError("size must be positive")
    result: List[List[T]] = []
    for i in range(0, len(lst), size):
        result.append(lst[i : i + size])
    return result
