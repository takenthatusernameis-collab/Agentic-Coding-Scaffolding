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
    "title_case",
    "camel_to_snake",
    "snake_to_camel",
    "slugify",
    "remove_whitespace",
    "word_count",
    "char_count",
    "is_blank",
    "normalize_whitespace",
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


def is_palindrome(s: str) -> bool:
    """Return True if the string reads the same forwards and backwards.

    Comparison is case-insensitive and ignores non-alphanumeric characters.
    """
    _require_string(s, "s")
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


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


def is_anagram(a: str, b: str) -> bool:
    """Return True if *a* and *b* are anagrams of each other.

    Comparison is case-insensitive and ignores all whitespace.
    """
    _require_string(a, "a")
    _require_string(b, "b")
    return sorted(a.lower().replace(" ", "")) == sorted(b.lower().replace(" ", ""))


def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each word in the string."""
    _require_string(s, "s")
    return " ".join(word[:1].upper() + word[1:] for word in s.split(" "))


def truncate(s: str, length: int, suffix: str = "...") -> str:
    """Truncate *s* to at most *length* characters, appending *suffix*."""
    _require_string(s, "s")
    _require_string(suffix, "suffix")
    _require_int(length, "length")
    if length < 0:
        raise ValueError("length must be non-negative")
    if length == 0:
        return ""
    if len(suffix) > length:
        raise ValueError("suffix must not be longer than length")
    if len(s) <= length:
        return s
    return s[: length - len(suffix)] + suffix


def levenshtein_distance(a: str, b: str) -> int:
    """Return the edit distance between *a* and *b*."""
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
