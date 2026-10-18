"""Advanced string manipulation utilities."""

import re
import textwrap
from typing import List, Optional

__all__: List[str] = [
    "slugify",
    "camel_to_snake",
    "snake_to_camel",
    "pluralize",
    "truncate",
    "wrap_text",
    "indent_text",
    "remove_extra_whitespace",
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
