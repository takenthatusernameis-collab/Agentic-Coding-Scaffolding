"""String utility functions for common text operations.

Provides helpers for reversing, inspecting, and transforming text. All
functions validate their inputs and raise :class:`TypeError` or
:class:`ValueError` on invalid arguments.
"""

from typing import List

__all__: List[str] = [
    "reverse_string",
    "is_palindrome",
    "count_vowels",
    "count_consonants",
    "is_anagram",
    "capitalize_words",
    "truncate",
    "levenshtein_distance",
]


def _require_string(value: object, name: str) -> str:
    """Validate that *value* is a string, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The argument name used in error messages.

    Returns:
        The validated string.

    Raises:
        TypeError: If ``value`` is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_int(value: object, name: str) -> int:
    """Validate that *value* is an int, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The argument name used in error messages.

    Returns:
        The validated integer.

    Raises:
        TypeError: If ``value`` is not an int.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def reverse_string(s: str) -> str:
    """Return the reverse of the given string.

    Args:
        s: The string to reverse.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("")
        ''
    """
    _require_string(s, "s")
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Return True if the string reads the same forwards and backwards.

    Comparison is case-insensitive and ignores non-alphanumeric characters.

    Args:
        s: The string to check.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
    """
    _require_string(s, "s")
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the given string.

    Comparison is case-insensitive.

    Args:
        s: The string to count vowels in.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> count_vowels("hello")
        2
        >>> count_vowels("rhythm")
        0
    """
    _require_string(s, "s")
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch in vowels)


def count_consonants(s: str) -> int:
    """Return the number of consonants in the given string.

    Comparison is case-insensitive and ignores non-alphabetic characters.

    Args:
        s: The string to count consonants in.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> count_consonants("hello")
        3
        >>> count_consonants("rhythm")
        5
        >>> count_consonants("hello world")
        7
    """
    _require_string(s, "s")
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch.isalpha() and ch not in vowels)


def is_anagram(a: str, b: str) -> bool:
    """Return True if *a* and *b* are anagrams of each other.

    Comparison is case-insensitive and ignores all whitespace.

    Args:
        a: The first string.
        b: The second string.

    Raises:
        TypeError: If *a* or *b* is not a string.

    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("hello", "world")
        False
        >>> is_anagram("The Eyes", "They See")
        True
    """
    _require_string(a, "a")
    _require_string(b, "b")

    def normalize(text: str) -> str:
        return "".join(sorted(ch.lower() for ch in text if not ch.isspace()))

    return normalize(a) == normalize(b)


def capitalize_words(s: str) -> str:
    """Return *s* with the first letter of every word capitalized.

    Args:
        s: The string to capitalize.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("python programming")
        'Python Programming'
    """
    _require_string(s, "s")
    return " ".join(word[:1].upper() + word[1:] for word in s.split(" "))


def truncate(s: str, length: int, suffix: str = "...") -> str:
    """Truncate *s* to at most *length* characters, appending *suffix*.

    If truncation is necessary, the returned string is exactly *length*
    characters long including the suffix. The suffix is only appended when
    the original string exceeds the limit.

    Args:
        s: The string to truncate.
        length: The maximum length of the returned string.
        suffix: The suffix to append when truncation occurs.

    Returns:
        The possibly truncated string.

    Raises:
        TypeError: If *s* or *suffix* is not a string, or *length* is not an int.
        ValueError: If *length* is negative or smaller than the suffix length.

    Examples:
        >>> truncate("hello world", 8)
        'hello...'
        >>> truncate("hi", 8)
        'hi'
        >>> truncate("hello world", 8, suffix="..")
        'hello w..'
    """
    _require_string(s, "s")
    _require_string(suffix, "suffix")
    _require_int(length, "length")
    if length < 0:
        raise ValueError("length must be non-negative")
    if len(suffix) > length:
        raise ValueError("suffix must not be longer than length")
    if len(s) <= length:
        return s
    return s[: length - len(suffix)] + suffix


def levenshtein_distance(a: str, b: str) -> int:
    """Return the edit distance between *a* and *b*.

    The edit distance is the minimum number of single-character edits
    (insertions, deletions, or substitutions) required to transform *a*
    into *b*.

    Args:
        a: The first string.
        b: The second string.

    Raises:
        TypeError: If *a* or *b* is not a string.

    Returns:
        The Levenshtein distance between the two strings.

    Examples:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("", "abc")
        3
        >>> levenshtein_distance("abc", "abc")
        0
    """
    _require_string(a, "a")
    _require_string(b, "b")
    if not a:
        return len(b)
    if not b:
        return len(a)
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        current = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            current[j] = min(
                current[j - 1] + 1,
                previous[j] + 1,
                previous[j - 1] + cost,
            )
        previous = current
    return previous[-1]