"""Utilities for numeric abstract base classes (wrapping :mod:`numbers`).

This module re-exports the numeric abstract base classes of the standard
library :mod:`numbers` module and adds small, hermetic predicates that work
for any object, regardless of whether it is registered with the ABC system.
Every helper validates its arguments before the computation starts, so a
caller gets a clear :class:`TypeError` instead of an opaque failure.
"""

from __future__ import annotations

import math
import numbers as _numbers

__all__: list[str] = [
    "Number",
    "Complex",
    "Real",
    "Rational",
    "Integral",
    "is_number",
    "is_integral",
    "is_complex",
    "is_real",
    "is_rational",
    "is_perfect_number",
    "is_almost_perfect_number",
    "is_semiperfect_number",
    "is_abundant_number",
    "is_deficient_number",
    "is_strong_number",
    "is_harshad_number",
    "is_neon_number",
    "is_armstrong_number",
    "is_automorphic_number",
    "is_disarium_number",
    "is_happy_number",
    "is_pronic_number",
    "is_pandigital_number",
    "is_spy_number",
    "is_polydivisible_number",
    "is_repdigit_number",
    "is_palindromic_number",
    "is_coprime",
    "is_duck_number",
    "is_odious_number",
    "is_evil_number",
    "is_perfect_power",
    "is_kaprekar_number",
    "is_perfect_square",
    "is_perfect_cube",
    "is_power_of_two",
    "is_triangular_number",
    "is_pentagonal_number",
    "is_hexagonal_number",
    "is_squarefree_number",
    "is_oblong_number",
    "is_ugly_number",
    "is_narcissistic_number",
    "is_narcissistic",
    "proper_divisors",
]

#: The abstract base class for all numbers.
Number = _numbers.Number

#: The abstract base class for complex numbers.
Complex = _numbers.Complex

#: The abstract base class for real numbers.
Real = _numbers.Real

#: The abstract base class for rational numbers.
Rational = _numbers.Rational

#: The abstract base class for integral numbers.
Integral = _numbers.Integral


def is_number(obj: object) -> bool:
    """Return ``True`` when *obj* is a number.

    A number is any object registered with (or subclass of) the
    :class:`numbers.Number` abstract base class, which covers ``int``,
    ``float``, ``complex``, ``Fraction``, ``Decimal``, and similar types.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is a number, ``False`` otherwise.

    Examples:
        >>> is_number(5)
        True
        >>> is_number(1.5)
        True
        >>> is_number(2 + 3j)
        True
        >>> is_number("x")
        False
    """
    return isinstance(obj, Number)


def is_integral(obj: object) -> bool:
    """Return ``True`` when *obj* is an integral number.

    An integral number is any object registered with (or subclass of) the
    :class:`numbers.Integral` abstract base class, which covers ``int``,
    ``bool``, and other exact integer-like types, but not ``float`` or
    ``complex``.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is an integral number, ``False`` otherwise.

    Examples:
        >>> is_integral(5)
        True
        >>> is_integral(True)
        True
        >>> is_integral(1.5)
        False
        >>> is_integral("x")
        False
    """
    return isinstance(obj, Integral)


def is_complex(obj: object) -> bool:
    """Return ``True`` when *obj* is a complex number.

    A complex number is any object registered with (or subclass of) the
    :class:`numbers.Complex` abstract base class, which covers ``int``,
    ``float``, ``complex``, and similar types. Every real number is also a
    complex number.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is a complex number, ``False`` otherwise.

    Examples:
        >>> is_complex(5)
        True
        >>> is_complex(1.5)
        True
        >>> is_complex(2 + 3j)
        True
        >>> is_complex("x")
        False
    """
    return isinstance(obj, Complex)


def is_real(obj: object) -> bool:
    """Return ``True`` when *obj* is a real number.

    A real number is any object registered with (or subclass of) the
    :class:`numbers.Real` abstract base class, which covers ``int``,
    ``float``, ``Fraction``, ``Decimal``, and similar types, but not
    ``complex`` with a non-zero imaginary part.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is a real number, ``False`` otherwise.

    Examples:
        >>> is_real(5)
        True
        >>> is_real(1.5)
        True
        >>> is_real(2 + 3j)
        False
        >>> is_real("x")
        False
    """
    return isinstance(obj, Real)


