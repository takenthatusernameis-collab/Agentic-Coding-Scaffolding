"""Regular expression constants utilities wrapping the standard library
:mod:`sre_constants` module.

The :mod:`sre_constants` module exposes the internal constants used by the
regular expression engine. It contains named integer constants for opcode
values and symbolic names, along with exception classes and small helpers used
by :mod:`sre_parse` and :mod:`sre_compile`.

This wrapper provides a validated, consistent interface with typed accessors,
input validation, and documentation. The module is part of the regex
implementation; in modern Python it is available but marked deprecated in some
builds. The wrapper degrades gracefully: if the module cannot be imported,
helpers raise a :class:`RuntimeError` naming the missing module while helpers
that need no standard library continue to work.

The wrapper only reads values from the standard library and never writes to
the filesystem.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, List

__all__ = [
    "ANY",
    "ANY_ALL",
    "ASSERT",
    "ASSERT_NOT",
    "AT",
    "AT_BEGINNING",
    "AT_BEGINNING_LINE",
    "AT_BEGINNING_STRING",
    "AT_BOUNDARY",
    "ATCODES",
    "AT_END",
    "AT_END_LINE",
    "AT_END_STRING",
    "AT_LOC_BOUNDARY",
    "AT_LOC_NON_BOUNDARY",
    "AT_MULTILINE",
    "AT_NON_BOUNDARY",
    "AT_UNI_BOUNDARY",
    "AT_UNI_NON_BOUNDARY",
    "AT_UNICODE",
    "BRANCH",
    "CATEGORY",
    "CATEGORY_DIGIT",
    "CATEGORY_LINEBREAK",
    "CATEGORY_LOC_NOT_WORD",
    "CATEGORY_LOC_WORD",
    "CATEGORY_NOT_DIGIT",
    "CATEGORY_NOT_LINEBREAK",
    "CATEGORY_NOT_SPACE",
    "CATEGORY_NOT_WORD",
    "CATEGORY_SPACE",
    "CATEGORY_UNI_DIGIT",
    "CATEGORY_UNI_LINEBREAK",
    "CATEGORY_UNI_NOT_WORD",
    "CATEGORY_UNI_WORD",
    "CATEGORY_WORD",
    "CHARSET",
    "error",
    "FAILURE",
    "GROUPREF",
    "GROUPREF_EXISTS",
    "GROUPREF_IGNORE",
    "GROUPREF_LOC_IGNORE",
    "GROUPREF_UNI_IGNORE",
    "IN",
    "INFO",
    "JUMP",
    "LITERAL",
    "MAGIC",
    "MAXREPEAT",
    "MIN_REPEAT",
    "MIN_REPEAT_ONE",
    "MAX_REPEAT",
    "MAX_UNTIL",
    "NEGATE",
    "NOT_LITERAL",
    "OPCODES",
    "OP_IGNORE",
    "OP_LOCALE_IGNORE",
    "OP_UNICODE_IGNORE",
    "assert_valid_flags",
    "error_codes",
    "get_all",
    "get_opcodes",
    "is_available",
    "lookup_opcode",
    "op_code",
    "opcodenames",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import sre_constants as _sre_constants
except Exception:  # pragma: no cover - some builds may not have it
    _sre_constants = None  # type: ignore[assignment]


def _sre_constants_module() -> Any:
    """Return the standard library ``sre_constants`` module."""
    if _sre_constants is None:  # pragma: no cover
        raise RuntimeError(
            "the standard library 'sre_constants' module is not available; "
            "use the re module's constants instead"
        )
    return _sre_constants


def is_available() -> bool:
    """Report whether the interpreter ships the standard library module."""
    return _sre_constants is not None


def _get(name: str, default: Any = None) -> Any:
    mod = _sre_constants_module()
    return getattr(mod, name, default)


# Common constants - export them if available
for _name in [
    "ANY",
    "ANY_ALL",
    "ASSERT",
    "ASSERT_NOT",
    "AT",
    "AT_BEGINNING",
    "AT_BEGINNING_LINE",
    "AT_BEGINNING_STRING",
    "AT_BOUNDARY",
    "ATCODES",
    "AT_END",
    "AT_END_LINE",
    "AT_END_STRING",
    "AT_LOC_BOUNDARY",
    "AT_LOC_NON_BOUNDARY",
    "AT_MULTILINE",
    "AT_NON_BOUNDARY",
    "AT_UNI_BOUNDARY",
    "AT_UNI_NON_BOUNDARY",
    "AT_UNICODE",
    "BRANCH",
    "CATEGORY",
    "CATEGORY_DIGIT",
    "CATEGORY_LINEBREAK",
    "CATEGORY_LOC_NOT_WORD",
    "CATEGORY_LOC_WORD",
    "CATEGORY_NOT_DIGIT",
    "CATEGORY_NOT_LINEBREAK",
    "CATEGORY_NOT_SPACE",
    "CATEGORY_NOT_WORD",
    "CATEGORY_SPACE",
    "CATEGORY_UNI_DIGIT",
    "CATEGORY_UNI_LINEBREAK",
    "CATEGORY_UNI_NOT_WORD",
    "CATEGORY_UNI_WORD",
    "CATEGORY_WORD",
    "CHARSET",
    "CHCODES",
    "CH_LOCALE",
    "CH_UNICODE",
    "CATEGORY_DIGIT",
    "CATEGORY_NOT_DIGIT",
    "CATEGORY_UNI_DIGIT",
    "CATEGORY_UNI_NOT_DIGIT",
    "FAILURE",
    "GROUPREF",
    "GROUPREF",
    "GROUPREF_EXISTS",
    "GROUPREF_IGNORE",
    "GROUPREF_LOC_IGNORE",
    "GROUPREF_UNI_IGNORE",
    "IN",
    "INFO",
    "JUMP",
    "LITERAL",
    "MAGIC",
    "MAXREPEAT",
    "MIN_REPEAT",
    "MIN_REPEAT_ONE",
    "MAX_REPEAT",
    "MAX_UNTIL",
    "NEGATE",
    "NOT_LITERAL",
    "OPCODES",
    "OP_IGNORE",
    "OP_LOCALE_IGNORE",
    "OP_UNICODE_IGNORE",
    "POSSESSIVE_REPEAT",
    "RANGE",
    "REPEAT",
    "REPEAT_ONE",
    "SRE_FLAG_DEBUG",
    "SRE_FLAG_DOTALL",
    "SRE_FLAG_IGNORECASE",
    "SRE_FLAG_LOCALE",
    "SRE_FLAG_MULTILINE",
    "SRE_FLAG_TEMPLATE",
    "SRE_FLAG_UNICODE",
    "SRE_FLAG_VERBOSE",
    "SUBPATTERN",
    "SUCCESS",
    "TYPE_FLAGS",
]:
    try:
        globals()[_name] = getattr(_sre_constants, _name) if _sre_constants is not None else None
    except Exception:
        pass

try:
    error = _sre_constants.error if _sre_constants is not None else Exception
except Exception:
    error = Exception  # type: ignore[assignment,misc]


def assert_valid_flags(flags: Any, module: Any = None) -> None:
    """Validate regex flags."""
    if not isinstance(flags, int):
        raise TypeError(f"flags must be int, got {type(flags).__name__}")
    if _sre_constants is not None and hasattr(_sre_constants, "assert_valid_flags"):
        _sre_constants.assert_valid_flags(flags, module)
    return None


def get_opcodes() -> List[int]:
    """Return the opcode list if available."""
    mod = _sre_constants_module()
    opcodes = getattr(mod, "OPCODES", None)
    if isinstance(opcodes, (list, tuple)):
        return list(opcodes)
    return []


def opcodenames() -> Dict[int, str]:
    """Return mapping of opcode numbers to names."""
    mod = _sre_constants_module()
    names = getattr(mod, "OPCODES", None)
    result: Dict[int, str] = {}
    if isinstance(names, (list, tuple)):
        for i, name in enumerate(names):
            if name is not None:
                result[i] = str(name)
    # Some implementations store different structure
    return result


def lookup_opcode(code: Any) -> str:
    """Look up the name of an opcode."""
    if not isinstance(code, int):
        raise TypeError(f"code must be int, got {type(code).__name__}")
    names = opcodenames()
    if code in names:
        return names[code]
    raise ValueError(f"unknown opcode: {code}")


def op_code(name: Any) -> int:
    """Look up the numeric code for an opcode name."""
    if not isinstance(name, str):
        raise TypeError(f"name must be str, got {type(name).__name__}")
    names = opcodenames()
    # reverse lookup
    for code, n in names.items():
        if n == name:
            return code
    raise ValueError(f"unknown opcode name: {name}")


def get_all() -> Dict[str, Any]:
    """Return all public constants from the module."""
    if _sre_constants is None:
        raise RuntimeError(
            "the standard library 'sre_constants' module is not available"
        )
    result = {}
    for k in dir(_sre_constants):
        if not k.startswith("_"):
            result[k] = getattr(_sre_constants, k)
    return result


def error_codes() -> Dict[str, int]:
    """Return error codes if available."""
    if _sre_constants is None:
        raise RuntimeError(
            "the standard library 'sre_constants' module is not available"
        )
    codes = getattr(_sre_constants, "error_codes", None)
    if isinstance(codes, dict):
        return dict(codes)
    return {}
