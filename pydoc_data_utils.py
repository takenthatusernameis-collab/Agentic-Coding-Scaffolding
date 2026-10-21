"""Documentation topic utilities wrapping the standard library :mod:`pydoc_data` package.

The :mod:`pydoc_data` package holds the topics of the Python Language
Reference: the text of every topic of the language, keyed by the name of the
topic.  The :mod:`pydoc` module reads that data when it answers a question of
the interactive help.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It never hands out the mapping of the standard library
itself, so a caller cannot change the documentation of the interpreter, and it
adds the helpers the standard library leaves to the caller: the names of the
topics, the title of a topic, the sections of a topic, the text of a single
section, a search over the topics, and a text that is wrapped for a terminal.

The module is pure computation, so it works on every platform and never
touches the network, the file system, or a process.
"""

from __future__ import annotations

import textwrap
from typing import Dict, List, Sequence

try:
    from pydoc_data import topics as _topics
except ImportError:  # pragma: no cover - the package ships with the interpreter
    _topics = None  # type: ignore[assignment]

__all__: list[str] = [
    "count_topics",
    "get_topic",
    "get_topic_names",
    "get_topic_section",
    "get_topic_sections",
    "get_topic_title",
    "get_topics",
    "get_topics_subset",
    "has_topic",
    "search_topics",
    "wrap_topic",
]

#: The characters a heading of a topic is underlined with.
_HEADING_MARKS = "=-~"

#: The characters the title of a topic is underlined with.
_TITLE_MARKS = "*"


def _require_str(value: object, name: str) -> str:
    """Return *value* when it is a string, and raise :class:`TypeError` otherwise."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_non_empty_str(value: object, name: str) -> str:
    """Return *value* when it is a string that is not empty."""
    text = _require_str(value, name)
    if not text:
        raise ValueError(f"{name} must not be empty")
    return text


def _require_positive_int(value: object, name: str) -> int:
    """Return *value* when it is a positive integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def _require_sequence(value: object, name: str) -> Sequence[str]:
    """Return *value* when it is a sequence of strings."""
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{name} must be a sequence of strings, not a single string")
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list or a tuple, got {type(value).__name__}")
    for entry in value:
        if not isinstance(entry, str):
            raise TypeError(f"{name} entries must be strings, got {type(entry).__name__}")
    return value


def _standard_topics() -> Dict[str, str]:
    """Return the topics of the standard library.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pydoc_data``
            package.
    """
    if _topics is None:
        raise RuntimeError("the standard library module 'pydoc_data' is not available")
    return _topics.topics


def _heading_positions(lines: Sequence[str]) -> List[int]:
    """Return the indexes of the lines that carry a heading.

    A heading is a line that is underlined with the characters of
    :data:`_HEADING_MARKS`.  The title of a topic is underlined with the
    characters of :data:`_TITLE_MARKS`, so it is not a heading.
    """
    positions: List[int] = []
    for index in range(len(lines) - 1):
        title = lines[index].strip()
        underline = lines[index + 1].strip()
        if not title or len(underline) < 3:
            continue
        if set(underline) <= set(_HEADING_MARKS):
            positions.append(index)
    return positions


def _headings(lines: Sequence[str]) -> List[str]:
    """Return the headings of the lines of a topic."""
    return [lines[index].strip() for index in _heading_positions(lines)]


def count_topics() -> int:
    """Return the number of topics the standard library holds.

    Returns:
        The number of topics of the documentation of the language.
    """
    return len(_standard_topics())


def get_topics() -> Dict[str, str]:
    """Return the topics of the documentation of the language.

    The mapping of the standard library is copied, so a caller that changes the
    returned mapping does not change the documentation of the interpreter.

    Returns:
        A copy of the mapping of the names of the topics to their text.
    """
    return dict(_standard_topics())


def get_topic_names() -> List[str]:
    """Return the names of the topics of the documentation of the language.

    Returns:
        The names of the topics, in ascending order.
    """
    return sorted(_standard_topics())


