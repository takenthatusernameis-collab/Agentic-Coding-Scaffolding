"""Prime number utility functions."""

from __future__ import annotations

import math
from typing import List

__all__: List[str] = [
    "is_prime",
    "is_composite",
    "prime_factors",
    "nth_prime",
    "primes_up_to",
    "is_coprime",
    "next_prime",
    "prev_prime",
    "is_perfect_square",
    "is_power_of_two",
    "is_semiprime",
    "is_squarefree",
    "is_prime_power",
    "is_emirp",
    "is_twin_prime",
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


def is_composite(n: int) -> bool:
    """Return True if *n* is a composite number.

    A composite number is a positive integer that has at least one positive
    divisor other than one or itself (i.e. has more than two positive
    divisors). The number 1 is neither prime nor composite; 0 and all
    negative integers are neither prime nor composite.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is composite, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 1:
        return False
    if is_prime(n):
        return False
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


def is_power_of_two(n: int) -> bool:
    """Return True if *n* is a power of two.

    A power of two is a positive integer of the form 2^k for some
    non-negative integer *k* (so 1, 2, 4, 8, ... are powers of two).
    Zero and negative integers are never powers of two.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a power of two, False otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_power_of_two(1)
        True
        >>> is_power_of_two(16)
        True
        >>> is_power_of_two(18)
        False
        >>> is_power_of_two(0)
        False
    """
    _require_int(n, "n")
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def is_semiprime(n: int) -> bool:
    """Return True if *n* is a semiprime.

    A semiprime is a natural number that is the product of exactly two
    prime numbers. The two primes may be equal (so 4, 9, p^2 are
    semiprimes). Primes themselves are not semiprimes; 1, 0, and
    negative numbers are not semiprimes. Numbers with more than two
    prime factors counting multiplicity (like 8 = 2*2*2) are not
    semiprimes by this definition.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a semiprime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 3:
        return False
    if n == 4:
        return True
    factors = prime_factors(n)
    return len(factors) == 2


def is_squarefree(n: int) -> bool:
    """Return True if *n* is squarefree.

    A squarefree number is an integer which is divisible by no square
    of a prime number other than 1. In other words, in the prime
    factorization of the number, every prime factor appears at most
    once. Primes, 1, and numbers like 6=2*3 are squarefree; 4=2^2, 8=2^3,
    and 12=2^2*3 are not squarefree (because they are divisible by 4).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is squarefree, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n == 0:
        return False
    if n < 0:
        n = -n
    if n == 1:
        return True
    seen = set()
    for p in prime_factors(n):
        if p in seen:
            return False
        seen.add(p)
    return True


def is_prime_power(n: int) -> bool:
    """Return True if *n* is a prime power.

    A prime power is a positive integer that is a power of a single prime
    number. This includes prime numbers themselves (p^1) and prime powers
    like p^2, p^3, etc. By definition, 1 is not considered a prime power.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a prime power, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 1:
        return False
    if is_prime(n):
        return True
    if n < 0:
        n = -n
    if n <= 1:
        return False
    # Find integer k >= 2 such that there exists prime p with p^k == n
    # Find maximum possible exponent
    max_exp = n.bit_length()
    for k in range(2, max_exp + 1):
        # Try to find integer p = n^(1/k)
        p_float = n ** (1.0 / k)
        p = round(p_float)
        if p < 2:
            continue
        # Check p, p+0,p±1 due to floating point precision
        for candidate in [p - 1, p, p + 1]:
            if candidate < 2:
                continue
            pow_val = candidate ** k
            if pow_val == n and is_prime(candidate):
                return True
            if pow_val > n:
                break
    return False


def is_emirp(n: int) -> bool:
    """Return True if *n* is an emirp.

    An emirp (a prime spelled backwards) is a prime number that results
    in a different prime when its decimal digits are reversed. In other
    words, *n* is prime, its reverse *r* is prime, and *n != r*.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is an emirp, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    if n < 10:
        return False
    s = str(abs(n))
    r_s = s[::-1]
    if r_s == s:
        return False
    try:
        r = int(r_s)
    except ValueError:
        return False
    if r < 2:
        return False
    return is_prime(r)


def is_twin_prime(n: int) -> bool:
    """Return True if *n* is a twin prime.

    A twin prime is a prime number that is either 2 less or 2 more than
    another prime number. This function returns True if *n* is prime and
    either n+2 or n-2 is also prime.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a twin prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    return is_prime(n - 2) or is_prime(n + 2)
