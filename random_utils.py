"""Random number generation and sampling utilities."""

import random
from typing import List, Optional, Sequence, TypeVar

T = TypeVar("T")


def _seed_rng(seed: Optional[int]) -> random.Random:
    """Create a seeded ``random.Random`` instance for reproducible results."""
    return random.Random(seed)


def random_int(low: int, high: int, seed: Optional[int] = None) -> int:
    """Return a random integer N such that ``low <= N <= high``.

    Args:
        low: The inclusive lower bound of the range.
        high: The inclusive upper bound of the range.
        seed: Optional seed for reproducible results. When provided, the
            returned value is deterministic for a given seed.

    Returns:
        A random integer in the inclusive range ``[low, high]``.

    Raises:
        ValueError: If ``low`` is greater than ``high``.

    Examples:
        >>> random_int(1, 10, seed=42) == random_int(1, 10, seed=42)
        True
    """
    if low > high:
        raise ValueError("low must be <= high")
    return _seed_rng(seed).randint(low, high)


def random_choice(items: Sequence[T], seed: Optional[int] = None) -> T:
    """Return a random element from ``items``.

    Args:
        items: A non-empty sequence to choose from.
        seed: Optional seed for reproducible results.

    Returns:
        A randomly selected element.

    Raises:
        ValueError: If ``items`` is empty.

    Examples:
        >>> random_choice(["a", "b", "c"], seed=0) in ("a", "b", "c")
        True
    """
    if len(items) == 0:
        raise ValueError("Cannot choose from an empty sequence")
    return _seed_rng(seed).choice(items)


def random_sample(items: Sequence[T], n: int, seed: Optional[int] = None) -> List[T]:
    """Return ``n`` unique elements sampled without replacement.

    Args:
        items: A sequence to sample from.
        n: The number of elements to sample.
        seed: Optional seed for reproducible results.

    Returns:
        A list of ``n`` randomly selected, unique elements.

    Raises:
        ValueError: If ``items`` is empty, if ``n`` is negative, or if
            ``n`` is greater than the number of items.

    Examples:
        >>> len(random_sample([1, 2, 3, 4], 2, seed=1))
        2
    """
    if len(items) == 0:
        raise ValueError("Cannot sample from an empty sequence")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n > len(items):
        raise ValueError("n cannot be greater than the number of items")
    return _seed_rng(seed).sample(list(items), n)


def random_shuffle(items: Sequence[T], seed: Optional[int] = None) -> List[T]:
    """Return a shuffled copy of ``items``.

    The original sequence is not modified.

    Args:
        items: The sequence to shuffle.
        seed: Optional seed for reproducible results.

    Returns:
        A new list containing the elements of ``items`` in random order.

    Raises:
        ValueError: If ``items`` is empty.

    Examples:
        >>> random_shuffle([1, 2, 3, 4], seed=7) != [1, 2, 3, 4]
        True
    """
    if len(items) == 0:
        raise ValueError("Cannot shuffle an empty sequence")
    shuffled = list(items)
    _seed_rng(seed).shuffle(shuffled)
    return shuffled


def weighted_choice(
    items: Sequence[T],
    weights: Sequence[float],
    seed: Optional[int] = None,
) -> T:
    """Return an element from ``items`` chosen with probability proportional to ``weights``.

    Args:
        items: A non-empty sequence to choose from.
        weights: A sequence of non-negative weights, one per item.
        seed: Optional seed for reproducible results.

    Returns:
        A randomly selected element, weighted by ``weights``.

    Raises:
        ValueError: If ``items`` is empty, if ``weights`` length does not
            match ``items`` length, or if any weight is negative.

    Examples:
        >>> weighted_choice(["a", "b"], [0, 1], seed=5) == "b"
        True
    """
    if len(items) == 0:
        raise ValueError("Cannot choose from an empty sequence")
    if len(weights) != len(items):
        raise ValueError("weights length must match items length")
    if any(w < 0 for w in weights):
        raise ValueError("weights must be non-negative")
    if sum(weights) == 0:
        raise ValueError("weights must sum to a positive value")
    return _seed_rng(seed).choices(items, weights=weights, k=1)[0]