def is_rational(obj: object) -> bool:
    """Return ``True`` when *obj* is a rational number.

    A rational number is any object registered with (or subclass of) the
    :class:`numbers.Rational` abstract base class, which covers ``int``,
    ``Fraction``, and similar exact types, but not ``float`` or ``complex``.

    Args:
        obj: The value to test.

    Returns:
        ``True`` if *obj* is a rational number, ``False`` otherwise.

    Examples:
        >>> is_rational(5)
        True
        >>> is_rational(1.5)
        False
        >>> is_rational(2 + 3j)
        False
        >>> is_rational("x")
        False
    """
    return isinstance(obj, Rational)


def is_abundant_number(n: int) -> bool:
    """Return ``True`` when *n* is an abundant number.

    An abundant number is a positive integer whose sum of proper divisors
    (the divisors excluding the number itself) is greater than the number.
    The smallest abundant number is 12 (= 1 + 2 + 3 + 4 + 6).

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an abundant number, ``False`` otherwise. Numbers
        below 2 are never abundant.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_abundant_number(12)
        True
        >>> is_abundant_number(24)
        True
        >>> is_abundant_number(6)
        False
        >>> is_abundant_number(1)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 2:
        return False
    total = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate:
                total += other
        candidate += 1
    return bool(total > n)


def is_deficient_number(n: int) -> bool:
    """Return ``True`` when *n* is a deficient number.

    A deficient number is a positive integer whose sum of proper divisors
    (the divisors excluding the number itself) is less than the number.
    The smallest deficient number is 1 (sum is 0) and most numbers are
    deficient; primes p have sum of proper divisors 1 < p for p > 1.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a deficient number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_deficient_number(1)
        True
        >>> is_deficient_number(2)
        True
        >>> is_deficient_number(4)
        True
        >>> is_deficient_number(6)
        False
        >>> is_deficient_number(12)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    if n == 1:
        return True
    total = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate:
                total += other
        candidate += 1
    return bool(total < n)


def is_perfect_number(n: int) -> bool:
    """Return ``True`` when *n* is a perfect number.

    A perfect number is a positive integer that is equal to the sum of its
    proper positive divisors (the divisors excluding the number itself).
    The first few perfect numbers are 6, 28, 496, 8128, ...

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a perfect number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_perfect_number(6)
        True
        >>> is_perfect_number(28)
        True
        >>> is_perfect_number(496)
        True
        >>> is_perfect_number(12)
        False
        >>> is_perfect_number(1)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    if n == 1:
        return False
    total = 1
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            total += candidate
            other = n // candidate
            if other != candidate:
                total += other
        candidate += 1
    return bool(total == n)


def is_almost_perfect_number(n: int) -> bool:
    """Return ``True`` when *n* is an almost perfect number.

    An almost perfect number is a positive integer whose sum of proper
    divisors equals the number minus one (``sum(proper_divisors(n)) == n - 1``).
    The known almost perfect numbers are the powers of two (1, 2, 4, 8, 16, ...);
    it is conjectured that no others exist.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an almost perfect number, ``False`` otherwise.
        Numbers below 1 are never almost perfect.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_almost_perfect_number(1)
        True
        >>> is_almost_perfect_number(2)
        True
        >>> is_almost_perfect_number(4)
        True
        >>> is_almost_perfect_number(8)
        True
        >>> is_almost_perfect_number(16)
        True
        >>> is_almost_perfect_number(6)
        False
        >>> is_almost_perfect_number(0)
        False
        >>> is_almost_perfect_number(-4)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    return sum(proper_divisors(n)) == n - 1


