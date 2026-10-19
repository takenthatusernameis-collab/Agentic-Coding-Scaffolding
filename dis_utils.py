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
    """Wrapper for dis.findlinestarts with py3.12/3.13 compatibility."""
    # In 3.12 it takes code.co_code; in general pass through to stdlib
    try:
        return _dis.findlinestarts(code)
    except Exception:
        # Fallback
        if hasattr(code, "co_code"):
            try:
                return _dis.findlinestarts(code.co_code)
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
