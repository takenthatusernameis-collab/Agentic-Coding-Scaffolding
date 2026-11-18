"""Time-to-live cache utilities.

This module provides a :class:`TTLCache` mapping whose entries expire after a
configured time-to-live, and a :func:`ttl_cache` decorator factory that memoizes
a function call with per-entry TTL expiry. Expired entries are treated as absent
and are evicted lazily on access (and proactively when the cache is full).

Example:
    >>> cache = TTLCache(ttl=60, maxsize=2)
    >>> cache["a"] = 1
    >>> cache["b"] = 2
    >>> cache["a"]
    1
    >>> "c" in cache
    False
    >>> len(cache)
    2
    >>> cache["c"] = 3
    >>> "b" in cache
    False
    >>> cache["a"]
    1
    >>> cache.clear()
    >>> len(cache)
    0
"""

from __future__ import annotations

import functools
import time
from typing import Any, Callable, Optional, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

__all__ = ["Expired", "F", "TTLCache", "ttl_cache"]


class Expired(KeyError):
    """Raised when a cache entry has expired and is treated as absent."""


class TTLCache:
    """A mapping whose entries expire after a fixed time-to-live.

    Args:
        ttl: Time-to-live in seconds for every entry. Must be a non-negative
            number.
        maxsize: Maximum number of entries to retain. When full, the
            least-recently-used entry is evicted. Pass ``None`` for unbounded.

    Raises:
        TypeError: If ``ttl`` is not a number or ``maxsize`` is not an int or
            ``None`` (booleans are rejected).
        ValueError: If ``ttl`` is negative or ``maxsize`` is not positive.

    Example:
        >>> cache = TTLCache(ttl=10, maxsize=2)
        >>> cache["x"] = 1
        >>> cache["y"] = 2
        >>> cache["x"]
        1
    """

    __slots__ = (
        "_ttl",
        "_maxsize",
        "_data",
        "_expires_at",
        "_order",
        "_hits",
        "_misses",
        "_expired_count",
    )

    def __init__(self, ttl: float, maxsize: Optional[int] = 128) -> None:
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be a number")
        if ttl < 0:
            raise ValueError("ttl must be non-negative")
        if maxsize is not None and (isinstance(maxsize, bool) or not isinstance(maxsize, int)):
            raise TypeError("maxsize must be an integer or None")
        if maxsize is not None and maxsize < 1:
            raise ValueError("maxsize must be a positive integer or None")
        self._ttl = float(ttl)
        self._maxsize = maxsize
        self._data: dict[Any, Any] = {}
        self._expires_at: dict[Any, float] = {}
        self._order: list[Any] = []
        self._hits = 0
        self._misses = 0
        self._expired_count = 0

    def _now(self) -> float:
        return time.monotonic()

    def _expired(self, key: Any) -> bool:
        return key in self._expires_at and self._now() >= self._expires_at[key]

    def _touch(self, key: Any) -> None:
        if key in self._data:
            self._order.remove(key)
            self._order.append(key)

    def _remove(self, key: Any) -> None:
        self._data.pop(key, None)
        self._expires_at.pop(key, None)
        if key in self._order:
            self._order.remove(key)

    def _purge_expired(self) -> None:
        now = self._now()
        for key in list(self._data):
            if key in self._expires_at and now >= self._expires_at[key]:
                self._remove(key)
                self._expired_count += 1

    def _evict_if_needed(self) -> None:
        if self._maxsize is None or len(self._data) <= self._maxsize:
            return
        for old_key in list(self._order):
            if old_key in self._data:
                self._remove(old_key)
                return

    def __contains__(self, key: object) -> bool:
        if key not in self._data:
            return False
        if self._expired(key):
            self._remove(key)
            self._expired_count += 1
            return False
        return True

    def __getitem__(self, key: Any) -> Any:
        if key not in self._data:
            self._misses += 1
            raise KeyError(key)
        if self._expired(key):
            self._remove(key)
            self._expired_count += 1
            self._misses += 1
            raise Expired(key)
        self._hits += 1
        self._touch(key)
        return self._data[key]

    def get(self, key: Any, default: Any = None) -> Any:
        """Return the value for *key*, or *default* when missing or expired."""
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key: Any, value: Any) -> None:
        self._purge_expired()
        if key in self._data:
            self._data[key] = value
            self._expires_at[key] = self._now() + self._ttl
            self._touch(key)
            return
        self._data[key] = value
        self._expires_at[key] = self._now() + self._ttl
        self._order.append(key)
        self._evict_if_needed()

    def __delitem__(self, key: Any) -> None:
        if key not in self._data:
            raise KeyError(key)
        if self._expired(key):
            self._remove(key)
            self._expired_count += 1
            raise KeyError(key)
        self._remove(key)

    def pop(self, key: Any, default: Any = None) -> Any:
        """Remove *key* and return its value, or *default* when missing/expired."""
        if key not in self._data:
            return default
        if self._expired(key):
            self._remove(key)
            self._expired_count += 1
            return default
        value = self._data[key]
        self._remove(key)
        return value

    def __len__(self) -> int:
        self._purge_expired()
        return len(self._data)

    def __iter__(self):
        self._purge_expired()
        return iter(list(self._order))

    def keys(self) -> list[Any]:
        """Return a list of live keys without affecting cache statistics."""
        return [key for key in self]

    def values(self) -> list[Any]:
        """Return a list of live values without affecting cache statistics."""
        return [self._data[key] for key in self]

    def items(self) -> list[tuple[Any, Any]]:
        """Return a list of live ``(key, value)`` pairs without affecting statistics."""
        return [(key, self._data[key]) for key in self]

    def expire(self, key: Any, ttl: Optional[float] = None) -> None:
        """Set (or refresh) the time-to-live for *key* in seconds."""
        if key not in self._data:
            raise KeyError(key)
        if ttl is None:
            ttl = self._ttl
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be a number")
        if ttl < 0:
            raise ValueError("ttl must be non-negative")
        self._expires_at[key] = self._now() + float(ttl)

    def clear(self) -> None:
        """Remove all entries and reset statistics."""
        self._data.clear()
        self._expires_at.clear()
        self._order.clear()
        self._hits = 0
        self._misses = 0
        self._expired_count = 0

    def cache_info(self) -> dict[str, Any]:
        """Return cache statistics: hits, misses, maxsize, currsize, expired."""
        self._purge_expired()
        return {
            "hits": self._hits,
            "misses": self._misses,
            "maxsize": self._maxsize,
            "currsize": len(self._data),
            "expired": self._expired_count,
        }


