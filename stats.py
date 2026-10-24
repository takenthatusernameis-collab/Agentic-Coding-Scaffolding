"""Statistical utility functions for data analysis."""

import math
from typing import List, TypeVar

T = TypeVar("T", int, float)

__all__: List[str] = [
    "mean",
    "median",
    "mode",
    "variance",
    "stddev",
    "range",
    "min_value",
    "max_value",
    "midrange",
    "sum_values",
    "sum_of_squares",
    "percentile",
    "iqr",
    "interquartile_range",
    "coefficient_of_variation",
    "geometric_mean",
    "harmonic_mean",
    "median_absolute_deviation",
    "weighted_mean",
]


def _require_numbers(numbers: List[T | float], name: str = "numbers") -> None:
    if not isinstance(numbers, list):
        raise TypeError(f"{name} must be a list")
    if not numbers:
        raise ValueError(f"Cannot calculate {name.replace('numbers', 'values')} of empty list")
    for x in numbers:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError(f"{name} must contain only numbers")


def mean(numbers: List[T | float]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The average of all numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> mean([1, 2, 3, 4, 5])
        3.0
        >>> mean([2, 4])
        3.0
    """
    _require_numbers(numbers, "numbers")
    return sum(numbers) / len(numbers)


def median(numbers: List[T | float]) -> float:
    """Return the median of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The median value.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> median([1, 2, 3, 4, 5])
        3
        >>> median([1, 2, 3, 4])
        2.5
    """
    _require_numbers(numbers, "numbers")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 1:
        return float(sorted_nums[n // 2])
    mid1 = sorted_nums[n // 2 - 1]
    mid2 = sorted_nums[n // 2]
    return (mid1 + mid2) / 2.0


def mode(numbers: List[T | float]) -> float:
    """Return the mode (most frequent value) of a list of numbers.

    If there is more than one mode, returns the first one encountered
    in terms of the value that appears first in sorted order of values.

    Args:
        numbers: A list of numeric values.

    Returns:
        The most frequently occurring value.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> mode([1, 2, 2, 3, 4])
        2
        >>> mode([1, 1, 2, 2, 3])
        1
    """
    _require_numbers(numbers, "numbers")
    frequency: dict = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_count = max(frequency.values())
    for num in sorted(frequency.keys()):
        if frequency[num] == max_count:
            return float(num)
    raise ValueError("Cannot calculate mode of empty list")


def variance(numbers: List[T | float], population: bool = True) -> float:
    """Return the variance of a list of numbers.

    Args:
        numbers: A list of numeric values.
        population: If True, calculate population variance (divide by n).
                    If False, calculate sample variance (divide by n-1).
                    Defaults to True.

    Returns:
        The variance.

    Raises:
        ValueError: If the list is empty, or if calculating sample variance
                    with fewer than 2 elements.
        TypeError: If numbers is not a list, contains non-numeric values,
                   or population is not a bool.
    """
    _require_numbers(numbers, "numbers")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    if not population and len(numbers) < 2:
        raise ValueError("Cannot calculate sample variance with fewer than 2 elements")
    avg = mean(numbers)
    squared_diff = sum((x - avg) ** 2 for x in numbers)
    if population:
        return squared_diff / len(numbers)
    return squared_diff / (len(numbers) - 1)


def stddev(numbers: List[T | float], population: bool = True) -> float:
    """Return the standard deviation of a list of numbers.

    Args:
        numbers: A list of numeric values.
        population: If True, calculate population std dev (divide by n).
                    If False, calculate sample std dev (divide by n-1).
                    Defaults to True.

    Returns:
        The standard deviation.

    Raises:
        ValueError: If the list is empty, or if calculating sample std dev
                    with fewer than 2 elements.
        TypeError: If numbers is not a list, contains non-numeric values,
                   or population is not a bool.
    """
    _require_numbers(numbers, "numbers")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    var = variance(numbers, population=population)
    return math.sqrt(var)


def range(numbers: List[T | float]) -> float:
    """Return the range (max - min) of a list of numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.
    """
    _require_numbers(numbers, "numbers")
    return float(max(numbers) - min(numbers))


def min_value(numbers: List[T | float]) -> float:
    """Return the minimum value in a list of numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.
    """
    _require_numbers(numbers, "numbers")
    return float(min(numbers))


def max_value(numbers: List[T | float]) -> float:
    """Return the maximum value in a list of numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.
    """
    _require_numbers(numbers, "numbers")
    return float(max(numbers))


def midrange(numbers: List[T | float]) -> float:
    """Return the midrange of a list of numbers.

    The midrange is the arithmetic mean of the minimum and maximum values,
    a simple measure of central tendency.

    Args:
        numbers: A list of numeric values.

    Returns:
        The midrange of the numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> midrange([1, 2, 3, 4, 5])
        3.0
        >>> midrange([1, 9])
        5.0
    """
    _require_numbers(numbers, "numbers")
    return (min(numbers) + max(numbers)) / 2.0


def sum_values(numbers: List[T | float]) -> float:
    """Return the sum of all values in a list of numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.
    """
    _require_numbers(numbers, "numbers")
    return float(sum(numbers))


def sum_of_squares(numbers: List[T | float]) -> float:
    """Return the sum of the squares of the values in a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The sum of the squared values.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> sum_of_squares([1, 2, 3])
        14.0
    """
    _require_numbers(numbers, "numbers")
    return float(sum(x * x for x in numbers))


def percentile(numbers: List[T | float], p: float) -> float:
    """Return the p-th percentile of a list of numbers (linear interpolation).

    Args:
        numbers: A list of numeric values.
        p: The percentile to compute, between 0 and 100 inclusive.

    Returns:
        The p-th percentile value.

    Raises:
        ValueError: If the list is empty, or if p is outside [0, 100].
        TypeError: If numbers is not a list, contains non-numeric values,
                   or p is not a number.

    Examples:
        >>> percentile([1, 2, 3, 4, 5], 50)
        3.0
        >>> percentile([1, 2, 3, 4], 50)
        2.5
    """
    _require_numbers(numbers, "numbers")
    if not isinstance(p, (int, float)) or isinstance(p, bool):
        raise TypeError("p must be a number")
    if p < 0 or p > 100:
        raise ValueError("p must be between 0 and 100")
    sorted_nums = sorted(float(x) for x in numbers)
    if p == 0:
        return sorted_nums[0]
    if p == 100:
        return sorted_nums[-1]
    k = (len(sorted_nums) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_nums[int(k)]
    return sorted_nums[f] * (c - k) + sorted_nums[c] * (k - f)


def iqr(numbers: List[T | float]) -> float:
    """Return the interquartile range (Q3 - Q1)."""
    _require_numbers(numbers, "numbers")
    q1 = percentile(numbers, 25)
    q3 = percentile(numbers, 75)
    return float(q3 - q1)


def interquartile_range(numbers: List[T | float]) -> float:
    """Return the interquartile range (Q3 - Q1).

    This is an alias for :func:`iqr`.
    """
    return iqr(numbers)


def coefficient_of_variation(numbers: List[T | float], population: bool = True) -> float:
    """Return the coefficient of variation (stddev / mean)."""
    _require_numbers(numbers, "numbers")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    m = mean(numbers)
    if m == 0:
        raise ValueError("Cannot calculate coefficient of variation when mean is 0")
    s = stddev(numbers, population=population)
    return float(abs(s) / abs(m))


def geometric_mean(numbers: List[T | float]) -> float:
    """Return the geometric mean."""
    _require_numbers(numbers, "numbers")
    product = 1.0
    for x in numbers:
        if float(x) <= 0:
            raise ValueError("All numbers must be positive")
        product *= float(x)
    return float(product ** (1.0 / len(numbers)))


def harmonic_mean(numbers: List[T | float]) -> float:
    """Return the harmonic mean."""
    _require_numbers(numbers, "numbers")
    total = 0.0
    for x in numbers:
        if float(x) <= 0:
            raise ValueError("All numbers must be positive")
        total += 1.0 / float(x)
    return float(len(numbers) / total)


def median_absolute_deviation(numbers: List[T | float]) -> float:
    """Return the median absolute deviation of a list of numbers.

    The median absolute deviation (MAD) is the median of the absolute
    deviations of each number from the median of the list. It is a robust
    measure of statistical dispersion.

    Args:
        numbers: A list of numeric values.

    Returns:
        The median absolute deviation of the numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> median_absolute_deviation([1, 2, 3])
        1.0
        >>> median_absolute_deviation([2, 2, 2, 2])
        0.0
    """
    _require_numbers(numbers, "numbers")
    med = median(numbers)
    deviations = [abs(x - med) for x in numbers]
    return median(deviations)


def weighted_mean(values: List[T | float], weights: List[T | float]) -> float:
    """Return the weighted arithmetic mean.

    Args:
        values: A list of numeric values.
        weights: A list of weights for each value (same length as values).

    Returns:
        The weighted arithmetic mean.

    Raises:
        ValueError: If values or weights is empty, lengths differ, or any weight is non-positive.
        TypeError: If inputs are not lists or contain non-numeric values.
    """
    _require_numbers(values, "values")
    _require_numbers(weights, "weights")
    if len(values) != len(weights):
        raise ValueError("values and weights must have the same length")
    total_weight = 0.0
    weighted_sum = 0.0
    for v, w in zip(values, weights):
        w_f = float(w)
        if w_f <= 0:
            raise ValueError("weights must be positive")
        v_f = float(v)
        total_weight += w_f
        weighted_sum += v_f * w_f
    if total_weight == 0:
        raise ValueError("weights must sum to a positive value")
    return float(weighted_sum / total_weight)
