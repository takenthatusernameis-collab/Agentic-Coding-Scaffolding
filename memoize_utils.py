"""Memoization utilities.

This module provides a ``memoize`` decorator that caches the return value of a
wrapped function keyed by its call arguments, avoiding repeated computation for
identical inputs.
"""

from __future__ import annotations

import collections
import functools
from typing import Any, Callable, TypeVar

T = TypeVar("T")

__all__ = ["memoize", "lru_memoize"]


def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Return a memoized version of ``func``.

    Results are cached keyed by the positional and keyword arguments passed to
    the function. Subsequent calls with the same arguments return the cached
    result without re-invoking ``func``. The wrapped function exposes a
    ``cache_clear`` method that empties the cache.

    Args:
        func: The function to memoize.

    Returns:
        A callable that caches results by arguments.

    Raises:
        TypeError: If ``func`` is not callable.
    """
    if not callable(func):
        raise TypeError("func must be callable")

    cache: dict[tuple[Any, ...], T] = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    def cache_clear() -> None:
        """Empty the memoization cache."""
        cache.clear()

    wrapper.cache_clear = cache_clear  # type: ignore[attr-defined]
    return wrapper


def lru_memoize(func: Callable[..., T] = None, maxsize: int = 128) -> Callable[..., T]:  # type: ignore[assignment]
    """Return a least-recently-used memoized version of ``func``.

    Behaves like :func:`memoize` but evicts the least recently used entry when
    the cache exceeds ``maxsize``. A ``maxsize`` of ``0`` disables caching.

    Args:
        func: The function to memoize.
        maxsize: Maximum number of cached results.

    Returns:
        A callable that caches results by arguments.

    Raises:
        TypeError: If ``func`` is not callable or ``maxsize`` is not an int.
        ValueError: If ``maxsize`` is negative.
    """
    if func is None:
        def factory(f: Callable[..., T]) -> Callable[..., T]:
            return lru_memoize(f, maxsize=maxsize)
        return factory  # type: ignore[return-value]

    if not callable(func):
        raise TypeError("func must be callable")
    if not isinstance(maxsize, int):
        raise TypeError("maxsize must be an int")
    if maxsize < 0:
        raise ValueError("maxsize must be non-negative")

    cache: "collections.OrderedDict[tuple[Any, ...], T]" = collections.OrderedDict()

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            cache.move_to_end(key)
            return cache[key]
        if maxsize == 0:
            return func(*args, **kwargs)
        result = func(*args, **kwargs)
        cache[key] = result
        if len(cache) > maxsize:
            cache.popitem(last=False)
        return result

    def cache_clear() -> None:
        cache.clear()

    wrapper.cache_clear = cache_clear  # type: ignore[attr-defined]
    return wrapper
