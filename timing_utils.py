"""Performance measurement utilities for timing code execution.

This module provides helpers for measuring and benchmarking code execution,
including a context manager for timing blocks, a function to calculate elapsed
time, and a decorator for benchmarking function execution.
"""

import functools
import time
from typing import Any, Callable, Generator, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


class timer:
    """Context manager for measuring execution time of a code block.

    Args:
        label: Optional label to display with the timing result.

    Examples:
        >>> with timer("Database query"):
        ...     # Execute database query
        ...     pass
        Database query: 0.00s

        >>> with timer():
        ...     time.sleep(0.1)
        Elapsed: 0.10s
    """

    def __init__(self, label: str = "Elapsed") -> None:
        self.label = label
        self.start_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> "timer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.elapsed = time.perf_counter() - self.start_time
        if self.label:
            print(f"{self.label}: {self.elapsed:.2f}s")


def elapsed_time(start_time: float) -> float:
    """Calculate elapsed time since a start time.

    Args:
        start_time: Start time as returned by time.perf_counter() or time.time().

    Returns:
        Elapsed time in seconds.

    Examples:
        >>> start = time.perf_counter()
        >>> time.sleep(0.05)
        >>> elapsed_time(start)
        0.05...
    """
    return time.perf_counter() - start_time


def benchmark(
    iterations: int = 1,
) -> Callable[[F], F]:
    """Decorator that benchmarks a function by running it multiple times.

    Args:
        iterations: Number of times to run the function for averaging.
                   Must be positive. Defaults to 1.

    Returns:
        Decorated function that prints timing information and returns the
        result of the final function call.

    Examples:
        >>> @benchmark(iterations=3)
        ... def slow_function():
        ...     time.sleep(0.1)
        ...     return "done"
        >>> result = slow_function()
        slow_function (avg of 3 runs): 0.30s
        >>> result
        'done'
    """
    if iterations < 1:
        raise ValueError("iterations must be positive")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            total_time = 0.0
            result = None
            for i in range(iterations):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                total_time += time.perf_counter() - start
            avg_time = total_time / iterations
            print(f"{func.__name__} (avg of {iterations} runs): {avg_time:.2f}s")
            return result

        return cast(F, wrapper)

    return decorator


if __name__ == "__main__":
    # Simple demonstration when run directly
    import random

    @benchmark(iterations=2)
    def example_function():
        time.sleep(0.05)
        return "completed"

    result = example_function()
    print(f"Function returned: {result}")

    # Example of timer context manager
    with timer("Example block"):
        time.sleep(0.02)
        print("Inside timed block")

    # Example of elapsed_time function
    start = time.perf_counter()
    time.sleep(0.03)
    elapsed = elapsed_time(start)
    print(f"Elapsed time: {elapsed:.2f}s")