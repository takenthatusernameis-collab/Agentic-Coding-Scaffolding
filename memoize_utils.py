"""Memoization utilities.

This module provides a ``memoize`` decorator that caches the return value of a
wrapped function keyed by its call arguments, avoiding repeated computation for
identical inputs.
"""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

T = TypeVar("T")


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
