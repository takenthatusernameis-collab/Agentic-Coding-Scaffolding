"""Statistical utility functions for data analysis."""

import math
from typing import List, Tuple, TypeVar

T = TypeVar("T", int, float)


def harmonic_mean(numbers: List[T | float]) -> float:
    """Return the harmonic mean of a list of numbers.

    The harmonic mean is the reciprocal of the arithmetic mean of the reciprocals.

    Args:
        numbers: A list of numeric values.

    Returns:
        The harmonic mean.

    Raises:
        ValueError: If the list is empty or contains zero.

    Examples:
        >>> harmonic_mean([1, 2, 4])
        1.7142857142857142
        >>> harmonic_mean([1, 1, 1])
        1.0
    """
    if not numbers:
        raise ValueError("Cannot calculate harmonic mean of empty list")
    # Check for zeros
    if any(x == 0 for x in numbers):
        raise ValueError("Harmonic mean is undefined for values equal to zero")
    reciprocal_sum = sum(1.0 / x for x in numbers)
    return len(numbers) / reciprocal_sum


def geometric_mean(numbers: List[T | float]) -> float:
    """Return the geometric mean of a list of numbers.

    The geometric mean is the nth root of the product of the numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The geometric mean.

    Raises:
        ValueError: If the list is empty or contains negative values.

    Examples:
        >>> geometric_mean([1, 2, 3, 4, 5])
        2.605171084697352
        >>> geometric_mean([1, 1, 1])
        1.0
    """
    if not numbers:
        raise ValueError("Cannot calculate geometric mean of empty list")
    # Check for negatives
    if any(x < 0 for x in numbers):
        raise ValueError("Geometric mean is undefined for negative numbers")
    product = 1.0
    for x in numbers:
        product *= x
    return float(product ** (1.0 / len(numbers)))


def median_even(numbers: List[T | float]) -> Tuple[float, float]:
    """Return the two middle values of a sorted list (for even-length lists).

    For odd-length lists, returns the same value twice (the median).

    Args:
        numbers: A list of numeric values.

    Returns:
        A tuple (lower_middle, upper_middle) where:
        - For even length: the two middle values after sorting.
        - For odd length: (median, median).

    Raises:
        ValueError: If the list is empty.

    Examples:
        >>> median_even([1, 2, 3, 4])
        (2, 3)
        >>> median_even([1, 2, 3])
        (2, 2)
    """
    if not numbers:
        raise ValueError("Cannot calculate median_even of empty list")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        lower = sorted_nums[n // 2 - 1]
        upper = sorted_nums[n // 2]
        return (float(lower), float(upper))
    else:
        median_val = float(sorted_nums[n // 2])
        return (median_val, median_val)


def percentile(numbers: List[T | float], p: float) -> float:
    """Return the p-th percentile of a list of numbers.

    Uses linear interpolation between closest ranks method similar to numpy's
    percentile with method='linear'.

    Args:
        numbers: A list of numeric values.
        p: Percentile to compute (0 <= p <= 100).

    Returns:
        The p-th percentile value.

    Raises:
        ValueError: If the list is empty or p is out of range.

    Examples:
        >>> percentile([1, 2, 3, 4, 5], 50)
        3.0
        >>> percentile([1, 2, 3, 4, 5], 0)
        1.0
        >>> percentile([1, 2, 3, 4, 5], 100)
        5.0
    """
    if not numbers:
        raise ValueError("Cannot calculate percentile of empty list")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100 inclusive")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    # Method: linear interpolation between closest ranks
    # Compute the rank: r = p/100 * (n - 1) + 1
    # Then split into integer part and fraction
    if n == 1:
        return float(sorted_nums[0])
    rank = (p / 100.0) * (n - 1) + 1
    lower_idx = int(math.floor(rank) - 1)  # zero-indexed
    upper_idx = int(math.ceil(rank) - 1)
    weight = rank - math.floor(rank)
    if lower_idx == upper_idx:
        return float(sorted_nums[lower_idx])
    lower_val = float(sorted_nums[lower_idx])
    upper_val = float(sorted_nums[upper_idx])
    return lower_val + weight * (upper_val - lower_val)


def covariance(x: List[T | float], y: List[T | float]) -> float:
    """Return the sample covariance of two lists of numbers.

    Args:
        x: First list of numeric values.
        y: Second list of numeric values.

    Returns:
        The sample covariance.

    Raises:
        ValueError: If the lists are empty, have different lengths,
                    or have fewer than 2 elements.

    Examples:
        >>> covariance([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        -2.5
        >>> covariance([1, 2, 3], [1, 2, 3])
        1.0
    """
    if not x or not y:
        raise ValueError("Cannot calculate covariance of empty list")
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length")
    if len(x) < 2:
        raise ValueError("Covariance requires at least two elements")
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    return cov / (len(x) - 1)


def correlation(x: List[T | float], y: List[T | float]) -> float:
    """Return the Pearson correlation coefficient of two lists.

    Args:
        x: First list of numeric values.
        y: Second list of numeric values.

    Returns:
        The correlation coefficient between -1 and 1.

    Raises:
        ValueError: If the lists are empty, have different lengths,
                    have fewer than 2 elements, or have zero variance.

    Examples:
        >>> correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        -1.0
        >>> correlation([1, 2, 3], [1, 2, 3])
        1.0
    """
    if not x or not y:
        raise ValueError("Cannot calculate correlation of empty list")
    if len(x) != len(y):
        raise ValueError("Both lists must have the same length")
    if len(x) < 2:
        raise ValueError("Correlation requires at least two elements")
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    # Compute covariance and variances
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)
    if var_x == 0 or var_y == 0:
        raise ValueError("Correlation is undefined when variance is zero")
    return cov / math.sqrt(var_x * var_y)


def z_score(numbers: List[T | float]) -> List[float]:
    """Return the z-scores (standard scores) of a list of numbers.

    Each z-score is (x - mean) / population standard deviation.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of z-scores corresponding to each input number.

    Raises:
        ValueError: If the list is empty or if the standard deviation is zero
                    (e.g., all values are identical).

    Examples:
        >>> z_score([1, 2, 3, 4, 5])
        [-1.414213562373095, -0.7071067811865475, 0.0, 0.7071067811865475, 1.414213562373095]
    """
    if not numbers:
        raise ValueError("Cannot calculate z-scores of empty list")
    mean_val = sum(numbers) / len(numbers)
    # Population standard deviation
    variance = sum((x - mean_val) ** 2 for x in numbers) / len(numbers)
    if variance == 0:
        raise ValueError("Standard deviation is zero; cannot compute z-scores")
    std_dev = math.sqrt(variance)
    return [(x - mean_val) / std_dev for x in numbers]


def normalize(numbers: List[T | float]) -> List[float]:
    """Normalize a list of numbers to the range [0, 1] using min-max scaling.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of normalized values where min maps to 0 and max maps to 1.
        If all values are equal, returns a list of 0.0.

    Raises:
        ValueError: If the list is empty.

    Examples:
        >>> normalize([1, 2, 3, 4, 5])
        [0.0, 0.25, 0.5, 0.75, 1.0]
        >>> normalize([5, 5, 5])
        [0.0, 0.0, 0.0]
    """
    if not numbers:
        raise ValueError("Cannot normalize empty list")
    min_val = min(numbers)
    max_val = max(numbers)
    if min_val == max_val:
        return [0.0 for _ in numbers]
    scale = max_val - min_val
    return [(x - min_val) / scale for x in numbers]
