"""Prime number utility functions."""

from __future__ import annotations

import math
from typing import List

__all__: List[str] = [
    "is_prime",
    "primes_up_to",
    "nth_prime",
    "prime_factors",
    "is_coprime",
    "next_prime",
    "prev_prime",
    "is_perfect_square",
]


def _require_int(value: object, name: str) -> int:
    """Validate that *value* is an int, raising ``TypeError`` otherwise."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def is_prime(n: int) -> bool:
    """Return True if *n* is a prime number.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


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


def next_prime(n: int) -> int:
    """Return the smallest prime number greater than or equal to *n*.

    Args:
        n: The lower bound for the search.

    Returns:
        The smallest prime >= *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If no such prime exists (n < 2 returns 2).
    """
    _require_int(n, "n")
    if n <= 2:
        return 2
    candidate = n if n % 2 != 0 else n + 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def prev_prime(n: int) -> int:
    """Return the largest prime number less than or equal to *n*.

    Args:
        n: The upper bound for the search.

    Returns:
        The largest prime <= *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If no prime <= *n* exists.
    """
    _require_int(n, "n")
    if n < 2:
        raise ValueError("n must be >= 2")
    candidate = n
    if candidate % 2 == 0 and candidate != 2:
        candidate -= 1
    while candidate >= 2 and not is_prime(candidate):
        candidate -= 2
    if candidate < 2:
        return 2
    return candidate


def is_coprime(a: int, b: int) -> bool:
    """Return True if *a* and *b* are coprime.

    Args:
        a: The first integer.
        b: The second integer.

    Returns:
        True if the greatest common divisor of *a* and *b* is 1.

    Raises:
        TypeError: If *a* or *b* is not an int.
    """
    _require_int(a, "a")
    _require_int(b, "b")
    return math.gcd(a, b) == 1


def is_perfect_square(n: int) -> bool:
    """Return True if *n* is a perfect square.

    A perfect square is a non-negative integer that is the square of an
    integer (e.g. 0, 1, 4, 9, 16). Negative integers are never perfect
    squares.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a perfect square, False otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_perfect_square(0)
        True
        >>> is_perfect_square(1)
        True
        >>> is_perfect_square(4)
        True
        >>> is_perfect_square(16)
        True
        >>> is_perfect_square(2)
        False
        >>> is_perfect_square(-4)
        False
    """
    _require_int(n, "n")
    if n < 0:
        return False
    root = math.isqrt(n)
    return root * root == n
