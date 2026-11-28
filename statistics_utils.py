"""Statistical utility functions for data analysis."""

import math
from typing import List, Tuple, TypeVar

T = TypeVar("T", int, float)
__all__ = [
    "T",
    "correlation",
    "covariance",
    "geometric_mean",
    "harmonic_mean",
    "median_even",
    "normalize",
    "percentile",
    "z_score",
]


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
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in numbers):
        raise ValueError("numbers must not contain NaN or infinite values")
    # Scale by the smallest magnitude so every reciprocal stays at or below 1;
    # otherwise a tiny input (e.g. 1e-320) overflows ``1.0 / x`` to ``inf`` and
    # the mean collapses to ``0.0``.
    scale = min(abs(x) for x in numbers)
    scaled_reciprocal_sum = math.fsum(scale / x for x in numbers)
    try:
        return float(len(numbers) * scale / scaled_reciprocal_sum)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def geometric_mean(numbers: List[T | float]) -> float:
    """Return the geometric mean of a list of numbers.

    The geometric mean is the nth root of the product of the numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The geometric mean.

    Raises:
        ValueError: If the list is empty or contains negative values.
        ValueError: If the result is too large to represent as a finite float.

    Examples:
        >>> geometric_mean([1, 2, 3, 4, 5])
        2.6051710846973517
        >>> geometric_mean([1, 1, 1])
        1.0
    """
    if not numbers:
        raise ValueError("Cannot calculate geometric mean of empty list")
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in numbers):
        raise ValueError("numbers must not contain NaN or infinite values")
    # Check for negatives
    if any(x < 0 for x in numbers):
        raise ValueError("Geometric mean is undefined for negative numbers")
    if any(x == 0 for x in numbers):
        return 0.0
    # Use log-space computation to avoid overflow with large integers.
    # For any positive x, log(geometric_mean) = mean(log(x)).
    try:
        return float(math.exp(math.fsum(math.log(float(x)) for x in numbers) / len(numbers)))
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


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
        (2.0, 3.0)
        >>> median_even([1, 2, 3])
        (2.0, 2.0)
    """
    if not numbers:
        raise ValueError("Cannot calculate median_even of empty list")
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in numbers):
        raise ValueError("numbers must not contain NaN or infinite values")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    if n % 2 == 0:
        lower = sorted_nums[n // 2 - 1]
        upper = sorted_nums[n // 2]
        try:
            return (float(lower), float(upper))
        except OverflowError:
            raise ValueError("result is too large to represent as a finite float")
    else:
        try:
            median_val = float(sorted_nums[n // 2])
        except OverflowError:
            raise ValueError("result is too large to represent as a finite float")
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
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in numbers):
        raise ValueError("numbers must not contain NaN or infinite values")
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100 inclusive")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    # Method: linear interpolation between closest ranks
    # Compute the rank: r = p/100 * (n - 1) + 1
    # Then split into integer part and fraction
    if n == 1:
        try:
            return float(sorted_nums[0])
        except OverflowError:
            raise ValueError("result is too large to represent as a finite float")
    rank = (p / 100.0) * (n - 1) + 1
    lower_idx = int(math.floor(rank) - 1)  # zero-indexed
    upper_idx = int(math.ceil(rank) - 1)
    weight = rank - math.floor(rank)
    if lower_idx == upper_idx:
        try:
            return float(sorted_nums[lower_idx])
        except OverflowError:
            raise ValueError("result is too large to represent as a finite float")
    try:
        lower_val = float(sorted_nums[lower_idx])
        upper_val = float(sorted_nums[upper_idx])
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")
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
    if any(isinstance(v, float) and (math.isnan(v) or math.isinf(v)) for v in (*x, *y)):
        raise ValueError("numbers must not contain NaN or infinite values")
    try:
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        return cov / (len(x) - 1)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def correlation(x: List[T | float], y: List[T | float]) -> float:
    """Return the Pearson correlation coefficient of two lists.

    The computation scales deviations by their peak magnitude before squaring,
    so large but finite inputs (around ``1e155`` and above) do not overflow the
    intermediate sum of squares; the result stays within ``[-1, 1]``.

    Args:
        x: First list of numeric values.
        y: Second list of numeric values.

    Returns:
        The correlation coefficient between -1 and 1.

    Raises:
        ValueError: If the lists are empty, have different lengths,
                    have fewer than 2 elements, or have zero variance.
        ValueError: If the result is too large to represent as a finite float.

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
    if any(isinstance(v, float) and (math.isnan(v) or math.isinf(v)) for v in (*x, *y)):
        raise ValueError("numbers must not contain NaN or infinite values")
    try:
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        # Compute covariance and variances on deviations scaled by their peak
        # magnitude. Squaring raw deviations around ``1e155`` overflows the
        # finite float range even though the correlation is bounded to
        # ``[-1, 1]``; scaling first keeps every intermediate finite.
        dx = [xi - mean_x for xi in x]
        dy = [yi - mean_y for yi in y]
        scale_x = max(abs(v) for v in dx)
        scale_y = max(abs(v) for v in dy)
        if scale_x == 0 or scale_y == 0:
            raise ValueError("Correlation is undefined when variance is zero")
        sx = [v / scale_x for v in dx]
        sy = [v / scale_y for v in dy]
        cov = sum(a * b for a, b in zip(sx, sy))
        var_x = sum(a * a for a in sx)
        var_y = sum(b * b for b in sy)
        return cov / math.sqrt(var_x * var_y)
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def z_score(numbers: List[T | float]) -> List[float]:
    """Return the z-scores (standard scores) of a list of numbers.

    Each z-score is (x - mean) / population standard deviation.

    The standard deviation is computed on deviations scaled by their peak
    magnitude, so large but finite inputs (around ``1e155`` and above) do not
    overflow the intermediate variance.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of z-scores corresponding to each input number.

    Raises:
        ValueError: If the list is empty or if the standard deviation is zero
                    (e.g., all values are identical).
        ValueError: If the result is too large to represent as a finite float.

    Examples:
        >>> z_score([1, 2, 3, 4, 5])
        [-1.414213562373095, -0.7071067811865475, 0.0, 0.7071067811865475, 1.414213562373095]
    """
    if not numbers:
        raise ValueError("Cannot calculate z-scores of empty list")
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in numbers):
        raise ValueError("numbers must not contain NaN or infinite values")
    try:
        mean_val = sum(numbers) / len(numbers)
        # Population standard deviation, computed on deviations scaled by their
        # peak magnitude. Squaring raw deviations around ``1e155`` overflows the
        # finite float range even though the z-scores are finite; scaling first
        # keeps every intermediate finite.
        deviations = [x - mean_val for x in numbers]
        scale = max(abs(v) for v in deviations)
        if scale == 0:
            raise ValueError("Standard deviation is zero; cannot compute z-scores")
        scaled = [v / scale for v in deviations]
        variance = sum(s * s for s in scaled) / len(numbers)
        std_dev = math.sqrt(variance)
        return [s / std_dev for s in scaled]
    except OverflowError:
        raise ValueError("result is too large to represent as a finite float")


def normalize(numbers: List[T | float]) -> List[float]:
    """Normalize a list of numbers to the range [0, 1] using min-max scaling.

    Args:
        numbers: A list of numeric values.

    Returns:
        A list of normalized values where min maps to 0 and max maps to 1.
        If all values are equal, returns a list of 0.0.

    Raises:
        ValueError: If the list is empty or contains non-finite values
            (NaN or infinity).

    Examples:
        >>> normalize([1, 2, 3, 4, 5])
        [0.0, 0.25, 0.5, 0.75, 1.0]
        >>> normalize([5, 5, 5])
        [0.0, 0.0, 0.0]
    """
    if not numbers:
        raise ValueError("Cannot normalize empty list")
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in numbers):
        raise ValueError("numbers must not contain NaN or infinite values")
    min_val = min(numbers)
    max_val = max(numbers)
    if min_val == max_val:
        return [0.0 for _ in numbers]
    scale = max_val - min_val
    return [(x - min_val) / scale for x in numbers]
