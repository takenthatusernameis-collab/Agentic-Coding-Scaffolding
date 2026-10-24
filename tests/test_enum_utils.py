"""Tests for enum_utils module."""

from enum_utils import (
    Enum,
    Flag,
    IntEnum,
    as_dict,
    as_list,
    auto,
    get_member,
    get_member_name,
    get_member_value,
    has_name,
    has_value,
    is_enum,
    is_enum_member,
    names,
    unique,
    values,
)


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Status(IntEnum):
    OK = 200
    NOT_FOUND = 404


class Permissions(Flag):
    READ = 1
    WRITE = 2
    EXEC = 4


@unique
class Priority(Enum):
    LOW = 1
    HIGH = 2


def test_is_enum_class():
    assert is_enum(Color) is True
    assert is_enum(Enum) is True


def test_is_enum_member():
    assert is_enum_member(Color.RED) is True
    assert is_enum_member(Color) is False


def test_get_member():
    assert get_member(Color, "RED") is Color.RED


def test_get_member_name():
    assert get_member_name(Color.GREEN) == "GREEN"


def test_get_member_value():
    assert get_member_value(Color.BLUE) == 3


def test_names():
    assert names(Color) == ["RED", "GREEN", "BLUE"]


def test_values():
    assert values(Color) == [1, 2, 3]


def test_as_dict():
    assert as_dict(Color) == {"RED": 1, "GREEN": 2, "BLUE": 3}


def test_as_list():
    assert as_list(Color) == [("RED", 1), ("GREEN", 2), ("BLUE", 3)]


def test_has_name():
    assert has_name(Color, "RED") is True
    assert has_name(Color, "YELLOW") is False


def test_has_value():
    assert has_value(Color, 2) is True
    assert has_value(Color, 99) is False


def test_int_enum():
    assert isinstance(Status.OK, int)
    assert Status.OK + 1 == 201


def test_flag():
    assert Permissions.READ | Permissions.WRITE


def test_auto():
    class AutoEnum(Enum):
        FIRST = auto()
        SECOND = auto()
    assert AutoEnum.FIRST.value != AutoEnum.SECOND.value


def test_get_member_type_errors():
    try:
        get_member("not_enum", "X")
        assert False
    except TypeError:
        pass


def test_get_member_name_type_error():
    try:
        get_member_name(Color)
        assert False
    except TypeError:
        pass


def test_names_type_error():
    try:
        names(Color.RED)
        assert False
    except TypeError:
        pass
