"""itertools utilities for common iteration patterns.

Provides convenient wrappers around the standard library ``itertools``
module with input validation.
"""

from itertools import (
    accumulate,
    chain,
    combinations,
    combinations_with_replacement,
    compress,
    count,
    cycle,
    dropwhile,
    filterfalse,
    groupby,
    islice,
    pairwise,
    permutations,
    product,
    repeat,
    starmap,
    takewhile,
    tee,
    zip_longest,
)
try:
    from itertools import batched
except ImportError:
    batched = None  # type: ignore[assignment]
from typing import Any, Callable, Iterable, List, Optional, Tuple


def _ensure_iterable(value: Any, name: str = "iterable") -> None:
    if not hasattr(value, "__iter__"):
        raise TypeError(f"{name} must be iterable, got {type(value).__name__}")


def chain_iterables(*iterables: Iterable[Any]) -> List[Any]:
    """Chain multiple iterables into one list."""
    for it in iterables:
        _ensure_iterable(it)
    return list(chain(*iterables))


def flatten_once(iterable: Iterable[Iterable[Any]]) -> List[Any]:
    """Flatten one level of nesting."""
    _ensure_iterable(iterable)
    return list(chain.from_iterable(iterable))


def take_while_pred(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> List[Any]:
    """Take elements while predicate is truthy."""
    _ensure_iterable(iterable)
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return list(takewhile(predicate, iterable))


def chunk_iterable(iterable: Iterable[Any], size: int) -> List[List[Any]]:
    """Split an iterable into chunks of the given size."""
    _ensure_iterable(iterable)
    if not isinstance(size, int):
        raise TypeError("size must be an int")
    if size <= 0:
        raise ValueError("size must be positive")
    it = iter(iterable)
    result: List[List[Any]] = []
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        result.append(chunk)
    return result


def product_of(iterables: Iterable[Iterable[Any]]) -> List[Tuple[Any, ...]]:
    """Compute the Cartesian product of the given iterables."""
    _ensure_iterable(iterables)
    lists = [list(x) for x in iterables]
    for original in iterables:
        _ensure_iterable(original)
    return list(product(*lists))


def combinations_of(iterable: Iterable[Any], r: int) -> List[Tuple[Any, ...]]:
    """Return all r-combinations of the input iterable."""
    _ensure_iterable(iterable)
    if not isinstance(r, int):
        raise TypeError("r must be an int")
    if r < 0:
        raise ValueError("r must be non-negative")
    return list(combinations(iterable, r))


def combinations_with_replacement_of(iterable: Iterable[Any], r: int) -> List[Tuple[Any, ...]]:
    """Return all r-combinations with replacement of the input iterable."""
    _ensure_iterable(iterable)
    if not isinstance(r, int):
        raise TypeError("r must be an int")
    if r < 0:
        raise ValueError("r must be non-negative")
    return list(combinations_with_replacement(iterable, r))


def permutations_of(iterable: Iterable[Any], r: Optional[int] = None) -> List[Tuple[Any, ...]]:
    """Return all r-permutations of the input iterable."""
    _ensure_iterable(iterable)
    if r is None:
        return list(permutations(iterable))
    if not isinstance(r, int):
        raise TypeError("r must be an int")
    if r < 0:
        raise ValueError("r must be non-negative")
    return list(permutations(iterable, r))


def group_by_key(iterable: Iterable[Any], key: Callable[[Any], Any]) -> dict:
    """Group consecutive items by key, returning {key: [...]} dict."""
    _ensure_iterable(iterable)
    if not callable(key):
        raise TypeError("key must be callable")
    result: dict = {}
    for k, g in groupby(iterable, key=key):
        result.setdefault(k, []).extend(g)
    return result


def accumulate_values(
    iterable: Iterable[Any], func: Optional[Callable[[Any, Any], Any]] = None
) -> List[Any]:
    """Running accumulation of the input iterable."""
    _ensure_iterable(iterable)
    if func is None:
        return list(accumulate(iterable))
    if not callable(func):
        raise TypeError("func must be callable")
    return list(accumulate(iterable, func))


def repeat_value(value: Any, times: Optional[int] = None) -> List[Any]:
    """Repeat a value; if times is None, repeat 3 times by default."""
    if times is None:
        times = 3
    if not isinstance(times, int):
        raise TypeError("times must be an int")
    if times < 0:
        raise ValueError("times must be non-negative")
    return list(repeat(value, times))


def cycle_take(iterable: Iterable[Any], n: int) -> List[Any]:
    """Take n items from an infinitely cycled iterable."""
    _ensure_iterable(iterable)
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    return list(islice(cycle(iterable), n))


def compress_iterable(data: Iterable[Any], selectors: Iterable[Any]) -> List[Any]:
    """Filter data by selectors using itertools.compress."""
    _ensure_iterable(data, "data")
    _ensure_iterable(selectors, "selectors")
    return list(compress(data, selectors))


def filter_false_iterable(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> List[Any]:
    """Filter elements where predicate returns false."""
    _ensure_iterable(iterable, "iterable")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return list(filterfalse(predicate, iterable))


def pairwise_iterable(iterable: Iterable[Any]) -> List[Tuple[Any, Any]]:
    """Return successive overlapping pairs from the input iterable."""
    _ensure_iterable(iterable, "iterable")
    return list(pairwise(iterable))


def partition(
    iterable: Iterable[Any], predicate: Callable[[Any], bool]
) -> tuple[List[Any], List[Any]]:
    """Split an iterable into two lists: truthy and falsy items.

    Items for which ``predicate`` is truthy go into the first list, the rest
    into the second. Order is preserved within each list.

    Args:
        iterable: The iterable to split.
        predicate: A callable returning a truthy/falsy value per item.

    Returns:
        A ``(truthy, falsy)`` tuple of lists.

    Raises:
        TypeError: If ``iterable`` is not iterable or ``predicate`` is not
            callable.

    Examples:
        >>> partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        ([2, 4], [1, 3, 5])
        >>> partition([], bool)
        ([], [])
    """
    _ensure_iterable(iterable)
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    truthy: List[Any] = []
    falsy: List[Any] = []
    for item in iterable:
        if predicate(item):
            truthy.append(item)
        else:
            falsy.append(item)
    return truthy, falsy


def zip_longest_iterables(
    *iterables: Iterable[Any], fillvalue: Any = None
) -> List[Tuple[Any, ...]]:
    """Zip multiple iterables, stopping at the longest, filling missing values.

    Args:
        *iterables: The iterables to zip together.
        fillvalue: The value used when an iterable is exhausted before the
            others (defaults to ``None``).

    Returns:
        A list of tuples, one per position up to the length of the longest
        iterable, with *fillvalue* substituting for exhausted iterables.

    Raises:
        TypeError: If any argument is not iterable.

    Examples:
        >>> zip_longest_iterables([1, 2, 3], ["a", "b"])
        [(1, 'a'), (2, 'b'), (3, None)]
        >>> zip_longest_iterables([1, 2], [3, 4], fillvalue=-1)
        [(1, 3), (2, 4)]
        >>> zip_longest_iterables()
        []
    """
    if not iterables:
        return []
    for it in iterables:
        _ensure_iterable(it)
    return list(zip_longest(*iterables, fillvalue=fillvalue))


def zip_strict_iterables(*iterables: Iterable[Any]) -> List[Tuple[Any, ...]]:
    """Zip multiple iterables, raising if they are not all the same length.

    Args:
        *iterables: The iterables to zip together.

    Returns:
        A list of tuples, one per position up to the length of the shortest
        iterable.

    Raises:
        TypeError: If any argument is not iterable.
        ValueError: If the iterables are not all the same length.

    Examples:
        >>> zip_strict_iterables([1, 2, 3], ["a", "b", "c"])
        [(1, 'a'), (2, 'b'), (3, 'c')]
        >>> zip_strict_iterables()
        []
    """
    if not iterables:
        return []
    for it in iterables:
        _ensure_iterable(it)
    zipped = list(zip(*iterables))
    lengths = [len(list(it)) for it in iterables]
    if len(set(lengths)) > 1:
        raise ValueError("iterables must all be the same length")
    return zipped


__all__ = [
    "chain_iterables",
    "flatten_once",
    "take_while_pred",
    "chunk_iterable",
    "product_of",
    "combinations_of",
    "combinations_with_replacement_of",
    "permutations_of",
    "group_by_key",
    "accumulate_values",
    "repeat_value",
    "cycle_take",
    "compress_iterable",
    "filter_false_iterable",
    "pairwise_iterable",
    "partition",
    "zip_longest_iterables",
    "zip_strict_iterables",
    "batched_iterable",
    "take_while_pred",
    "drop_while_pred",
    "tee_iterables",
    "starmap_iterable",
    "count_from",
    "islice_iterable",
]


def batched_iterable(iterable: Iterable[Any], n: int) -> List[Tuple[Any, ...]]:
    """Batch data into tuples of length n (Python 3.12+ itertools.batched)."""
    _ensure_iterable(iterable, "iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 1:
        raise ValueError("n must be at least one")
    if batched is not None:
        return list(batched(iterable, n))
    # Fallback for older Python
    it = iter(iterable)
    result = []
    while True:
        batch = []
        for _ in range(n):
            try:
                batch.append(next(it))
            except StopIteration:
                break
        if not batch:
            break
        result.append(tuple(batch))
    return result


def drop_while_pred(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> List[Any]:
    """Drop elements from the start while predicate holds, then keep the rest.

    Args:
        iterable: The iterable to process.
        predicate: A callable returning True for elements to drop.

    Returns:
        A list of the remaining elements.

    Raises:
        TypeError: If iterable is not iterable or predicate is not callable.

    Examples:
        >>> drop_while_pred([1, 2, 3, 4], lambda x: x < 3)
        [3, 4]
        >>> drop_while_pred([5, 6, 7], lambda x: x < 3)
        [5, 6, 7]
        >>> drop_while_pred([], lambda x: True)
        []
    """
    _ensure_iterable(iterable, "iterable")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    return list(dropwhile(predicate, iterable))


def tee_iterables(iterable: Iterable[Any], n: int = 2) -> List[List[Any]]:
    """Split an iterable into n independent iterators/lists."""
    _ensure_iterable(iterable, "iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    tees = tee(iterable, n)
    return [list(t) for t in tees]


def starmap_iterable(function: Callable[..., Any], iterable: Iterable[Iterable[Any]]) -> List[Any]:
    """Apply function to arguments unpacked from iterable."""
    if not callable(function):
        raise TypeError("function must be callable")
    _ensure_iterable(iterable, "iterable")
    return list(starmap(function, iterable))


def count_from(start: int = 0, step: int = 1) -> List[Any]:
    """Count infinitely from start with step; return first 1000 as list for safety."""
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if not isinstance(step, int) or isinstance(step, bool):
        raise TypeError("step must be an int")
    return list(islice(count(start, step), 1000))


def islice_iterable(iterable: Iterable[Any], *args: Any) -> List[Any]:
    """Slice an iterable."""
    _ensure_iterable(iterable, "iterable")
    return list(islice(iterable, *args))
