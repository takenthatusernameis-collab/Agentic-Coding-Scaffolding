"""Prompt utility functions for working with text prompts.

Provides helpers for truncating, formatting, cleaning, extracting keywords
from, wrapping, and estimating tokens for text prompts. All functions
validate their inputs and raise :class:`TypeError` or :class:`ValueError`
on invalid arguments.
"""

from __future__ import annotations

import re
from typing import Any, List

__all__: List[str] = [
    "truncate_prompt",
    "format_prompt_template",
    "clean_prompt",
    "extract_keywords",
    "wrap_prompt",
    "estimate_token_count",
    "count_words",
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


def truncate_prompt(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a prompt to a maximum length.

    Args:
        text: The text to truncate.
        max_length: The maximum length in characters.
        suffix: The suffix to append when truncated.

    Returns:
        The truncated text.

    Raises:
        TypeError: If *text*, *max_length*, or *suffix* are not the expected
            types.
        ValueError: If *max_length* is negative.

    Examples:
        >>> truncate_prompt("Hello world", 5)
        'He...'
        >>> truncate_prompt("Short", 10)
        'Short'
    """
    _require_string(text, "text")
    _require_int(max_length, "max_length")
    if max_length < 0:
        raise ValueError("max_length must be non-negative")
    _require_string(suffix, "suffix")
    if len(text) <= max_length:
        return text
    if max_length <= len(suffix):
        return text[:max_length]
    return text[: max_length - len(suffix)] + suffix


def format_prompt_template(template: str, **kwargs: Any) -> str:
    """Format a prompt template with keyword arguments.

    Args:
        template: The template string with {key} placeholders.
        **kwargs: The values to substitute.

    Returns:
        The formatted string.

    Raises:
        TypeError: If *template* is not a string.
        ValueError: If the template references a missing keyword.

    Examples:
        >>> format_prompt_template(
        ...     "Hello {name}, welcome to {place}!",
        ...     name="Alice",
        ...     place="Wonderland",
        ... )
        'Hello Alice, welcome to Wonderland!'
    """
    _require_string(template, "template")
    try:
        return template.format(**kwargs)
    except KeyError as exc:
        raise ValueError(f"template references missing keyword: {exc}") from exc


def clean_prompt(text: str) -> str:
    """Clean up whitespace in a prompt.

    Args:
        text: The text to clean.

    Returns:
        Cleaned text with normalized whitespace.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> clean_prompt("Hello   world")
        'Hello world'
    """
    _require_string(text, "text")
    # Replace multiple whitespace characters with single space
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()


def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text (simple word extraction).

    Args:
        text: The text to extract keywords from.
        min_length: Minimum length of keywords to extract.

    Returns:
        A list of keywords.

    Raises:
        TypeError: If *text* is not a string or *min_length* is not an int.
        ValueError: If *min_length* is negative.

    Examples:
        >>> extract_keywords("The quick brown fox jumps")
        ['quick', 'brown', 'fox', 'jumps']
    """
    _require_string(text, "text")
    _require_int(min_length, "min_length")
    if min_length < 0:
        raise ValueError("min_length must be non-negative")
    # Extract words (alphanumeric sequences)
    words = re.findall(r"\b\w+\b", text.lower())
    # Filter by minimum length and remove common stop words
    stop_words = {
        "the",
        "and",
        "is",
        "in",
        "to",
        "of",
        "a",
        "for",
        "on",
        "with",
        "as",
        "by",
        "an",
        "at",
        "are",
        "be",
        "this",
        "that",
        "these",
        "those",
    }
    keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
    # Remove duplicates while preserving order
    seen = set()
    result: List[str] = []
    for k in keywords:
        if k not in seen:
            seen.add(k)
            result.append(k)
    return result


def wrap_prompt(text: str, width: int = 80) -> str:
    """Wrap prompt text to a specific width.

    Args:
        text: The text to wrap.
        width: The maximum line width.

    Returns:
        Wrapped text.

    Raises:
        TypeError: If *text* is not a string or *width* is not an int.
        ValueError: If *width* is negative.

Examples:
        >>> wrap_prompt("This is a long line that should be wrapped", 24)
        'This is a long line that\nshould be wrapped'
    """
    _require_string(text, "text")
    _require_int(width, "width")
    if width < 0:
        raise ValueError("width must be non-negative")
    if width == 0:
        return text
    words = text.split()
    lines: List[str] = []
    current_line: List[str] = []

    for word in words:
        if len(" ".join(current_line + [word])) <= width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    if current_line:
        lines.append(" ".join(current_line))
    return "\n".join(lines)


def estimate_token_count(text: str) -> int:
    """Estimate token count for a text (rough approximation).

    Uses a simple heuristic: ~4 characters per token on average for English text.

    Args:
        text: The text to estimate tokens for.

    Returns:
        Estimated token count.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> estimate_token_count("Hello world")
        2
        >>> estimate_token_count("This is a test")
        3
    """
    _require_string(text, "text")
    if not text:
        return 0
    # Rough approximation: 4 chars per token
    return max(1, len(text) // 4)


def count_words(text: str) -> int:
    """Count the number of whitespace-delimited words in *text*.

    Args:
        text: The text to count words in.

    Returns:
        The number of words.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> count_words("Hello world")
        2
        >>> count_words("")
        0
    """
    _require_string(text, "text")
    return len(text.split())
