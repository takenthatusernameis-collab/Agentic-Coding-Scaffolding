"""Prime number utility functions."""

__all__ = ["primes_up_to", "nth_prime", "prime_factors", "is_coprime"]


def primes_up_to(n: int) -> list[int]:
    """Return all prime numbers up to and including *n* using the Sieve of Eratosthenes."""
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
    """Return the *n*-th prime number (1-indexed)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    upper = max(10, n * 20)
    while True:
        primes = primes_up_to(upper)
        if len(primes) >= n:
            return primes[n - 1]
        upper *= 2


def prime_factors(n: int) -> list[int]:
    """Return the prime factorization of *n* as a list of prime factors."""
    if n < 2:
        raise ValueError("n must be >= 2")
    factors: list[int] = []
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
    """Return True if *a* and *b* are coprime."""
    import math

    return math.gcd(a, b) == 1
