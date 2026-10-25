"""Case conversion utilities."""

from __future__ import annotations

import re
from typing import List

__all__: List[str] = [
    "kebab_case",
    "pascal_case",
    "constant_case",
    "snake_case",
    "camel_case",
]


def _require_string(value: str, name: str) -> str:
    """Validate that *value* is a string, raising ``TypeError`` otherwise.

    Args:
        value: The value to validate.
        name: The argument name used in error messages.

    Returns:
        The validated string.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _split_words(text: str) -> List[str]:
    """Split *text* into a list of lowercased words.

    Words are delimited by whitespace, separators (hyphens, underscores, dots,
    slashes), and case transitions such as camelCase and PascalCase boundaries.

    Args:
        text: The string to split.

    Returns:
        A list of lowercased words.

    Raises:
        TypeError: If *text* is not a string.
    """
    _require_string(text, "text")
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    spaced = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", spaced)
    spaced = re.sub(r"[^A-Za-z0-9]+", " ", spaced)
    return [word.lower() for word in spaced.split() if word]


def kebab_case(text: str) -> str:
    """Convert *text* to kebab-case (lowercase words joined by hyphens).

    Args:
        text: The string to convert.

    Returns:
        The kebab-case form of *text*.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> kebab_case("Hello World")
        'hello-world'
        >>> kebab_case("xmlParser")
        'xml-parser'
        >>> kebab_case("already-kebab")
        'already-kebab'
    """
    return "-".join(_split_words(text))


def pascal_case(text: str) -> str:
    """Convert *text* to PascalCase (capitalized words joined without separators).

    Args:
        text: The string to convert.

    Returns:
        The PascalCase form of *text*.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> pascal_case("hello world")
        'HelloWorld'
        >>> pascal_case("xml_parser")
        'XmlParser'
        >>> pascal_case("alreadyPascal")
        'AlreadyPascal'
    """
    return "".join(word.capitalize() for word in _split_words(text))


def constant_case(text: str) -> str:
    """Convert *text* to CONSTANT_CASE (uppercase words joined by underscores).

    Args:
        text: The string to convert.

    Returns:
        The CONSTANT_CASE form of *text*.

    Raises:
        TypeError: If *text_ is not a string.

    Examples:
        >>> constant_case("hello world")
        'HELLO_WORLD'
        >>> constant_case("xmlParser")
        'XML_PARSER'
        >>> constant_case("MAX_SIZE")
        'MAX_SIZE'
    """
    return "_".join(word.upper() for word in _split_words(text))


def snake_case(text: str) -> str:
    """Convert *text* to snake_case (lowercase words joined by underscores).

    Args:
        text: The string to convert.

    Returns:
        The snake_case form of *text*.

    Raises:
        TypeError: If *text_ is not a string.

    Examples:
        >>> snake_case("Hello World")
        'hello_world'
        >>> snake_case("xmlParser")
        'xml_parser'
        >>> snake_case("already_snake")
        'already_snake'
    """
    return "_".join(word.lower() for word in _split_words(text))


def camel_case(text: str) -> str:
    """Convert *text* to camelCase (first word lowercase, rest capitalized).

    Args:
        text: The string to convert.

    Returns:
        The camelCase form of *text_.

    Raises:
        TypeError: If *text_ is not a string.

    Examples:
        >>> camel_case("hello world")
        'helloWorld'
        >>> camel_case("xml_parser")
        'xmlParser'
        >>> camel_case("alreadyCamel")
        'alreadyCamel'
    """
    words = _split_words(text)
    if not words:
        return ""
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])
