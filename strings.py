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
    "is_binary",
    "is_octal",
    "is_digit",
    "is_hex",
    "is_integer",
    "is_decimal",
    "is_printable",
    "is_identifier",
    "is_pangram",
    "is_rotation",
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
    "count_digits",
    "count_letters",
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
    """Return the reverse of the given string.

    Args:
        s: The string to reverse.

    Returns:
        The characters of *s* in reverse order. The empty string is returned
        unchanged.

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


def reverse_words(s: str) -> str:
    """Return the string with the order of its words reversed.

    Words are the whitespace-delimited runs of characters in *s*; the words
    are returned in reverse order, separated by a single space.

    Args:
        s: The string whose words to reverse.

    Returns:
        A string with the words of *s* in reverse order. Leading, trailing,
        and internal runs of whitespace are collapsed to a single separating
        space, so ``reverse_words("  hello   world  ")`` is ``"world hello"``.
        The empty string and a single word are returned unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> reverse_words("hello world")
        'world hello'
        >>> reverse_words("one")
        'one'
        >>> reverse_words("")
        ''
    """
    _require_string(s, "s")
    words = s.split()
    return " ".join(reversed(words))


def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the given string.

    Comparison is case-insensitive.

    Args:
        s: The string to count vowels in.

    Returns:
        The number of vowel characters. Non-alphabetic characters are ignored.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> count_vowels("hello world")
        3
        >>> count_vowels("HELLO")
        2
        >>> count_vowels("rhythm")
        0
        >>> count_vowels("")
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

    Returns:
        The number of consonant characters.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> count_consonants("hello world")
        7
        >>> count_consonants("HELLO")
        3
        >>> count_consonants("a1e2")
        0
        >>> count_consonants("")
        0
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

    Examples:
        >>> count_uppercase("Hello World")
        2
        >>> count_uppercase("HELLO")
        5
        >>> count_uppercase("hello")
        0
        >>> count_uppercase("")
        0
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

    Examples:
        >>> count_lowercase("Hello World")
        8
        >>> count_lowercase("hello")
        5
        >>> count_lowercase("HELLO")
        0
        >>> count_lowercase("")
        0
    """
    _require_string(s, "s")
    return sum(1 for ch in s if ch.islower())


def is_anagram(s1: str, s2: str) -> bool:
    """Return True if s1 and s2 are anagrams of each other.

    Comparison is case-insensitive and ignores whitespace.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        True when the alphabetic characters of *s1* and *s2* are the same
        multiset, False otherwise. The empty string is an anagram of itself.

    Raises:
        TypeError: If either argument is not a string.

    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("Hello", "World")
        False
        >>> is_anagram("", "")
        True
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


def is_rotation(s1: str, s2: str) -> bool:
    """Return True if *s2* is a rotation of *s1*.

    A string *s2* is a rotation of *s1* when it can be formed by moving some
    number of characters from the front of *s1* to its end (for example,
    rotating ``"abcde"`` by two positions yields ``"cdeab"``). Two strings
    are rotations of each other only when they have the same length and *s2*
    appears as a substring of *s1* concatenated with itself.

    Args:
        s1: The string to rotate.
        s2: The candidate rotation.

    Returns:
        True if *s2* is a rotation of *s1*, False otherwise. The empty string
        is a rotation of itself.

    Raises:
        TypeError: If either argument is not a string.

    Examples:
        >>> is_rotation("abcde", "cdeab")
        True
        >>> is_rotation("abcde", "abced")
        False
        >>> is_rotation("", "")
        True
    """
    _require_string(s1, "s1")
    _require_string(s2, "s2")
    if len(s1) != len(s2):
        return False
    return s2 in s1 + s1


def capitalize_words(s: str) -> str:
    """Capitalize the first letter of each whitespace-delimited word in *s*.

    Each word has its first character upper-cased and the rest lower-cased.
    Words are separated by single spaces in the output, so runs of whitespace
    in *s* are collapsed.

    Args:
        s: The string to capitalize.

    Returns:
        A string with the first letter of each word capitalized. The empty
        string is returned unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("a b c")
        'A B C'
        >>> capitalize_words("")
        ''
    """
    _require_string(s, "s")
    return " ".join(word.capitalize() for word in s.split(" "))


def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """Return True if *s* is a palindrome.

    Args:
        s: The string to check.
        ignore_case: Whether to ignore case differences (default True).
        ignore_spaces: Whether to ignore whitespace (default True).

    Returns:
        True if the string is a palindrome, False otherwise. The empty string
        is a palindrome.

    Raises:
        TypeError: If *s* is not a string, or if *ignore_case* or
            *ignore_spaces* is not a bool.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("A man a plan a canal Panama")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("")
        True
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
        The truncated string. If *s* is already no longer than *length*, it
        is returned unchanged. When *length* is zero, the empty string is
        returned. When *suffix* is longer than *length*, a ``ValueError`` is
        raised.

    Raises:
        TypeError: If *s* is not a string or *length* is not an int.
        ValueError: If *length* is negative or *suffix* is longer than
            *length*.

    Examples:
        >>> truncate("hello world", 5)
        'he...'
        >>> truncate("hello", 10)
        'hello'
        >>> truncate("hello world", 0)
        ''
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
    """Return the Levenshtein distance between *s1* and *s2*.

    The Levenshtein distance is the minimum number of single-character
    insertions, deletions, or substitutions required to turn *s1* into *s2*.

    Args:
        s1: The first string.
        s2: The second string.

    Returns:
        The edit distance between the two strings. Identical strings have a
        distance of 0; an empty string compared with a string of length *n*
        has a distance of *n*.

    Raises:
        TypeError: If either argument is not a string.

    Examples:
        >>> levenshtein_distance("kitten", "sitting")
        3
        >>> levenshtein_distance("abc", "abc")
        0
        >>> levenshtein_distance("", "abc")
        3
    """
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
    """Convert string to title case.

    Each whitespace-delimited word of *s* has its first character
    upper-cased and the remaining characters lower-cased.

    Args:
        s: The string to title-case.

    Returns:
        The title-cased string. The empty string is returned unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> title_case("hello world")
        'Hello World'
        >>> title_case("a b c")
        'A B C'
        >>> title_case("")
        ''
    """
    _require_string(s, "s")
    return " ".join(word.capitalize() for word in s.split())


