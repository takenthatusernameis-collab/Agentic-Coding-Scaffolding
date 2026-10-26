"""Statistical utility functions for data analysis."""

import math
from typing import List, TypeVar

T = TypeVar("T", int, float)

__all__: List[str] = [
    "mean",
    "median",
    "mode",
    "multimode",
    "variance",
    "stddev",
    "skewness",
    "range",
    "min_value",
    "max_value",
    "midrange",
    "trimmed_mean",
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
    "kurtosis",
    "covariance",
    "correlation",
    "z_scores",
]


def _require_numbers(numbers: List[T | float], name: str = "numbers") -> None:
    if not isinstance(numbers, list):
        raise TypeError(f"{name} must be a list")
    if not numbers:
        raise ValueError(f"Cannot calculate {name.replace('numbers', 'values')} of empty list")
    for x in numbers:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise TypeError(f"{name} must contain only numbers")


def _require_int(value: object, name: str) -> int:
    """Validate that *value* is an int, raising ``TypeError`` otherwise."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


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


def multimode(numbers: List[T | float]) -> List[float]:
    """Return the list of modes (most frequent values) of a list of numbers.

    Unlike :func:`mode`, which returns a single mode, this returns every value
    that shares the highest frequency, in the order each value first appears in
    *numbers*.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of the most frequently occurring values.

    Raises:
        ValueError: If the list is empty.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> multimode([1, 2, 2, 3, 3])
        [2.0, 3.0]
        >>> multimode([1, 1, 2, 2])
        [1.0, 2.0]
    """
    _require_numbers(numbers, "numbers")
    frequency: dict = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    max_count = max(frequency.values())
    seen: set = set()
    result: List[float] = []
    for num in numbers:
        if frequency[num] == max_count and num not in seen:
            seen.add(num)
            result.append(float(num))
    return result


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


def skewness(numbers: List[T | float]) -> float:
    """Return the population skewness of a list of numbers.

    Skewness measures the asymmetry of a distribution about its mean. A
    symmetric distribution has skewness 0; a distribution with a longer
    right tail has positive skewness, and one with a longer left tail has
    negative skewness.

    Args:
        numbers: A list of numeric values.

    Returns:
        The population skewness of the numbers.

    Raises:
        ValueError: If the list is empty, has fewer than 3 elements, or if
            the standard deviation is 0.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> skewness([1, 2, 3])
        0.0
        >>> skewness([1, 1, 1, 1, 10])
        1.5
    """
    _require_numbers(numbers, "numbers")
    n = len(numbers)
    if n < 3:
        raise ValueError("Cannot calculate skewness with fewer than 3 elements")
    m = mean(numbers)
    s = stddev(numbers)
    if s == 0:
        raise ValueError("Cannot calculate skewness when standard deviation is 0")
    return float(sum(((x - m) / s) ** 3 for x in numbers) / n)


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


def trimmed_mean(numbers: List[T | float], trim_count: int = 0) -> float:
    """Return the trimmed mean of a list of numbers.

    The *trim_count* smallest and *trim_count* largest values are discarded
    before computing the arithmetic mean of the remaining values. This makes
    the result robust to outliers. When *trim_count* is 0 (the default) the
    result is identical to :func:`mean`.

    Args:
        numbers: A list of numeric values.
        trim_count: How many values to drop from each end of the sorted
            list. Must be non-negative and strictly less than half the list
            length so that at least one value remains.

    Returns:
        The arithmetic mean of the interior values.

    Raises:
        ValueError: If the list is empty, if *trim_count* is negative, or if
            *trim_count* is greater than or equal to half the list length.
        TypeError: If *numbers* is not a list, contains non-numeric values,
            or *trim_count* is not an int.

    Examples:
        >>> trimmed_mean([1, 2, 3, 4, 5])
        3.0
        >>> trimmed_mean([1, 2, 3, 4, 5], trim_count=1)
        3.0
        >>> trimmed_mean([1, 2, 3, 4, 5, 6], trim_count=1)
        3.5
    """
    _require_numbers(numbers, "numbers")
    _require_int(trim_count, "trim_count")
    if trim_count < 0:
        raise ValueError("trim_count must be non-negative")
    n = len(numbers)
    if trim_count >= n / 2:
        raise ValueError(
            "trim_count must be less than half the list length, "
            f"got {trim_count} for list of length {n}"
        )
    sorted_nums = sorted(numbers)
    trimmed = sorted_nums[trim_count: n - trim_count]
    return sum(trimmed) / len(trimmed)


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


def kurtosis(numbers: List[T | float]) -> float:
    """Return the excess kurtosis of a list of numbers.

    Kurtosis measures the "tailedness" of a distribution. This function
    returns the excess kurtosis (kurtosis minus 3), so a normal
    distribution has an excess kurtosis of 0.

    Args:
        numbers: A list of numeric values.

    Returns:
        The excess kurtosis of the numbers.

    Raises:
        ValueError: If the list has fewer than 4 elements, or if the
            standard deviation is 0.
        TypeError: If numbers is not a list or contains non-numeric values.

    Examples:
        >>> kurtosis([1, 2, 3, 4, 5])
        -1.3
    """
    _require_numbers(numbers, "numbers")
    n = len(numbers)
    if n < 4:
        raise ValueError("Cannot calculate kurtosis with fewer than 4 elements")
    m = mean(numbers)
    s = stddev(numbers)
    if s == 0:
        raise ValueError("Cannot calculate kurtosis when standard deviation is 0")
    return float(sum(((x - m) / s) ** 4 for x in numbers) / n - 3.0)


def _require_same_length(x: List[T | float], y: List[T | float], name: str = "values") -> None:
    """Validate that *x* and *y* are numeric lists of equal length."""
    _require_numbers(x, name)
    _require_numbers(y, "weights")
    if len(x) != len(y):
        raise ValueError(f"{name} and weights must have the same length")


def covariance(x: List[T | float], y: List[T | float], population: bool = True) -> float:
    """Return the covariance between two lists of numbers.

    Args:
        x: The first list of numeric values.
        y: The second list of numeric values (same length as *x*).
        population: If True, divide by *n* (population covariance). If False,
            divide by *n - 1* (sample covariance). Defaults to True.

    Returns:
        The covariance between *x* and *y*.

    Raises:
        ValueError: If the lists are empty, have different lengths, or if
            sample covariance is requested with fewer than 2 elements.
        TypeError: If inputs are not lists, contain non-numeric values, or
            *population* is not a bool.
    """
    _require_same_length(x, y, "values")
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    if not population and len(x) < 2:
        raise ValueError("Cannot calculate sample covariance with fewer than 2 elements")
    mx = mean(x)
    my = mean(y)
    n = len(x)
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    if population:
        return float(cov / n)
    return float(cov / (n - 1))


def correlation(x: List[T | float], y: List[T | float]) -> float:
    """Return the Pearson correlation coefficient between two lists of numbers.

    The correlation measures the strength and direction of a linear
    relationship between *x* and *y*, ranging from -1 (perfect negative
    correlation) to 1 (perfect positive correlation). A value of 0 means no
    linear correlation.

    Args:
        x: The first list of numeric values.
        y: The second list of numeric values (same length as *x*).

    Returns:
        The Pearson correlation coefficient.

    Raises:
        ValueError: If the lists are empty, have different lengths, have
            fewer than 2 elements, or if either list has zero standard
            deviation.
        TypeError: If inputs are not lists or contain non-numeric values.
    """
    _require_same_length(x, y, "values")
    n = len(x)
    if n < 2:
        raise ValueError("Cannot calculate correlation with fewer than 2 elements")
    sx = stddev(x)
    sy = stddev(y)
    if sx == 0 or sy == 0:
        raise ValueError("Cannot calculate correlation when standard deviation is 0")
    cov = covariance(x, y, population=True)
    return float(cov / (sx * sy))


def z_scores(numbers: List[T | float], population: bool = True) -> List[float]:
    """Return the z-scores of the values in *numbers*.

    Each z-score measures how many standard deviations a value is from
    the mean of *numbers*. When *population* is True the population
    standard deviation is used, otherwise the sample standard deviation.

    Args:
        numbers: A list of numeric values.
        population: Use population standard deviation when True (default).

    Returns:
        A list of z-scores in the same order as *numbers*.

    Raises:
        ValueError: If *numbers* is empty or has zero standard deviation.
        TypeError: If *numbers* is not a list or contains non-numeric values,
            or if *population* is not a bool.
    """
    _require_numbers(numbers)
    if not isinstance(population, bool):
        raise TypeError("population must be a bool")
    m = mean(numbers)
    s = stddev(numbers, population=population)
    if s == 0:
        raise ValueError("Cannot calculate z-scores when standard deviation is 0")
    return [float((x - m) / s) for x in numbers]
