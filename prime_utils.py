"""Prime number utilities."""

from math_utils import is_prime


def prime_factors(n: int) -> list[int]:
    """Return the prime factors of n in non-decreasing order.

    Args:
        n: The integer to factorize (n >= 2).

    Returns:
        A list of prime factors whose product is n.

    Raises:
        ValueError: If n < 2.

    Examples:
        >>> prime_factors(12)
        [2, 2, 3]
        >>> prime_factors(17)
        [17]
    """
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
        ValueError: If n < 1.

    Examples:
        >>> nth_prime(1)
        2
        >>> nth_prime(6)
        13
    """
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

    Examples:
        >>> primes_up_to(10)
        [2, 3, 5, 7]
    """
    if limit < 2:
        return []
    return [p for p in range(2, limit + 1) if is_prime(p)]


def next_prime(n: int) -> int:
    """Return the smallest prime strictly greater than n.

    Args:
        n: The integer to start from.

    Returns:
        The next prime after n.

    Examples:
        >>> next_prime(7)
        11
        >>> next_prime(1)
        2
    """
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
        ValueError: If n <= 2.

    Examples:
        >>> previous_prime(11)
        7
        >>> previous_prime(3)
        2
    """
    if n <= 2:
        raise ValueError("previous_prime is only defined for n > 2")
    candidate = n - 1
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 1
    raise ValueError("No prime found below n")
