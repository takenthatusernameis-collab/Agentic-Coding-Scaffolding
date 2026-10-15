"""Prompt utility functions for working with text prompts."""

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
]


def truncate_prompt(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a prompt to a maximum length.

    Args:
        text: The text to truncate.
        max_length: The maximum length in characters.
        suffix: The suffix to append when truncated.

    Returns:
        The truncated text.

    Examples:
        >>> truncate_prompt("Hello world", 5)
        'Hell...'
        >>> truncate_prompt("Short", 10)
        'Short'
    """
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

    Examples:
        >>> format_prompt_template(
        ...     "Hello {name}, welcome to {place}!",
        ...     name="Alice",
        ...     place="Wonderland",
        ... )
        'Hello Alice, welcome to Wonderland!'
    """
    return template.format(**kwargs)


def clean_prompt(text: str) -> str:
    """Clean up whitespace in a prompt.

    Args:
        text: The text to clean.

    Returns:
        Cleaned text with normalized whitespace.

    Examples:
        >>> clean_prompt("Hello   world\n\nHow are you?")
        'Hello world How are you?'
    """
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

    Examples:
        >>> extract_keywords("The quick brown fox jumps")
        ['quick', 'brown', 'jumps']
    """
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

    Examples:
        >>> wrap_prompt("This is a long line that should be wrapped", 20)
        'This is a long line\\nthat should be wrapped'
    """
    if width <= 0:
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

    Examples:
        >>> estimate_token_count("Hello world")
        2
        >>> estimate_token_count("This is a test")
        4
    """
    if not text:
        return 0
    # Rough approximation: 4 chars per token
    return max(1, len(text) // 4)
