"""Regular expression parse utilities wrapping the standard library :mod:`sre_parse` module.

The :mod:`sre_parse` module parses a regular expression pattern into a tree of
opcodes that the regular expression engine can compile.  It exposes the
``parse`` function, the ``parse_template`` helper, the ``SubPattern`` and
``State`` classes, the ``error`` exception, and a large set of opcode and flag
constants.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` instead of an opaque failure from the
standard library.  It adds the conveniences the standard library leaves to the
caller: the width of a pattern is reported as a tuple, a parsed pattern can be
dumped as text without printing to the standard output, and the parsed tree is
returned together with its width.

.. note::

   The :mod:`sre_parse` module is an internal module of the regular expression
   engine.  It is deprecated and slated for removal in Python 3.13 as part of
   :pep:`594`.  The import below degrades gracefully: when the interpreter no
   longer ships the module, the helpers that parse a pattern raise a
   :class:`RuntimeError` that names the missing module, while helpers that need
   no standard library keep working.

The wrapper never writes to the filesystem.
"""

from __future__ import annotations

import contextlib
import io
import warnings
from typing import Any, List, Optional, Tuple, cast

__all__ = [
    "ANY",
    "ASSERT",
    "ASSERT_NOT",
    "AT",
    "BRANCH",
    "CHARSET",
    "GROUPREF",
    "GROUPREF_EXISTS",
    "GROUPREF_IGNORE",
    "IN",
    "LITERAL",
    "MAXREPEAT",
    "MIN_REPEAT",
    "MIN_REPEAT_ONE",
    "MAX_REPEAT",
    "MAX_UNTIL",
    "NEGATE",
    "NOT_LITERAL",
    "OPCODES",
    "POSSESSIVE_REPEAT",
    "POSSESSIVE_REPEAT_ONE",
    "RANGE",
    "REPEAT",
    "REPEAT_ONE",
    "SRE_FLAG_ASCII",
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
    "SubPattern",
    "State",
    "error",
    "is_available",
    "parse_pattern",
    "parse_template",
    "pattern_dump",
    "pattern_width",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import sre_parse as _sre_parse
except Exception:  # pragma: no cover - removed in Python 3.13
    _sre_parse = None  # type: ignore[assignment]


def _sre_parse_module() -> Any:
    """Return the standard library ``sre_parse`` module.

    Returns:
        The imported :mod:`sre_parse` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``sre_parse``
            module.
    """
    if _sre_parse is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'sre_parse' module was removed in Python 3.13; "
            "use the re module instead"
        )
    return _sre_parse


def is_available() -> bool:
    """Report whether the interpreter ships the standard library ``sre_parse`` module.

    Returns:
        ``True`` when the module is importable, ``False`` otherwise.
    """
    return _sre_parse is not None


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for every other type."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str, not {type(value).__name__}")
    return value


