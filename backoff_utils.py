"""Backoff strategy utilities for retry and resilience patterns.

This module provides backoff delay calculators used by retry decorators,
circuit breakers, and other resilience mechanisms. Each strategy computes
the delay before the next attempt given the current attempt number.

The standard library does not include a unified backoff API; this module
fills that gap with type-safe, validated helpers that work independently
or compose with :mod:`retry_utils` and :mod:`circuit_breaker_utils`.
"""

from __future__ import annotations

import random
from typing import Literal

__all__ = [
    "backoff_delay",
    "constant_backoff",
    "exponential_backoff",
    "jittered_backoff",
]


def constant_backoff(delay: float, *, attempt: int = 1) -> float:
    """Return a fixed backoff delay regardless of attempt number.

    Args:
        delay: The fixed delay in seconds. Must be non-negative.
        attempt: The current attempt number (1-indexed). Ignored but accepted
            for API compatibility with other backoff strategies.

    Returns:
        The delay to wait before the next attempt.

    Raises:
        TypeError: If *delay* is not a number.
        ValueError: If *delay* is negative.

    Examples:
        >>> constant_backoff(1.0)
        1.0
        >>> constant_backoff(0.5, attempt=3)
        0.5
        >>> constant_backoff(-1.0)
        Traceback (most recent call last):
        ...
        ValueError: delay must be non-negative
    """
    if isinstance(delay, bool) or not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")
    if delay < 0:
        raise ValueError("delay must be non-negative")
    return float(delay)


def exponential_backoff(
    initial: float, factor: float, max_delay: float, *, attempt: int = 1
) -> float:
    """Return an exponentially growing backoff delay for the given attempt.

    The delay grows as ``initial * factor ** attempt`` and is capped at
    ``max_delay``.

    Args:
        initial: The starting delay in seconds. Must be non-negative.
        factor: The multiplier applied each attempt. Must be >= 1.
        max_delay: The maximum delay in seconds. Must be non-negative.
        attempt: The current attempt number (1-indexed). The first retry
            uses attempt=1, giving ``initial * factor``.

    Returns:
        The delay to wait before the next attempt, capped at ``max_delay``.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If *initial*, *max_delay* are negative, or *factor* < 1.

    Examples:
        >>> exponential_backoff(1.0, 2.0, 100.0, attempt=1)
        2.0
        >>> exponential_backoff(1.0, 2.0, 100.0, attempt=2)
        4.0
        >>> exponential_backoff(1.0, 2.0, 100.0, attempt=3)
        8.0
        >>> exponential_backoff(10.0, 2.0, 15.0, attempt=1)
        15.0
        >>> exponential_backoff(-1.0, 2.0, 100.0)
        Traceback (most recent call last):
        ...
        ValueError: initial must be non-negative
        >>> exponential_backoff(1.0, 0.5, 100.0)
        Traceback (most recent call last):
        ...
        ValueError: factor must be >= 1
    """
    if isinstance(initial, bool) or not isinstance(initial, (int, float)):
        raise TypeError("initial must be a number")
    if isinstance(factor, bool) or not isinstance(factor, (int, float)):
        raise TypeError("factor must be a number")
    if isinstance(max_delay, bool) or not isinstance(max_delay, (int, float)):
        raise TypeError("max_delay must be a number")
    if isinstance(attempt, bool) or not isinstance(attempt, int):
        raise TypeError("attempt must be an integer")
    if initial < 0:
        raise ValueError("initial must be non-negative")
    if max_delay < 0:
        raise ValueError("max_delay must be non-negative")
    if factor < 1:
        raise ValueError("factor must be >= 1")
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    delay = initial * (factor ** attempt)
    return min(delay, max_delay)


def backoff_delay(
    *,
    strategy: Literal["constant", "exponential"] = "constant",
    attempt: int = 1,
    **kwargs: float,
) -> float:
    """Return a backoff delay for the named strategy and attempt.

    Args:
        strategy: Either "constant" or "exponential".
        attempt: The current attempt number (1-indexed).
        kwargs: Strategy-specific parameters:
            - "constant": ``delay``
            - "exponential": ``initial``, ``factor``, ``max_delay``

    Returns:
        The delay to wait before the next attempt.

    Raises:
        TypeError: If *attempt* is not an integer.
        ValueError: If *strategy* is unknown or required parameters are missing.

    Examples:
        >>> backoff_delay(strategy="constant", delay=2.5)
        2.5
        >>> call = dict(initial=1.0, factor=2.0, max_delay=50.0, attempt=1)
        >>> backoff_delay(strategy="exponential", **call)
        2.0
        >>> call = dict(initial=1.0, factor=2.0, max_delay=50.0, attempt=2)
        >>> backoff_delay(strategy="exponential", **call)
        4.0
        >>> backoff_delay(strategy="nonexistent", delay=1.0)
        Traceback (most recent call last):
        ...
        ValueError: unknown backoff strategy: 'nonexistent'
    """
    if isinstance(attempt, bool) or not isinstance(attempt, int):
        raise TypeError("attempt must be an integer")
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    if strategy == "constant":
        return constant_backoff(kwargs["delay"], attempt=attempt)
    if strategy == "exponential":
        return exponential_backoff(
            kwargs["initial"], kwargs["factor"], kwargs["max_delay"], attempt=attempt
        )
    raise ValueError(f"unknown backoff strategy: {strategy!r}")


def jittered_backoff(delay: float, jitter: float = 0.1) -> float:
    """Return a backoff delay multiplied by a random jitter factor.

    The returned delay is uniformly distributed in
    ``[delay * (1 - jitter), delay * (1 + jitter)]``.

    Args:
        delay: The base delay in seconds. Must be non-negative.
        jitter: The maximum relative jitter in [0, 1]. Defaults to 0.1 (10%).

    Returns:
        A jittered delay in seconds.

    Raises:
        TypeError: When *delay* or *jitter* is not a number.
        ValueError: When *delay* is negative or *jitter* is out of range.

    Examples:
        >>> jittered_backoff(10.0, 0.0)
        10.0
        >>> 8.0 <= jittered_backoff(10.0, 0.2) <= 12.0
        True
        >>> jittered_backoff(-1.0)
        Traceback (most recent call last):
        ...
        ValueError: delay must be non-negative
        >>> jittered_backoff(1.0, 1.5)
        Traceback (most recent call last):
        ...
        ValueError: jitter must be between 0 and 1
    """
    if isinstance(delay, bool) or not isinstance(delay, (int, float)):
        raise TypeError("delay must be a number")
    if isinstance(jitter, bool) or not isinstance(jitter, (int, float)):
        raise TypeError("jitter must be a number")
    if delay < 0:
        raise ValueError("delay must be non-negative")
    if jitter < 0 or jitter > 1:
        raise ValueError("jitter must be between 0 and 1")
    factor = random.uniform(1 - jitter, 1 + jitter)
    return delay * factor


if __name__ == "__main__":
    import doctest

    doctest.testmod()
