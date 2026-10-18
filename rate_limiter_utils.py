"""Rate limiting utilities for controlling the frequency of operations.

This module provides helpers for rate limiting using the token bucket algorithm,
including a RateLimiter class, a token_bucket context manager, and a rate_limit
decorator.
"""

import time
from typing import Any, Callable, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class RateLimiter:
    """Token bucket rate limiter.

    Args:
        rate: Maximum frequency (in tokens per second).
        capacity: Maximum tokens in the bucket. If not provided, defaults to rate.
    """

    def __init__(self, rate: float, capacity: Optional[float] = None):
        if rate <= 0:
            raise ValueError("rate must be positive")
        self.rate = float(rate)
        self.capacity = float(capacity if capacity is not None else rate)
        self.tokens = self.capacity
        self.last_updated = time.monotonic()

    def _update(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_updated
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_updated = now

    def acquire(self, tokens: float = 1) -> bool:
        """Acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire.

        Returns:
            True if tokens were acquired, False otherwise.
        """
        self._update()
        if tokens > self.capacity:
            # Cannot acquire more than capacity at once
            return False
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def acquire_blocking(self, tokens: float = 1) -> None:
        """Block until tokens can be acquired.

        Args:
            tokens: Number of tokens to acquire.
        """
        while not self.acquire(tokens):
            time.sleep(0.001)  # Sleep briefly to avoid busy loop


class token_bucket:
    """Context manager that acquires tokens from a RateLimiter.

    Args:
        rate_limiter: A RateLimiter instance.
        tokens: Number of tokens to acquire. Defaults to 1.

    Examples:
        >>> limiter = RateLimiter(rate=2.0)  # 2 tokens per second
        >>> with token_bucket(limiter):
        ...     # This block will execute, but will be rate-limited
        ...     pass
    """

    def __init__(self, rate_limiter: RateLimiter, tokens: float = 1):
        self.rate_limiter = rate_limiter
        self.tokens = tokens

    def __enter__(self) -> None:
        self.rate_limiter.acquire_blocking(self.tokens)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


def rate_limit(
    rate: float,
    capacity: Optional[float] = None,
) -> Callable[[F], F]:
    """Decorator that limits the rate at which a function can be called.

    Args:
        rate: Maximum frequency (in calls per second).
        capacity: Maximum burst size. If not provided, defaults to rate.

    Returns:
        Decorated function that will be rate-limited.

    Examples:
        >>> @rate_limit(rate=2.0)  # Allow at most 2 calls per second
        ... def limited_function():
        ...     return "result"
        >>> result = limited_function()
    """
    limiter = RateLimiter(rate=rate, capacity=capacity)

    def decorator(func: F) -> F:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            limiter.acquire_blocking()
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator


if __name__ == "__main__":
    # Simple demonstration when run directly
    import time

    @rate_limit(rate=2.0)  # 2 calls per second
    def example_function():
        return "completed"

    # Call the function multiple times and see the rate limiting
    start = time.monotonic()
    for i in range(5):
        result = example_function()
        elapsed = time.monotonic() - start
        print(f"Call {i + 1}: {result} at {elapsed:.2f}s")
        # We don't sleep here because the decorator will block if needed
