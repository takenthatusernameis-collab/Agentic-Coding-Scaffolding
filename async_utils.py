"""Asynchronous utility functions."""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, List, Optional, TypeVar

T = TypeVar("T")

__all__: List[str] = [
    "run_in_thread",
    "gather_with_timeout",
    "async_sleep",
    "retry_async",
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


async def gather_with_timeout(
    *coros: Awaitable[Any], timeout: Optional[float] = None
) -> List[Any]:
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
        max_attempts: Maximum number of attempts. Defaults to 3.
        delay: Delay between attempts in seconds. Defaults to 0.1.
        **kwargs: Keyword arguments for the function.

    Returns:
        The result of the function.

    Raises:
        Exception: The last exception if all attempts fail.

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
    last_exception: Exception = Exception("No attempts made")
    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001
            last_exception = exc
            if attempt < max_attempts - 1:
                await asyncio.sleep(delay)
    raise last_exception
