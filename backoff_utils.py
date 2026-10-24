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
