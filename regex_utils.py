"""Regular expression utility functions.

Provides safe, documented helpers for compiling, matching, searching,
replacing, splitting, and extracting with regular expressions.
"""

from __future__ import annotations

import re
from typing import List, Match, Optional, Pattern, Tuple

__all__: List[str] = [
    "compile_pattern",
    "is_valid_pattern",
    "match_pattern",
    "search_pattern",
    "find_all",
    "replace_pattern",
    "split_pattern",
    "escape_pattern",
    "extract_groups",
    "named_groups",
]


def compile_pattern(pattern: str, flags: int = 0) -> Pattern[str]:
    """Compile a regular expression pattern into a reusable pattern object.

    Args:
        pattern: The regular expression string to compile.
        flags: Regex flags to control matching behavior (e.g. re.IGNORECASE).

    Returns:
        A compiled regular expression pattern object.

    Raises:
        ValueError: If the pattern is not a valid regular expression.

    Examples:
        >>> compile_pattern(r"\\d+")
        re.compile(r'\\d+')
    """
    try:
        return re.compile(pattern, flags)
    except re.error as exc:
        raise ValueError(f"Invalid regular expression: {exc}") from exc


def is_valid_pattern(pattern: str, flags: int = 0) -> bool:
    r"""Return True if the pattern is a valid regular expression.

    Args:
        pattern: The regular expression string to validate.
        flags: Regex flags to control matching behavior.

    Returns:
        True if the pattern compiles successfully, False otherwise.

    Examples:
        >>> is_valid_pattern(r"\d+")
        True
        >>> is_valid_pattern("(")
        False
    """
    try:
        re.compile(pattern, flags)
        return True
    except re.error:
        return False


def match_pattern(pattern: str, text: str, flags: int = 0) -> Optional[Match[str]]:
    """Check if the pattern matches at the beginning of the text.

    Args:
        pattern: The regular expression string.
        text: The text to match against.
        flags: Regex flags to control matching behavior.

    Returns:
        A match object if the pattern matches at the start, else None.

    Examples:
        >>> match_pattern(r"Hello", "Hello world")
        <re.Match object; span=(0, 5), match='Hello'>
        >>> match_pattern(r"World", "Hello world") is None
        True
    """
    return re.match(pattern, text, flags)


def search_pattern(pattern: str, text: str, flags: int = 0) -> Optional[Match[str]]:
    """Search the text for the first location where the pattern matches.

    Args:
        pattern: The regular expression string.
        text: The text to search.
        flags: Regex flags to control matching behavior.

    Returns:
        A match object for the first match, else None.

    Examples:
        >>> search_pattern(r"world", "Hello world")
        <re.Match object; span=(6, 11), match='world'>
        >>> search_pattern(r"zzz", "Hello world") is None
        True
    """
    return re.search(pattern, text, flags)


def find_all(pattern: str, text: str, flags: int = 0) -> List[str]:
    r"""Return all non-overlapping matches of the pattern in the text.

    Args:
        pattern: The regular expression string.
        text: The text to search.
        flags: Regex flags to control matching behavior.

    Returns:
        A list of matched strings.

    Examples:
        >>> find_all(r"\d+", "abc123def456")
        ['123', '456']
        >>> find_all(r"\d+", "no numbers here")
        []
    """
    return re.findall(pattern, text, flags)


def replace_pattern(pattern: str, repl: str, text: str, flags: int = 0) -> str:
    r"""Replace occurrences of the pattern in the text with repl.

    Args:
        pattern: The regular expression string.
        repl: The replacement string.
        text: The text to modify.
        flags: Regex flags to control matching behavior.

    Returns:
        The text with replacements applied.

    Examples:
        >>> replace_pattern(r"\s+", "-", "Hello   world")
        'Hello-world'
    """
    return re.sub(pattern, repl, text, flags=flags)


def split_pattern(pattern: str, text: str, flags: int = 0) -> List[str]:
    """Split the text by occurrences of the pattern.

    Args:
        pattern: The regular expression string.
        text: The text to split.
        flags: Regex flags to control matching behavior.

    Returns:
        A list of substrings.

    Examples:
        >>> split_pattern(r",\\s*", "a, b, c")
        ['a', 'b', 'c']
    """
    return re.split(pattern, text, flags=flags)


def escape_pattern(text: str) -> str:
    """Escape all special regular expression characters in the text.

    Args:
        text: The literal text to escape.

    Returns:
        The escaped string safe to use as a regex pattern.

    Examples:
        >>> escape_pattern("a.b*c?")
        'a\\.b\\*c\\?'
    """
    return re.escape(text)


def extract_groups(pattern: str, text: str, flags: int = 0) -> Optional[Tuple[str, ...]]:
    """Return the captured groups of the first match, if any.

    Args:
        pattern: The regular expression string with capturing groups.
        text: The text to match against.
        flags: Regex flags to control matching behavior.

    Returns:
        A tuple of captured group strings, or None if no match.

    Examples:
        >>> extract_groups(r"(\\d+)-(\\d+)", "ID 12-34 here")
        ('12', '34')
    """
    match = re.search(pattern, text, flags)
    if match is None:
        return None
    return match.groups()


def named_groups(pattern: str, text: str, flags: int = 0) -> Optional[dict]:
    """Return the named captured groups of the first match, if any.

    Args:
        pattern: The regular expression string with named capturing groups.
        text: The text to match against.
        flags: Regex flags to control matching behavior.

    Returns:
        A dictionary mapping group names to matched strings, or None if no match.

    Examples:
        >>> named_groups(r"(?P<year>\\d{4})-(?P<month>\\d{2})", "2024-01")
        {'year': '2024', 'month': '01'}
    """
    match = re.search(pattern, text, flags)
    if match is None:
        return None
    return match.groupdict()