def is_semiperfect_number(n: int) -> bool:
    """Return ``True`` when *n* is a semiperfect number.

    A semiperfect number is a positive integer that can be expressed as the
    sum of some (but not necessarily all) of its proper divisors. Every
    multiple of a semiperfect number is also semiperfect, and every
    abundant number that is not weird is semiperfect. Perfect numbers are
    semiperfect (they equal the sum of all of their proper divisors).

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is semiperfect, ``False`` otherwise. Numbers below
        1 are never semiperfect.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_semiperfect_number(12)
        True
        >>> is_semiperfect_number(18)
        True
        >>> is_semiperfect_number(20)
        True
        >>> is_semiperfect_number(6)
        True
        >>> is_semiperfect_number(28)
        True
        >>> is_semiperfect_number(70)
        False
        >>> is_semiperfect_number(2)
        False
        >>> is_semiperfect_number(4)
        False
        >>> is_semiperfect_number(7)
        False
        >>> is_semiperfect_number(0)
        False
        >>> is_semiperfect_number(-12)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    divisors = proper_divisors(n)
    # Subset-sum check: can some subset of proper divisors sum to n?
    # Use a dynamic-programming approach bounded by n to keep it efficient.
    reachable = {0}
    for d in divisors:
        if d > n:
            continue
        new_values = set()
        for total in reachable:
            s = total + d
            if s == n:
                return True
            if s < n:
                new_values.add(s)
        reachable.update(new_values)
    return False


def is_spy_number(n: int) -> bool:
    """Return ``True`` when *n* is a spy number.

    A spy number is a positive integer whose sum of decimal digits equals
    the product of its decimal digits. For example, ``1124`` has digit sum
    ``1 + 1 + 2 + 4 = 8`` and digit product ``1 * 1 * 2 * 4 = 8``.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a spy number, ``False`` otherwise. Numbers
        below 1 are never spy numbers.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_spy_number(123)
        True
        >>> is_spy_number(1124)
        True
        >>> is_spy_number(22)
        True
        >>> is_spy_number(1234)
        False
        >>> is_spy_number(0)
        False
        >>> is_spy_number(-123)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    digits = str(n)
    total = 0
    product = 1
    for d in digits:
        digit = ord(d) - ord("0")
        total += digit
        product *= digit
    return bool(total == product)


def proper_divisors(n: int) -> list[int]:
    """Return the proper divisors of *n* (divisors excluding *n* itself).

    Args:
        n: The positive integer whose proper divisors are returned.

    Returns:
        A sorted list of the proper divisors of *n*.

    Raises:
        TypeError: If *n* is not an int.
        ValueError: If *n* is less than 1.

    Examples:
        >>> proper_divisors(1)
        []
        >>> proper_divisors(6)
        [1, 2, 3]
        >>> proper_divisors(28)
        [1, 2, 4, 7, 14]
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        raise ValueError(f"n must be a positive integer, got {n}")
    if n == 1:
        return []
    result = [1]
    candidate = 2
    while candidate * candidate <= n:
        if n % candidate == 0:
            result.append(candidate)
            other = n // candidate
            if other != candidate and other != n:
                result.append(other)
        candidate += 1
    result = sorted(set(result))
    if n in result:
        result.remove(n)
    return result


def is_strong_number(n: int) -> bool:
    """Return ``True`` when *n* is a strong number.

    A strong number (also called a factorial number) is a positive integer
    whose sum of the factorial of its digits is equal to the number itself.
    The first few strong numbers are 1, 2, 145, 40585, 40585, ...

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a strong number, ``False`` otherwise. Numbers
        below 1 are never strong.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_strong_number(1)
        True
        >>> is_strong_number(2)
        True
        >>> is_strong_number(145)
        True
        >>> is_strong_number(40585)
        True
        >>> is_strong_number(123)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False

    def _factorial(x: int) -> int:
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result

    total = 0
    for digit in str(n):
        total += _factorial(int(digit))
    return bool(total == n)


def is_harshad_number(n: int) -> bool:
    """Return ``True`` when *n* is a harshad (Niven) number.

    A harshad number is an integer divisible by the sum of its decimal
    digits. Also known as a Niven number.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is divisible by the sum of its digits,
        ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_harshad_number(18)
        True
        >>> is_harshad_number(19)
        False
        >>> is_harshad_number(1)
        True
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n == 0:
        return True
    digit_sum = sum(int(d) for d in str(abs(n)))
    if digit_sum == 0:
        return False
    return n % digit_sum == 0


def is_neon_number(n: int) -> bool:
    """Return ``True`` when *n* is a neon number.

    A neon number is a number where the sum of the digits of its square is
    equal to the number itself (e.g. 9 is neon because 9^2 = 81 and 8 + 1 = 9).
    The only neon numbers are 0, 1, and 9.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a neon number, ``False`` otherwise. Numbers below 0
        are never neon.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_neon_number(9)
        True
        >>> is_neon_number(1)
        True
        >>> is_neon_number(0)
        True
        >>> is_neon_number(45)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    total = sum(int(d) for d in str(n * n))
    return bool(total == n)


