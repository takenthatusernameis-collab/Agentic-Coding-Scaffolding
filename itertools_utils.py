"""itertools utilities for common iteration patterns.

Provides convenient wrappers around the standard library ``itertools``
module with input validation.
"""

from itertools import (
    accumulate,
    chain,
    combinations,
    cycle,
    groupby,
    islice,
    permutations,
    product,
    repeat,
    takewhile,
)
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


__all__ = [
    "chain_iterables",
    "flatten_once",
    "take_while_pred",
    "chunk_iterable",
    "product_of",
    "combinations_of",
    "permutations_of",
    "group_by_key",
    "accumulate_values",
    "repeat_value",
    "cycle_take",
]