def camel_to_snake(s: str) -> str:
    """Convert a camelCase string to snake_case.

    Args:
        s: The camelCase string to convert.

    Returns:
        The snake_case form of *s*. The empty string is returned unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> camel_to_snake("camelCase")
        'camel_case'
        >>> camel_to_snake("HTMLParser")
        'html_parser'
        >>> camel_to_snake("")
        ''
    """
    _require_string(s, "s")
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(s: str, capitalize_first: bool = False) -> str:
    """Convert a snake_case string to camelCase.

    Args:
        s: The snake_case string to convert.
        capitalize_first: If True, produce PascalCase (first letter
            capitalized); if False (the default), produce lower camelCase.

    Returns:
        The camelCase form of *s*. The empty string is returned unchanged.

    Raises:
        TypeError: If *s* is not a string or *capitalize_first* is not a bool.

    Examples:
        >>> snake_to_camel("hello_world")
        'helloWorld'
        >>> snake_to_camel("hello_world", capitalize_first=True)
        'HelloWorld'
        >>> snake_to_camel("")
        ''
    """
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
    """Convert a string to a URL-friendly slug.

    The string is lower-cased, stripped, and runs of non-word characters,
    whitespace, underscores, and hyphens are collapsed to a single
    hyphen. Leading and trailing hyphens are removed.

    Args:
        s: The string to slugify.

    Returns:
        The slug form of *s*. The empty string is returned unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("  Some Title  ")
        'some-title'
        >>> slugify("")
        ''
    """
    _require_string(s, "s")
    import re

    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    s = re.sub(r"^-+|-+$", "", s)
    return s


def remove_whitespace(s: str) -> str:
    """Remove all whitespace characters from *s*.

    Args:
        s: The string to strip whitespace from.

    Returns:
        *s* with every whitespace character (spaces, tabs, newlines, etc.)
        removed. The empty string is returned unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> remove_whitespace("hello world")
        'helloworld'
        >>> remove_whitespace("a\tb\nc")
        'abc'
        >>> remove_whitespace("")
        ''
    """
    _require_string(s, "s")
    return "".join(s.split())