def is_armstrong_number(n: int) -> bool:
    """Return ``True`` when *n* is an Armstrong (narcissistic) number.

    An Armstrong number is a number that is equal to the sum of its own
    digits each raised to the power of the number of digits.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an Armstrong number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_armstrong_number(153)
        True
        >>> is_armstrong_number(370)
        True
        >>> is_armstrong_number(371)
        True
        >>> is_armstrong_number(407)
        True
        >>> is_armstrong_number(123)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    digits = str(n)
    power = len(digits)
    total = sum(int(d) ** power for d in digits)
    return bool(total == n)


def is_automorphic_number(n: int) -> bool:
    """Return ``True`` when *n* is an automorphic number.

    An automorphic number is a number whose square ends with the same
    digits as the number itself. For example, 5^2 = 25 ends with 5,
    25^2 = 625 ends with 25.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an automorphic number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_automorphic_number(5)
        True
        >>> is_automorphic_number(6)
        True
        >>> is_automorphic_number(25)
        True
        >>> is_automorphic_number(76)
        True
        >>> is_automorphic_number(2)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    square = str(n * n)
    num_str = str(n)
    return square.endswith(num_str)


def is_happy_number(n: int) -> bool:
    """Return ``True`` when *n* is a happy number.

    A happy number is a positive integer that, when replaced by the sum of
    the squares of its decimal digits repeatedly, eventually reaches 1. A
    number that enters a cycle not containing 1 is unhappy. Zero is happy.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is happy, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_happy_number(1)
        True
        >>> is_happy_number(7)
        True
        >>> is_happy_number(19)
        True
        >>> is_happy_number(2)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    seen: set[int] = set()
    current = n
    while current != 1 and current not in seen:
        seen.add(current)
        current = sum(int(d) * int(d) for d in str(current))
    return current == 1


def is_disarium_number(n: int) -> bool:
    """Return ``True`` when *n* is a disarium number.

    A disarium number is an integer whose sum of its digits each raised to
    the power of its 1-based position equals the number itself. For example,
    135 is disarium because 1^1 + 3^2 + 5^3 = 1 + 9 + 125 = 135.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a disarium number, ``False`` otherwise. Numbers
        below 0 are never disarium.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_disarium_number(135)
        True
        >>> is_disarium_number(89)
        True
        >>> is_disarium_number(175)
        True
        >>> is_disarium_number(10)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    digits = str(n)
    total = sum(int(d) ** (i + 1) for i, d in enumerate(digits))
    return bool(total == n)


def is_pronic_number(n: int) -> bool:
    """Return ``True`` when *n* is a pronic number.

    A pronic number (also called a rectangular number) is the product of
    two consecutive integers ``n = k * (k + 1)`` for some integer ``k``.
    Pronic numbers are always even except ``0``. Zero and negative numbers
    are not pronic.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is pronic, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_pronic_number(0)
        False
        >>> is_pronic_number(2)
        True
        >>> is_pronic_number(6)
        True
        >>> is_pronic_number(12)
        True
        >>> is_pronic_number(4)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return False
    import math

    k = math.isqrt(n)
    return bool(k * (k + 1) == n or (k + 1) * k == n)


def is_polydivisible_number(n: int) -> bool:
    """Return ``True`` when *n* is a polydivisible number.

    A polydivisible number is a number where the first *k* digits form a
    number divisible by *k* for all *k* from 1 to the number of digits.
    Numbers below 0 are never polydivisible. Single or zero-digit numbers:
    0 is often considered polydivisible in some definitions; following
    common convention this returns ``True`` only for non-negative integers
    where every prefix passes the divisibility test.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a polydivisible number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_polydivisible_number(1)
        True
        >>> is_polydivisible_number(12)
        True
        >>> is_polydivisible_number(123)
        True
        >>> is_polydivisible_number(100)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    s = str(n)
    num = 0
    for i in range(1, len(s) + 1):
        num = num * 10 + int(s[i - 1])
        if num % i != 0:
            return False
    return True


