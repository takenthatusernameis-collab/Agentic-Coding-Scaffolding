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
    "extract_placeholders",
    "has_placeholders",
    "wrap_prompt",
    "estimate_token_count",
    "count_words",
    "collapse_blank_lines",
    "count_placeholders",
    "count_sentences",
    "truncate_words",
    "truncate_lines",
    "indent_lines",
    "dedent_lines",
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


def extract_placeholders(template: str) -> List[str]:
    """Extract placeholder names from a prompt template.

    Scans *template* for ``{name}`` placeholders (as used by
    :func:`format_prompt_template`) and returns the placeholder names in the
    order they first appear, without duplicates.

    Args:
        template: The template string to scan for placeholders.

    Returns:
        A list of placeholder name strings, in order of first appearance.

    Raises:
        TypeError: If *template* is not a string.

    Examples:
        >>> extract_placeholders("Hello {name}, welcome to {place}!")
        ['name', 'place']
        >>> extract_placeholders("{a} {b} {a}")
        ['a', 'b']
        >>> extract_placeholders("No placeholders here")
        []
    """
    _require_string(template, "template")
    placeholders = re.findall(r"\{(\w+)\}", template)
    seen = set()
    result: List[str] = []
    for name in placeholders:
        if name not in seen:
            seen.add(name)
            result.append(name)
    return result


def has_placeholders(template: str) -> bool:
    """Return True if *template* contains any ``{name}`` placeholders.

    A lightweight boolean companion to :func:`extract_placeholders` and
    :func:`count_placeholders` that reports whether a template string
    contains at least one placeholder.

    Args:
        template: The template string to scan for placeholders.

    Returns:
        ``True`` if *template* contains at least one placeholder, ``False``
        otherwise.

    Raises:
        TypeError: If *template* is not a string.

    Examples:
        >>> has_placeholders("Hello {name}!")
        True
        >>> has_placeholders("No placeholders here")
        False
        >>> has_placeholders("")
        False
    """
    _require_string(template, "template")
    return bool(re.findall(r"\{\w+\}", template))


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


def collapse_blank_lines(text: str) -> str:
    """Collapse runs of three or more newlines into a single blank line.

    Args:
        text: The text to normalize.

    Returns:
        Text with consecutive blank lines collapsed to at most one.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> collapse_blank_lines("a\\n\\n\\nb")
        'a\\n\\nb'
        >>> collapse_blank_lines("a\\nb")
        'a\\nb'
    """
    _require_string(text, "text")
    return re.sub(r"\n{3,}", "\n\n", text)


def count_placeholders(template: str) -> int:
    """Count the number of placeholders in *template*.

    Counts every ``{name}`` placeholder occurrence, including duplicates.

    Args:
        template: The template string to scan.

    Returns:
        The number of placeholder occurrences.

    Raises:
        TypeError: If *template* is not a string.

    Examples:
        >>> count_placeholders("Hello {name}, {greeting}!")
        2
        >>> count_placeholders("No placeholders")
        0
    """
    _require_string(template, "template")
    return len(re.findall(r"\{\w+\}", template))


def count_sentences(text: str) -> int:
    """Count the number of sentences in *text*.

    A sentence is delimited by a terminating punctuation mark (``.``,
    ``!`` or ``?``) followed by whitespace or end of string.

    Args:
        text: The text to count sentences in.

    Returns:
        The number of sentences.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> count_sentences("Hello world. How are you?")
        2
        >>> count_sentences("")
        0
    """
    _require_string(text, "text")
    if not text.strip():
        return 0
    return len(re.findall(r"[.!?](?:\s|$)", text))


def truncate_words(text: str, max_words: int, suffix: str = "...") -> str:
    """Truncate *text* to at most *max_words* whitespace-delimited words.

    Args:
        text: The text to truncate.
        max_words: The maximum number of words to keep.
        suffix: The suffix to append when truncated.

    Returns:
        The truncated text.

    Raises:
        TypeError: If *text* or *suffix* is not a string or *max_words* is
            not an int.
        ValueError: If *max_words* is negative.

    Examples:
        >>> truncate_words("one two three four", 2)
        'one two...'
        >>> truncate_words("short text", 5)
        'short text'
    """
    _require_string(text, "text")
    _require_int(max_words, "max_words")
    if max_words < 0:
        raise ValueError("max_words must be non-negative")
    _require_string(suffix, "suffix")
    words = text.split()
    if len(words) <= max_words:
        return text
    if max_words == 0:
        return suffix if suffix else ""
    return " ".join(words[:max_words]) + suffix


