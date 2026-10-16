"""Bitwise utility functions for working with binary representations of integers.

This module provides utilities for counting bits, manipulating individual bits,
detecting powers of two, reversing bits, and rotating bit fields. All functions
operate on non-negative integers unless otherwise noted.
"""

from __future__ import annotations

from typing import Optional

__all__: list[str] = [
    "count_set_bits",
    "is_power_of_two",
    "next_power_of_two",
    "prev_power_of_two",
    "reverse_bits",
    "rotate_left",
    "rotate_right",
    "get_bit",
    "set_bit",
    "clear_bit",
    "toggle_bit",
    "is_even",
    "is_odd",
]


def _validate_nonnegative_int(value: int, name: str = "value") -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _validate_index(index: int) -> None:
    if not isinstance(index, int) or isinstance(index, bool):
        raise TypeError("index must be an integer")
    if index < 0:
        raise ValueError("index must be non-negative")


def _validate_positive_int(value: int, name: str = "value") -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def count_set_bits(value: int) -> int:
    """Return the number of set bits (1s) in the binary representation of value.

    Args:
        value: A non-negative integer.

    Returns:
        The count of set bits.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative.

    Examples:
        >>> count_set_bits(0)
        0
        >>> count_set_bits(5)  # 0b101
        2
        >>> count_set_bits(7)  # 0b111
        3
    """
    _validate_nonnegative_int(value)
    return bin(value).count("1")


def is_power_of_two(value: int) -> bool:
    """Return True if value is a power of two.

    Args:
        value: An integer.

    Returns:
        True if value is a power of two, False otherwise.

    Examples:
        >>> is_power_of_two(1)
        True
        >>> is_power_of_two(16)
        True
        >>> is_power_of_two(18)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return value > 0 and (value & (value - 1)) == 0


def next_power_of_two(value: int) -> int:
    """Return the smallest power of two greater than or equal to value.

    Args:
        value: A non-negative integer.

    Returns:
        The next power of two.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative.

    Examples:
        >>> next_power_of_two(0)
        1
        >>> next_power_of_two(5)
        8
        >>> next_power_of_two(16)
        16
    """
    _validate_nonnegative_int(value)
    if value == 0:
        return 1
    return 1 << (value - 1).bit_length()


def prev_power_of_two(value: int) -> int:
    """Return the largest power of two less than or equal to value.

    Args:
        value: A non-negative integer.

    Returns:
        The previous power of two, or 0 if value is 0.

    Raises:
        TypeError: If value is not an integer.
        ValueError: If value is negative.

    Examples:
        >>> prev_power_of_two(0)
        0
        >>> prev_power_of_two(5)
        4
        >>> prev_power_of_two(16)
        16
    """
    _validate_nonnegative_int(value)
    if value == 0:
        return 0
    return 1 << (value.bit_length() - 1)


def reverse_bits(value: int, width: Optional[int] = None) -> int:
    """Reverse the bits of value within the given width.

    Args:
        value: A non-negative integer.
        width: The bit width to reverse within. Defaults to the minimal width
            needed to represent value.

    Returns:
        The integer with bits reversed.

    Raises:
        TypeError: If value or width is not an integer.
        ValueError: If value is negative or width is not positive.

    Examples:
        >>> reverse_bits(0b0001, 4)
        8
        >>> reverse_bits(13, 4)  # 1101 -> 1011
        11
    """
    _validate_nonnegative_int(value)
    if width is None:
        width = value.bit_length() or 1
    _validate_positive_int(width, "width")
    result = 0
    for i in range(width):
        if (value >> i) & 1:
            result |= 1 << (width - 1 - i)
    return result


def rotate_left(value: int, shift: int, width: int) -> int:
    """Rotate the bits of value left by shift positions within width bits.

    Args:
        value: A non-negative integer.
        shift: Number of positions to rotate.
        width: The bit width to rotate within.

    Returns:
        The rotated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or width is not positive.

    Examples:
        >>> rotate_left(0b0001, 1, 4)
        2
        >>> rotate_left(0b1000, 1, 4)
        1
    """
    _validate_nonnegative_int(value)
    if not isinstance(shift, int) or isinstance(shift, bool):
        raise TypeError("shift must be an integer")
    _validate_positive_int(width, "width")
    shift %= width
    mask = (1 << width) - 1
    return ((value << shift) | (value >> (width - shift))) & mask


def rotate_right(value: int, shift: int, width: int) -> int:
    """Rotate the bits of value right by shift positions within width bits.

    Args:
        value: A non-negative integer.
        shift: Number of positions to rotate.
        width: The bit width to rotate within.

    Returns:
        The rotated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or width is not positive.

    Examples:
        >>> rotate_right(0b1000, 1, 4)
        4
        >>> rotate_right(0b0001, 1, 4)
        8
    """
    _validate_nonnegative_int(value)
    if not isinstance(shift, int) or isinstance(shift, bool):
        raise TypeError("shift must be an integer")
    _validate_positive_int(width, "width")
    shift %= width
    mask = (1 << width) - 1
    return ((value >> shift) | (value << (width - shift))) & mask


def get_bit(value: int, index: int) -> int:
    """Return the bit at index (0 = least significant bit).

    Args:
        value: A non-negative integer.
        index: The bit index to read.

    Returns:
        0 or 1.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> get_bit(0b1010, 1)
        1
        >>> get_bit(0b1010, 2)
        0
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return (value >> index) & 1


def set_bit(value: int, index: int) -> int:
    """Return value with the bit at index set to 1.

    Args:
        value: A non-negative integer.
        index: The bit index to set.

    Returns:
        The updated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> set_bit(0b0000, 2)
        4
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return value | (1 << index)


def clear_bit(value: int, index: int) -> int:
    """Return value with the bit at index cleared to 0.

    Args:
        value: A non-negative integer.
        index: The bit index to clear.

    Returns:
        The updated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> clear_bit(0b1111, 1)
        13
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return value & ~(1 << index)


def toggle_bit(value: int, index: int) -> int:
    """Return value with the bit at index flipped.

    Args:
        value: A non-negative integer.
        index: The bit index to toggle.

    Returns:
        The updated integer.

    Raises:
        TypeError: If arguments are not integers.
        ValueError: If value is negative or index is negative.

    Examples:
        >>> toggle_bit(0b1010, 1)
        8
        >>> toggle_bit(0b1010, 0)
        11
    """
    _validate_nonnegative_int(value)
    _validate_index(index)
    return value ^ (1 << index)


def is_even(value: int) -> bool:
    """Return True if value is even.

    Args:
        value: An integer.

    Returns:
        True if value is even, False otherwise.

    Examples:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return (value & 1) == 0


def is_odd(value: int) -> bool:
    """Return True if value is odd.

    Args:
        value: An integer.

    Returns:
        True if value is odd, False otherwise.

    Examples:
        >>> is_odd(4)
        False
        >>> is_odd(7)
        True
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("value must be an integer")
    return (value & 1) == 1
