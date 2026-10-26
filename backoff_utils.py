import random


def constant_backoff(delay: float) -> float:
    """Return a fixed backoff delay for every attempt.

    Args:
        delay: The fixed delay in seconds.

    Returns:
        The delay to wait before the next attempt.
    """
    return delay


def exponential_backoff(initial: float, factor: float, max_delay: float) -> float:
    """Return an exponentially growing backoff delay.

    Args:
        initial: The starting delay in seconds.
        factor: The multiplier applied each attempt.
        max_delay: The maximum delay in seconds.

    Returns:
        The delay to wait before the next attempt, capped at max_delay.
    """
    return min(initial * factor, max_delay)


def backoff_delay(*, strategy: str = "constant", **kwargs: float) -> float:
    """Return a backoff delay for the named strategy.

    Args:
        strategy: Either "constant" or "exponential".
        kwargs: Strategy-specific parameters.

    Returns:
        The delay to wait before the next attempt.

    Raises:
        ValueError: When *strategy* is unknown.
    """
    if strategy == "constant":
        return constant_backoff(kwargs["delay"])
    if strategy == "exponential":
        return exponential_backoff(kwargs["initial"], kwargs["factor"], kwargs["max_delay"])
    raise ValueError(f"unknown backoff strategy: {strategy!r}")


def jittered_backoff(delay: float, jitter: float = 0.1) -> float:
    """Return a backoff delay multiplied by a random jitter factor.

    Args:
        delay: The base delay in seconds.
        jitter: The maximum relative jitter in [0, 1].

    Returns:
        A delay in [delay * (1 - jitter), delay * (1 + jitter)].

    Raises:
        TypeError: When *delay* or *jitter* is not a number.
        ValueError: When *delay* is negative or *jitter* is out of range.
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
