"""Tests for enum_utils module."""

import enum

import enum_utils


class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Status(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CLOSED = "closed"


def test_enum_to_dict():
    assert enum_utils.enum_to_dict(Color) == {"RED": 1, "GREEN": 2, "BLUE": 3}


def test_get_enum_member_by_name():
    assert enum_utils.get_enum_member(Color, "RED") is Color.RED


def test_get_enum_member_by_value():
    assert enum_utils.get_enum_member(Color, 2) is Color.GREEN


def test_get_enum_member_not_found():
    try:
        enum_utils.get_enum_member(Color, 99)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_is_enum_member():
    assert enum_utils.is_enum_member(Color, 2) is True
    assert enum_utils.is_enum_member(Color, 99) is False


def test_list_enum_members():
    assert enum_utils.list_enum_members(Color) == [Color.RED, Color.GREEN, Color.BLUE]


def test_enum_value_from_name():
    assert enum_utils.enum_value_from_name(Status, "ACTIVE") == "active"


def test_enum_name_from_value():
    assert enum_utils.enum_name_from_value(Color, 3) == "BLUE"


def test_enum_name_from_value_not_found():
    try:
        enum_utils.enum_name_from_value(Color, 99)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_invalid_enum_class_raises():
    for fn in (
        enum_utils.enum_to_dict,
        enum_utils.get_enum_member,
        enum_utils.is_enum_member,
        enum_utils.list_enum_members,
        enum_utils.enum_value_from_name,
        enum_utils.enum_name_from_value,
    ):
        try:
            fn(int, "x")  # type: ignore[arg-type]
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError from {fn.__name__}")
