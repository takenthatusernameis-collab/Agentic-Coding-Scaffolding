"""String utility functions for common text operations.

Provides helpers for reversing, inspecting, and transforming text. All
functions validate their inputs and raise :class:`TypeError` or
:class:`ValueError` on invalid arguments.
"""

from typing import List

__all__: List[str] = [
    "reverse_string",
    "reverse_words",
    "is_palindrome",
    "count_vowels",
    "count_consonants",
    "count_lowercase",
    "count_uppercase",
    "is_anagram",
    "capitalize_words",
    "truncate",
    "levenshtein_distance",
    "title_case",
    "camel_to_snake",
    "snake_to_camel",
    "slugify",
    "remove_whitespace",
    "word_count",
    "char_count",
    "is_blank",
    "normalize_whitespace",
    "is_upper",
    "is_lower",
    "is_title",
    "is_ascii",
    "is_whitespace",
    "is_space",
    "is_alpha",
    "is_alphanumeric",
    "is_digit",
    "is_hex",
    "is_integer",
    "is_printable",
    "is_identifier",
    "is_pangram",
    "is_subsequence",
    "initials",
    "swap_case",
    "count_occurrences",
    "starts_with",
    "ends_with",
    "pad_left",
    "pad_right",
    "center",
    "lstrip_chars",
    "rstrip_chars",
    "strip_chars",
    "removeprefix",
    "removesuffix",
    "partition",
    "rpartition",
    "split_lines",
    "join_lines",
    "replace_many",
    "strip_html",
    "common_prefix",
    "common_suffix",
    "char_frequency",
    "first_n",
    "last_n",
    "take",
    "drop",
    "between",
    "contains_any",
    "contains_all",
    "count_words",
    "remove_punctuation",
    "remove_digits",
    "remove_blank_lines",
    "chunk_string",
    "remove_vowels",
    "remove_consonants",
]


def _require_string(value: object, name: str) -> str:
    """Validate that *value* is a string, raising ``TypeError`` otherwise."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_int(value: object, name: str) -> int:
    """Validate that *value* is an int, raising ``TypeError`` otherwise."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def reverse_string(s: str) -> str:
    """Return the reverse of the given string."""
    _require_string(s, "s")
    return s[::-1]


def reverse_words(s: str) -> str:
    """Return the string with the order of its words reversed."""
    _require_string(s, "s")
    words = s.split()
    return " ".join(reversed(words))


def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the given string.

    Comparison is case-insensitive.
    """
    _require_string(s, "s")
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch in vowels)


def count_consonants(s: str) -> int:
    """Return the number of consonants in the given string.

    Comparison is case-insensitive and ignores non-alphabetic characters.
    """
    _require_string(s, "s")
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch.isalpha() and ch not in vowels)


def count_uppercase(s: str) -> int:
    """Return the number of uppercase letters in *s*.

    Args:
        s: The string to count uppercase letters in.

    Returns:
        The number of uppercase alphabetic characters.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    return sum(1 for ch in s if ch.isupper())


def count_lowercase(s: str) -> int:
    """Return the number of lowercase letters in *s*.

    Args:
        s: The string to count lowercase letters in.

    Returns:
        The number of lowercase alphabetic characters.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    return sum(1 for ch in s if ch.islower())


def is_anagram(s1: str, s2: str) -> bool:
    """Return True if s1 and s2 are anagrams of each other.

    Comparison is case-insensitive and ignores whitespace.
    """
    _require_string(s1, "s1")
    _require_string(s2, "s2")
    cleaned1 = "".join(ch.lower() for ch in s1 if not ch.isspace())
    cleaned2 = "".join(ch.lower() for ch in s2 if not ch.isspace())
    return sorted(cleaned1) == sorted(cleaned2)


def is_subsequence(needle: str, haystack: str) -> bool:
    """Return True if *needle* is a subsequence of *haystack*.

    A subsequence is formed by deleting zero or more characters from
    *haystack* without changing the order of the remaining characters, so
    every character of *needle* must appear in *haystack* in the same
    relative order (not necessarily consecutively). The empty string is a
    subsequence of any string.

    Args:
        needle: The subsequence to search for.
        haystack: The string to search within.

    Returns:
        True if *needle* is a subsequence of *haystack*.

    Raises:
        TypeError: If either argument is not a string.

    Examples:
        >>> is_subsequence("abc", "aebdc")
        True
        >>> is_subsequence("abc", "acb")
        False
        >>> is_subsequence("", "anything")
        True
    """
    _require_string(needle, "needle")
    _require_string(haystack, "haystack")
    if not needle:
        return True
    i = 0
    for ch in haystack:
        if ch == needle[i]:
            i += 1
            if i == len(needle):
                return True
    return False


def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each word."""
    _require_string(s, "s")
    return " ".join(word.capitalize() for word in s.split(" "))


