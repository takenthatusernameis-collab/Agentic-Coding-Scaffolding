"""Asynchronous utility functions."""

from __future__ import annotations

import asyncio
import math
from typing import Any, Awaitable, Callable, List, Optional, TypeVar

T = TypeVar("T")

__all__ = [
    "T",
    "async_sleep",
    "gather_with_timeout",
    "retry_async",
    "run_in_thread",
]


async def run_in_thread(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Run a synchronous function in a thread pool.

    Args:
        func: The synchronous function to run.
        *args: Positional arguments for the function.
        **kwargs: Keyword arguments for the function.

    Returns:
        The result of the function.

    Examples:
        >>> import asyncio
        >>> async def example():
        ...     return await run_in_thread(sum, [1, 2, 3])
        >>> asyncio.run(example())
        6
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def gather_with_timeout(*coros: Awaitable[Any], timeout: Optional[float] = None) -> List[Any]:
    """Gather multiple coroutines with an optional timeout.

    Args:
        *coros: The coroutines to gather.
        timeout: Timeout in seconds. If None, no timeout.

    Returns:
        A list of results.

    Raises:
        asyncio.TimeoutError: If the timeout is exceeded.

    Examples:
        >>> import asyncio
        >>> async def example():
        ...     results = await gather_with_timeout(
        ...         asyncio.sleep(0.01, result=1),
        ...         asyncio.sleep(0.01, result=2),
        ...         timeout=1.0,
        ...     )
        ...     return results
        >>> asyncio.run(example())
        [1, 2]
    """
    if timeout is None:
        return await asyncio.gather(*coros)
    return await asyncio.wait_for(asyncio.gather(*coros), timeout=timeout)


async def async_sleep(seconds: float) -> None:
    """Sleep for the specified number of seconds asynchronously.

    Args:
        seconds: Number of seconds to sleep.

    Examples:
        >>> import asyncio
        >>> asyncio.run(async_sleep(0.001))
    """
    await asyncio.sleep(seconds)


def _validate_retry_args(max_attempts: int, delay: float) -> None:
    """Validate ``retry_async`` arguments, raising clear errors for misuse.

    Mirrors :func:`retry_utils.retry`: ``max_attempts`` must be a positive
    integer and ``delay`` a non-negative number. ``bool`` is rejected for both
    because it is a subclass of ``int``; without this check ``max_attempts``
    of ``False``/``True`` silently meant zero/one attempt and a boolean
    ``delay`` was accepted as ``0.0``/``1.0`` seconds.
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


async def retry_async(
    func: Callable[..., Awaitable[T]],
    *args: Any,
    max_attempts: int = 3,
    delay: float = 0.1,
    **kwargs: Any,
) -> T:
    """Retry an async function on exceptions.

    Args:
        func: The async function to retry.
        *args: Positional arguments for the function.
        max_attempts: Maximum number of attempts. Defaults to 3. Must be a
            positive integer.
        delay: Delay between attempts in seconds. Defaults to 0.1. Must be a
            non-negative number.
        **kwargs: Keyword arguments for the function.

    Returns:
        The result of the function.

    Raises:
        TypeError: If ``max_attempts`` is not an int or ``delay`` is not a
            number.
        ValueError: If ``max_attempts`` is less than 1 or ``delay`` is negative.
        Exception: The last exception if all attempts fail.  # audit-ignore: Exception

    Examples:
        >>> import asyncio
        >>> attempts = []
        >>> async def flaky():
        ...     attempts.append(1)
        ...     if len(attempts) < 2:
        ...         raise ValueError("fail")
        ...     return "success"
        >>> asyncio.run(retry_async(flaky))
        'success'
    """
    _validate_retry_args(max_attempts, delay)
    last_exception: Exception = Exception("No attempts made")
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            last_exception = exc
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay)
    raise last_exception
