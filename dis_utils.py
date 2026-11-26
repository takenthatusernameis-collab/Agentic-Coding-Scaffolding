"""Disassembly utilities wrapping stdlib dis."""

from __future__ import annotations

import dis as _dis
from typing import Any, Iterable, List, Tuple

__all__ = [
    "dis",
    "disassemble",
    "show_code",
    "get_instructions",
    "code_info",
    "distb",
    "disco",
    "findlinestarts",
    "findlabels",
    "Bytecode",
]


dis = _dis.dis
disassemble = _dis.disassemble
show_code = _dis.show_code
get_instructions = _dis.get_instructions
code_info = _dis.code_info
distb = _dis.distb
disco = _dis.disco
Bytecode = _dis.Bytecode


def findlinestarts(code: Any) -> Iterable[Tuple[int, int]]:
    """Wrapper for dis.findlinestarts with py3.12/3.13 compatibility.

    ``dis.findlinestarts`` is a generator function, so calling it never raises;
    the ``AttributeError`` for a non-code argument surfaces only while the
    generator is iterated. The result is therefore materialized inside the
    ``try`` block so the ``co_code`` fallback below is actually reachable and
    invalid input yields an empty list instead of leaking that error.
    """
    try:
        return list(_dis.findlinestarts(code))
    except Exception:
        # Fallback
        if hasattr(code, "co_code"):
            try:
                return list(_dis.findlinestarts(code.co_code))
            except Exception:
                return []
        return []


def findlabels(code: Any) -> List[int]:
    """Wrapper for dis.findlabels with py3.12/3.13 compatibility."""
    try:
        return _dis.findlabels(code)
    except Exception:
        if hasattr(code, "co_code"):
            try:
                return _dis.findlabels(code.co_code)
            except Exception:
                return []
        return []
