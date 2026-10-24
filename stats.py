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
    "sum_values",
    "percentile",
    "iqr",
    "coefficient_of_variation",
    "geometric_mean",
    "harmonic_mean",
]


def _require_list_of_numbers(numbers: List[T | float], name: str = "numbers") -> None:
    if not isinstance(numbers, list):
        raise TypeError(f"{name} must be a list")
    if not numbers:
        raise ValueError(f"Cannot calculate {name.replace('numbers', 'values')} of empty list")
    # allow ints/floats; be permissive like existing code


def mean(numbers: List[T | float]) -> float:
    """Return the arithmetic mean of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The average of all numbers.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list.

    Examples:
        >>> mean([1, 2, 3, 4, 5])
        3.0
        >>> mean([2, 4])
        3.0
    """
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(numbers) / len(numbers)


def median(numbers: List[T | float]) -> float:
    """Return the median of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The median value.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list.

    Examples:
        >>> median([1, 2, 3, 4, 5])
        3
        >>> median([1, 2, 3, 4])
        2.5
    """
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")
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
        TypeError: If numbers is not a list.

    Examples:
        >>> mode([1, 2, 2, 3, 4])
        2
        >>> mode([1, 1, 2, 2, 3])
        1
    """
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate mode of empty list")
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
        TypeError: If numbers is not a list or population is not a bool.
    """
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    if not numbers:
        raise ValueError("Cannot calculate variance of empty list")
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
        TypeError: If numbers is not a list or population is not a bool.
    """
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    var = variance(numbers, population=population)
    return math.sqrt(var)


def range(numbers: List[T | float]) -> float:
    """Return the range (max - min) of a list of numbers."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate range of empty list")
    return float(max(numbers) - min(numbers))


def min_value(numbers: List[T | float]) -> float:
    """Return the minimum value in a list of numbers."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate min of empty list")
    return float(min(numbers))


def max_value(numbers: List[T | float]) -> float:
    """Return the maximum value in a list of numbers."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate max of empty list")
    return float(max(numbers))


def sum_values(numbers: List[T | float]) -> float:
    """Return the sum of all values in a list of numbers."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate sum of empty list")
    return float(sum(numbers))


def percentile(numbers: List[T | float], p: float) -> float:
    """Return the p-th percentile of a list of numbers (linear interpolation)."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not isinstance(p, (int, float)) or isinstance(p, bool):
        raise TypeError("p must be a number")
    if not numbers:
        raise ValueError("Cannot calculate percentile of empty list")
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
    if not numbers:
        raise ValueError("Cannot calculate harmonic mean of empty list")
    total = 0.0
    for x in numbers:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("numbers must contain only numbers")
        if float(x) <= 0:
            raise ValueError("All numbers must be positive")
        total += 1.0 / float(x)
    return float(len(numbers) / total)


def iqr(numbers: List[T | float]) -> float:
    """Return the interquartile range (Q3 - Q1)."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate iqr of empty list")
    q1 = percentile(numbers, 25)
    q3 = percentile(numbers, 75)
    return float(q3 - q1)


def coefficient_of_variation(numbers: List[T | float], population: bool = True) -> float:
    """Return the coefficient of variation (stddev / mean)."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    if not numbers:
        raise ValueError("Cannot calculate coefficient of variation of empty list")
    m = mean(numbers)
    if m == 0:
        raise ValueError("Cannot calculate coefficient of variation when mean is 0")
    s = stddev(numbers, population=population)
    return float(abs(s) / abs(m))


def geometric_mean(numbers: List[T | float]) -> float:
    """Return the geometric mean."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate geometric mean of empty list")
    product = 1.0
    for x in numbers:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("numbers must contain only numbers")
        if float(x) <= 0:
            raise ValueError("All numbers must be positive")
        product *= float(x)
    return float(product ** (1.0 / len(numbers)))


def harmonic_mean(numbers: List[T | float]) -> float:
    """Return the harmonic mean."""
    if not isinstance(numbers, list):
        raise TypeError("numbers must be a list")
    if not numbers:
        raise ValueError("Cannot calculate harmonic mean of empty list")
    total = 0.0
    for x in numbers:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError("numbers must contain only numbers")
        if float(x) <= 0:
            raise ValueError("All numbers must be positive")
        total += 1.0 / float(x)
    return float(len(numbers) / total)
