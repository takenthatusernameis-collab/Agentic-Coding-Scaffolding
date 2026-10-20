"""Encoding name utilities wrapping the standard library :mod:`encodings` module.

The :mod:`encodings` module is the registry of the codecs of the Python
interpreter.  It maps encoding aliases such as ``"utf8"`` to their canonical
names such as ``"utf_8"``, and it normalizes encoding names so that
``"UTF-8"`` becomes ``"UTF_8"``.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` instead of an opaque failure.  It
also adds the conveniences that the standard library leaves to the caller: the
aliases are exposed as a read-only mapping, every canonical encoding is listed
with :func:`all_encodings`, and the aliases of one encoding are listed with
:func:`encoding_aliases`.

The module is pure computation, so it works on every platform and never
touches the file system, the network, or a process.
"""

from __future__ import annotations

import encodings as _encodings
import encodings.aliases as _aliases
from types import MappingProxyType
from typing import Mapping

__all__: list[str] = [
    "ALIASES",
    "all_aliases",
    "all_encodings",
    "encoding_aliases",
    "is_alias",
    "is_known_encoding",
    "normalize_encoding",
]

#: The read-only mapping of every encoding alias to its canonical name.
ALIASES: Mapping[str, str] = MappingProxyType(dict(_aliases.aliases))


def normalize_encoding(name: str) -> str:
    """Return the canonical form of the encoding name *name*.

    Args:
        name: The encoding name to normalize, such as ``"UTF-8"``.

    Returns:
        The normalized encoding name, such as ``"utf_8"``.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    return _encodings.normalize_encoding(name)


def is_known_encoding(name: str) -> bool:
    """Report whether *name* is a known encoding alias or canonical name.

    A name is known when it is an alias of the interpreter or when its
    normalized form matches a canonical encoding name.  The comparison is
    case-insensitive, so ``"UTF-8"`` and ``"utf_8"`` are both known.

    Args:
        name: The encoding name to check.

    Returns:
        ``True`` when *name* is an alias or a canonical encoding name.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    canonicals = set(ALIASES.values())
    normalized = _encodings.normalize_encoding(name).lower()
    return name in ALIASES or normalized in canonicals


def is_alias(name: str) -> bool:
    """Report whether *name* is an encoding alias rather than a canonical name.

    Args:
        name: The encoding name to check.

    Returns:
        ``True`` when *name* is an alias of another encoding.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    return name in ALIASES


def encoding_aliases(name: str) -> tuple[str, ...]:
    """Return the aliases of the encoding *name*.

    The aliases are resolved to the canonical name of *name* first, so an
    alias such as ``"utf8"`` yields the same result as its canonical name
    ``"utf_8"``.  The returned aliases are sorted and include *name* itself
    when it is an alias.

    Args:
        name: An encoding alias or canonical name.

    Returns:
        The sorted aliases of the encoding.

    Raises:
        TypeError: If *name* is not a string.
        ValueError: If *name* is not a known encoding.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    if name in ALIASES:
        canonical = ALIASES[name]
    elif name in set(ALIASES.values()):
        canonical = name
    else:
        raise ValueError(f"unknown encoding: {name}")
    found = [alias for alias, target in ALIASES.items() if target == canonical]
    return tuple(sorted(found))


def all_aliases() -> Mapping[str, str]:
    """Return the read-only mapping of every alias to its canonical name.

    Returns:
        The alias mapping of the interpreter.
    """
    return ALIASES


def all_encodings() -> tuple[str, ...]:
    """Return every canonical encoding name of the interpreter.

    Returns:
        The sorted canonical encoding names.
    """
    return tuple(sorted(set(ALIASES.values())))