def is_perfect_power(n: int) -> bool:
    """Return ``True`` if *n* is a perfect power.

    A perfect power is a positive integer that can be expressed as an
    integer power of another positive integer with exponent >= 2.
    By this definition, 1 is not considered a perfect power.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n <= 1:
        return False
    max_exp = n.bit_length()
    for b in range(2, max_exp + 1):
        a_float = n ** (1.0 / b)
        a = round(a_float)
        if a < 2:
            continue
        for candidate in (a - 1, a, a + 1):
            if candidate < 2:
                continue
            try:
                if candidate**b == n:
                    return True
            except OverflowError:
                continue
    return False


def _gcd_int(a: int, b: int) -> int:
    """Compute GCD of two non-negative ints."""
    a = abs(a)
    b = abs(b)
    while b:
        a, b = b, a % b
    return a


def is_coprime(a: int, b: int) -> bool:
    """Return ``True`` if *a* and *b* are coprime (gcd is 1)."""
    if isinstance(a, bool) or not isinstance(a, int):
        raise TypeError(f"a must be an int, got {type(a).__name__}")
    if isinstance(b, bool) or not isinstance(b, int):
        raise TypeError(f"b must be an int, got {type(b).__name__}")
    return _gcd_int(a, b) == 1


def is_palindromic_number(n: int) -> bool:
    """Return ``True`` when *n* is a palindromic number in base 10.

    A palindromic number reads the same forward and backward. Negative
    numbers are not considered palindromes.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("n must be non-negative")
    s = str(n)
    return s == s[::-1]


def is_repdigit_number(n: int) -> bool:
    """Return ``True`` when *n* is a repdigit number."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    s = str(n)
    if not s:
        return False
    return all(d == s[0] for d in s)


def is_pandigital_number(n: int, base: int = 10) -> bool:
    """Return ``True`` when *n* is a pandigital number in the given *base*.

    A pandigital number uses every digit of the base at least once in its
    representation. For base *b* the digits are ``0`` through ``b - 1``; for
    example 1023456789 is pandigital in base 10 and ``012`` (i.e. 12) is
    pandigital in base 4. Negative numbers are never pandigital, and a
    representation that omits any required digit returns ``False``.

    Args:
        n: The integer to test.
        base: The radix whose digit set must all appear. Must be between 2
            and 36 (inclusive).

    Returns:
        ``True`` if *n* is pandigital in *base*, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int or *base* is not an int.
        ValueError: If *base* is outside the range 2..36.

    Examples:
        >>> is_pandigital_number(1023456789)
        True
        >>> is_pandigital_number(1234567890)
        True
        >>> is_pandigital_number(12345)
        False
        >>> is_pandigital_number(75, base=4)
        True
        >>> is_pandigital_number(1023456789, base=9)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if isinstance(base, bool) or not isinstance(base, int):
        raise TypeError(f"base must be an int, got {type(base).__name__}")
    if base < 2 or base > 36:
        raise ValueError(f"base must be between 2 and 36, got {base}")
    if n < 0:
        return False
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return base == 2
    seen: set[str] = set()
    value = n
    while value > 0:
        seen.add(digits[value % base])
        value //= base
    expected = {digits[d] for d in range(base)}
    return expected.issubset(seen)


def is_kaprekar_number(n: int) -> bool:
    """Return ``True`` when *n* is a Kaprekar number.

    A Kaprekar number is a non-negative integer whose square can be split
    into two parts that sum to the original number. The right part has as
    many digits as *n* (or one fewer for a perfect square split); for example
    45 is Kaprekar because 45 ** 2 == 2025 and 20 + 25 == 45.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a Kaprekar number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_kaprekar_number(45)
        True
        >>> is_kaprekar_number(297)
        True
        >>> is_kaprekar_number(10)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    square = n * n
    s = str(square)
    for i in range(1, len(s)):
        left = s[:i]
        right = s[i:]
        if right.lstrip("0") == "":
            continue
        if int(left or "0") + int(right) == n:
            return True
    return False


def is_duck_number(n: int) -> bool:
    """Return ``True`` when *n* is a duck number.

    A duck number is a number that contains at least one zero digit but does
    not start with zero (e.g. 101, 203).

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a duck number, ``False`` otherwise. Numbers below 0
        are never duck numbers.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_duck_number(101)
        True
        >>> is_duck_number(203)
        True
        >>> is_duck_number(123)
        False
        >>> is_duck_number(0)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    s = str(n)
    return "0" in s[1:]


