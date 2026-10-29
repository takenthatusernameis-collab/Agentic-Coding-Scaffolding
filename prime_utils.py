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
    "is_circular_prime",
    "is_chen_prime",
    "next_prime",
    "prev_prime",
    "is_perfect_square",
    "is_power_of_two",
    "is_semiprime",
    "is_squarefree",
    "is_prime_power",
    "is_emirp",
    "is_twin_prime",
    "is_palindromic_prime",
    "is_mersenne_prime",
    "is_sophie_germain_prime",
    "is_safe_prime",
    "sum_of_proper_divisors",
    "aliquot_sum",
    "is_perfect_number",
    "is_abundant_number",
    "is_deficient_number",
    "is_cousin_prime",
    "is_pythagorean_prime",
    "is_sexy_prime",
    "radical",
    "prime_count",
    "prime_gap",
    "primorial",
    "total_prime_factors",
    "distinct_prime_factors",
    "largest_prime_factor",
    "is_automorphic",
    "coprime",
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


# Alias
coprime = is_coprime



def is_circular_prime(n: int) -> bool:
    """Return True if *n* is a circular prime.

    A circular prime is a prime number that remains prime under every
    cyclic rotation of its decimal digits (e.g. 197, because 197, 971,
    and 719 are all prime). Single-digit primes are circular primes.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a circular prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_circular_prime(2)
        True
        >>> is_circular_prime(197)
        True
        >>> is_circular_prime(23)
        False
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    digits = str(n)
    for i in range(len(digits)):
        rotation = int(digits[i:] + digits[:i])
        if not is_prime(rotation):
            return False
    return True


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


def is_palindromic_prime(n: int) -> bool:
    """Return True if *n* is a palindromic prime.

    A palindromic prime is a prime number that is also a palindromic
    number in base 10, meaning its decimal representation reads the same
    forwards and backwards (e.g., 2, 3, 5, 7, 11, 101, 131, ...).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a palindromic prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    s = str(abs(n))
    return s == s[::-1]


def is_mersenne_prime(n: int) -> bool:
    """Return True if *n* is a Mersenne prime.

    A Mersenne prime is a prime number of the form M_p = 2^p - 1
    for some prime number *p*. Known examples include 3 (2^2-1),
    7 (2^3-1), 31 (2^5-1), 127 (2^7-1), etc.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a Mersenne prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    if n == 3:
        return True  # 2^2 - 1, p=2 (prime)
    if n < 7:
        return False
    # n = 2^p - 1 implies p = log2(n+1)
    m = n + 1
    if m <= 0 or (m & (m - 1)) != 0:
        return False
    # Find exponent p
    p = m.bit_length() - 1
    # Verify m == 2^p
    if (1 << p) != m:
        return False
    if p < 2:
        return False
    return is_prime(p)


def is_sophie_germain_prime(n: int) -> bool:
    """Return True if *n* is a Sophie Germain prime.

    A Sophie Germain prime is a prime number *p* such that 2*p + 1 is also
    prime (the latter is called a safe prime).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a Sophie Germain prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    return is_prime(2 * n + 1)


def is_safe_prime(n: int) -> bool:
    """Return True if *n* is a safe prime.

    A safe prime is a prime number *p* such that (p - 1) / 2 is also prime
    (the latter is called a Sophie Germain prime).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a safe prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    if n < 5:
        return False
    return is_prime((n - 1) // 2)


def is_chen_prime(n: int) -> bool:
    """Return True if *n* is a Chen prime.

    A Chen prime is a prime number *p* such that *p + 2* is either a prime
    or a semiprime (a product of exactly two prime numbers, counting
    multiplicity). This is connected to Chen's theorem, which states that
    every sufficiently large even integer is the sum of a prime and a
    semiprime.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a Chen prime, False otherwise. Non-prime integers
        are never Chen primes.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_chen_prime(2)
        True
        >>> is_chen_prime(3)
        True
        >>> is_chen_prime(7)
        True
        >>> is_chen_prime(43)
        False
    """
    _require_int(n, "n")
    if not is_prime(n):
        return False
    return is_prime(n + 2) or is_semiprime(n + 2)


def sum_of_proper_divisors(n: int) -> int:
    """Return the sum of proper divisors of *n*.

    Proper divisors are positive divisors other than *n* itself.

    Args:
        n: The integer to sum proper divisors of.

    Returns:
        The sum of proper positive divisors of *n*.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 1:
        return 0
    total = 0
    for i in range(1, int(math.sqrt(abs(n))) + 1):
        if n % i == 0:
            a = i
            b = n // i
            if a < abs(n):
                total += a
            if b != a and b < abs(n):
                total += b
    return total


