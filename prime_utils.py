"""Prime number utilities."""

import math

from math_utils import is_prime

__all__ = [
    "prime_factors",
    "nth_prime",
    "primes_up_to",
    "next_prime",
    "previous_prime",
    "is_prime_power",
    "prime_sieve_of_eratosthenes",
]


def prime_factors(n: int) -> list[int]:
    """Return the prime factors of n in non-decreasing order.

    Args:
        n: The integer to factorize (n >= 2).

    Returns:
        A list of prime factors whose product is n.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n < 2.

    Examples:
        >>> prime_factors(12)
        [2, 2, 3]
        >>> prime_factors(17)
        [17]
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 2:
        raise ValueError("Prime factorization is only defined for integers >= 2")
    factors: list[int] = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    divisor = 3
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 2
    if n > 1:
        factors.append(n)
    return factors


def nth_prime(n: int) -> int:
    """Return the nth prime number (1-indexed).

    Args:
        n: The position of the prime to return (n >= 1).

    Returns:
        The nth prime number.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n < 1.

    Examples:
        >>> nth_prime(1)
        2
        >>> nth_prime(6)
        13
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError("nth_prime is only defined for n >= 1")
    count = 0
    candidate = 2
    while True:
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate
        candidate = 3 if candidate == 2 else candidate + 2


def primes_up_to(limit: int) -> list[int]:
    """Return all prime numbers less than or equal to limit.

    Args:
        limit: The upper bound (inclusive).

    Returns:
        A list of primes <= limit.

    Raises:
        TypeError: If limit is not an int.
    """
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError(f"limit must be an int, got {type(limit).__name__}")
    if limit < 2:
        return []
    return [p for p in range(2, limit + 1) if is_prime(p)]


def prime_sieve_of_eratosthenes(limit: int) -> list[int]:
    """Return all prime numbers up to and including limit using the sieve of Eratosthenes."""
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError(f"limit must be an int, got {type(limit).__name__}")
    if limit < 2:
        return []
    is_prime_arr = [True for _ in range(limit + 1)]
    p = 2
    primes = []
    while p * p <= limit:
        if is_prime_arr[p]:
            for i in range(p * p, limit + 1, p):
                is_prime_arr[i] = False
        p += 1

    for p_val in range(2, limit + 1):
        if is_prime_arr[p_val]:
            primes.append(p_val)
    return primes


def next_prime(n: int) -> int:
    """Return the smallest prime strictly greater than n.

    Args:
        n: The integer to start from.

    Returns:
        The next prime after n.

    Raises:
        TypeError: If n is not an int.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    candidate = n + 1
    if candidate <= 2:
        return 2
    if candidate % 2 == 0:
        candidate += 1
    while not is_prime(candidate):
        candidate += 2
    return candidate


def previous_prime(n: int) -> int:
    """Return the largest prime strictly less than n.

    Args:
        n: The integer to start from (n > 2).

    Returns:
        The previous prime before n.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n <= 2.

    Examples:
        >>> previous_prime(11)
        7
        >>> previous_prime(3)
        2
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n <= 2:
        raise ValueError("previous_prime is only defined for n > 2")
    candidate = n - 1
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 1
    raise ValueError("No prime found below n")


def is_prime_power(n: int) -> bool:
    """Return True if n is a prime power p^k for some prime p and integer k >= 2."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 4:
        return False
    # Try all possible exponents k >= 2 such that p^k <= n
    # Find max k
    max_k = int(math.log(n, 2))
    for k in range(max_k, 1, -1):
        # try integer root
        p_float = n ** (1.0 / k)
        p = round(p_float)
        if p < 2:
            continue
        # check a few values around p due to floating point
        for p_cand in {p - 1, p, p + 1}:
            if p_cand < 2:
                continue
            val = p_cand ** k
            if val == n and is_prime(p_cand):
                return True
            if val > n:
                break
    # Check prime bases
    for p in prime_sieve_of_eratosthenes(int(math.sqrt(n))):
        if p == 2 and n % 2 == 1:
            continue
        power = p
        k = 1
        while power < n:
            power *= p
            k += 1
            if k >= 2 and power == n:
                return True
        if power > n:
            break
    return False
