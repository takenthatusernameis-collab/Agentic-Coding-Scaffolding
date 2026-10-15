"""Retry utility functions for retrying operations with backoff."""

import functools
import random
import time
from typing import Any, Callable, Tuple, Type


def retry(
    max_attempts: int = 3,
    delay: float = 0.1,
    backoff: float = 1.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function if it raises an exception.

    Args:
        max_attempts: Maximum number of attempts (including initial attempt).
        delay: Initial delay between attempts in seconds.
        backoff: Multiplier applied to delay after each attempt.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries on specified exceptions.

    Examples:
        >>> @retry(max_attempts=3, delay=0.1, backoff=2.0)
        ... def unreliable_function():
        ...     import random
        ...     if random.random() < 0.7:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> # May succeed after retries
        >>> result = unreliable_function()
    """

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
        initial_delay: Initial delay between attempts in seconds.
        backoff_factor: Multiplier for delay after each attempt.
        jitter: If True, adds random jitter to delay to prevent thundering herd.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that retries with exponential backoff.

    Examples:
        >>> @retry_with_backoff(max_attempts=3, initial_delay=0.1, backoff_factor=2.0)
        ... def unreliable_function():
        ...     import random
        ...     if random.random() < 0.7:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> # May succeed after retries with increasing delays
        >>> result = unreliable_function()
    """

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
        delay: Initial delay between attempts in seconds.
        backoff: Multiplier applied to delay after each attempt.
        exceptions: Tuple of exception types to catch and retry on.

    Returns:
        Decorated function that returns (result, retry_count) where retry_count
        is the number of retries that occurred (0 if no retries needed).

    Examples:
        >>> @retry_count(max_attempts=3, delay=0.1)
        ... def unreliable_function():
        ...     import random
        ...     if random.random() < 0.8:
        ...         raise ValueError("Random failure")
        ...     return "success"
        >>> result, count = unreliable_function()  # count is number of retries
        >>> isinstance(result, str)
        True
        >>> isinstance(count, int)
        True
        >>> count >= 0
        True
    """

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