aliquot_sum = sum_of_proper_divisors


def is_perfect_number(n: int) -> bool:
    """Return True if *n* is a perfect number.

    A perfect number is a positive integer that is equal to the sum of its
    proper positive divisors (e.g., 6, 28, 496, 8128).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is perfect, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 0:
        return False
    return sum_of_proper_divisors(n) == n


def is_abundant_number(n: int) -> bool:
    """Return True if *n* is an abundant number.

    An abundant number is a number for which the sum of its proper divisors
    is greater than the number itself (e.g., 12, 18, 20, 24).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is abundant, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 0:
        return False
    return sum_of_proper_divisors(n) > n


def is_deficient_number(n: int) -> bool:
    """Return True if *n* is a deficient number.

    A deficient number is a number for which the sum of its proper divisors
    is less than the number itself (e.g., 1, 2, 3, 4, 5, 7, ...). All primes
    and prime powers are deficient.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is deficient, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n <= 0:
        return False
    return sum_of_proper_divisors(n) < n


def is_cousin_prime(n: int) -> bool:
    """Return True if *n* is a cousin prime.

    A cousin prime is a prime that is a member of a pair of primes that
    differ by 4 (e.g., 3 and 7, 7 and 11, 13 and 17).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a cousin prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n < 2:
        return False
    if not is_prime(n):
        return False
    return is_prime(n - 4) or is_prime(n + 4)


def is_pythagorean_prime(n: int) -> bool:
    """Return True if *n* is a Pythagorean prime.

    A Pythagorean prime is a prime number of the form 4*k + 1 (e.g., 5, 13, 17, 41).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a Pythagorean prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n < 2:
        return False
    if not is_prime(n):
        return False
    return n % 4 == 1


def is_sexy_prime(n: int) -> bool:
    """Return True if *n* is a sexy prime.

    A sexy prime is a prime that is a member of a pair of primes that
    differ by 6 (e.g., 5 and 11, 7 and 13, 11 and 17).

    Args:
        n: The integer to test.

    Returns:
        True if *n* is a sexy prime, False otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n < 2:
        return False
    if not is_prime(n):
        return False
    return is_prime(n - 6) or is_prime(n + 6)