def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """Return True if *s* is a palindrome.

    Args:
        s: The string to check.
        ignore_case: Whether to ignore case differences (default True).
        ignore_spaces: Whether to ignore whitespace (default True).

    Returns:
        True if the string is a palindrome, False otherwise.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    if not isinstance(ignore_case, bool):
        raise TypeError(f"ignore_case must be a bool, got {type(ignore_case).__name__}")
    if not isinstance(ignore_spaces, bool):
        raise TypeError(f"ignore_spaces must be a bool, got {type(ignore_spaces).__name__}")
    cleaned = []
    for c in s:
        if ignore_spaces and c.isspace():
            continue
        if not c.isalnum():
            continue
        if ignore_case:
            cleaned.append(c.lower())
        else:
            cleaned.append(c)
    cleaned_str = "".join(cleaned)
    return cleaned_str == cleaned_str[::-1]


def truncate(s: str, length: int, suffix: str = "...") -> str:
    """Truncate a string to a specified length.

    Args:
        s: The string to truncate.
        length: Maximum length of the result.
        suffix: Suffix to append if truncated (default "...").

    Returns:
        Truncated string.

    Raises:
        TypeError: If *s* is not a string or *length* is not an int.
        ValueError: If *length* is negative.
    """
    _require_string(s, "s")
    _require_int(length, "length")
    _require_string(suffix, "suffix")
    if length < 0:
        raise ValueError("length must be non-negative")
    if length == 0:
        return ""
    if len(s) <= length:
        return s
    if len(suffix) > length:
        raise ValueError("suffix cannot be longer than length")
    return s[: max(0, length - len(suffix))] + suffix


def levenshtein_distance(s1: str, s2: str) -> int:
    """Return the Levenshtein distance between s1 and s2."""
    _require_string(s1, "s1")
    _require_string(s2, "s2")
    if s1 == s2:
        return 0
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    previous = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous[j + 1] + 1
            deletions = current[j] + 1
            substitutions = previous[j] + (c1 != c2)
            current.append(min(insertions, deletions, substitutions))
        previous = current
    return previous[-1]


def title_case(s: str) -> str:
    """Convert string to title case."""
    _require_string(s, "s")
    return " ".join(word.capitalize() for word in s.split())


def camel_to_snake(s: str) -> str:
    """Convert camelCase to snake_case."""
    _require_string(s, "s")
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(s: str, capitalize_first: bool = False) -> str:
    """Convert snake_case to camelCase."""
    _require_string(s, "s")
    if not isinstance(capitalize_first, bool):
        raise TypeError(f"capitalize_first must be a bool, got {type(capitalize_first).__name__}")
    components = s.split("_")
    if not components:
        return s
    if capitalize_first:
        return "".join(x.title() for x in components)
    return components[0] + "".join(x.title() for x in components[1:])


def slugify(s: str) -> str:
    """Convert string to URL-friendly slug."""
    _require_string(s, "s")
    import re

    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def remove_whitespace(s: str) -> str:
    """Remove all whitespace from string."""
    _require_string(s, "s")
    return "".join(s.split())


def word_count(s: str) -> int:
    """Count words in string."""
    _require_string(s, "s")
    if not s.strip():
        return 0
    return len(s.split())


def char_count(s: str) -> int:
    """Count characters in string."""
    _require_string(s, "s")
    return len(s)


def normalize_whitespace(s: str) -> str:
    """Collapse runs of whitespace to a single space and trim."""
    _require_string(s, "s")
    import re

    return re.sub(r"\s+", " ", s).strip()


def is_blank(s: str) -> bool:
    """Return True if string is empty or contains only whitespace."""
    _require_string(s, "s")
    return s.strip() == ""


def is_upper(s: str) -> bool:
    """Return True if all alphabetic chars are uppercase and at least one alphabetic char."""
    _require_string(s, "s")
    if not any(c.isalpha() for c in s):
        return False
    return s == s.upper()


def is_lower(s: str) -> bool:
    """Return True if all alphabetic chars are lowercase and at least one alphabetic char."""
    _require_string(s, "s")
    if not any(c.isalpha() for c in s):
        return False
    return s == s.lower()


def is_title(s: str) -> bool:
    """Return True if the string is titlecased and contains at least one cased character."""
    _require_string(s, "s")
    if not any(c.isalpha() for c in s):
        return False
    return s == s.title()


def is_alpha(s: str) -> bool:
    """Return True if all characters in the string are alphabetic and at least one character.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_alpha("hello")
        True
        >>> is_alpha("hello world")
        False
        >>> is_alpha("123")
        False
        >>> is_alpha("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch.isalpha() for ch in s)


def is_alphanumeric(s: str) -> bool:
    """Return True if all characters in the string are alphanumeric and at least one character.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_alphanumeric("hello123")
        True
        >>> is_alphanumeric("hello world")
        False
        >>> is_alphanumeric("123")
        True
        >>> is_alphanumeric("")
        False
        >>> is_alphanumeric("hello!")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch.isalnum() for ch in s)


def is_ascii(s: str) -> bool:
    """Return True if all characters in the string are ASCII and at least one character.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_ascii("hello")
        True
        >>> is_ascii("héllo")
        False
        >>> is_ascii("123")
        True
        >>> is_ascii("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ord(ch) < 128 for ch in s)


def is_whitespace(s: str) -> bool:
    """Return True if the string contains only whitespace characters.

    Args:
        s: The string to test.

    Returns:
        True if all characters are whitespace, False otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_whitespace("   ")
        True
        >>> is_whitespace("\\t\\n")
        True
        >>> is_whitespace("hello")
        False
        >>> is_whitespace("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return s.isspace()


def is_space(s: str) -> bool:
    """Return True if the string contains only whitespace characters.

    Alias for :func:`is_whitespace`.

    Args:
        s: The string to test.

    Returns:
        True if all characters are whitespace, False otherwise.

    Raises:
        TypeError: If *s* is not a string.
    """
    return is_whitespace(s)


def is_digit(s: str) -> bool:
    """Return True if all characters in the string are digits and at least one character.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_digit("123")
        True
        >>> is_digit("12.3")
        False
        >>> is_digit("-1")
        False
        >>> is_digit("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch.isdigit() for ch in s)


def is_hex(s: str) -> bool:
    """Return True if all characters in the string are hexadecimal digits.

    A hexadecimal digit is one of 0-9, a-f, or A-F. The string must be
    non-empty.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_hex("1a2f")
        True
        >>> is_hex("1A2F")
        True
        >>> is_hex("1g3")
        False
        >>> is_hex("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in s)


def is_integer(s: str) -> bool:
    """Return True if the string represents an integer (optionally with sign).

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_integer("123")
        True
        >>> is_integer("-123")
        True
        >>> is_integer("+123")
        True
        >>> is_integer("12.3")
        False
        >>> is_integer("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    s_stripped = s.strip()
    if not s_stripped:
        return False
    if s_stripped[0] in ('+', '-'):
        if len(s_stripped) == 1:
            return False
        return s_stripped[1:].isdigit()
    return s_stripped.isdigit()


def is_printable(s: str) -> bool:
    """Return True if all characters in the string are printable.

    Args:
        s: The string to test.

    Returns:
        True if all characters are printable and the string is not empty.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch.isprintable() for ch in s)


def is_identifier(s: str) -> bool:
    """Return True if the string is a valid Python identifier.

    Args:
        s: The string to test.

    Returns:
        True if *s* is a non-empty valid Python identifier.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    if not s:
        return False
    return s.isidentifier()


def is_pangram(s: str) -> bool:
    """Return True if *s* contains every letter of the alphabet at least once.

    The check is case-insensitive and ignores non-alphabetic characters. A
    pangram uses all 26 letters of the English alphabet (e.g. ``"The quick
    brown fox jumps over the lazy dog"``).

    Args:
        s: The string to test.

    Returns:
        True if *s* is a pangram, False otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_pangram("The quick brown fox jumps over the lazy dog")
        True
        >>> is_pangram("Pack my box with five dozen liquor jugs")
        True
        >>> is_pangram("Hello world")
        False
        >>> is_pangram("")
        False
    """
    _require_string(s, "s")
    letters = {ch.lower() for ch in s if ch.isalpha()}
    return set("abcdefghijklmnopqrstuvwxyz").issubset(letters)


def swap_case(s: str) -> str:
    """Return a copy of the string with uppercase converted to lowercase and vice versa."""
    _require_string(s, "s")
    return s.swapcase()


def count_occurrences(s: str, substring: str) -> int:
    """Return the number of non-overlapping occurrences of substring in s."""
    _require_string(s, "s")
    _require_string(substring, "substring")
    if substring == "":
        raise ValueError("substring cannot be empty")
    return s.count(substring)


def starts_with(s: str, prefix: str) -> bool:
    """Return True if string starts with prefix."""
    _require_string(s, "s")
    _require_string(prefix, "prefix")
    return s.startswith(prefix)


def ends_with(s: str, suffix: str) -> bool:
    """Return True if string ends with suffix."""
    _require_string(s, "s")
    _require_string(suffix, "suffix")
    return s.endswith(suffix)


def pad_left(s: str, width: int, fillchar: str = " ") -> str:
    """Pad string on the left to reach width."""
    _require_string(s, "s")
    _require_int(width, "width")
    _require_string(fillchar, "fillchar")
    if len(fillchar) != 1:
        raise ValueError("fillchar must be a single character")
    return s.rjust(width, fillchar)


def pad_right(s: str, width: int, fillchar: str = " ") -> str:
    """Pad string on the right to reach width."""
    _require_string(s, "s")
    _require_int(width, "width")
    _require_string(fillchar, "fillchar")
    if len(fillchar) != 1:
        raise ValueError("fillchar must be a single character")
    return s.ljust(width, fillchar)


def center(s: str, width: int, fillchar: str = " ") -> str:
    """Center string within width."""
    _require_string(s, "s")
    _require_int(width, "width")
    _require_string(fillchar, "fillchar")
    if len(fillchar) != 1:
        raise ValueError("fillchar must be a single character")
    return s.center(width, fillchar)


def lstrip_chars(s: str, chars: str) -> str:
    """Remove leading characters in chars."""
    _require_string(s, "s")
    _require_string(chars, "chars")
    return s.lstrip(chars)


def rstrip_chars(s: str, chars: str) -> str:
    """Remove trailing characters in chars."""
    _require_string(s, "s")
    _require_string(chars, "chars")
    return s.rstrip(chars)


def strip_chars(s: str, chars: str) -> str:
    """Remove leading and trailing characters in chars."""
    _require_string(s, "s")
    _require_string(chars, "chars")
    return s.strip(chars)


def removeprefix(s: str, prefix: str) -> str:
    """Remove prefix if present."""
    _require_string(s, "s")
    _require_string(prefix, "prefix")
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


def removesuffix(s: str, suffix: str) -> str:
    """Remove suffix if present."""
    _require_string(s, "s")
    _require_string(suffix, "suffix")
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def partition(s: str, sep: str) -> tuple:
    """Split string at first occurrence of sep into (before, sep, after)."""
    _require_string(s, "s")
    _require_string(sep, "sep")
    if sep == "":
        raise ValueError("sep cannot be empty")
    return s.partition(sep)


def rpartition(s: str, sep: str) -> tuple:
    """Split string at last occurrence of sep into (before, sep, after)."""
    _require_string(s, "s")
    _require_string(sep, "sep")
    if sep == "":
        raise ValueError("sep cannot be empty")
    return s.rpartition(sep)


def split_lines(s: str, keepends: bool = False) -> List[str]:
    """Split string into lines."""
    _require_string(s, "s")
    if not isinstance(keepends, bool):
        raise TypeError(f"keepends must be a bool, got {type(keepends).__name__}")
    return s.splitlines(keepends=keepends)


def join_lines(lines: List[str], sep: str = "\n") -> str:
    """Join lines with separator."""
    if not isinstance(lines, list):
        raise TypeError(f"lines must be a list, got {type(lines).__name__}")
    for i, line in enumerate(lines):
        if not isinstance(line, str):
            raise TypeError(f"lines[{i}] must be a string, got {type(line).__name__}")
    _require_string(sep, "sep")
    return sep.join(lines)


def replace_many(s: str, replacements: dict) -> str:
    """Replace multiple substrings using a mapping."""
    _require_string(s, "s")
    if not isinstance(replacements, dict):
        raise TypeError(f"replacements must be a dict, got {type(replacements).__name__}")
    result = s
    for old, new in replacements.items():
        if not isinstance(old, str) or not isinstance(new, str):
            raise TypeError("replacements keys and values must be strings")
        result = result.replace(old, new)
    return result


def strip_html(s: str) -> str:
    """Remove HTML tags from string (simple heuristic)."""
    _require_string(s, "s")
    import re

    return re.sub(r"<[^>]+>", "", s)


def common_prefix(s1: str, s2: str) -> str:
    """Return the longest common prefix of two strings.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The longest leading substring shared by both strings.

    Raises:
        TypeError: If either argument is not a string.

    Examples:
        >>> common_prefix("interstellar", "internet")
        'inter'
        >>> common_prefix("hello", "world")
        ''
    """
    _require_string(s1, "s1")
    _require_string(s2, "s2")
    limit = min(len(s1), len(s2))
    index = 0
    while index < limit and s1[index] == s2[index]:
        index += 1
    return s1[:index]


def common_suffix(s1: str, s2: str) -> str:
    """Return the longest common suffix of two strings.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The longest trailing substring shared by both strings.

    Raises:
        TypeError: If either argument is not a string.

    Examples:
        >>> common_suffix("running", "walking")
        'ing'
        >>> common_suffix("hello", "world")
        ''
    """
    _require_string(s1, "s1")
    _require_string(s2, "s2")
    limit = min(len(s1), len(s2))
    index = 0
    while index < limit and s1[-1 - index] == s2[-1 - index]:
        index += 1
    return s1[len(s1) - index:]


def char_frequency(s: str) -> dict:
    """Return a dictionary of character frequencies."""
    _require_string(s, "s")
    freq: dict = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def first_n(s: str, n: int) -> str:
    """Return first n characters of string."""
    _require_string(s, "s")
    _require_int(n, "n")
    if n < 0:
        raise ValueError("n cannot be negative")
    return s[:n]


def last_n(s: str, n: int) -> str:
    """Return last n characters of string."""
    _require_string(s, "s")
    _require_int(n, "n")
    if n < 0:
        raise ValueError("n cannot be negative")
    if n == 0:
        return ""
    return s[-n:]


# aliases
take = first_n


def drop(s: str, n: int) -> str:
    """Return all but the first *n* characters of *s* (alias for ``s[n:]``).

    Args:
        s: The string to slice.
        n: The number of characters to drop from the start.

    Returns:
        The substring starting at index *n*.

    Raises:
        TypeError: If *s* is not a string or *n* is not an integer.
        ValueError: If *n* is negative.
    """
    _require_string(s, "s")
    _require_int(n, "n")
    if n < 0:
        raise ValueError("n cannot be negative")
    return s[n:]


def between(s: str, start: str, end: str) -> str:
    """Return substring between start and end (first occurrence)."""
    _require_string(s, "s")
    _require_string(start, "start")
    _require_string(end, "end")
    if start not in s:
        return ""
    start_idx = s.index(start) + len(start)
    if end not in s[start_idx:]:
        return ""
    end_idx = s.index(end, start_idx)
    return s[start_idx:end_idx]


def contains_any(s: str, substrings: List[str]) -> bool:
    """Return True if s contains any of the substrings."""
    _require_string(s, "s")
    if not isinstance(substrings, list):
        raise TypeError(f"substrings must be a list, got {type(substrings).__name__}")
    for sub in substrings:
        if not isinstance(sub, str):
            raise TypeError("substrings must contain only strings")
    return any(sub in s for sub in substrings)


def contains_all(s: str, substrings: List[str]) -> bool:
    """Return True if s contains all of the substrings."""
    _require_string(s, "s")
    if not isinstance(substrings, list):
        raise TypeError(f"substrings must be a list, got {type(substrings).__name__}")
    for sub in substrings:
        if not isinstance(sub, str):
            raise TypeError("substrings must contain only strings")
    return all(sub in s for sub in substrings)


def count_words(s: str) -> int:
    """Return number of words in string."""
    _require_string(s, "s")
    words = s.split()
    return len(words)


def remove_punctuation(s: str) -> str:
    """Remove all punctuation characters from string."""
    _require_string(s, "s")
    import string

    return "".join(ch for ch in s if ch not in string.punctuation)


def remove_digits(s: str) -> str:
    """Remove all digit characters from string."""
    _require_string(s, "s")
    return "".join(ch for ch in s if not ch.isdigit())


def remove_blank_lines(s: str) -> str:
    """Remove blank lines from *s*, preserving order of non-blank lines."""
    _require_string(s, "s")
    return "\n".join(line for line in s.splitlines() if line.strip() != "")


def chunk_string(s: str, size: int) -> List[str]:
    """Split string *s* into chunks of length *size*.

    Args:
        s: The string to split.
        size: The maximum length of each chunk.

    Returns:
        A list of string chunks. If *s* is empty, an empty list is returned.

    Raises:
        TypeError: If *s* is not a string or *size* is not an int.
        ValueError: If *size* is not positive.
    """
    _require_string(s, "s")
    _require_int(size, "size")
    if size <= 0:
        raise ValueError("size must be positive")
    if not s:
        return []
    return [s[i : i + size] for i in range(0, len(s), size)]


def initials(s: str, *, separator: str = "") -> str:
    """Return the initials of each whitespace-delimited word in *s*.

    Args:
        s: The string to extract initials from.
        separator: The string placed between initials.

    Returns:
        The concatenated initials (uppercase).

    Raises:
        TypeError: If *s* or *separator* is not a string.
    """
    _require_string(s, "s")
    _require_string(separator, "separator")
    words = s.split()
    return separator.join(word[0].upper() for word in words if word)


def remove_vowels(s: str) -> str:
    """Remove all vowel characters (a, e, i, o, u) from *s*.

    Comparison is case-insensitive; non-alphabetic characters are kept.
    """
    _require_string(s, "s")
    vowels = set("aeiouAEIOU")
    return "".join(ch for ch in s if ch not in vowels)


def remove_consonants(s: str) -> str:
    """Remove all consonant characters from *s*.

    Comparison is case-insensitive; non-alphabetic characters are kept.
    """
    _require_string(s, "s")
    vowels = set("aeiouAEIOU")
    return "".join(ch for ch in s if not ch.isalpha() or ch in vowels)


def strip_non_ascii(s: str) -> str:
    """Remove all non-ASCII characters from string *s*.

    Args:
        s: The string to process.

    Returns:
        String with only ASCII characters retained.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    return "".join(ch for ch in s if ord(ch) < 128)


def truncate_bytes(s: str, max_bytes: int, encoding: str = "utf-8") -> str:
    """Truncate string *s* to at most *max_bytes* bytes in given encoding.

    Args:
        s: The string to truncate.
        max_bytes: Maximum number of bytes allowed.
        encoding: Encoding to use for byte length calculation.

    Returns:
        Truncated string that fits within *max_bytes* when encoded.

    Raises:
        TypeError: If *s* is not a string or *max_bytes* is not an int.
        ValueError: If *max_bytes* is negative.
    """
    _require_string(s, "s")
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool):
        raise TypeError("max_bytes must be an integer")
    if max_bytes < 0:
        raise ValueError("max_bytes must be non-negative")
    encoded = s.encode(encoding)
    if len(encoded) <= max_bytes:
        return s
    truncated = encoded[:max_bytes]
    return truncated.decode(encoding, errors="ignore")
