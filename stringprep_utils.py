"""String preparation utilities wrapping the standard library :mod:`stringprep` module.

The :mod:`stringprep` module exposes the tables of RFC 3454, the "String
Preparation" framework that the internationalized domain names of RFC 3491
are built on.  A table is either a set, which answers whether a character
belongs to it, or a mapping, which turns a character into another one.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It also adds the conveniences that the
standard library leaves to the caller: the tables are addressed by their name
such as ``"b1"``, the prohibited output of RFC 3454 is summarized by
:func:`is_prohibited`, and :func:`map_text` performs the mapping step of the
framework in one call.

The module is pure computation, so it works on every platform and never
touches the file system, the network, or a process.
"""

from __future__ import annotations

import stringprep as _stringprep
from types import MappingProxyType
from typing import Callable, Mapping

__all__: list[str] = [
    "MAP_TABLES",
    "TABLES",
    "find_problems",
    "in_table",
    "is_allowed",
    "is_bidi_allowed",
    "is_mapped_to_nothing",
    "is_preparable",
    "is_prohibited",
    "is_unassigned",
    "map_table",
    "map_table_names",
    "map_text",
    "table_names",
]


#: The set tables of RFC 3454, addressed by their name.
TABLES: Mapping[str, Callable[[str], bool]] = MappingProxyType(
    {
        "a1": _stringprep.in_table_a1,
        "b1": _stringprep.in_table_b1,
        "c11": _stringprep.in_table_c11,
        "c12": _stringprep.in_table_c12,
        "c11_c12": _stringprep.in_table_c11_c12,
        "c21": _stringprep.in_table_c21,
        "c22": _stringprep.in_table_c22,
        "c21_c22": _stringprep.in_table_c21_c22,
        "c3": _stringprep.in_table_c3,
        "c4": _stringprep.in_table_c4,
        "c5": _stringprep.in_table_c5,
        "c6": _stringprep.in_table_c6,
        "c7": _stringprep.in_table_c7,
        "c8": _stringprep.in_table_c8,
        "c9": _stringprep.in_table_c9,
        "d1": _stringprep.in_table_d1,
        "d2": _stringprep.in_table_d2,
    }
)

#: The mapping tables of RFC 3454, addressed by their name.
MAP_TABLES: Mapping[str, Callable[[str], str]] = MappingProxyType(
    {
        "b2": _stringprep.map_table_b2,
        "b3": _stringprep.map_table_b3,
    }
)

# The tables of the prohibited output of RFC 3454.  Table C.1.1, the plain
# space, is not one of them: it is allowed in a stored string.
_PROHIBITED_TABLES: tuple[str, ...] = (
    "c12",
    "c21",
    "c22",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c9",
)


def _character(value: str, name: str = "character") -> str:
    """Return *value* after checking that it is a single character.

    Args:
        value: The character to check.
        name: The name of the argument, used in the error messages.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* is empty or holds more than one character.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    if len(value) != 1:
        raise ValueError(f"{name} must be a single character, got {len(value)}")
    return value


def table_names() -> tuple[str, ...]:
    """Return the names of the set tables of RFC 3454.

    The names are the ones the framework uses: ``"a1"`` for the unassigned
    code points, ``"b1"`` for the characters that are commonly mapped to
    nothing, ``"c11"`` up to ``"c9"`` for the prohibited output, and ``"d1"``
    and ``"d2"`` for the bidirectional characters.
    """
    return tuple(sorted(TABLES))


def map_table_names() -> tuple[str, ...]:
    """Return the names of the mapping tables of RFC 3454.

    The names are the ones the framework uses: ``"b2"`` for the case folding
    with the compatibility decomposition and ``"b3"`` for the plain case
    folding.
    """
    return tuple(sorted(MAP_TABLES))


def in_table(name: str, character: str) -> bool:
    """Report whether a character belongs to a set table of RFC 3454.

    Args:
        name: The name of the table, such as ``"b1"``.
        character: The character to look for.

    Returns:
        ``True`` when the character belongs to the table.

    Raises:
        TypeError: If *name* or *character* is not a string.
        ValueError: If *name* is not the name of a set table, or if
            *character* is not a single character.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    table = TABLES.get(name)
    if table is None:
        raise ValueError(f"unknown table: {name}")
    return bool(table(_character(character)))


