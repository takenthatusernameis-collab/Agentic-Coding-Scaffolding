"""Opcode utility functions for working with Python bytecode."""

from __future__ import annotations

import opcode
from typing import Any

__all__: list[str] = [
    "stack_effect",
    "get_opmap",
    "get_opname",
    "is_compare",
    "is_const",
    "is_free",
    "is_jump_abs",
    "is_jump_rel",
    "is_local",
    "is_name",
    "get_cmp_op",
    "has_argument",
]


def stack_effect(opcode_val: int, oparg: int | None = None, *, jump: bool | None = None) -> int:
    """Compute the stack effect of a bytecode operation."""
    return opcode.stack_effect(opcode_val, oparg, jump=jump)


def get_opmap() -> dict[str, int]:
    """Return the mapping of opcode names to byte values."""
    return dict(opcode.opmap)


def get_opname() -> list[str]:
    """Return the list of opcode names by byte value."""
    return list(opcode.opname)


def is_compare(opcode_val: int) -> bool:
    """Return True if the opcode is a comparison operator."""
    return opcode_val in opcode.hascompare


def is_const(opcode_val: int) -> bool:
    """Return True if the opcode takes a constant."""
    return opcode_val in opcode.hasconst


def is_free(opcode_val: int) -> bool:
    """Return True if the opcode takes a free variable."""
    return opcode_val in opcode.hasfree


def is_jump_abs(opcode_val: int) -> bool:
    """Return True if the opcode has an absolute jump."""
    return opcode_val in opcode.hasjabs


def is_jump_rel(opcode_val: int) -> bool:
    """Return True if the opcode has a relative jump."""
    return opcode_val in opcode.hasjrel


def is_local(opcode_val: int) -> bool:
    """Return True if the opcode takes a local variable."""
    return opcode_val in opcode.haslocal


def is_name(opcode_val: int) -> bool:
    """Return True if the opcode takes a name."""
    return opcode_val in opcode.hasname


def get_cmp_op() -> tuple[str, ...]:
    """Return the comparison operator names."""
    return tuple(opcode.cmp_op)


def has_argument(opcode_val: int) -> bool:
    """Return True if the opcode has an argument."""
    return opcode_val in opcode.hasarg
