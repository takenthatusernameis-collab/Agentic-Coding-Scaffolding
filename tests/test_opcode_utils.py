"""Tests for opcode_utils."""

from opcode_utils import (
    get_cmp_op,
    get_opmap,
    get_opname,
    has_argument,
    is_compare,
    is_const,
    is_free,
    is_jump_abs,
    is_jump_rel,
    is_local,
    is_name,
    stack_effect,
)


def test_stack_effect():
    assert stack_effect(1)  # POP_TOP has effect -1
    assert isinstance(stack_effect(1), int)


def test_get_opmap():
    opmap = get_opmap()
    assert isinstance(opmap, dict)
    assert len(opmap) > 0


def test_get_opname():
    opname = get_opname()
    assert isinstance(opname, list)
    assert len(opname) > 0


def test_is_compare():
    cmp_op = get_cmp_op()
    assert isinstance(is_compare(107), bool)


def test_is_const():
    assert isinstance(is_const(100), bool)


def test_is_free():
    assert isinstance(is_free(135), bool)


def test_is_jump_abs():
    assert isinstance(is_jump_abs(93), bool)


def test_is_jump_rel():
    assert isinstance(is_jump_rel(110), bool)


def test_is_local():
    assert isinstance(is_local(124), bool)


def test_is_name():
    assert isinstance(is_name(90), bool)


def test_get_cmp_op():
    cmp_op = get_cmp_op()
    assert isinstance(cmp_op, tuple)
    assert len(cmp_op) > 0


def test_has_argument():
    assert isinstance(has_argument(90), bool)
