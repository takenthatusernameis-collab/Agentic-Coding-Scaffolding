"""Cooldown and throttling utilities for rate-limiting function calls."""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")

__all__ = ["cooldown", "Cooldown", "is_available"]


def is_available() -> bool:
    """Return True because this module has no external dependencies."""
    return True


class Cooldown:
    """Enforce a minimum interval between calls to a callable.

    The cooldown tracks the last time a call was allowed and rejects any
    call that arrives before the configured interval has elapsed. The class
    is thread-safe so a single instance can be shared across threads.
    """

    def __init__(self, interval: float) -> None:
        """Create a cooldown with the given minimum interval in seconds.

        Args:
            interval: Minimum seconds between allowed calls. Must be positive.

        Raises:
            TypeError: If interval is not a real number.
            ValueError: If interval is not positive.
        """
        if not isinstance(interval, (int, float)) or isinstance(interval, bool):
            raise TypeError("interval must be a real number")
        if interval <= 0:
            raise ValueError("interval must be positive")
        self._interval = float(interval)
        self._last_call: float | None = None
        self._lock = threading.Lock()

    def ready(self) -> bool:
        """Return True if a call is allowed right now."""
        now = time.monotonic()
        with self._lock:
            if self._last_call is None:
                return True
            return now - self._last_call >= self._interval

    def remaining(self) -> float:
        """Return the seconds left before the next call is allowed."""
        now = time.monotonic()
        with self._lock:
            if self._last_call is None:
                return 0.0
            return max(0.0, self._interval - (now - self._last_call))

    def call(self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> T:
        """Call *func* if the cooldown interval has elapsed.

        Args:
            func: The callable to invoke.
            *args: Positional arguments for func.
            **kwargs: Keyword arguments for func.

        Raises:
            TimeoutError: If the cooldown interval has not yet elapsed.
            TypeError: If func is not callable.
        """
        if not callable(func):
            raise TypeError("func must be callable")
        with self._lock:
            now = time.monotonic()
            if self._last_call is not None and now - self._last_call < self._interval:
                raise TimeoutError(
                    f"cooldown not ready: {self.remaining():.3f}s remaining"
                )
            self._last_call = now
        return func(*args, **kwargs)

    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        """Return a wrapped callable that enforces the cooldown on each call."""

        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            return self.call(func, *args, **kwargs)

        return wrapped


def cooldown(interval: float) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator that limits a function to one call per interval.

    Args:
        interval: Minimum seconds between allowed calls. Must be positive.

    Returns:
        A decorator that wraps the callable with a cooldown.

    Raises:
        TypeError: If interval is not a real number.
        ValueError: If interval is not positive.
    """
    return Cooldown(interval)
