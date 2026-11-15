"""Call-once execution utilities.

This module provides a ``call_once`` decorator that ensures a wrapped function
is executed only a single time, caching its return value for every subsequent
call. Execution is thread-safe, so concurrent callers all observe the same
single invocation and result.
"""

from __future__ import annotations

import threading
from typing import Any, Callable, Optional, TypeVar

__all__ = [
    "T",
    "call_once",
]

T = TypeVar("T")


def call_once(func: Callable[..., T]) -> Callable[..., T]:
    """Return a wrapper that invokes ``func`` only once.

    The first call executes ``func`` with the supplied arguments and caches its
    return value. Every subsequent call returns the cached result without
    re-invoking ``func``. The wrapped function is safe to call from multiple
    threads; exactly one invocation of ``func`` occurs even under concurrency.

    If the single invocation raises, that exception is cached and re-raised to
    every later caller without re-invoking ``func``. This keeps the contract
    that the wrapped body executes at most once: a raising first call does not
    grant a retry on the next call. ``reset`` clears the cached state so the
    next call performs a fresh single invocation.

    Args:
        func: The function to invoke at most once.

    Returns:
        A callable that executes ``func`` once and returns the cached result on
        all later calls. The wrapper exposes a ``reset`` method that clears the
        cached state so the next call re-invokes ``func``.

    Raises:
        TypeError: If ``func`` is not callable.
    """
    if not callable(func):
        raise TypeError("func must be callable")

    lock = threading.Lock()
    called = False
    result: Optional[T] = None
    # When the single invocation raises, the cached exception is re-raised to
    # later callers instead of re-invoking ``func``.
    cached_exc: Optional[BaseException] = None

    def wrapper(*args: Any, **kwargs: Any) -> T:
        nonlocal called, result, cached_exc
        with lock:
            if not called:
                try:
                    result = func(*args, **kwargs)
                except BaseException as exc:
                    cached_exc = exc
                    raise
                finally:
                    called = True
            if cached_exc is not None:
                raise cached_exc
            return result  # type: ignore[return-value]

    def reset() -> None:
        """Clear the cached result so the next call re-invokes ``func``."""
        nonlocal called, result, cached_exc
        with lock:
            called = False
            result = None
            cached_exc = None

    wrapper.reset = reset  # type: ignore[attr-defined]
    return wrapper