def _require_flags(value: Any, name: str) -> int:
    """Return *value* as an integer flags mask, raising ``TypeError`` otherwise."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be int, not {type(value).__name__}")
    return value


def parse_pattern(pattern: Any, flags: int = 0) -> Any:
    """Parse a regular expression pattern into a :class:`SubPattern` tree.

    Args:
        pattern: The regular expression pattern to parse.
        flags: The compilation flags, as a combination of the ``SRE_FLAG_*``
            constants or the flags of the :mod:`re` module.

    Returns:
        The parsed pattern as a :class:`SubPattern` tree.

    Raises:
        TypeError: If *pattern* is not a string or *flags* is not an integer.
        RuntimeError: If the interpreter no longer ships the ``sre_parse``
            module.
        sre_parse.error: If *pattern* is not a valid regular expression.
    """
    pattern = _require_text(pattern, "pattern")
    flags = _require_flags(flags, "flags")
    module = _sre_parse_module()
    return module.parse(pattern, flags=flags)


def parse_template(template: Any, pattern: Any) -> List[Any]:
    """Parse a replacement template into a list of literals and group references.

    Args:
        template: The replacement template to parse, such as ``r"\\g<1>"``.
        pattern: A compiled :mod:`re` pattern, used to resolve group references
            by name or number.  Must have ``groups`` and ``groupindex``.

    Returns:
        A list of literal strings and group-reference integers, as produced by
        :func:`sre_parse.parse_template`.

    Raises:
        TypeError: If *template* is not a string or *pattern* is not a compiled
            regular expression pattern.
        RuntimeError: If the interpreter no longer ships the ``sre_parse``
            module.
        sre_parse.error: If *template* is not a valid template.
    """
    template = _require_text(template, "template")
    if not hasattr(pattern, "groups") or not hasattr(pattern, "groupindex"):
        raise TypeError(
            f"pattern must be a compiled regular expression, not {type(pattern).__name__}"
        )
    module = _sre_parse_module()
    return cast(List[Any], module.parse_template(template, pattern))


def pattern_width(pattern: Any, flags: int = 0) -> Optional[Tuple[int, int]]:
    """Return the minimum and maximum width of a parsed pattern.

    Args:
        pattern: The regular expression pattern to measure.
        flags: The compilation flags, as a combination of the ``SRE_FLAG_*``
            constants or the flags of the :mod:`re` module.

    Returns:
        A tuple of ``(min_width, max_width)``, or ``None`` when the width cannot
        be determined.

    Raises:
        TypeError: If *pattern* is not a string or *flags* is not an integer.
        RuntimeError: If the interpreter no longer ships the ``sre_parse``
            module.
        sre_parse.error: If *pattern* is not a valid regular expression.
    """
    parsed = parse_pattern(pattern, flags=flags)
    width = getattr(parsed, "getwidth", None)
    if callable(width):
        result = width()
        if isinstance(result, tuple) and len(result) == 2:
            return result  # type: ignore[return-value]
    return None


def pattern_dump(pattern: Any, flags: int = 0) -> str:
    """Return the text dump of a parsed pattern.

    Args:
        pattern: The regular expression pattern to dump.
        flags: The compilation flags, as a combination of the ``SRE_FLAG_*``
            constants or the flags of the :mod:`re` module.

    Returns:
        The text representation of the parsed pattern tree, with one opcode per
        line.

    Raises:
        TypeError: If *pattern* is not a string or *flags* is not an integer.
        RuntimeError: If the interpreter no longer ships the ``sre_parse``
            module.
        sre_parse.error: If *pattern* is not a valid regular expression.
    """
    parsed = parse_pattern(pattern, flags=flags)
    dump = getattr(parsed, "dump", None)
    if callable(dump):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            dump()
        return buffer.getvalue()
    return ""


# Re-export classes and the error exception if available.
if _sre_parse is not None:
    SubPattern = _sre_parse.SubPattern
    State = _sre_parse.State
    error = _sre_parse.error
else:  # pragma: no cover - Python 3.13 removed the module

    class SubPattern:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _sre_parse_module()

    class State:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _sre_parse_module()

    class error(Exception):  # type: ignore[no-redef]
        pass


# Re-export the most useful constants if available.
for _name in [
    "ANY",
    "ASSERT",
    "ASSERT_NOT",
    "AT",
    "BRANCH",
    "CHARSET",
    "GROUPREF",
    "GROUPREF_EXISTS",
    "GROUPREF_IGNORE",
    "IN",
    "LITERAL",
    "MAXREPEAT",
    "MIN_REPEAT",
    "MIN_REPEAT_ONE",
    "MAX_REPEAT",
    "MAX_UNTIL",
    "NEGATE",
    "NOT_LITERAL",
    "OPCODES",
    "POSSESSIVE_REPEAT",
    "POSSESSIVE_REPEAT_ONE",
    "RANGE",
    "REPEAT",
    "REPEAT_ONE",
    "SRE_FLAG_ASCII",
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
]:
    try:
        _value = getattr(_sre_parse, _name) if _sre_parse is not None else None
        globals()[_name] = _value
    except Exception:
        pass
