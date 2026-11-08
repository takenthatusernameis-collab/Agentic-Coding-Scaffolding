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
    from itertools import batched  # type: ignore[attr-defined]
except ImportError:
    batched = None  # type: ignore[assignment]
try:
    from itertools import pairwise as _pairwise  # type: ignore[attr-defined]
except ImportError:
    _pairwise = None  # type: ignore[assignment,misc]
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
    """Return successive overlapping pairs taken from the input iterable."""
    _ensure_iterable(iterable)
    return list(pairwise(iterable))


def sliding_window(iterable: Iterable[Any], n: int) -> List[Tuple[Any, ...]]:
    """Return successive overlapping windows of length n from the input iterable."""
    _ensure_iterable(iterable)
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    it = iter(iterable)
    window = list(islice(it, n))
    if len(window) < n:
        return []
    result: List[Tuple[Any, ...]] = [tuple(window)]
    for element in it:
        window = window[1:] + [element]
        result.append(tuple(window))
    return result


def window(iterable: Iterable[Any], n: int) -> List[Tuple[Any, ...]]:
    """Alias for sliding_window."""
    return sliding_window(iterable, n)


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


def is_empty_iterable(iterable: Iterable[Any]) -> bool:
    """Return ``True`` when *iterable* contains no elements.

    Unlike ``len(iterable)``, this works for any iterable — including
    generators and other one-shot iterators — by consuming elements only
    until the first item is seen.

    Args:
        iterable: The iterable to inspect.

    Returns:
        ``True`` when the iterable yields no items, ``False`` otherwise.

    Raises:
        TypeError: If *iterable* is not iterable.

    Examples:
        >>> is_empty_iterable([])
        True
        >>> is_empty_iterable([1, 2, 3])
        False
        >>> is_empty_iterable(iter(()))
        True
        >>> is_empty_iterable(x for x in [])
        True
    """
    _ensure_iterable(iterable, "iterable")
    for element in iterable:
        return False
    return True


def first_or_default(iterable: Iterable[Any], default: Any = None) -> Any:
    """Return the first element of *iterable*, or *default* if it is empty.

    Works for any iterable, including one-shot generators, by consuming only
    until the first element is seen.

    Args:
        iterable: The iterable to inspect.
        default: Value returned when the iterable is empty.

    Returns:
        The first element of *iterable*, or *default*.

    Raises:
        TypeError: If *iterable* is not iterable.

    Examples:
        >>> first_or_default([1, 2, 3])
        1
        >>> first_or_default([])
        >>> first_or_default([], default="none")
        'none'
        >>> first_or_default(x for x in range(5))
        0
    """
    _ensure_iterable(iterable, "iterable")
    for element in iterable:
        return element
    return default


def last_or_default(iterable: Iterable[Any], default: Any = None) -> Any:
    """Return the last element of *iterable*, or *default* if it is empty.

    Consumes the iterable fully to determine the last element.

    Args:
        iterable: The iterable to inspect.
        default: Value returned when the iterable is empty.

    Returns:
        The last element of *iterable*, or *default*.

    Raises:
        TypeError: If *iterable* is not iterable.

    Examples:
        >>> last_or_default([1, 2, 3])
        3
        >>> last_or_default([])
        >>> last_or_default([], default="none")
        'none'
        >>> last_or_default(x for x in range(5))
        4
    """
    _ensure_iterable(iterable, "iterable")
    result = default
    found = False
    for element in iterable:
        result = element
        found = True
    return result if found else default


def nth_or_default(iterable: Iterable[Any], n: int, default: Any = None) -> Any:
    """Return the element at index *n* of *iterable*, or *default* if out of range.

    Works for any iterable — including one-shot generators — by consuming
    elements only until the *n*-th (0-indexed) item is seen.

    Args:
        iterable: The iterable to inspect.
        n: The 0-based index of the element to retrieve.
        default: Value returned when *n* is out of range.

    Returns:
        The element at index *n*, or *default* when the iterable is too short.

    Raises:
        TypeError: If *iterable* is not iterable or *n* is not an int.

    Examples:
        >>> nth_or_default([1, 2, 3], 1)
        2
        >>> nth_or_default([1, 2, 3], 5)
        >>> nth_or_default([1, 2, 3], 5, default="none")
        'none'
        >>> nth_or_default((x for x in range(5)), 3)
        3
    """
    _ensure_iterable(iterable, "iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be a non-negative index")
    for index, element in enumerate(iterable):
        if index == n:
            return element
    return default


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


def unique_everseen(iterable: Iterable[Any], key: Callable[[Any], Any] | None = None) -> List[Any]:
    """List unique elements, preserving order. Remember all seen elements."""
    _ensure_iterable(iterable, "iterable")
    if key is not None and not callable(key):
        raise TypeError("key must be callable")
    seen: set[Any] = set()
    seen_add = seen.add
    result: List[Any] = []
    if key is None:
        for element in iterable:
            if element not in seen:
                seen_add(element)
                result.append(element)
        return result
    for element in iterable:
        k = key(element)
        if k not in seen:
            seen_add(k)
            result.append(element)
    return result