def word_count(s: str) -> int:
    """Count the number of whitespace-delimited words in *s*.

    Args:
        s: The string to count words in.

    Returns:
        The number of words. Whitespace-only and empty strings return 0.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> word_count("hello world")
        2
        >>> word_count("   ")
        0
        >>> word_count("")
        0
    """
    _require_string(s, "s")
    if not s.strip():
        return 0
    return len(s.split())


def char_count(s: str) -> int:
    """Return the number of characters in *s*.

    Equivalent to ``len(s)`` but provided as a typed helper.

    Args:
        s: The string to count characters in.

    Returns:
        The number of characters in *s*, including whitespace.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> char_count("hello")
        5
        >>> char_count("")
        0
    """
    _require_string(s, "s")
    return len(s)


def normalize_whitespace(s: str) -> str:
    """Collapse runs of whitespace in *s* to a single space and trim ends.

    Args:
        s: The string to normalize.

    Returns:
        *s* with all runs of whitespace replaced by a single space and
        leading/trailing whitespace removed. The empty string is returned
        unchanged.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> normalize_whitespace("hello   world")
        'hello world'
        >>> normalize_whitespace("  a  b  ")
        'a b'
        >>> normalize_whitespace("")
        ''
    """
    _require_string(s, "s")
    import re

    return re.sub(r"\s+", " ", s).strip()


def is_blank(s: str) -> bool:
    """Return True if *s* is empty or contains only whitespace.

    Args:
        s: The string to check.

    Returns:
        True when *s* is empty or every character is whitespace, False
        otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_blank("")
        True
        >>> is_blank("   ")
        True
        >>> is_blank("hello")
        False
    """
    _require_string(s, "s")
    return s.strip() == ""


def is_upper(s: str) -> bool:
    """Return True if all alphabetic chars in *s* are uppercase.

    At least one alphabetic character must be present for the result to be
    True, so strings containing no letters return False.

    Args:
        s: The string to check.

    Returns:
        True when *s* contains at least one alphabetic character and every
        alphabetic character is uppercase, False otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_upper("HELLO")
        True
        >>> is_upper("Hello")
        False
        >>> is_upper("123")
        False
        >>> is_upper("")
        False
    """
    _require_string(s, "s")
    if not any(c.isalpha() for c in s):
        return False
    return s == s.upper()


def is_lower(s: str) -> bool:
    """Return True if all alphabetic chars in *s* are lowercase.

    At least one alphabetic character must be present for the result to be
    True, so strings containing no letters return False.

    Args:
        s: The string to check.

    Returns:
        True when *s* contains at least one alphabetic character and every
        alphabetic character is lowercase, False otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_lower("hello")
        True
        >>> is_lower("Hello")
        False
        >>> is_lower("123")
        False
        >>> is_lower("")
        False
    """
    _require_string(s, "s")
    if not any(c.isalpha() for c in s):
        return False
    return s == s.lower()


def is_title(s: str) -> bool:
    """Return True if *s* is titlecased.

    A string is titlecased when each word starts with an uppercase character
    and the remaining characters are lowercase, and at least one cased
    character is present.

    Args:
        s: The string to check.

    Returns:
        True when *s* is titlecased, False otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_title("Hello World")
        True
        >>> is_title("hello World")
        False
        >>> is_title("")
        False
    """
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