def get_topics_subset(names: Sequence[str]) -> Dict[str, str]:
    """Return the topics of the given names.

    Args:
        names: The names of the topics.

    Returns:
        A mapping of the names of the topics to their text, in the order of the
        given names.

    Raises:
        TypeError: If *names* is not a sequence of strings.
        ValueError: If a name is empty or names no topic.
    """
    _require_sequence(names, "names")
    topics = _standard_topics()
    selected: Dict[str, str] = {}
    for name in names:
        _require_non_empty_str(name, "names entries")
        if name not in topics:
            raise ValueError(f"unknown topic: {name!r}")
        selected[name] = topics[name]
    return selected


def has_topic(name: str) -> bool:
    """Report whether the standard library holds a topic.

    Args:
        name: The name of the topic.

    Returns:
        ``True`` when the topic exists, ``False`` otherwise.
    """
    _require_non_empty_str(name, "name")
    return name in _standard_topics()


def get_topic(name: str) -> str:
    """Return the text of a topic.

    Args:
        name: The name of the topic.

    Returns:
        The text of the topic, the way the standard library stores it.

    Raises:
        TypeError: If *name* is not a string.
        ValueError: If *name* is empty or names no topic.
    """
    _require_non_empty_str(name, "name")
    topics = _standard_topics()
    try:
        return topics[name]
    except KeyError:
        raise ValueError(f"unknown topic: {name!r}") from None


def get_topic_title(name: str) -> str:
    """Return the title of a topic.

    The title of a topic is the first line of its text, the way the standard
    library writes it.

    Args:
        name: The name of the topic.

    Returns:
        The title of the topic.
    """
    text = get_topic(name)
    return text.split("\n", 1)[0].strip()


def get_topic_sections(name: str) -> List[str]:
    """Return the sections of a topic.

    A section of a topic is a part of the text that carries a heading of its
    own.  The title of the topic is not one of them.

    Args:
        name: The name of the topic.

    Returns:
        The headings of the sections of the topic, in the order of the text.
    """
    return _headings(get_topic(name).split("\n"))


def get_topic_section(name: str, section: str) -> str:
    """Return the text of a section of a topic.

    Args:
        name: The name of the topic.
        section: The heading of the section.

    Returns:
        The text of the section, without its heading.

    Raises:
        TypeError: If an argument is not a string.
        ValueError: If an argument is empty, names no topic, or names no
            section of the topic.
    """
    _require_non_empty_str(section, "section")
    lines = get_topic(name).split("\n")
    positions = _heading_positions(lines)
    for index in positions:
        if lines[index].strip() != section:
            continue
        end = len(lines)
        for later in positions:
            if later > index:
                end = later
                break
        body = lines[index + 2 : end]
        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()
        return "\n".join(body)
    raise ValueError(f"unknown section: {section!r} in topic {name!r}")


def search_topics(query: str) -> List[str]:
    """Return the topics that hold a text.

    The name of a topic and its text are searched, and the search ignores the
    case of the text.

    Args:
        query: The text to look for.

    Returns:
        The names of the topics that hold the text, in ascending order.
    """
    _require_non_empty_str(query, "query")
    needle = query.lower()
    topics = _standard_topics()
    return [
        name
        for name in sorted(topics)
        if needle in name.lower() or needle in topics[name].lower()
    ]


def wrap_topic(name: str, width: int = 76) -> str:
    """Return the text of a topic, wrapped for a terminal.

    The prose of the topic is wrapped again, and the parts of the text that
    are indented, such as the grammar of the language, are kept as they are.

    Args:
        name: The name of the topic.
        width: The width of the wrapped text.

    Returns:
        The text of the topic, wrapped to the given width.
    """
    _require_positive_int(width, "width")
    lines: List[str] = []
    paragraph: List[str] = []

    def flush() -> None:
        """Write the collected prose of a paragraph to the lines of the text."""
        if not paragraph:
            return
        lines.extend(textwrap.wrap(" ".join(paragraph), width=width))
        paragraph.clear()

    for line in get_topic(name).split("\n"):
        stripped = line.strip()
        if not stripped:
            flush()
            lines.append("")
            continue
        if line[:1].isspace() or set(stripped) <= set(_HEADING_MARKS + _TITLE_MARKS):
            flush()
            lines.append(line)
            continue
        paragraph.append(stripped)
    flush()
    return "\n".join(lines)