def prime_count(n: int) -> int:
    """Return the number of prime numbers less than or equal to *n*.

    This is the prime counting function, commonly denoted π(*n*). It
    returns 0 for any integer *n* less than 2.

    Args:
        n: The upper bound (inclusive) of the prime count.

    Returns:
        The count of primes less than or equal to *n*.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if n < 2:
        return 0
    return len(primes_up_to(n))


def prime_gap(n: int) -> int:
    """Return the gap between *n* and the next prime after *n*.

    The prime gap is the difference between the next prime greater than *n*
    and *n* itself. If *n* is already prime, this returns the gap to the
    prime immediately after *n* (i.e. ``next_prime(n + 1) - n``).

    Args:
        n: The integer to measure the gap from.

    Returns:
        The difference between the next prime after *n* and *n*.

    Raises:
        TypeError: If *n* is not an int.
    """
    _require_int(n, "n")
    if is_prime(n):
        p = next_prime(n + 1)
    else:
        p = next_prime(n)
    return p - n


def radical(n: int) -> int:
    """Return the radical of *n* (product of the distinct prime factors).

    The radical rad(n) is the product of the distinct prime numbers
    dividing *n*.

    Args:
        n: The integer to analyze.

    Returns:
        The product of the distinct prime factors of *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.
    """
    _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 1
    result = 1
    d = 2
    remaining = n
    if remaining % 2 == 0:
        result *= 2
        while remaining % 2 == 0:
            remaining //= 2
    d = 3
    while d * d <= remaining:
        if remaining % d == 0:
            result *= d
            while remaining % d == 0:
                remaining //= d
        d += 2
    if remaining > 1:
        result *= remaining
    return result


def primorial(n: int) -> int:
    """Return the primorial of *n*.

    The primorial *n#* is the product of all prime numbers less than or
    equal to *n*. For example, ``5# = 2 * 3 * 5 = 30`` and
    ``0# = 1# = 1``.

    Args:
        n: The upper bound for primes to multiply together.

    Returns:
        The product of all primes <= *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 0.
    """
    _require_int(n, "n")
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return 1
    result = 1
    for p in primes_up_to(n):
        result *= p
    return result


def total_prime_factors(n: int) -> int:
    """Return the total number of prime factors of *n* with multiplicity.

    This is the arithmetic function ``Omega(n)``: for example,
    ``total_prime_factors(12) == 3`` because ``12 = 2 * 2 * 3``.

    Args:
        n: The integer to analyze.

    Returns:
        The number of prime factors of *n* counted with multiplicity.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.
    """
    _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 0
    count = 0
    remaining = n
    if remaining % 2 == 0:
        while remaining % 2 == 0:
            remaining //= 2
            count += 1
    d = 3
    while d * d <= remaining:
        while remaining % d == 0:
            remaining //= d
            count += 1
        d += 2
    if remaining > 1:
        count += 1
    return count


def distinct_prime_factors(n: int) -> int:
    """Return the number of distinct prime factors of *n*.

    This is the arithmetic function ``omega(n)``: for example,
    ``distinct_prime_factors(12) == 2`` because ``12 = 2 * 2 * 3``.

    Args:
        n: The integer to analyze.

    Returns:
        The number of distinct prime factors of *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.
    """
    _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 0
    count = 0
    remaining = n
    if remaining % 2 == 0:
        count += 1
        while remaining % 2 == 0:
            remaining //= 2
    d = 3
    while d * d <= remaining:
        if remaining % d == 0:
            count += 1
            while remaining % d == 0:
                remaining //= d
        d += 2
    if remaining > 1:
        count += 1
    return count


def largest_prime_factor(n: int) -> int:
    """Return the largest prime factor of *n*.

    Args:
        n: The positive integer to factor.

    Returns:
        The largest prime factor of *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.

    Examples:
        >>> largest_prime_factor(12)
        3
        >>> largest_prime_factor(17)
        17
        >>> largest_prime_factor(1)
        Traceback (most recent call last):
        ...
        ValueError: n must be >= 1
    """
    _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        raise ValueError("n must be >= 2")
    largest = 0
    remaining = n
    if remaining % 2 == 0:
        largest = 2
        while remaining % 2 == 0:
            remaining //= 2
    d = 3
    while d * d <= remaining:
        if remaining % d == 0:
            largest = d
            while remaining % d == 0:
                remaining //= d
        d += 2
    if remaining > 1:
        largest = remaining
    return largest


def is_automorphic(n: int) -> bool:
    """Return True if *n* is an automorphic number.

    An automorphic number is a non-negative integer whose square ends with
    the decimal representation of the number itself (e.g. 5, because
    ``5 * 5 = 25`` ends in 5; 25, because ``25 * 25 = 625`` ends in 25).
    Zero is automorphic.

    Args:
        n: The integer to test.

    Returns:
        True if *n* is automorphic, False otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_automorphic(0)
        True
        >>> is_automorphic(5)
        True
        >>> is_automorphic(6)
        True
        >>> is_automorphic(25)
        True
        >>> is_automorphic(7)
        False
        >>> is_automorphic(10)
        False
    """
    _require_int(n, "n")
    if n < 0:
        return False
    square = n * n
    return str(square).endswith(str(n))