def is_binary(s: str) -> bool:
    """Return True if all characters in the string are binary digits (0 or 1).

    A binary digit is one of 0 or 1. The string must be non-empty.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_binary("1010")
        True
        >>> is_binary("0")
        True
        >>> is_binary("102")
        False
        >>> is_binary("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch in "01" for ch in s)


def is_octal(s: str) -> bool:
    """Return True if all characters in the string are octal digits (0-7).

    An octal digit is one of 0, 1, 2, 3, 4, 5, 6, 7. The string must be non-empty.

    Args:
        s: The string to test.

    Raises:
        TypeError: If s is not a string.

    Examples:
        >>> is_octal("755")
        True
        >>> is_octal("0")
        True
        >>> is_octal("89")
        False
        >>> is_octal("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch in "01234567" for ch in s)


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


def is_decimal(s: str) -> bool:
    """Return True if the string represents a decimal number.

    A decimal number is a sequence of digits (0-9) with an optional leading
    sign (``+`` or ``-``) and an optional decimal point. At least one digit
    must appear on each side of the decimal point when present. Surrounding
    whitespace is ignored, so ``" 12.5 "`` is accepted.

    Args:
        s: The string to test.

    Returns:
        True if *s* is a decimal number, False otherwise. The empty string
        and strings containing only whitespace return False.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_decimal("123")
        True
        >>> is_decimal("12.5")
        True
        >>> is_decimal("-3.14")
        True
        >>> is_decimal("+0.5")
        True
        >>> is_decimal("0.0")
        True
        >>> is_decimal("12.")
        False
        >>> is_decimal(".5")
        False
        >>> is_decimal("12.3.4")
        False
        >>> is_decimal("12a")
        False
        >>> is_decimal("")
        False
        >>> is_decimal(" 12.5 ")
        True
    """
    _require_string(s, "s")
    if not s:
        return False
    s_stripped = s.strip()
    if not s_stripped:
        return False
    if s_stripped[0] in ("+", "-"):
        s_stripped = s_stripped[1:]
    if not s_stripped:
        return False
    if s_stripped.count(".") > 1:
        return False
    if "." in s_stripped:
        int_part, _, frac_part = s_stripped.partition(".")
        return int_part.isdigit() and frac_part.isdigit() and (
            int_part or frac_part
        )
    return s_stripped.isdigit()


def is_printable(s: str) -> bool:
    """Return True if all characters in *s* are printable.

    A character is printable when ``str.isprintable()`` returns True for it;
    whitespace characters other than the space character are not printable.

    Args:
        s: The string to test.

    Returns:
        True if *s* is non-empty and every character is printable, False
        otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_printable("hello world!")
        True
        >>> is_printable("hello\tworld")
        False
        >>> is_printable("")
        False
    """
    _require_string(s, "s")
    if not s:
        return False
    return all(ch.isprintable() for ch in s)


def is_identifier(s: str) -> bool:
    """Return True if *s* is a valid Python identifier.

    Args:
        s: The string to test.

    Returns:
        True if *s* is non-empty and ``str.isidentifier()`` returns True for
        it, False otherwise.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> is_identifier("foo")
        True
        >>> is_identifier("_foo")
        True
        >>> is_identifier("123foo")
        False
        >>> is_identifier("foo-bar")
        False
        >>> is_identifier("")
        False
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
    """Remove *prefix* from *s* if present, otherwise return *s* unchanged.

    Args:
        s: The string to strip the prefix from.
        prefix: The prefix to remove.

    Returns:
        *s* with *prefix* removed when it starts with *prefix*; *s* otherwise.

    Raises:
        TypeError: If *s* or *prefix* is not a string.

    Examples:
        >>> removeprefix("prefix-value", "prefix-")
        'value'
        >>> removeprefix("value", "prefix-")
        'value'
        >>> removeprefix("abc", "")
        'abc'
    """
    _require_string(s, "s")
    _require_string(prefix, "prefix")
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


def removesuffix(s: str, suffix: str) -> str:
    """Remove *suffix* from *s* if present, otherwise return *s* unchanged.

    Args:
        s: The string to strip the suffix from.
        suffix: The suffix to remove.

    Returns:
        *s* with *suffix* removed when it ends with *suffix*; *s* otherwise.

    Raises:
        TypeError: If *s* or *suffix* is not a string.

    Examples:
        >>> removesuffix("value-suffix", "-suffix")
        'value'
        >>> removesuffix("value", "-suffix")
        'value'
        >>> removesuffix("abc", "")
        'abc'
    """
    _require_string(s, "s")
    _require_string(suffix, "suffix")
    if not suffix:
        return s
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


def count_digits(s: str) -> int:
    """Return the number of digit characters in *s*.

    Args:
        s: The string to count digits in.

    Returns:
        The number of digit characters.

    Raises:
        TypeError: If *s* is not a string.

    Examples:
        >>> count_digits("abc123")
        3
        >>> count_digits("2024")
        4
        >>> count_digits("hello")
        0
        >>> count_digits("")
        0
    """
    _require_string(s, "s")
    return sum(1 for ch in s if ch.isdigit())


def count_letters(s: str) -> int:
    """Return the number of alphabetic characters in *s*.

    Args:
        s: The string to count letters in.

    Returns:
        The number of alphabetic characters.

    Raises:
        TypeError: If *s* is not a string.
    """
    _require_string(s, "s")
    return sum(1 for ch in s if ch.isalpha())
