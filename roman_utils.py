"""Roman numeral conversion utilities.

Converts between integers and Roman numerals with input validation.
Supports the standard range 1 through 3999.
"""

_ROMAN_NUMERALS = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

_ROMAN_DIGITS = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}

_ROMAN_PATTERN = (
    r"^(?=.)M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)


def to_roman(number: int) -> str:
    """Convert an integer to a Roman numeral.

    Args:
        number: Integer in the range 1 to 3999 inclusive.

    Returns:
        The Roman numeral representation of *number*.

    Raises:
        TypeError: If *number* is not an integer.
        ValueError: If *number* is outside the supported range.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("number must be an integer")
    if number < 1 or number > 3999:
        raise ValueError("number must be in the range 1 to 3999")
    result = []
    for value, symbol in _ROMAN_NUMERALS:
        count, number = divmod(number, value)
        result.append(symbol * count)
    return "".join(result)


def from_roman(roman: str) -> int:
    """Convert a Roman numeral to an integer.

    Args:
        roman: Roman numeral string to convert.

    Returns:
        The integer value of *roman*.

    Raises:
        TypeError: If *roman* is not a string.
        ValueError: If *roman* is not a valid Roman numeral.
    """
    if not isinstance(roman, str):
        raise TypeError("roman must be a string")
    if not roman:
        raise ValueError("roman must not be empty")
    total = 0
    index = 0
    for value, symbol in _ROMAN_NUMERALS:
        while roman[index:index + len(symbol)] == symbol:
            total += value
            index += len(symbol)
    if index != len(roman):
        raise ValueError(f"invalid Roman numeral: {roman!r}")
    if to_roman(total) != roman:
        raise ValueError(f"invalid Roman numeral: {roman!r}")
    return total


def is_valid_roman(roman: str) -> bool:
    """Return ``True`` when *roman* is a valid Roman numeral.

    Args:
        roman: Roman numeral string to validate.

    Returns:
        ``True`` if *roman* is a valid Roman numeral, ``False`` otherwise.
    """
    try:
        from_roman(roman)
    except (TypeError, ValueError):
        return False
    return True
