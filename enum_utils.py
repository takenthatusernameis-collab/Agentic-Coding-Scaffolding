"""Enum utilities wrapping the standard library enum module.

Provides typed helpers for working with enums, including safe lookups,
membership checks, and conversions to common representations.
"""

from __future__ import annotations

import enum
from typing import Any, Dict, List, Tuple, Type

__all__ = [
    "Enum",
    "IntEnum",
    "StrEnum",
    "Flag",
    "IntFlag",
    "auto",
    "unique",
    "is_enum",
    "is_enum_member",
    "get_member",
    "get_member_name",
    "get_member_value",
    "names",
    "values",
    "as_dict",
    "as_list",
    "has_name",
    "has_value",
]


Enum = enum.Enum
IntEnum = enum.IntEnum
StrEnum = getattr(enum, "StrEnum", enum.Enum)
Flag = enum.Flag
IntFlag = enum.IntFlag
auto = enum.auto
unique = enum.unique


def is_enum(obj: Any) -> bool:
    """Return True if obj is an Enum class or Enum member."""
    if isinstance(obj, enum.EnumMeta):
        return True
    return isinstance(obj, enum.Enum)


def is_enum_member(obj: Any) -> bool:
    """Return True if obj is an instance of an Enum member."""
    return isinstance(obj, enum.Enum) and not isinstance(obj, enum.EnumMeta)


def get_member(enum_cls: Type[enum.Enum], name: str) -> enum.Enum:
    """Get an enum member by name.

    Args:
        enum_cls: The enum class to look up in.
        name: The name of the member.

    Returns:
        The enum member.

    Raises:
        TypeError: If enum_cls is not an Enum class or name is not a string.
        AttributeError: If the member does not exist.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    try:
        return getattr(enum_cls, name)  # type: ignore[no-any-return]
    except AttributeError as exc:
        raise AttributeError(f"{enum_cls.__name__} has no member named {name!r}") from exc


def get_member_name(member: enum.Enum) -> str:
    """Return the name of an enum member.

    Args:
        member: The enum member.

    Returns:
        The member name.

    Raises:
        TypeError: If member is not an Enum member.
    """
    if not isinstance(member, enum.Enum) or isinstance(member, enum.EnumMeta):
        raise TypeError("member must be an Enum member")
    return member.name


def get_member_value(member: enum.Enum) -> Any:
    """Return the value of an enum member.

    Args:
        member: The enum member.

    Returns:
        The member value.

    Raises:
        TypeError: If member is not an Enum member.
    """
    if not isinstance(member, enum.Enum) or isinstance(member, enum.EnumMeta):
        raise TypeError("member must be an Enum member")
    return member.value


def names(enum_cls: Type[enum.Enum]) -> List[str]:
    """Return a list of member names for an enum class.

    Args:
        enum_cls: The enum class.

    Returns:
        List of member names.

    Raises:
        TypeError: If enum_cls is not an Enum class.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    return [m.name for m in enum_cls]


def values(enum_cls: Type[enum.Enum]) -> List[Any]:
    """Return a list of member values for an enum class.

    Args:
        enum_cls: The enum class.

    Returns:
        List of member values.

    Raises:
        TypeError: If enum_cls is not an Enum class.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    return [m.value for m in enum_cls]


def as_dict(enum_cls: Type[enum.Enum]) -> Dict[str, Any]:
    """Return a mapping of member names to values.

    Args:
        enum_cls: The enum class.

    Returns:
        Dict mapping names to values.

    Raises:
        TypeError: If enum_cls is not an Enum class.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    return {m.name: m.value for m in enum_cls}


def as_list(enum_cls: Type[enum.Enum]) -> List[Tuple[str, Any]]:
    """Return a list of (name, value) tuples for an enum class.

    Args:
        enum_cls: The enum class.

    Returns:
        List of (name, value) pairs.

    Raises:
        TypeError: If enum_cls is not an Enum class.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    return [(m.name, m.value) for m in enum_cls]


def has_name(enum_cls: Type[enum.Enum], name: str) -> bool:
    """Return True if the enum class has a member with the given name.

    Args:
        enum_cls: The enum class.
        name: The name to check.

    Returns:
        True if member exists, False otherwise.

    Raises:
        TypeError: If enum_cls is not an Enum class or name is not a string.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    return hasattr(enum_cls, name)


def has_value(enum_cls: Type[enum.Enum], value: Any) -> bool:
    """Return True if the enum class has a member with the given value.

    Args:
        enum_cls: The enum class.
        value: The value to check.

    Returns:
        True if any member has this value, False otherwise.

    Raises:
        TypeError: If enum_cls is not an Enum class.
    """
    if not isinstance(enum_cls, enum.EnumMeta):
        raise TypeError("enum_cls must be an Enum class")
    try:
        return any(m.value == value for m in enum_cls)
    except Exception:
        return False