def random_uniform(low: float, high: float, seed: Optional[int] = None) -> float:
    """Return a random floating-point number N such that ``low <= N <= high``.

    Args:
        low: The inclusive lower bound of the range.
        high: The inclusive upper bound of the range.
        seed: Optional seed for reproducible results.

    Returns:
        A random float in the inclusive range ``[low, high]``.

    Raises:
        ValueError: If ``low`` is greater than ``high``.

    Examples:
        >>> 0 <= random_uniform(0, 1, seed=11) <= 1
        True
    """
    if low > high:
        raise ValueError("low must be <= high")
    return _seed_rng(seed).uniform(low, high)


def random_gaussian(mu: float = 0.0, sigma: float = 1.0, seed: Optional[int] = None) -> float:
    """Return a random number drawn from a Gaussian (normal) distribution.

    Args:
        mu: The mean of the distribution.
        sigma: The standard deviation of the distribution.
        seed: Optional seed for reproducible results.

    Returns:
        A random float sampled from ``N(mu, sigma)``.

    Raises:
        ValueError: If ``sigma`` is negative.

    Examples:
        >>> isinstance(random_gaussian(seed=3), float)
        True
    """
    if sigma < 0:
        raise ValueError("sigma must be non-negative")
    return _seed_rng(seed).gauss(mu, sigma)


def random_bool(probability: float = 0.5, seed: Optional[int] = None) -> bool:
    """Return a random boolean with the given probability of being True.

    Args:
        probability: The probability of returning True in [0, 1].
        seed: Optional seed for reproducible results.

    Returns:
        True with probability ``probability``, False otherwise.

    Raises:
        TypeError: If ``probability`` is not a number.
        ValueError: If ``probability`` is outside [0, 1].

    Examples:
        >>> isinstance(random_bool(seed=1), bool)
        True
        >>> random_bool(1.0, seed=0)
        True
        >>> random_bool(0.0, seed=0)
        False
    """
    if isinstance(probability, bool) or not isinstance(probability, (int, float)):
        raise TypeError("probability must be a number")
    if probability < 0 or probability > 1:
        raise ValueError("probability must be between 0 and 1")
    return _seed_rng(seed).random() < probability


def random_choices(
    items: Sequence[T],
    weights: Optional[Sequence[float]] = None,
    k: int = 1,
    seed: Optional[int] = None,
) -> List[T]:
    """Return ``k`` elements chosen with replacement.

    Args:
        items: A non-empty sequence to choose from.
        weights: Optional sequence of non-negative weights, one per item.
        k: The number of elements to sample with replacement.
        seed: Optional seed for reproducible results.

    Returns:
        A list of ``k`` randomly selected elements (with replacement).

    Raises:
        ValueError: If ``items`` is empty, if ``k`` is negative, if
            ``weights`` length does not match ``items`` length, if any weight
            is negative, or if weights sum to zero.
        TypeError: If ``k`` is not an int.

    Examples:
        >>> len(random_choices([1, 2, 3], k=4, seed=1))
        4
        >>> random_choices(["x"], k=3, seed=0)
        ['x', 'x', 'x']
    """
    if len(items) == 0:
        raise ValueError("Cannot choose from an empty sequence")
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k must be an int")
    if k < 0:
        raise ValueError("k must be non-negative")
    if weights is not None:
        if len(weights) != len(items):
            raise ValueError("weights length must match items length")
        if any(w < 0 for w in weights):
            raise ValueError("weights must be non-negative")
        if sum(weights) == 0:
            raise ValueError("weights must sum to a positive value")
        return _seed_rng(seed).choices(items, weights=weights, k=k)
    return _seed_rng(seed).choices(items, k=k)


def coin_flip(seed: Optional[int] = None) -> bool:
    """Return a fair coin flip.

    Args:
        seed: Optional seed for reproducible results.

    Returns:
        True or False with equal probability.

    Examples:
        >>> isinstance(coin_flip(seed=2), bool)
        True
    """
    return random_bool(0.5, seed=seed)


# aliases
random_choice_with_replacement = random_choices


__all__: List[str] = [
    "coin_flip",
    "random_bool",
    "random_choice",
    "random_choice_with_replacement",
    "random_choices",
    "random_gaussian",
    "random_int",
    "random_sample",
    "random_shuffle",
    "random_uniform",
    "weighted_choice",
]
