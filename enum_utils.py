"""Enum utilities for working with Python ``enum.Enum`` classes."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Type, TypeVar

E = TypeVar("E", bound=Enum)

__all__ = [
    "enum_to_dict",
    "get_enum_member",
    "is_enum_member",
    "list_enum_members",
    "enum_value_from_name",
    "enum_name_from_value",
]


def enum_to_dict(enum_class: Type[E]) -> Dict[str, Any]:
    """Convert an enum class to a dictionary mapping member names to values.

    Args:
        enum_class: The Enum subclass to convert.

    Returns:
        A dictionary mapping each member name to its value.

    Raises:
        TypeError: If ``enum_class`` is not an Enum subclass.

    Examples:
        >>> class Color(enum.Enum):
        ...     RED = 1
        ...     GREEN = 2
        >>> enum_to_dict(Color)
        {'RED': 1, 'GREEN': 2}
    """
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise TypeError("enum_class must be an Enum subclass")
    return {member.name: member.value for member in enum_class}


def get_enum_member(enum_class: Type[E], key: Any) -> E:
    """Return the enum member matching ``key`` by name or value.

    Args:
        enum_class: The Enum subclass to search.
        key: The member name (str) or value to look up.

    Returns:
        The matching enum member.

    Raises:
        TypeError: If ``enum_class`` is not an Enum subclass.
        ValueError: If no member matches ``key``.
    """
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise TypeError("enum_class must be an Enum subclass")
    try:
        return enum_class[key]  # type: ignore[call-overload]
    except (KeyError, TypeError):
        pass
    try:
        return enum_class(key)  # type: ignore[call-overload]
    except ValueError:
        raise ValueError(
            f"No enum member in {enum_class.__name__} matches {key!r}"
        )


def is_enum_member(enum_class: Type[E], value: Any) -> bool:
    """Return True if ``value`` matches any member value of ``enum_class``.

    Args:
        enum_class: The Enum subclass to search.
        value: The value to check.

    Returns:
        True if a member with ``value`` exists, False otherwise.

    Raises:
        TypeError: If ``enum_class`` is not an Enum subclass.
    """
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise TypeError("enum_class must be an Enum subclass")
    return any(member.value == value for member in enum_class)


def list_enum_members(enum_class: Type[E]) -> List[E]:
    """Return all members of ``enum_class`` in declaration order.

    Args:
        enum_class: The Enum subclass to list.

    Returns:
        A list of all enum members.

    Raises:
        TypeError: If ``enum_class`` is not an Enum subclass.
    """
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise TypeError("enum_class must be an Enum subclass")
    return list(enum_class)


def enum_value_from_name(enum_class: Type[E], name: str) -> Any:
    """Return the value of the enum member with the given ``name``.

    Args:
        enum_class: The Enum subclass to search.
        name: The name of the member.

    Returns:
        The value of the matching member.

    Raises:
        TypeError: If ``enum_class`` is not an Enum subclass or ``name`` is
            not a string.
        ValueError: If no member with ``name`` exists.
    """
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise TypeError("enum_class must be an Enum subclass")
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    try:
        return enum_class[name].value  # type: ignore[call-overload]
    except KeyError:
        raise ValueError(
            f"{enum_class.__name__} has no member named {name!r}"
        )


def enum_name_from_value(enum_class: Type[E], value: Any) -> str:
    """Return the name of the enum member with the given ``value``.

    Args:
        enum_class: The Enum subclass to search.
        value: The value of the member.

    Returns:
        The name of the matching member.

    Raises:
        TypeError: If ``enum_class`` is not an Enum subclass.
        ValueError: If no member with ``value`` exists.
    """
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise TypeError("enum_class must be an Enum subclass")
    for member in enum_class:
        if member.value == value:
            return member.name
    raise ValueError(
        f"{enum_class.__name__} has no member with value {value!r}"
    )
