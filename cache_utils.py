"""Caching utilities for memoizing function results.

This module provides a small, consistent API around function result caching,
including a ``memoize`` decorator factory, a ``clear_cache`` helper to invalidate
stored results, and a ``cache_info`` helper to inspect cache statistics.
"""

import functools
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

__all__: List[str] = [
    "cache_info",
    "clear_cache",
    "memoize",
]


def memoize(
    maxsize: Optional[int] = 128,
    typed: bool = False,
) -> Callable[[F], F]:
    """Decorator factory that caches a function's return values.

    The wrapped function stores results keyed by its call arguments so that
    subsequent invocations with the same arguments return the cached value
    without re-executing the body. ``functools.wraps`` is used, so the
    decorated function's metadata (``__name__``, ``__doc__``, etc.) is
    preserved.

    Args:
        maxsize: The maximum number of cached entries to retain. When the
            cache exceeds this size, the least-recently-used entry is evicted.
            Pass ``None`` for an unbounded cache. Defaults to ``128``.
        typed: If ``True``, arguments of the same value but different types
            (e.g. ``1`` and ``1.0``) are cached separately. Defaults to
            ``False``.

    Returns:
        A decorator that wraps a function with caching behavior.

    Example:
        >>> @memoize()
        ... def square(n: int) -> int:
        ...     return n * n
        ...
        >>> square(4)
        16
    """
    if maxsize is not None and (not isinstance(maxsize, int) or isinstance(maxsize, bool)):
        raise TypeError("maxsize must be an integer or None")
    if maxsize is not None and maxsize < 1:
        raise ValueError("maxsize must be a positive integer or None")

    def decorator(func: F) -> F:
        cache: Dict[Any, Any] = {}
        order: List[Any] = []
        hits = [0]
        misses = [0]

        def _make_key(args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Any:
            """Build a hashable cache key from positional and keyword arguments."""
            key_args: Tuple[Any, ...] = tuple(args)
            key_kwargs: Tuple[Tuple[str, Any], ...] = tuple(sorted(kwargs.items()))
            if typed:
                return (key_args, key_kwargs, tuple(type(a) for a in args))
            return (key_args, key_kwargs)

        def _evict_if_needed() -> None:
            """Evict the least-recently-used entry when the cache is full."""
            if maxsize is None or len(cache) <= maxsize:
                return
            # Evict the oldest key that is still present.
            for old_key in order:
                if old_key in cache:
                    cache.pop(old_key, None)
                    order.remove(old_key)
                    return

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _make_key(args, kwargs)
            if key in cache:
                hits[0] += 1
                return cache[key]
            misses[0] += 1
            result = func(*args, **kwargs)
            cache[key] = result
            order.append(key)
            _evict_if_needed()
            return result

        def clear() -> None:
            """Remove all cached entries and reset statistics."""
            cache.clear()
            order.clear()
            hits[0] = 0
            misses[0] = 0

        def info() -> Dict[str, Any]:
            """Return a dictionary describing the current cache state."""
            return {
                "hits": hits[0],
                "misses": misses[0],
                "maxsize": maxsize,
                "currsize": len(cache),
            }

        # Attach helpers to the wrapped function so callers can introspect
        # or invalidate the cache without needing to keep a separate reference.
        wrapper.clear_cache = clear  # type: ignore[attr-defined]
        wrapper.cache_info = info  # type: ignore[attr-defined]
        return cast(F, wrapper)

    return decorator


def clear_cache(func: F) -> None:
    """Clear the cache of a function decorated with :func:`memoize`.

    Args:
        func: A function previously decorated with :func:`memoize`.

    Raises:
        TypeError: If ``func`` does not expose a ``clear_cache`` attribute,
            meaning it was not memoized.

    Example:
        >>> @memoize()
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        ...
        >>> add(1, 2)
        3
        >>> clear_cache(add)
    """
    clear = getattr(func, "clear_cache", None)
    if not callable(clear):
        raise TypeError(
            "clear_cache can only be used on functions decorated with memoize"
        )
    clear()


def cache_info(func: F) -> Dict[str, Any]:
    """Return cache statistics for a function decorated with :func:`memoize`.

    Args:
        func: A function previously decorated with :func:`memoize`.

    Returns:
        A dictionary with ``hits``, ``misses``, ``maxsize``, and ``currsize``
        keys describing the current state of the cache.

    Raises:
        TypeError: If ``func`` does not expose a ``cache_info`` attribute,
            meaning it was not memoized.

    Example:
        >>> @memoize()
        ... def mul(a: int, b: int) -> int:
        ...     return a * b
        ...
        >>> mul(2, 3)
        6
        >>> info = cache_info(mul)
        >>> info["misses"]
        1
    """
    info = getattr(func, "cache_info", None)
    if not callable(info):
        raise TypeError(
            "cache_info can only be used on functions decorated with memoize"
        )
    return cast(Dict[str, Any], info())
