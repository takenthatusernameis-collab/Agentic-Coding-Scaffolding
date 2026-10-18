"""Utilities for numeric abstract base classes (wrapping :mod:`numbers`)."""

import numbers as _numbers

Number = _numbers.Number
Complex = _numbers.Complex
Real = _numbers.Real
Rational = _numbers.Rational
Integral = _numbers.Integral


def is_number(obj):
    return isinstance(obj, Number)


def is_integral(obj):
    return isinstance(obj, Integral)