def map_table(name: str, character: str) -> str:
    """Map a character with a mapping table of RFC 3454.

    Args:
        name: The name of the table, such as ``"b2"``.
        character: The character to map.

    Returns:
        The mapped character, which may be empty for a character that is
        mapped to nothing.

    Raises:
        TypeError: If *name* or *character* is not a string.
        ValueError: If *name* is not the name of a mapping table, or if
            *character* is not a single character.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    table = MAP_TABLES.get(name)
    if table is None:
        raise ValueError(f"unknown mapping table: {name}")
    return str(table(_character(character)))


def is_unassigned(character: str) -> bool:
    """Report whether a character is an unassigned code point.

    The unassigned code points are the ones of table A.1 of RFC 3454.

    Raises:
        TypeError: If *character* is not a string.
        ValueError: If *character* is not a single character.
    """
    return bool(_stringprep.in_table_a1(_character(character)))


def is_mapped_to_nothing(character: str) -> bool:
    """Report whether a character is commonly mapped to nothing.

    The characters of table B.1 of RFC 3454, such as the soft hyphen, are
    removed while a string is prepared.

    Raises:
        TypeError: If *character* is not a string.
        ValueError: If *character* is not a single character.
    """
    return bool(_stringprep.in_table_b1(_character(character)))


def is_prohibited(character: str) -> bool:
    """Report whether a character belongs to the prohibited output.

    The prohibited output of RFC 3454 gathers the tables C.1.2 up to C.9, so
    the non-ASCII spaces, the control characters, the private use characters,
    the non-character code points, the surrogates, and the characters that
    are inappropriate for plain text or for a canonical representation.

    Raises:
        TypeError: If *character* is not a string.
        ValueError: If *character* is not a single character.
    """
    _character(character)
    return any(TABLES[name](character) for name in _PROHIBITED_TABLES)


def is_allowed(character: str) -> bool:
    """Report whether a character may be stored in a prepared string.

    A character is allowed when it is neither an unassigned code point nor
    part of the prohibited output of RFC 3454.  The characters that are
    commonly mapped to nothing stay allowed, because they are removed while
    the string is mapped rather than rejected.

    Raises:
        TypeError: If *character* is not a string.
        ValueError: If *character* is not a single character.
    """
    _character(character)
    return not is_unassigned(character) and not is_prohibited(character)


def is_bidi_allowed(character: str) -> bool:
    """Report whether a character may appear in a bidirectional name.

    The characters of the tables D.1 and D.2 of RFC 3454, the right-to-left
    and the left-to-right characters, may appear in a name that mixes the two
    directions.

    Raises:
        TypeError: If *character* is not a string.
        ValueError: If *character* is not a single character.
    """
    _character(character)
    return bool(_stringprep.in_table_d1(character) or _stringprep.in_table_d2(character))


def map_text(text: str) -> str:
    """Map a string with the mapping step of RFC 3454.

    The characters of table B.1 are removed, the rest is mapped with the
    table B.2, and the result is mapped with the table B.3.

    Args:
        text: The string to map.

    Returns:
        The mapped string.

    Raises:
        TypeError: If *text* is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    removed = "".join(char for char in text if not _stringprep.in_table_b1(char))
    folded = "".join(_stringprep.map_table_b2(char) for char in removed)
    return "".join(_stringprep.map_table_b3(char) for char in folded)


def find_problems(text: str) -> list[str]:
    """Return the problems of a string that holds the prohibited output.

    Every character that is an unassigned code point or that belongs to the
    prohibited output of RFC 3454 is reported, so a caller can show why a
    string cannot be stored.

    Args:
        text: The string to inspect.

    Returns:
        One message per offending character, in the order of the string.

    Raises:
        TypeError: If *text* is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    problems: list[str] = []
    for char in text:
        if is_unassigned(char):
            problems.append(f"unassigned code point U+{ord(char):04X}")
        elif is_prohibited(char):
            problems.append(f"prohibited code point U+{ord(char):04X}")
    return problems


def is_preparable(text: str) -> bool:
    """Report whether a string may be prepared and stored.

    Args:
        text: The string to inspect.

    Returns:
        ``True`` when the string holds no unassigned code point and no part
        of the prohibited output of RFC 3454.

    Raises:
        TypeError: If *text* is not a string.
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    return not find_problems(text)
