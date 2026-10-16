"""Collection utility functions for working with iterables and data structures."""

from __future__ import annotations

from collections import Counter, deque
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

__all__: List[str] = [
    "chunk",
    "flatten",
    "deep_flatten",
    "windowed",
    "uniq",
    "uniq_by",
    "frequency",
    "most_common",
    "least_common",
    "merge_dicts",
    "to_deque",
    "pluck",
    "compact",
    "partition_by",
]


def chunk(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Split an iterable into chunks of a specified size.

    Args:
        iterable: The iterable to chunk.
        size: The maximum size of each chunk.

    Yields:
        Lists containing up to ``size`` elements each.

    Raises:
        TypeError: If ``size`` is not an integer.
        ValueError: If ``size`` is less than or equal to 0.

    Examples:
        >>> list(chunk([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an integer")
    if size <= 0:
        raise ValueError("size must be greater than 0")

    it = iter(iterable)
    while True:
        batch: List[T] = []
        try:
            for _ in range(size):
                batch.append(next(it))
        except StopIteration:
            if batch:
                yield batch
            break
        yield batch


def flatten(iterable: Iterable[Union[T, Iterable[T]]]) -> List[T]:
    """Flatten a one-level nested iterable.

    Args:
        iterable: The iterable to flatten.

    Returns:
        A flat list containing all top-level elements of nested iterables.

    Examples:
        >>> flatten([1, [2, 3], [4], 5])
        [1, 2, 3, 4, 5]
    """
    result: List[T] = []
    for item in iterable:
        if isinstance(item, (list, tuple, set)):
            result.extend(item)  # type: ignore[arg-type]
        else:
            result.append(item)  # type: ignore[arg-type]
    return result


def deep_flatten(iterable: Iterable[Any]) -> List[Any]:
    """Recursively flatten a nested iterable.

    Args:
        iterable: The iterable to deeply flatten.

    Returns:
        A flat list containing all non-iterable elements.

    Examples:
        >>> deep_flatten([1, [2, [3, 4]], 5])
        [1, 2, 3, 4, 5]
    """
    result: List[Any] = []
    for item in iterable:
        if isinstance(item, (list, tuple, set)):
            result.extend(deep_flatten(item))  # type: ignore[arg-type]
        else:
            result.append(item)
    return result


def windowed(iterable: Iterable[T], size: int) -> Iterator[Tuple[T, ...]]:
    """Create sliding windows over an iterable.

    Args:
        iterable: The iterable to window.
        size: The size of each window.

    Yields:
        Tuples containing consecutive elements in each window.

    Raises:
        TypeError: If ``size`` is not an integer.
        ValueError: If ``size`` is less than or equal to 0.

    Examples:
        >>> list(windowed([1, 2, 3, 4], 2))
        [(1, 2), (2, 3), (3, 4)]
    """
    if not isinstance(size, int) or isinstance(size, bool):
        raise TypeError("size must be an integer")
    if size <= 0:
        raise ValueError("size must be greater than 0")

    it = iter(iterable)
    win: Deque[T] = deque()
    for item in it:
        win.append(item)
        if len(win) == size:
            yield tuple(win)
            win.popleft()


def uniq(iterable: Iterable[T]) -> List[T]:
    """Remove duplicate elements while preserving order.

    Args:
        iterable: The iterable to deduplicate.

    Returns:
        A list with duplicate elements removed, preserving first occurrence order.

    Examples:
        >>> uniq([1, 2, 2, 3, 1])
        [1, 2, 3]
    """
    seen: Set[T] = set()
    result: List[T] = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def uniq_by(iterable: Iterable[T], key_func: Callable[[T], Any]) -> List[T]:
    """Remove duplicate elements based on a key function while preserving order.

    Args:
        iterable: The iterable to deduplicate.
        key_func: Function to compute the deduplication key.

    Returns:
        A list with duplicates (by key) removed, preserving first occurrence order.

    Examples:
        >>> uniq_by([{'id': 1}, {'id': 2}, {'id': 1}], lambda x: x['id'])
        [{'id': 1}, {'id': 2}]
    """
    seen: Set[Any] = set()
    result: List[T] = []
    for item in iterable:
        key = key_func(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def frequency(iterable: Iterable[T]) -> Dict[T, int]:
    """Count frequency of each element in an iterable.

    Args:
        iterable: The iterable to analyze.

    Returns:
        A dictionary mapping each element to its count.

    Examples:
        >>> freq = frequency([1, 2, 2, 3])
        >>> freq[2]
        2
    """
    return dict(Counter(iterable))


def most_common(iterable: Iterable[T], n: Optional[int] = None) -> List[Tuple[T, int]]:
    """Return the most common elements from an iterable.

    Args:
        iterable: The iterable to analyze.
        n: Number of top elements to return (None returns all, sorted desc).

    Returns:
        List of (element, count) tuples sorted by count descending.

    Examples:
        >>> most_common([1, 2, 2, 3, 3, 3])
        [(3, 3), (2, 2), (1, 1)]
    """
    counter = Counter(iterable)
    return counter.most_common(n)  # type: ignore[return-value]


def least_common(iterable: Iterable[T], n: Optional[int] = None) -> List[Tuple[T, int]]:
    """Return the least common elements from an iterable.

    Args:
        iterable: The iterable to analyze.
        n: Number of bottom elements to return (None returns all).

    Returns:
        List of (element, count) tuples sorted by count ascending.

    Examples:
        >>> least_common([1, 2, 2, 3, 3, 3], n=1)
        [(1, 1)]
    """
    counter = Counter(iterable)
    items = counter.most_common()  # all sorted desc
    items_reversed = list(reversed(items))
    if n is None:
        return items_reversed
    return items_reversed[:n]


def merge_dicts(*dicts: Dict[K, V]) -> Dict[K, V]:
    """Merge multiple dictionaries, with later dicts taking precedence.

    Args:
        *dicts: Dictionaries to merge.

    Returns:
        A new merged dictionary.

    Examples:
        >>> merge_dicts({'a': 1}, {'b': 2}, {'a': 3})
        {'a': 3, 'b': 2}
    """
    result: Dict[K, V] = {}
    for d in dicts:
        if isinstance(d, dict):
            result.update(d)
    return result


def to_deque(iterable: Iterable[T], maxlen: Optional[int] = None) -> Deque[T]:
    """Convert an iterable to a deque.

    Args:
        iterable: The iterable to convert.
        maxlen: Maximum length of deque (optional).

    Returns:
        A deque containing all elements from iterable.

    Examples:
        >>> d = to_deque([1, 2, 3])
        >>> len(d)
        3
    """
    return deque(iterable, maxlen=maxlen) if maxlen is not None else deque(iterable)


def pluck(iterable: Iterable[Dict[K, Any]], key: K) -> List[Any]:
    """Extract values for a specific key from a list of dictionaries.

    Args:
        iterable: Iterable of dictionaries.
        key: The key to extract values for.

    Returns:
        List of values for the key (skips missing keys).

    Examples:
        >>> pluck([{'a': 1}, {'a': 2}, {'b': 3}], 'a')
        [1, 2]
    """
    result: List[Any] = []
    for item in iterable:
        if isinstance(item, dict) and key in item:
            result.append(item[key])
    return result


def compact(iterable: Iterable[T]) -> List[T]:
    """Remove falsy values from an iterable.

    Removes values that are Falsey: False, None, 0, "", [], {}, set().

    Args:
        iterable: The iterable to compact.

    Returns:
        List with falsy values removed.

    Examples:
        >>> compact([0, 1, False, 2, '', 3, None])
        [1, 2, 3]
    """
    result: List[T] = []
    for item in iterable:
        if item:
            result.append(item)
    return result


def partition_by(iterable: Iterable[T], key_func: Callable[[T], Any]) -> List[List[T]]:
    """Partition an iterable into groups with consecutive equal keys.

    Args:
        iterable: The iterable to partition.
        key_func: Function to compute the partition key.

    Returns:
        List of lists, where each inner list contains consecutive elements
        with the same key.

    Examples:
        >>> list_of_groups = partition_by([1, 1, 2, 2, 3], lambda x: x)
        >>> list_of_groups
        [[1, 1], [2, 2], [3]]
    """
    result: List[List[T]] = []
    it = iter(iterable)
    try:
        first = next(it)
        current_key = key_func(first)
        current_group: List[T] = [first]
    except StopIteration:
        return result

    for item in it:
        key = key_func(item)
        if key == current_key:
            current_group.append(item)
        else:
            result.append(current_group)
            current_key = key
            current_group = [item]
    result.append(current_group)
    return result
