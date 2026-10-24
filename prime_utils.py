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
    "is_coprime",
    "gcd",
    "lcm",
    "phi",
]


def prime_factors(n: int) -> list[int]:
    """Return the prime factors of n in non-decreasing order.

    Args:
        n: A positive integer greater than 1.

    Returns:
        A list of prime factors of n.

    Raises:
        TypeError: If n is not an int.
        ValueError: If n is less than 2.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 2:
        raise ValueError("n must be >= 2")
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        if d == 2:
            d += 1
        else:
            d += 2
    if temp > 1:
        factors.append(temp)
    return factors


def prime_sieve_of_eratosthenes(limit: int) -> list[int]:
    """Return a list of prime numbers up to the specified limit."""
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


def nth_prime(n: int) -> int:
    """Return the nth prime number (1-indexed)."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError("n must be >= 1")
    count = 0
    num = 1
    while count < n:
        num += 1
        if is_prime(num):
            count += 1
    return num


def next_prime(n: int) -> int:
    """Return the smallest prime greater than n."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate


def previous_prime(n: int) -> int:
    """Return the largest prime less than n."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n <= 2:
        raise ValueError("no prime less than n")
    candidate = n - 1
    while candidate >= 2 and not is_prime(candidate):
        candidate -= 1
    if candidate < 2:
        raise ValueError("no prime less than n")
    return candidate


def primes_up_to(limit: int) -> list[int]:
    """Return all prime numbers up to limit."""
    return prime_sieve_of_eratosthenes(limit)


def is_prime_power(n: int) -> bool:
    """Return True if n is a prime power p^k for some prime p and integer k >= 2."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 4:
        return False
    max_k = int(math.log(n, 2))
    for k in range(max_k, 1, -1):
        p_float = n ** (1.0 / k)
        p = round(p_float)
        if p < 2:
            continue
        for p_cand in {p - 1, p, p + 1}:
            if p_cand < 2:
                continue
            val = p_cand ** k
            if val == n and is_prime(p_cand):
                return True
            if val > n:
                break
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


def is_coprime(a: int, b: int) -> bool:
    """Return True if a and b are coprime (gcd is 1)."""
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    return gcd(abs(a), abs(b)) == 1


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of a and b."""
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """Return the least common multiple of a and b."""
    if not isinstance(a, int) or isinstance(a, bool):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if not isinstance(b, int) or isinstance(b, bool):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    if a == 0 or b == 0:
        return 0
    return abs((a // gcd(a, b)) * b)


def phi(n: int) -> int:
    """Compute Euler's totient function phi for positive integer n."""
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError("n must be positive")
    result = n
    num = n
    p = 2
    while p * p <= num:
        if num % p == 0:
            while num % p == 0:
                num //= p
            result -= result // p
        if p == 2:
            p += 1
        else:
            p += 2
    if num > 1:
        result -= result // num
    return result