def truncate_lines(text: str, max_lines: int, suffix: str = "...") -> str:
    """Truncate *text* to at most *max_lines* lines.

    Splits *text* on newline characters, keeps the first *max_lines* lines,
    and appends *suffix* when lines are removed. Returns *text* unchanged
    when it already has at most *max_lines* lines.

    Args:
        text: The text to truncate.
        max_lines: The maximum number of lines to keep.
        suffix: The suffix to append when truncated.

    Returns:
        The truncated text.

    Raises:
        TypeError: If *text* or *suffix* is not a string or *max_lines* is
            not an int.
        ValueError: If *max_lines* is negative.

    Examples:
        >>> truncate_lines("a\\nb\\nc\\nd", 2)
        'a\\nb...'
        >>> truncate_lines("a\\nb", 5)
        'a\\nb'
    """
    _require_string(text, "text")
    _require_int(max_lines, "max_lines")
    if max_lines < 0:
        raise ValueError("max_lines must be non-negative")
    _require_string(suffix, "suffix")
    lines = text.split("\n")
    if len(lines) <= max_lines:
        return text
    if max_lines == 0:
        return suffix if suffix else ""
    return "\n".join(lines[:max_lines]) + suffix


def indent_lines(text: str, prefix: str = "    ", *, skip_blank: bool = False) -> str:
    """Prefix every line of *text* with *prefix*.

    A companion to :func:`truncate_lines` and :func:`wrap_prompt` that adds a
    leading prefix to each line. Blank lines are left untouched when
    *skip_blank* is True (the default), which is useful for indenting code
    blocks without turning empty lines into lines of whitespace.

    Args:
        text: The text to indent.
        prefix: The string to prepend to each non-blank line.
        skip_blank: If True, leave blank lines without the prefix.

    Returns:
        The indented text.

    Raises:
        TypeError: If *text* or *prefix* is not a string, or *skip_blank* is
            not a bool.

    Examples:
        >>> indent_lines("a\\nb\\nc")
        '    a\\n    b\\n    c'
        >>> indent_lines("a\\n\\nb", skip_blank=True)
        '    a\\n\\n    b'
    """
    _require_string(text, "text")
    _require_string(prefix, "prefix")
    if not isinstance(skip_blank, bool):
        raise TypeError(f"skip_blank must be a bool, got {type(skip_blank).__name__}")
    if not text:
        return text
    lines = text.split("\n")
    result: List[str] = []
    for line in lines:
        if skip_blank and line.strip() == "":
            result.append(line)
        else:
            result.append(prefix + line)
    return "\n".join(result)

def dedent_lines(text: str) -> str:
    """Remove common leading whitespace from every line in *text*.

    This is similar to Python's ``textwrap.dedent`` but implemented as a
    simple helper for prompt strings. It finds the minimum indentation
    (spaces/tabs) among non-blank lines and removes that much whitespace
    from the start of every line.

    Args:
        text: The text to dedent.

    Returns:
        The dedented text.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> dedent_lines("    hello\\n      world")
        'hello\\n  world'
        >>> dedent_lines("\\n    hello\\n\\n    world\\n")
        '\\nhello\\n\\nworld\\n'
    """
    _require_string(text, "text")
    if not text:
        return text
    lines = text.split("\n")
    # Find minimum indentation for non-blank lines
    min_indent = None
    for line in lines:
        if line.strip() == "":
            continue
        # Count leading whitespace
        indent = 0
        for ch in line:
            if ch == " ":
                indent += 1
            elif ch == "\t":
                indent += 4  # treat tabs as 4 spaces
            else:
                break
        if min_indent is None or indent < min_indent:
            min_indent = indent
    if min_indent is None or min_indent == 0:
        return text
    result: List[str] = []
    for line in lines:
        if line.strip() == "":
            result.append(line)
            continue
        # Remove min_indent worth of whitespace
        new_line = line
        # Remove from start
        chars = list(new_line)
        j = 0
        removed_count = 0
        while j < len(chars) and removed_count < min_indent:
            if chars[j] == " ":
                removed_count += 1
                j += 1
            elif chars[j] == "\t":
                removed_count += 4
                j += 1
                # If we went over due to tab, that's fine as approximation
            else:
                break
        result.append("".join(chars[j:]))
    return "\n".join(result)
