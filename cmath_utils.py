"""Complex mathematics utilities wrapping the standard library cmath module.

This module provides a validated wrapper around the standard library ``cmath``
module for complex number trigonometric, transcendental, and classification
operations. All functions validate their inputs and raise ``TypeError`` for
non-numeric arguments.
"""

from __future__ import annotations

import cmath
from numbers import Real
from typing import Any, Optional, Tuple, Union

Number = Union[int, float, complex]


def _validate_number(value: Any, name: str) -> None:
    """Validate that *value* is a numeric type, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The name of the argument (used in error messages).

    Raises:
        TypeError: If value is not a real or complex number.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, complex)):
        raise TypeError(f"{name} must be a real or complex number")


def phase(z: Number) -> float:
    """Return the phase of a complex number.

    Args:
        z: A real or complex number.

    Returns:
        The phase (argument) of z, in radians.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> phase(1 + 1j)
        0.7853981633974483
        >>> phase(-1)
        3.141592653589793
    """
    _validate_number(z, "z")
    return cmath.phase(z)


def polar(z: Number) -> Tuple[float, float]:
    """Return the polar coordinates of a complex number.

    Args:
        z: A real or complex number.

    Returns:
        A ``(modulus, phase)`` tuple.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> polar(1 + 1j)
        (1.4142135623730951, 0.7853981633974483)
    """
    _validate_number(z, "z")
    return cmath.polar(z)


def rect(r: Real, phi: Real) -> complex:
    """Convert polar coordinates to a complex number.

    Args:
        r: The modulus (magnitude).
        phi: The phase in radians.

    Returns:
        The complex number ``r * (cos(phi) + sin(phi)*1j)``.

    Raises:
        TypeError: If r or phi is not a real number.

    Examples:
        >>> rect(1, 0)
        (1+0j)
    """
    if isinstance(r, bool) or not isinstance(r, (int, float)):
        raise TypeError("r must be a real number")
    if isinstance(phi, bool) or not isinstance(phi, (int, float)):
        raise TypeError("phi must be a real number")
    return cmath.rect(r, phi)


def exp(z: Number) -> complex:
    """Return the complex exponential e**z.

    Args:
        z: A real or complex number.

    Returns:
        e raised to the power of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> exp(0)
        (1+0j)
        >>> exp(1)
        (2.718281828459045+0j)
    """
    _validate_number(z, "z")
    return cmath.exp(z)


def log(z: Number, base: Optional[Number] = None) -> complex:
    """Return the logarithm of z to the given base.

    Args:
        z: A real or complex number.
        base: The logarithm base (defaults to e).

    Returns:
        The logarithm of z.

    Raises:
        TypeError: If z or base is not a real or complex number.
        ValueError: If z is zero.

    Examples:
        >>> log(1)
        0j
        >>> log(math.e)
        (1+0j)
        >>> log(8, 2)
        (3+0j)
    """
    _validate_number(z, "z")
    if base is not None:
        _validate_number(base, "base")
        return cmath.log(z, base)
    return cmath.log(z)


def log10(z: Number) -> complex:
    """Return the base-10 logarithm of z.

    Args:
        z: A real or complex number.

    Returns:
        The base-10 logarithm of z.

    Raises:
        TypeError: If z is not a real or complex number.
        ValueError: If z is zero.

    Examples:
        >>> log10(100)
        (2+0j)
        >>> log10(1)
        0j
    """
    _validate_number(z, "z")
    return cmath.log10(z)


def sqrt(z: Number) -> complex:
    """Return the square root of z.

    Args:
        z: A real or complex number.

    Returns:
        The square root of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> sqrt(-1)
        1j
        >>> sqrt(4)
        (2+0j)
    """
    _validate_number(z, "z")
    return cmath.sqrt(z)


def sin(z: Number) -> complex:
    """Return the complex sine of z.

    Args:
        z: A real or complex number.

    Returns:
        The sine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> sin(0)
        0j
        >>> sin(math.pi / 2)
        (1+0j)
    """
    _validate_number(z, "z")
    return cmath.sin(z)


def cos(z: Number) -> complex:
    """Return the complex cosine of z.

    Args:
        z: A real or complex number.

    Returns:
        The cosine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> cos(0)
        (1+0j)
        >>> cos(math.pi)
        (-1+0j)
    """
    _validate_number(z, "z")
    return cmath.cos(z)


def tan(z: Number) -> complex:
    """Return the complex tangent of z.

    Args:
        z: A real or complex number.

    Returns:
        The tangent of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> tan(0)
        0j
    """
    _validate_number(z, "z")
    return cmath.tan(z)


def asin(z: Number) -> complex:
    """Return the complex arc sine of z.

    Args:
        z: A real or complex number.

    Returns:
        The arc sine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> asin(0)
        0j
        >>> asin(1)
        (1.5707963267948966+0j)
    """
    _validate_number(z, "z")
    return cmath.asin(z)


def acos(z: Number) -> complex:
    """Return the complex arc cosine of z.

    Args:
        z: A real or complex number.

    Returns:
        The arc cosine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> acos(1)
        0j
        >>> acos(0)
        (1.5707963267948966+0j)
    """
    _validate_number(z, "z")
    return cmath.acos(z)


def atan(z: Number) -> complex:
    """Return the complex arc tangent of z.

    Args:
        z: A real or complex number.

    Returns:
        The arc tangent of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> atan(0)
        0j
        >>> atan(1)
        (0.7853981633974483+0j)
    """
    _validate_number(z, "z")
    return cmath.atan(z)


def sinh(z: Number) -> complex:
    """Return the complex hyperbolic sine of z.

    Args:
        z: A real or complex number.

    Returns:
        The hyperbolic sine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> sinh(0)
        0j
    """
    _validate_number(z, "z")
    return cmath.sinh(z)


def cosh(z: Number) -> complex:
    """Return the complex hyperbolic cosine of z.

    Args:
        z: A real or complex number.

    Returns:
        The hyperbolic cosine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> cosh(0)
        (1+0j)
    """
    _validate_number(z, "z")
    return cmath.cosh(z)


def tanh(z: Number) -> complex:
    """Return the complex hyperbolic tangent of z.

    Args:
        z: A real or complex number.

    Returns:
        The hyperbolic tangent of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> tanh(0)
        0j
    """
    _validate_number(z, "z")
    return cmath.tanh(z)


def asinh(z: Number) -> complex:
    """Return the complex inverse hyperbolic sine of z.

    Args:
        z: A real or complex number.

    Returns:
        The inverse hyperbolic sine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> asinh(0)
        0j
    """
    _validate_number(z, "z")
    return cmath.asinh(z)


def acosh(z: Number) -> complex:
    """Return the complex inverse hyperbolic cosine of z.

    Args:
        z: A real or complex number.

    Returns:
        The inverse hyperbolic cosine of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> acosh(1)
        0j
    """
    _validate_number(z, "z")
    return cmath.acosh(z)


def atanh(z: Number) -> complex:
    """Return the complex inverse hyperbolic tangent of z.

    Args:
        z: A real or complex number.

    Returns:
        The inverse hyperbolic tangent of z.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> atanh(0)
        0j
    """
    _validate_number(z, "z")
    return cmath.atanh(z)


def isfinite(z: Number) -> bool:
    """Return True if z is finite (not infinite or NaN).

    Args:
        z: A real or complex number.

    Returns:
        True if both the real and imaginary parts are finite.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> isfinite(1 + 2j)
        True
        >>> isfinite(complex(float("inf"), 0))
        False
    """
    _validate_number(z, "z")
    return cmath.isfinite(z)


def isinf(z: Number) -> bool:
    """Return True if the real or imaginary part of z is infinite.

    Args:
        z: A real or complex number.

    Returns:
        True if z is infinite.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> isinf(complex(float("inf"), 0))
        True
        >>> isinf(1 + 2j)
        False
    """
    _validate_number(z, "z")
    return cmath.isinf(z)


def isnan(z: Number) -> bool:
    """Return True if the real or imaginary part of z is NaN.

    Args:
        z: A real or complex number.

    Returns:
        True if z is NaN.

    Raises:
        TypeError: If z is not a real or complex number.

    Examples:
        >>> isnan(complex(float("nan"), 0))
        True
        >>> isnan(1 + 2j)
        False
    """
    _validate_number(z, "z")
    return cmath.isnan(z)


def isclose(a: Number, b: Number, *, rel_tol: float = 1e-09, abs_tol: float = 0.0) -> bool:
    """Return True if complex values a and b are close to each other.

    Args:
        a: A real or complex number.
        b: A real or complex number.
        rel_tol: Relative tolerance (default: 1e-09).
        abs_tol: Absolute tolerance (default: 0.0).

    Returns:
        True if a and b are within the tolerances.

    Raises:
        TypeError: If a or b is not a real or complex number.
        ValueError: If rel_tol or abs_tol is negative.

    Examples:
        >>> isclose(1 + 1j, 1 + 1j)
        True
        >>> isclose(1 + 1j, 1 + 2j)
        False
    """
    _validate_number(a, "a")
    _validate_number(b, "b")
    if rel_tol < 0 or abs_tol < 0:
        raise ValueError("tolerances must be non-negative")
    return cmath.isclose(a, b, rel_tol=rel_tol, abs_tol=abs_tol)
