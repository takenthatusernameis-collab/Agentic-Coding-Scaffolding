"""Advanced string manipulation utilities."""

import re
import textwrap
from typing import List, Optional

__all__: List[str] = [
    "slugify",
    "camel_to_snake",
    "snake_to_camel",
    "is_isogram",
    "pluralize",
    "truncate",
    "wrap_text",
    "indent_text",
    "remove_extra_whitespace",
    "remove_blank_lines",
    "truncate_words",
    "wrap_words",
    "title_case",
]

_SMALL_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "but",
    "by",
    "en",
    "for",
    "if",
    "in",
    "nor",
    "of",
    "on",
    "or",
    "per",
    "the",
    "to",
    "via",
    "vs",
}


def _require_string(value: str, name: str) -> str:
    """Validate that ``value`` is a string, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The argument name used in error messages.

    Returns:
        The validated string.

    Raises:
        TypeError: If ``value`` is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def slugify(text: str) -> str:
    """Convert a string to a URL-friendly slug.

    Lowercases the text, replaces whitespace and underscores with hyphens,
    removes non-alphanumeric characters (except hyphens), and collapses
    consecutive hyphens.

    Args:
        text: The string to slugify.

    Returns:
        A URL-friendly slug.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> slugify("Hello World")
        'hello-world'
        >>> slugify("  Python   is   Great!  ")
        'python-is-great'
        >>> slugify("already-a-slug")
        'already-a-slug'
    """
    _require_string(text, "text")
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def camel_to_snake(text: str) -> str:
    """Convert a camelCase or PascalCase string to snake_case.

    Args:
        text: The camelCase or PascalCase string to convert.

    Returns:
        The snake_case equivalent.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> camel_to_snake("helloWorld")
        'hello_world'
        >>> camel_to_snake("XMLParser")
        'xml_parser'
        >>> camel_to_snake("already_snake")
        'already_snake'
    """
    _require_string(text, "text")
    snake = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    snake = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", snake)
    snake = snake.replace("-", "_").lower()
    return snake


def snake_to_camel(text: str) -> str:
    """Convert a snake_case string to camelCase.

    Args:
        text: The snake_case string to convert.

    Returns:
        The camelCase equivalent.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> snake_to_camel("hello_world")
        'helloWorld'
        >>> snake_to_camel("xml_parser")
        'xmlParser'
        >>> snake_to_camel("alreadyCamel")
        'alreadyCamel'
    """
    _require_string(text, "text")
    if "_" not in text:
        return text
    parts = text.split("_")
    camel = parts[0].lower()
    for part in parts[1:]:
        camel += part[:1].upper() + part[1:].lower() if part else ""
    return camel


def pluralize(word: str, count: Optional[int] = None) -> str:
    """Return the plural form of an English word.

    Applies simple inflection rules: words ending in ``s``, ``x``, ``z``,
    ``ch``, or ``sh`` take ``-es``; words ending in a consonant plus ``y``
    take ``-ies``; all others take ``-s``. When ``count`` is ``1`` (or not
    given), the singular form is returned.

    Args:
        word: The singular word to pluralize.
        count: Optional count. When ``1``, returns the singular form.

    Returns:
        The plural (or singular when count is 1) form of the word.

    Raises:
        TypeError: If ``word`` is not a string.

    Examples:
        >>> pluralize("cat")
        'cats'
        >>> pluralize("cat", 2)
        'cats'
        >>> pluralize("cat", 1)
        'cat'
        >>> pluralize("bus")
        'buses'
        >>> pluralize("baby")
        'babies'
    """
    _require_string(word, "word")
    if count == 1:
        return word
    if re.search(r"[sxz]$", word) or re.search(r"[chsh]$", word):
        return word + "es"
    if re.search(r"[^aeiou]y$", word):
        return word[:-1] + "ies"
    return word + "s"


def truncate(text: str, length: int, suffix: str = "...") -> str:
    """Truncate a string to the given length, appending a suffix.

    If the string is shorter than or equal to ``length``, it is returned
    unchanged. The suffix is included within the length limit.

    Args:
        text: The string to truncate.
        length: Maximum length of the result including the suffix.
        suffix: Suffix appended when truncation occurs (default: "...").

    Returns:
        The truncated string.

    Raises:
        TypeError: If ``text`` or ``suffix`` is not a string.
        ValueError: If ``length`` is negative.

    Examples:
        >>> truncate("Hello, world!", 5)
        'He...'
        >>> truncate("Hi", 10)
        'Hi'
        >>> truncate("Hello, world!", 8, suffix="")
        'Hello, w'
    """
    _require_string(text, "text")
    _require_string(suffix, "suffix")
    if length < 0:
        raise ValueError("length must be non-negative")
    if len(text) <= length:
        return text
    if length < len(suffix):
        return suffix[:length]
    return text[: length - len(suffix)] + suffix


def wrap_text(text: str, width: int = 70) -> str:
    """Wrap a string to the specified line width.

    Args:
        text: The string to wrap.
        width: Maximum line width (default: 70).

    Returns:
        The wrapped string with newlines inserted.

    Raises:
        TypeError: If ``text`` is not a string.
        ValueError: If ``width`` is not positive.

    Examples:
        >>> wrap_text("hello world", 5)
        'hello\\nworld'
    """
    _require_string(text, "text")
    if width <= 0:
        raise ValueError("width must be positive")
    return textwrap.fill(text, width=width)


def wrap_words(
    text: str, width: int = 70, break_long_words: bool = True
) -> str:
    """Wrap *text* into lines of at most *width* characters.

    Words are split on whitespace and greedily packed into lines. A word
    that does not fit on the current line starts a new line. When
    *break_long_words* is True, words longer than *width* are broken into
    chunks of at most *width* characters.

    Args:
        text: The string to wrap.
        width: Maximum line width (default: 70).
        break_long_words: Whether to break words longer than *width*.

    Returns:
        The wrapped string with newlines inserted.

    Raises:
        TypeError: If ``text`` is not a string, ``width`` is not an int,
            or ``break_long_words`` is not a bool.
        ValueError: If ``width`` is not positive.

    Examples:
        >>> wrap_words("hello world", 5)
        'hello\\nworld'
        >>> wrap_words("abcdefghij", 4, False)
        'abcdefghij'
    """
    _require_string(text, "text")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an integer")
    if width <= 0:
        raise ValueError("width must be positive")
    if not isinstance(break_long_words, bool):
        raise TypeError("break_long_words must be a bool")

    tokens = []
    for word in text.split():
        if break_long_words and len(word) > width:
            for i in range(0, len(word), width):
                tokens.append(word[i : i + width])
        else:
            tokens.append(word)

    lines: List[str] = []
    current = ""
    for token in tokens:
        if not current:
            current = token
        elif len(current) + 1 + len(token) <= width:
            current += " " + token
        else:
            lines.append(current)
            current = token
    if current:
        lines.append(current)
    return "\n".join(lines)


def indent_text(text: str, prefix: str = "    ") -> str:
    """Indent every line of a string with the given prefix.

    Args:
        text: The string to indent.
        prefix: The prefix to prepend to each line (default: four spaces).

    Returns:
        The indented string.

    Raises:
        TypeError: If ``text`` or ``prefix`` is not a string.

    Examples:
        >>> indent_text("line1\\nline2", "  ")
        '  line1\\n  line2'
    """
    _require_string(text, "text")
    _require_string(prefix, "prefix")
    lines = text.split("\n")
    return "\n".join(prefix + line for line in lines)


def remove_extra_whitespace(text: str) -> str:
    """Collapse runs of whitespace into single spaces and strip edges.

    Args:
        text: The string to clean.

    Returns:
        The string with normalized whitespace.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> remove_extra_whitespace("  hello   world  ")
        'hello world'
        >>> remove_extra_whitespace("a\\n\\tb")
        'a b'
    """
    _require_string(text, "text")
    return " ".join(text.split())


def remove_blank_lines(text: str) -> str:
    """Remove blank (whitespace-only) lines from *text*.

    Args:
        text: The text to filter.

    Returns:
        *text* with every blank line removed, preserving order of the
        remaining lines and the original newline structure otherwise.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> remove_blank_lines("a\\n\\nb\\n\\n\\nc")
        'a\\nb\\nc'
        >>> remove_blank_lines("")
        ''
    """
    _require_string(text, "text")
    if not text:
        return text
    lines = text.split("\n")
    result = [line for line in lines if line.strip() != ""]
    return "\n".join(result)


def truncate_words(text: str, max_words: int, suffix: str = "...") -> str:
    """Truncate a string to at most *max_words* words, appending *suffix*.

    Words are runs of non-whitespace characters separated by whitespace.
    If the number of words is less than or equal to *max_words*, *text* is
    returned unchanged. When truncation occurs, *suffix* is appended after
    a single space following the last kept word.

    Args:
        text: The string to truncate.
        max_words: Maximum number of words to keep.
        suffix: Suffix appended when truncation occurs (default: "...").

    Returns:
        The truncated string.

    Raises:
        TypeError: If *text* or *suffix* is not a string.
        ValueError: If *max_words* is negative.

    Examples:
        >>> truncate_words("the quick brown fox", 2)
        'the quick...'
        >>> truncate_words("hi", 5)
        'hi'
        >>> truncate_words("hi", 2)
        'hi'
    """
    _require_string(text, "text")
    _require_string(suffix, "suffix")
    if not isinstance(max_words, int) or isinstance(max_words, bool):
        raise TypeError("max_words must be an integer")
    if max_words < 0:
        raise ValueError("max_words must be non-negative")
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + suffix


def title_case(text: str, small_words: Optional[List[str]] = None) -> str:
    """Convert a string to title case.

    Major words are capitalized; small words (articles, conjunctions,
    prepositions) are lowercased unless they are the first or last word.

    Args:
        text: The string to convert.
        small_words: Optional list of words to keep lowercase. Defaults to a
            standard set of English small words.

    Returns:
        The title-cased string.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> title_case("hello world")
        'Hello World'
        >>> title_case("the quick brown fox")
        'The Quick Brown Fox'
        >>> title_case("war and peace")
        'War and Peace'
    """
    _require_string(text, "text")
    if small_words is None:
        small = _SMALL_WORDS
    else:
        small = {w.lower() for w in small_words}
    words = text.split()
    if not words:
        return text
    result: List[str] = []
    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word.lower() not in small:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return " ".join(result)


def is_isogram(text: str) -> bool:
    """Return True if *text* is an isogram (no repeating letters).

    An isogram is a word or phrase in which no letter appears more than
    once. The check is case-insensitive and ignores non-letter characters.

    Args:
        text: The string to check.

    Returns:
        True if *text* is an isogram, False otherwise. The empty string
        is considered an isogram.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> is_isogram("abc")
        True
        >>> is_isogram("hello")
        False
        >>> is_isogram("")
        True
        >>> is_isogram("Emily Jung Schwartzkopf")
        True
    """
    _require_string(text, "text")
    seen: set[str] = set()
    for ch in text.lower():
        if ch.isalpha():
            if ch in seen:
                return False
            seen.add(ch)
    return True
