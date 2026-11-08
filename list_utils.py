"""Advanced list utility functions for common manipulation tasks."""

from typing import Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")
K = TypeVar("K")

__all__ = [
    "K",
    "T",
    "chunks",
    "contains",
    "count_duplicates",
    "drop",
    "find",
    "find_index",
    "find_last",
    "find_last_index",
    "first_or_default",
    "flatten",
    "group_by",
    "has_duplicates",
    "intersperse",
    "is_empty",
    "is_sorted",
    "last_or_default",
    "partition",
    "safe_get",
    "take",
    "unique_preserve_order",
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
    """Find the first element in a list satisfying a predicate.

    Args:
        lst: The list to search.
        predicate: A function that returns True for the desired element.

    Returns:
        The first matching element, or None if no match is found.

    Raises:
        TypeError: If lst is not a list.

    Examples:
        >>> find([1, 2, 3, 4], lambda x: x > 2)
        3
        >>> find([1, 2, 3], lambda x: x > 10) is None
        True
    """
    if not isinstance(lst, list):
        raise TypeError(f"Expected a list, got {type(lst).__name__}")
    for item in lst:
        if predicate(item):
            return item
    return None


def find_index(lst: List[T], predicate: Callable[[T], bool]) -> Optional[int]:
    """Find the index of the first element in a list satisfying a predicate.

    Args:
        lst: The list to search.
        predicate: A function that returns True for the desired element.

    Returns:
        The index of the first matching element, or None if no match is found.

    Raises:
        TypeError: If lst is not a list.

    Examples:
        >>> find_index([10, 20, 30], lambda x: x == 20)
        1
        >>> find_index([1, 2, 3], lambda x: x > 10) is None
        True
    """
    if not isinstance(lst, list):
        raise TypeError(f"Expected a list, got {type(lst).__name__}")
    for i, item in enumerate(lst):
        if predicate(item):
            return i
    return None


def find_all(lst: List[T], predicate: Callable[[T], bool]) -> List[T]:
    """Return all elements in a list satisfying a predicate.

    Matching elements are returned in the order they appear. An empty list
    (or no matches) yields an empty list.

    Args:
        lst: The list to search.
        predicate: A function that returns True for desired elements.

    Returns:
        A list of all matching elements.

    Raises:
        TypeError: If lst is not a list or predicate is not callable.

    Examples:
        >>> find_all([1, 2, 3, 4], lambda x: x > 2)
        [3, 4]
        >>> find_all([1, 2, 3], lambda x: x > 10)
        []
        >>> find_all([], lambda x: True)
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return [item for item in lst if predicate(item)]


def find_all_indices(lst: List[T], predicate: Callable[[T], bool]) -> List[int]:
    """Return the indices of all elements in a list satisfying a predicate.

    Indices are returned in ascending order. An empty list (or no
    matches) yields an empty list.

    Args:
        lst: The list to search.
        predicate: A function that returns True for desired elements.

    Returns:
        A list of 0-based indices of all matching elements.

    Raises:
        TypeError: If lst is not a list or predicate is not callable.

    Examples:
        >>> find_all_indices([1, 2, 3, 4], lambda x: x > 2)
        [2, 3]
        >>> find_all_indices([1, 2, 3], lambda x: x > 10)
        []
        >>> find_all_indices([], lambda x: True)
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return [i for i, item in enumerate(lst) if predicate(item)]


def find_last(lst: List[T], predicate: Callable[[T], bool]) -> Optional[T]:
    """Return the last element in a list satisfying a predicate.

    Args:
        lst: The list to search.
        predicate: A function that returns True for the desired element.

    Returns:
        The last matching element, or None if no element matches.

    Raises:
        TypeError: If lst is not a list.

    Examples:
        >>> find_last([1, 2, 3, 4], lambda x: x > 2)
        4
        >>> find_last([1, 2, 3], lambda x: x > 10)
        >>> find_last([1, 2, 3], lambda x: x % 2 == 0)
        2
        >>> find_last([], lambda x: True)
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    for item in reversed(lst):
        if predicate(item):
            return item
    return None


def find_last_index(lst: List[T], predicate: Callable[[T], bool]) -> Optional[int]:
    """Find the index of the last element in a list satisfying a predicate.

    Args:
        lst: The list to search.
        predicate: A function that returns True for the desired element.

    Returns:
        The index of the last matching element, or None if no match is found.

    Raises:
        TypeError: If lst is not a list.

    Examples:
        >>> find_last_index([1, 2, 3, 2], lambda x: x == 2)
        3
        >>> find_last_index([1, 2, 3], lambda x: x > 10) is None
        True
    """
    if not isinstance(lst, list):
        raise TypeError(f"Expected a list, got {type(lst).__name__}")
    for i in range(len(lst) - 1, -1, -1):
        if predicate(lst[i]):
            return i
    return None


def contains(lst: List[T], element: T) -> bool:
    """Return ``True`` when *element* is present in *lst*.

    Uses equality comparison and short-circuits on the first match.

    Args:
        lst: The list to search.
        element: The value to look for.

    Returns:
        ``True`` if *element* equals any item in *lst*, ``False`` otherwise.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> contains([1, 2, 3, 4], 3)
        True
        >>> contains([1, 2, 3], 5)
        False
        >>> contains([], 1)
        False
        >>> contains(["a", "b", "c"], "b")
        True
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    return element in lst


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


def flatten(lst: List[List[T]]) -> List[T]:
    """Flatten a list of lists one level deep.

    Args:
        lst: The list of lists to flatten.

    Returns:
        A single list containing every element of the inner lists, in order.

    Raises:
        TypeError: If ``lst`` is not a list or if any element of ``lst`` is
            not a list.

    Examples:
        >>> flatten([[1, 2], [3, 4], [5]])
        [1, 2, 3, 4, 5]
        >>> flatten([[], [1], [2, 3]])
        [1, 2, 3]
        >>> flatten([["a", "b"], ["c"]])
        ['a', 'b', 'c']
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    result: List[T] = []
    for item in lst:
        if not isinstance(item, list):
            raise TypeError("all elements of lst must be lists")
        result.extend(item)
    return result


def unique_preserve_order(lst: List[T]) -> List[T]:
    """Return a new list with duplicates removed while preserving order.

    Args:
        lst: The list to deduplicate.

    Returns:
        A new list containing unique elements in their first occurrence order.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> unique_preserve_order([1, 2, 2, 3, 1])
        [1, 2, 3]
        >>> unique_preserve_order(["a", "b", "a"])
        ['a', 'b']
        >>> unique_preserve_order([])
        []
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    seen = set()
    result: List[T] = []
    for item in lst:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def is_empty(lst: List[T]) -> bool:
    """Return ``True`` when *lst* has no elements.

    Args:
        lst: The list to check.

    Returns:
        ``True`` if *lst* is empty, ``False`` otherwise.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> is_empty([])
        True
        >>> is_empty([1, 2])
        False
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    return len(lst) == 0


def count_duplicates(lst: List[T]) -> int:
    """Return the number of duplicate (extra) elements in *lst*.

    The result is ``len(lst)`` minus the number of distinct elements, so a
    list with no duplicates returns ``0``. Elements are compared by equality;
    hashable elements use a set for efficiency, and unhashable elements fall
    back to linear membership checks.

    Args:
        lst: The list to inspect.

    Returns:
        The number of elements beyond their first occurrence.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> count_duplicates([1, 2, 2, 3])
        1
        >>> count_duplicates([1, 2, 3])
        0
        >>> count_duplicates([])
        0
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    seen: set = set()
    unhashable: List[T] = []
    unique = 0
    for item in lst:
        try:
            if item in seen:
                continue
            seen.add(item)
            unique += 1
        except TypeError:
            if item in unhashable:
                continue
            unhashable.append(item)
            unique += 1
    return len(lst) - unique


def has_duplicates(lst: List[T]) -> bool:
    """Return ``True`` when *lst* contains any duplicate element.

    Elements are compared by equality; hashable elements use a set for
    efficiency. Unhashable elements fall back to linear membership checks.

    Args:
        lst: The list to inspect.

    Returns:
        ``True`` if any element appears more than once, ``False`` otherwise.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> has_duplicates([1, 2, 2, 3])
        True
        >>> has_duplicates([1, 2, 3])
        False
        >>> has_duplicates([])
        False
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    return count_duplicates(lst) > 0


def is_sorted(lst: List[T], reverse: bool = False) -> bool:
    """Return ``True`` when *lst* is sorted in non-descending order.

    Args:
        lst: The list to check.
        reverse: If ``True``, check for non-ascending (descending) order.

    Returns:
        ``True`` if *lst* is sorted in the requested direction, ``False``
        otherwise. An empty list or a single-element list is considered sorted.

    Raises:
        TypeError: If ``lst`` is not a list or ``reverse`` is not a bool.

    Examples:
        >>> is_sorted([1, 2, 3])
        True
        >>> is_sorted([3, 2, 1])
        False
        >>> is_sorted([3, 2, 1], reverse=True)
        True
        >>> is_sorted([])
        True
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    if not isinstance(reverse, bool):
        raise TypeError("reverse must be a bool")
    if len(lst) < 2:
        return True
    if reverse:
        return all(lst[i] >= lst[i + 1] for i in range(len(lst) - 1))
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


def first_or_default(lst: List[T], default: Optional[T] = None) -> Optional[T]:
    """Return the first element of a list, or ``default`` if empty.

    Args:
        lst: The list to inspect.
        default: The value to return when ``lst`` is empty.

    Returns:
        The first element of ``lst``, or ``default`` when empty.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> first_or_default([1, 2, 3])
        1
        >>> first_or_default([], 0)
        0
        >>> first_or_default([])
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    return lst[0] if lst else default


def last_or_default(lst: List[T], default: Optional[T] = None) -> Optional[T]:
    """Return the last element of a list, or ``default`` if empty.

    Args:
        lst: The list to inspect.
        default: The value to return when ``lst`` is empty.

    Returns:
        The last element of ``lst``, or ``default`` when empty.

    Raises:
        TypeError: If ``lst`` is not a list.

    Examples:
        >>> last_or_default([1, 2, 3])
        3
        >>> last_or_default([], 0)
        0
        >>> last_or_default([])
    """
    if not isinstance(lst, list):
        raise TypeError("lst must be a list")
    return lst[-1] if lst else default
