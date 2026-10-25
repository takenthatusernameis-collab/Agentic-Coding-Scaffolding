"""HTML entities utilities wrapping the standard library html.entities module.

Provides helpers for working with HTML entity names and numeric codes.
"""

from __future__ import annotations

import html.entities
from typing import Optional

__all__ = [
    "html5",
    "name2codepoint",
    "codepoint2name",
    "entitydefs",
    "get_entity_by_name",
    "name_to_codepoint",
    "codepoint_to_name",
    "decode_entity",
    "unescape_entity",
]


html5 = getattr(html.entities, "html5", {})
name2codepoint = html.entities.name2codepoint
codepoint2name = html.entities.codepoint2name
entitydefs = html.entities.entitydefs


def name_to_codepoint(name: str) -> Optional[int]:
    """Get the codepoint for a named HTML entity.

    Args:
        name: Entity name without ampersand and semicolon.

    Returns:
        Codepoint as int, or None if not found.

    Raises:
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return name2codepoint.get(name)


def get_entity_by_name(name: str) -> Optional[int]:
    """Alias for name_to_codepoint."""
    return name_to_codepoint(name)


def codepoint_to_name(codepoint: int) -> Optional[str]:
    """Get the entity name for a codepoint.

    Args:
        codepoint: Unicode codepoint.

    Returns:
        Entity name or None if not found.

    Raises:
        TypeError: If codepoint is not an int.
        ValueError: If codepoint is out of range.
    """
    if not isinstance(codepoint, int) or isinstance(codepoint, bool):
        raise TypeError("codepoint must be an int")
    if codepoint < 0 or codepoint > 0x10FFFF:
        raise ValueError("codepoint out of range")
    return codepoint2name.get(codepoint)


def decode_entity(name: str) -> Optional[str]:
    """Decode a named entity to its string character.

    Args:
        name: Entity name without ampersand and semicolon.

    Returns:
        Decoded character or None if not found.

    Raises:
        TypeError: If name is not a string.
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    code = name2codepoint.get(name)
    if code is None:
        return None
    return chr(code)


def unescape_entity(name: str) -> Optional[str]:
    """Alias for decode_entity."""
    return decode_entity(name)
