"""Failing-test-first verification of enum_utils.has_name / get_member."""
from enum_utils import Enum, has_name, get_member, get_member_name


class Color(Enum):
    RED = 1
    GREEN = 2


def test_has_name_rejects_non_member_attributes():
    assert has_name(Color, "RED") is True
    assert has_name(Color, "GREEN") is True
    assert has_name(Color, "__members__") is False
    assert has_name(Color, "mro") is False
    assert has_name(Color, "name") is False


def test_get_member_rejects_non_member_attributes():
    assert get_member(Color, "RED") is Color.RED
    try:
        get_member(Color, "__members__")
    except AttributeError:
        return
    raise AssertionError("get_member should reject non-member attributes")


def test_get_member_name_rejects_non_member():
    try:
        get_member_name(Color.__members__)
    except TypeError:
        return
    raise AssertionError("get_member_name should reject non-enum-member values")


if __name__ == "__main__":
    import sys
    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    sys.exit(1 if failures else 0)