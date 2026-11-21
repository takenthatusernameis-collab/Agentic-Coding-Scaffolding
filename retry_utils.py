"""Retry utility functions for retrying operations with backoff."""

import functools
import math
import random
import time
from typing import Any, Callable, Tuple, Type

__all__ = [
    "retry",
    "retry_count",
    "retry_with_backoff",
]


def _validate_retry_args(
    max_attempts: int,
    delay: float,
    backoff: float,
    exceptions: Tuple[Type[BaseException], ...],
) -> None:
    """Validate retry decorator parameters, raising clear errors for misuse.

    ``max_attempts`` must be at least one so the wrapped function is actually
    invoked; a value of zero previously fell through the loop and surfaced a
    misleading ``RuntimeError("Unexpected state in retry decorator")``. A
    negative ``delay`` likewise surfaced a low-level ``time.sleep`` error
    instead of an argument problem.
    """
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int):
        raise TypeError(f"max_attempts must be an int, got {type(max_attempts).__name__}")
    if max_attempts < 1:
        raise ValueError(f"max_attempts must be at least 1, got {max_attempts}")
    if isinstance(delay, bool) or not isinstance(delay, (int, float)):
        raise TypeError(f"delay must be a number, got {type(delay).__name__}")
    if not math.isfinite(delay):
        raise ValueError(f"delay must be finite, got {delay!r}")
    if delay < 0:
        raise ValueError(f"delay must be non-negative, got {delay}")
    if isinstance(backoff, bool) or not isinstance(backoff, (int, float)):
        raise TypeError(f"backoff must be a number, got {type(backoff).__name__}")
    if not math.isfinite(backoff):
        raise ValueError(f"backoff must be finite, got {backoff!r}")
    if backoff < 0:
        raise ValueError(f"backoff must be non-negative, got {backoff}")
    if not isinstance(exceptions, tuple):
        raise TypeError(f"exceptions must be a tuple, got {type(exceptions).__name__}")


def retry(
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function if it raises an exception.

    Args:
        max_attempts: Maximum number of attempts (including the initial
            attempt). Must be at least 1.
        delay: Initial delay between attempts in seconds. Must be non-negative
            and finite.
        backoff: Multiplier applied to delay after each attempt. Must be
            non-negative and finite.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries on specified exceptions.

    Raises:
        ValueError: If ``max_attempts`` is less than 1, ``delay`` or ``backoff`` is
            negative or non-finite (``NaN``/``±inf``).
        TypeError: If any argument has the wrong type.

    Examples:
        >>> attempts = []
        >>> @retry(max_attempts=3, delay=0.01, backoff=2.0)
        ... def unreliable_function():
        ...     attempts.append(1)
        ...     if len(attempts) < 2:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> result = unreliable_function()
        >>> result
        'success'
        >>> len(attempts)
        2
    """
    _validate_retry_args(max_attempts, delay, backoff, exceptions)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            _delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise
                    time.sleep(_delay)
                    _delay *= backoff
            # Should never reach here due to raise on last attempt
            raise RuntimeError("Unexpected state in retry decorator")

        return wrapper

    return decorator


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 0.1,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function with exponential backoff and optional jitter.

    Args:
        max_attempts: Maximum number of attempts (including initial attempt).
        initial_delay: Initial delay between attempts in seconds. Must be
            non-negative and finite.
        backoff_factor: Multiplier for delay after each attempt. Must be
            non-negative and finite.
        jitter: If True, adds random jitter to delay to prevent thundering herd.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries with exponential backoff.

    Raises:
        ValueError: If ``max_attempts`` is less than 1, ``initial_delay`` or
            ``backoff_factor`` is negative or non-finite (``NaN``/``±inf``).
        TypeError: If any argument has the wrong type.

    Examples:
        >>> attempts = []
        >>> @retry_with_backoff(
        ...     max_attempts=3, initial_delay=0.01, backoff_factor=2.0, jitter=False
        ... )
        ... def unreliable_function():
        ...     attempts.append(1)
        ...     if len(attempts) < 2:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> result = unreliable_function()
        >>> result
        'success'
        >>> len(attempts)
        2
    """
    if isinstance(jitter, bool) is False:
        raise TypeError(f"jitter must be a bool, got {type(jitter).__name__}")
    _validate_retry_args(max_attempts, initial_delay, backoff_factor, exceptions)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = initial_delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise
                    # Apply jitter if enabled
                    actual_delay = delay
                    if jitter:
                        actual_delay *= random.uniform(0.5, 1.5)
                    time.sleep(actual_delay)
                    delay *= backoff_factor
            # Should never reach here due to raise on last attempt
            raise RuntimeError("Unexpected state in retry_with_backoff decorator")

        return wrapper

    return decorator


def retry_count(
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function and returns the result along with retry count.

    Args:
        max_attempts: Maximum number of attempts (including initial attempt).
        delay: Initial delay between attempts in seconds. Must be non-negative
            and finite.
        backoff: Multiplier applied to delay after each attempt. Must be
            non-negative and finite.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that returns (result, retry_count) where retry_count
        is the number of retries that occurred (0 if no retries needed).

    Raises:
        ValueError: If ``max_attempts`` is less than 1, ``delay`` or ``backoff`` is
            negative or non-finite (``NaN``/``±inf``).
        TypeError: If any argument has the wrong type.

    Examples:
        >>> attempts = []
        >>> @retry_count(max_attempts=3, delay=0.01)
        ... def unreliable_function():
        ...     attempts.append(1)
        ...     if len(attempts) < 2:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> result, count = unreliable_function()
        >>> result
        'success'
        >>> count
        1
        >>> len(attempts)
        2
    """
    _validate_retry_args(max_attempts, delay, backoff, exceptions)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> tuple:
            _delay = delay
            retries = 0
            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)
                    return result, retries
                except exceptions:
                    if attempt == max_attempts - 1:  # Last attempt
                        raise
                    retries += 1
                    time.sleep(_delay)
                    _delay *= backoff
            # Should never reach here due to raise on last attempt
            raise RuntimeError("Unexpected state in retry_count decorator")

        return wrapper

    return decorator


if __name__ == "__main__":
    # Simple demonstration when run directly
    import random

    @retry(max_attempts=3, delay=0.01, backoff=2.0)
    def unstable_operation():
        if random.random() < 0.8:
            raise RuntimeError("Temporary failure")
        return "Success!"

    try:
        result = unstable_operation()
        print(f"Operation succeeded: {result}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")

    @retry_with_backoff(max_attempts=3, initial_delay=0.01, backoff_factor=2.0)
    def unstable_operation_with_backoff():
        if random.random() < 0.8:
            raise RuntimeError("Temporary failure")
        return "Success with backoff!"

    try:
        result = unstable_operation_with_backoff()
        print(f"Operation succeeded with backoff: {result}")
    except Exception as e:
        print(f"Operation failed after retries with backoff: {e}")

    @retry_count(max_attempts=3, delay=0.01)
    def unstable_operation_with_count():
        if random.random() < 0.8:
            raise RuntimeError("Temporary failure")
        return "Success with count!"

    try:
        result, count = unstable_operation_with_count()
        print(f"Operation succeeded: {result} (retried {count} times)")
    except Exception as e:
        print(f"Operation failed after retries: {e}")