def is_odious_number(n: int) -> bool:
    """Return ``True`` when *n* is an odious number.

    An odious number is a non-negative integer with an odd number of 1s
    in its binary representation.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an odious number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_odious_number(1)
        True
        >>> is_odious_number(2)
        True
        >>> is_odious_number(3)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    return bin(n).count("1") % 2 == 1


def is_evil_number(n: int) -> bool:
    """Return ``True`` when *n* is an evil number.

    An evil number is a non-negative integer with an even number of 1s
    in its binary representation.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is an evil number, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.

    Examples:
        >>> is_evil_number(3)
        True
        >>> is_evil_number(1)
        False
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    return bin(n).count("1") % 2 == 0


def is_perfect_square(n: int) -> bool:
    """Return ``True`` when *n* is a perfect square.

    A perfect square is a non-negative integer that is the square of an
    integer. By this definition, 0 and 1 are perfect squares.

    Args:
        n: The integer to test.

    Returns:
        ``True`` if *n* is a perfect square, ``False`` otherwise.

    Raises:
        TypeError: If *n* is not an int.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def is_perfect_cube(n: int) -> bool:
    """Return ``True`` when *n* is a perfect cube."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n == 0:
        return True
    m = abs(n)
    r = round(m ** (1.0 / 3.0))
    # check nearby values due to floating point
    for candidate in (r - 1, r, r + 1):
        if candidate < 0:
            continue
        if candidate**3 == m:
            return True
    return False


def is_power_of_two(n: int) -> bool:
    """Return ``True`` when *n* is a positive power of two."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n <= 0:
        return False
    return (n & (n - 1)) == 0


def is_triangular_number(n: int) -> bool:
    """Return ``True`` when *n* is a triangular number.

    A triangular number is of the form n = k*(k+1)/2 for some non-negative
    integer k.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    discriminant = 1 + 8 * n
    r = math.isqrt(discriminant)
    if r * r != discriminant:
        return False
    return r % 2 == 1


def is_pentagonal_number(n: int) -> bool:
    """Return ``True`` when *n* is a pentagonal number."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    discriminant = 1 + 24 * n
    r = math.isqrt(discriminant)
    if r * r != discriminant:
        return False
    return (1 + r) % 6 == 0


def is_hexagonal_number(n: int) -> bool:
    """Return ``True`` when *n* is a hexagonal number."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    if n == 0:
        return True
    discriminant = 1 + 8 * n
    r = math.isqrt(discriminant)
    if r * r != discriminant:
        return False
    return (1 + r) % 4 == 0


def is_squarefree_number(n: int) -> bool:
    """Return ``True`` if *n* is a squarefree number."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 1:
        return False
    m = n
    d = 2
    while d * d <= m:
        if m % d == 0:
            if m % (d * d) == 0:
                return False
            while m % d == 0:
                m //= d
        if d == 2:
            d += 1
        else:
            d += 2
    return True


def is_oblong_number(n: int) -> bool:
    """Return ``True`` if *n* is a pronic (oblong) number."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    discriminant = 4 * n + 1
    r = math.isqrt(discriminant)
    return r * r == discriminant and r % 2 == 1


def is_ugly_number(n: int) -> bool:
    """Return ``True`` if *n* is an ugly number."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n <= 0:
        return False
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return n == 1


def is_narcissistic_number(n: int) -> bool:
    """Return ``True`` if *n* is a narcissistic (Armstrong) number."""
    # Narcissistic numbers are same as Armstrong/Narcissistic
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        return False
    s = str(n)
    power = len(s)
    total = sum(int(d) ** power for d in s)
    return total == n


# Alias
is_narcissistic = is_narcissistic_number
