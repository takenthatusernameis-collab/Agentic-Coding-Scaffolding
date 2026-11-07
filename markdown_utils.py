"""Markdown utility functions."""

from __future__ import annotations

import re
from typing import List

__all__ = [
    "count_code_blocks",
    "count_headings",
    "count_words",
    "extract_code_blocks",
    "has_code_blocks",
    "has_headings",
    "has_words",
    "heading_level",
    "is_heading",
    "strip_markdown",
]


def extract_code_blocks(text: str) -> List[str]:
    """Extract fenced code blocks (``` ... ```) from markdown text."""
    pattern = re.compile(r"```(?:[a-zA-Z0-9_+-]*)\n(.*?)```", re.DOTALL)
    return [block.strip("\n") for block in pattern.findall(text)]


def count_code_blocks(text: str) -> int:
    """Count fenced code blocks (``` ... ```) in markdown text.

    This uses the same extraction rules as :func:`extract_code_blocks`.

    Args:
        text: The markdown string to inspect.

    Returns:
        The number of fenced code blocks found.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> count_code_blocks("no code")
        0
        >>> count_code_blocks("```\\na\\n```")
        1
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return len(extract_code_blocks(text))


def has_code_blocks(text: str) -> bool:
    """Return True if *text* contains at least one fenced code block.

    This is a boolean companion to :func:`count_code_blocks`; it returns
    ``True`` when *text* contains one or more fenced code blocks and ``False``
    otherwise.

    Args:
        text: The markdown string to inspect.

    Returns:
        ``True`` if *text* contains at least one fenced code block, ``False``
        otherwise.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> has_code_blocks("```\\na\\n```")
        True
        >>> has_code_blocks("plain text")
        False
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return count_code_blocks(text) > 0


def strip_markdown(text: str) -> str:
    """Strip common markdown formatting from text."""
    # Remove fenced code blocks entirely, keeping inner content
    text = re.sub(r"```[a-zA-Z0-9_+-]*\n", "", text)
    text = text.replace("```", "")
    # Remove inline code backticks
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove emphasis markers
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    # Remove heading markers
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    # Remove link markup, keep label
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    # Remove blockquote markers
    text = re.sub(r"^>\s?", "", text, flags=re.MULTILINE)
    return text


def count_words(text: str) -> int:
    """Count whitespace-delimited words in text."""
    return len(text.split())


def has_words(text: str) -> bool:
    """Return True if *text* contains at least one whitespace-delimited word.

    This is a boolean companion to :func:`count_words`; it returns ``True``
    when *text* contains one or more whitespace-delimited words and ``False``
    otherwise (including empty or whitespace-only text).

    Args:
        text: The string to inspect.

    Returns:
        ``True`` if *text* contains at least one word, ``False`` otherwise.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> has_words("Hello world")
        True
        >>> has_words("")
        False
        >>> has_words("   ")
        False
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return count_words(text) > 0


def count_headings(text: str) -> int:
    """Count Markdown headings in *text*.

    A heading is a line that starts with one to six ``#`` characters
    followed by whitespace and non-whitespace content, matching the same
    rule used by :func:`is_heading`.

    Args:
        text: The markdown string to inspect.

    Returns:
        The number of heading lines found.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> count_headings("# Title")
        1
        >>> count_headings("no headings here")
        0
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return sum(1 for line in text.splitlines() if is_heading(line))


def has_headings(text: str) -> bool:
    """Return True if *text* contains at least one Markdown heading.

    This is a boolean companion to :func:`count_headings`; it returns
    ``True`` when *text* contains one or more heading lines and ``False``
    otherwise.

    Args:
        text: The markdown string to inspect.

    Returns:
        ``True`` if *text* contains at least one heading, ``False`` otherwise.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> has_headings("# Title")
        True
        >>> has_headings("plain text")
        False
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return count_headings(text) > 0


def is_heading(line: str) -> bool:
    """Return True if line is a markdown heading."""
    return bool(re.match(r"^#{1,6}\s+\S", line))


def heading_level(line: str) -> int:
    """Return heading level (1-6) or 0 if not a heading."""
    match = re.match(r"^(#{1,6})\s+\S", line)
    if not match:
        return 0
    return len(match.group(1))
