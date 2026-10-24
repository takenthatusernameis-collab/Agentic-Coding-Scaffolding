"""String utility functions for common text operations."""


def reverse_string(s: str) -> str:
    """Return the reverse of the given string.

    Args:
        s: The string to reverse.

    Examples:
        >>> reverse_string("hello")
        'olleh'
        >>> reverse_string("")
        ''
    """
    return s[::-1]


def is_palindrome(s: str) -> bool:
    """Return True if the string reads the same forwards and backwards.

    Comparison is case-insensitive and ignores non-alphanumeric characters.

    Args:
        s: The string to check.

    Examples:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
        >>> is_palindrome("A man, a plan, a canal: Panama")
        True
    """
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]


def count_vowels(s: str) -> int:
    """Return the number of vowels (a, e, i, o, u) in the given string.

    Comparison is case-insensitive.

    Args:
        s: The string to count vowels in.

    Examples:
        >>> count_vowels("hello")
        2
        >>> count_vowels("rhythm")
        0
    """
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch in vowels)


def count_consonants(s: str) -> int:
    """Return the number of consonants in the given string.

    Comparison is case-insensitive and ignores non-alphabetic characters.

    Args:
        s: The string to count consonants in.

    Examples:
        >>> count_consonants("hello")
        3
        >>> count_consonants("rhythm")
        5
        >>> count_consonants("hello world")
        7
    """
    vowels = {"a", "e", "i", "o", "u"}
    return sum(1 for ch in s.lower() if ch.isalpha() and ch not in vowels)


def is_anagram(a: str, b: str) -> bool:
    """Return True if *a* and *b* are anagrams of each other.

    Comparison is case-insensitive and ignores all whitespace.

    Args:
        a: The first string.
        b: The second string.

    Examples:
        >>> is_anagram("listen", "silent")
        True
        >>> is_anagram("hello", "world")
        False
        >>> is_anagram("The Eyes", "They See")
        True
    """

    def normalize(text: str) -> str:
        return "".join(sorted(ch.lower() for ch in text if not ch.isspace()))

    return normalize(a) == normalize(b)



def capitalize_words(s: str) -> str:
    """Return *s* with the first letter of every word capitalized.

    Args:
        s: The string to capitalize.

    Examples:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("python programming")
        'Python Programming'
    """
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
        ValueError: If *length* is negative or smaller than the suffix length.

    Examples:
        >>> truncate("hello world", 8)
        'hello...'
        >>> truncate("hi", 8)
        'hi'
        >>> truncate("hello world", 8, suffix="..")
        'hello w..'
    """
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