def ttl_cache(
    ttl: float, maxsize: Optional[int] = 128
) -> Callable[[F], F]:
    """Decorator factory that memoizes a function with TTL expiry.

    Args:
        ttl: Time-to-live in seconds for each cached result.
        maxsize: Maximum number of cached results.

    Raises:
        TypeError: If ``ttl`` is not a number or ``maxsize`` is not an int or
            ``None`` (booleans rejected).
        ValueError: If ``ttl`` is negative or ``maxsize`` is not positive.

    Example:
        >>> @ttl_cache(ttl=60)
        ... def add(a: int, b: int) -> int:
        ...     return a + b
        >>> add(1, 2)
        3
        >>> add(1, 2)
        3
        >>> add.cache_info()["hits"]
        1
    """
    if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
        raise TypeError("ttl must be a number")
    if ttl < 0:
        raise ValueError("ttl must be non-negative")
    if maxsize is not None and (isinstance(maxsize, bool) or not isinstance(maxsize, int)):
        raise TypeError("maxsize must be an integer or None")
    if maxsize is not None and maxsize < 1:
        raise ValueError("maxsize must be a positive integer or None")

    cache = TTLCache(ttl=ttl, maxsize=maxsize)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            try:
                return cache[key]
            except KeyError:
                pass
            result = func(*args, **kwargs)
            cache[key] = result
            return result

        wrapper.cache = cache  # type: ignore[attr-defined]
        wrapper.cache_clear = cache.clear  # type: ignore[attr-defined]
        wrapper.cache_info = cache.cache_info  # type: ignore[attr-defined]
        return cast(F, wrapper)

    return decorator