def unique_justseen(iterable: Iterable[Any], key: Callable[[Any], Any] | None = None) -> List[Any]:
    """List unique elements, preserving order. Only remember the last seen element."""
    _ensure_iterable(iterable, "iterable")
    if key is not None and not callable(key):
        raise TypeError("key must be callable")
    result: List[Any] = []
    last = object()
    for element in iterable:
        k = key(element) if key is not None else element
        if k == last:
            continue
        result.append(element)
        last = k
    return result


def grouper(iterable: Iterable[Any], n: int, fillvalue: Any = None) -> List[Tuple[Any, ...]]:
    """Collect data into fixed-length chunks or blocks.

    Each chunk contains at most *n* items drawn from *iterable*. When the
    iterable's length is not a multiple of *n*, the final chunk is padded
    with *fillvalue* (which defaults to ``None``) so every returned tuple
    has exactly *n* elements. This matches the classic ``itertools`` recipe
    ``zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)``.

    Args:
        iterable: The iterable to chunk.
        n: Positive chunk size.
        fillvalue: Value used to pad the final, short chunk.

    Returns:
        A list of tuples, each of length *n* (the last one padded when
        needed).

    Raises:
        TypeError: If *iterable* is not iterable or *n* is not an int.
        ValueError: If *n* is less than one.

    Examples:
        >>> grouper([1, 2, 3, 4, 5], 2)
        [(1, 2), (3, 4), (5, None)]
        >>> grouper([1, 2, 3, 4, 5], 2, fillvalue=-1)
        [(1, 2), (3, 4), (5, -1)]
        >>> grouper([1, 2, 3, 4], 2)
        [(1, 2), (3, 4)]
        >>> grouper([], 3)
        []
    """
    _ensure_iterable(iterable, "iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 1:
        raise ValueError("n must be at least one")
    args = [iter(iterable)] * n
    result: List[Tuple[Any, ...]] = []
    for chunk in zip_longest(*args, fillvalue=fillvalue):
        result.append(tuple(chunk))
    return result


def roundrobin(*iterables: Iterable[Any]) -> List[Any]:
    """Visit input iterables in a cycle until each is exhausted."""
    if not iterables:
        return []
    for it in iterables:
        _ensure_iterable(it)
    from collections import deque

    iterators = deque(iter(iterable) for iterable in iterables)
    result: List[Any] = []
    while iterators:
        it = iterators.popleft()
        try:
            value = next(it)
        except StopIteration:
            continue
        else:
            result.append(value)
            iterators.append(it)
    return result


def padnone(iterable: Iterable[Any]) -> Iterable[Any]:
    """Returns the sequence elements followed by None indefinitely."""
    return chain(iterable, repeat(None))


def ncycles(iterable: Iterable[Any], n: int) -> List[Any]:
    """Returns the sequence elements n times."""
    _ensure_iterable(iterable, "iterable")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    if n < 0:
        raise ValueError("n must be non-negative")
    return list(chain.from_iterable(repeat(list(iterable), n)))


def count_if(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> int:
    """Count items in *iterable* for which *predicate* is truthy.

    Args:
        iterable: The iterable to inspect.
        predicate: A callable returning a truthy/falsy value per item.

    Returns:
        The number of items where *predicate(item)* is truthy.

    Raises:
        TypeError: If *iterable* is not iterable or *predicate* is not callable.

    Examples:
        >>> count_if([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        2
        >>> count_if([], bool)
        0
        >>> count_if([0, 1, 2], bool)
        2
    """
    _ensure_iterable(iterable, "iterable")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    total = 0
    for item in iterable:
        if predicate(item):
            total += 1
    return total


def has_any(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> bool:
    """Return ``True`` if any item in *iterable* satisfies *predicate*.

    Short-circuits on the first match.

    Args:
        iterable: The iterable to inspect.
        predicate: A callable returning a truthy/falsy value per item.

    Returns:
        ``True`` when at least one item satisfies *predicate*, ``False``
        otherwise (including for an empty iterable).

    Raises:
        TypeError: If *iterable* is not iterable or *predicate* is not callable.

    Examples:
        >>> has_any([1, 2, 3], lambda x: x > 2)
        True
        >>> has_any([1, 2, 3], lambda x: x > 5)
        False
        >>> has_any([], bool)
        False
    """
    _ensure_iterable(iterable, "iterable")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    for item in iterable:
        if predicate(item):
            return True
    return False


def has_all(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> bool:
    _ensure_iterable(iterable, "iterable")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    for item in iterable:
        if not predicate(item):
            return False
    return True


def has_none(iterable: Iterable[Any], predicate: Callable[[Any], bool]) -> bool:
    _ensure_iterable(iterable, "iterable")
    if not callable(predicate):
        raise TypeError("predicate must be callable")
    for item in iterable:
        if predicate(item):
            return False
    return True


__all__ = [
    "_ensure_iterable",
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
    "drop_while_pred",
    "tee_iterables",
    "starmap_iterable",
    "count_from",
    "islice_iterable",
    "is_empty_iterable",
    "first_or_default",
    "last_or_default",
    "nth_or_default",
    "unique_everseen",
    "unique_justseen",
    "sliding_window",
    "window",
    "grouper",
    "roundrobin",
    "padnone",
    "ncycles",
    "count_if",
    "has_any",
    "has_all",
    "has_none",
]
