"""Case conversion utilities."""

from __future__ import annotations

import re
from typing import Callable, List

__all__: List[str] = [
    "kebab_case",
    "pascal_case",
    "constant_case",
    "snake_case",
    "camel_case",
    "screaming_snake_case",
    "spinal_case",
    "train_case",
    "dot_case",
    "slash_case",
    "title_case",
    "sentence_case",
    "convert_case",
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
        The camelCase form of *text*.

    Raises:
        TypeError: If *text* is not a string.

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


# Common aliases
screaming_snake_case = constant_case
spinal_case = kebab_case
train_case = pascal_case


def dot_case(text: str) -> str:
    """Convert *text* to dot.case (lowercase words joined by dots).

    Args:
        text: The string to convert.

    Returns:
        The dot.case form of *text*.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> dot_case("Hello World")
        'hello.world'
        >>> dot_case("xmlParser")
        'xml.parser'
    """
    return ".".join(word.lower() for word in _split_words(text))


def slash_case(text: str) -> str:
    """Convert *text* to slash/case (lowercase words joined by slashes).

    Args:
        text: The string to convert.

    Returns:
        The slash/case form of *text*.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> slash_case("Hello World")
        'hello/world'
        >>> slash_case("xmlParser")
        'xml/parser'
    """
    return "/".join(word.lower() for word in _split_words(text))


def title_case(text: str) -> str:
    """Convert *text* to Title Case (spaces between capitalized words).

    Args:
        text: The string to convert.

    Returns:
        The Title Case form of *text*.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> title_case("hello world")
        'Hello World'
        >>> title_case("xml_parser")
        'Xml Parser'
    """
    return " ".join(word.capitalize() for word in _split_words(text))


def sentence_case(text: str) -> str:
    """Convert *text* to Sentence case (first word capitalized, rest lowercase)."""
    _require_string(text, "text")
    words = _split_words(text)
    if not words:
        return ""
    return " ".join([words[0].capitalize()] + [word.lower() for word in words[1:]])


_CASE_DISPATCH: dict[str, Callable[[str], str]] = {
    "kebab": kebab_case,
    "kebab_case": kebab_case,
    "pascal": pascal_case,
    "pascal_case": pascal_case,
    "constant": constant_case,
    "constant_case": constant_case,
    "snake": snake_case,
    "snake_case": snake_case,
    "camel": camel_case,
    "camel_case": camel_case,
    "screaming_snake": screaming_snake_case,
    "screaming_snake_case": screaming_snake_case,
    "spinal": spinal_case,
    "spinal_case": spinal_case,
    "train": train_case,
    "train_case": train_case,
    "dot": dot_case,
    "dot_case": dot_case,
    "slash": slash_case,
    "slash_case": slash_case,
    "title": title_case,
    "title_case": title_case,
    "sentence": sentence_case,
    "sentence_case": sentence_case,
}


def convert_case(text: str, case: str) -> str:
    """Convert *text* to the named *case* style.

    Args:
        text: The string to convert.
        case: The target case style, e.g. ``"snake"``, ``"camel"``,
            ``"pascal"``, ``"kebab"``, ``"constant"``, ``"title"``,
            ``"sentence"``, ``"dot"``, ``"slash"``, ``"spinal"``,
            ``"train"``, or ``"screaming_snake"``. The optional
            ``"_case"`` suffix is allowed and matching is case-insensitive;
            hyphens are treated as underscores.

    Returns:
        The converted string.

    Raises:
        TypeError: If *text* or *case* is not a string.
        ValueError: If *case* is not a recognized case style.

    Examples:
        >>> convert_case("Hello World", "snake")
        'hello_world'
        >>> convert_case("hello_world", "Pascal")
        'HelloWorld'
        >>> convert_case("XML Parser", "kebab-case")
        'xml-parser'
    """
    _require_string(text, "text")
    if not isinstance(case, str):
        raise TypeError("case must be a string")
    key = case.strip().lower().replace("-", "_")
    converter = _CASE_DISPATCH.get(key)
    if converter is None:
        raise ValueError(f"unknown case style: {case!r}")
    return converter(text)
