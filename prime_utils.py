"""Prime number utility functions."""

from __future__ import annotations

import math
from typing import List

__all__: List[str] = [
    "primes_up_to",
    "nth_prime",
    "prime_factors",
    "is_coprime",
]


def _require_int(value: object, name: str) -> int:
    """Validate that *value* is an int, raising ``TypeError`` otherwise."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def primes_up_to(n: int) -> List[int]:
    """Return all prime numbers up to and including *n* using the Sieve of Eratosthenes.

    Args:
        n: The upper bound (inclusive) of the prime search.

    Returns:
        A list of all prime numbers less than or equal to *n*.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    i = 2
    while i * i <= n:
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
        i += 1
    return [x for x, is_p in enumerate(sieve) if is_p]


def nth_prime(n: int) -> int:
    """Return the *n*-th prime number (1-indexed).

    Args:
        n: The 1-based index of the prime to return.

    Returns:
        The *n*-th prime number.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.
    """
    _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be >= 1")
    upper = max(10, n * 20)
    while True:
        primes = primes_up_to(upper)
        if len(primes) >= n:
            return primes[n - 1]
        upper *= 2


def prime_factors(n: int) -> List[int]:
    """Return the prime factorization of *n* as a list of prime factors.

    Args:
        n: The integer to factorize.

    Returns:
        A list of prime factors of *n*, in ascending order.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 2.
    """
    _require_int(n, "n")
    if n < 2:
        raise ValueError("n must be >= 2")
    factors: List[int] = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def is_coprime(a: int, b: int) -> bool:
    """Return True if *a* and *b* are coprime.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        True if the greatest common divisor of *a* and *b` is 1.

    Raises:
        TypeError: If *a* or *b* is not an int.
    """
    _require_int(a, "a")
    _require_int(b, "b")
    return math.gcd(a, b) == 1
