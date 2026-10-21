"""XML parsing utilities wrapping the standard library :mod:`pyexpat` module.

The :mod:`pyexpat` module is the binding of the expat parser that Python ships
as :mod:`pyexpat` and as :mod:`xml.parsers.expat`.  The standard library offers
the factory :func:`pyexpat.ParserCreate`, the error :class:`pyexpat.ExpatError`,
the error text :func:`pyexpat.ErrorString`, the version of the library, and a
parser with dozens of methods, among them :meth:`pyexpat.xmlparser.Parse`,
:meth:`pyexpat.xmlparser.ParseFile`, :meth:`pyexpat.xmlparser.SetBase`,
:meth:`pyexpat.xmlparser.GetBase`, :meth:`pyexpat.xmlparser.SetParamEntityParsing`,
:meth:`pyexpat.xmlparser.ExternalEntityParserCreate`,
:meth:`pyexpat.xmlparser.CurrentByteIndex`, :meth:`pyexpat.xmlparser.CurrentLineNumber`,
:meth:`pyexpat.xmlparser.CurrentColumnNumber`, :meth:`pyexpat.xmlparser.ErrorCode`,
:meth:`pyexpat.xmlparser.ErrorLineNumber`, :meth:`pyexpat.xmlparser.ErrorColumnNumber`,
and the ``*Handler`` setters.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure.  It adds the conveniences the standard library leaves to the
caller: the parser is created with the options of expat behind one validated
call, a document is parsed from text or from a file behind one helper that
names the file it reads, the attributes of an element are returned as a
mapping, and the parser reports the position of an error as one record instead
of three calls.

.. note::

   The :mod:`pyexpat` module ships with every CPython interpreter.  The import
   below degrades gracefully anyway: when the interpreter does not ship the
   module, the helpers raise a :class:`RuntimeError` that names the missing
   module, while :func:`is_available` keeps working.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, List, Mapping, NamedTuple, Optional, Tuple, cast

try:
    import pyexpat as _pyexpat
except ImportError:  # pragma: no cover - pyexpat ships with every CPython
    _pyexpat = None  # type: ignore[assignment]


class ErrorPosition(NamedTuple):
    """The position of an error reported by the parser.

    The standard library reports the position of an error with three separate
    attributes: the line number, the column number, and the error code.  The
    wrapper returns them as one record.

    Attributes:
        line: The line number where the error occurred.
        column: The column number where the error occurred.
        code: The error code of the standard library.
        byte_index: The byte index where the error occurred.
    """

    line: int
    column: int
    code: int
    byte_index: int


class CurrentPosition(NamedTuple):
    """The current position of the parser.

    Attributes:
        byte_index: The byte index of the current position.
        line_number: The line number of the current position.
        column_number: The column number of the current position.
    """

    byte_index: int
    line_number: int
    column_number: int


ElementAttributes = Dict[str, str]
StartElementHandler = Callable[[str, ElementAttributes], None]
EndElementHandler = Callable[[str], None]
CharacterDataHandler = Callable[[str], None]
ProcessingInstructionHandler = Callable[[str, str], None]


if _pyexpat is not None:
    EXPAT_VERSION: str = _pyexpat.EXPAT_VERSION  # type: ignore[assignment]
    XML_PARAM_ENTITY_PARSING_ALWAYS: int = (
        _pyexpat.XML_PARAM_ENTITY_PARSING_ALWAYS  # type: ignore[assignment]
    )
    XML_PARAM_ENTITY_PARSING_NEVER: int = (
        _pyexpat.XML_PARAM_ENTITY_PARSING_NEVER  # type: ignore[assignment]
    )
    XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE: int = (
        _pyexpat.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE  # type: ignore[assignment]
    )
    ExpatError = _pyexpat.ExpatError  # type: ignore[assignment]
else:
    EXPAT_VERSION: str = ""  # type: ignore[no-redef]
    XML_PARAM_ENTITY_PARSING_ALWAYS: int = 0  # type: ignore[no-redef]
    XML_PARAM_ENTITY_PARSING_NEVER: int = 0  # type: ignore[no-redef]
    XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE: int = 0  # type: ignore[no-redef]

    class ExpatError(Exception):  # type: ignore[no-redef]
        """The error of the expat parser (unavailable when pyexpat is missing)."""


def ParserCreate(*args: Any, **kwargs: Any) -> Any:
    """Create a parser with the options of expat behind one validated call.

    Args:
        *args: Positional arguments forwarded to :func:`pyexpat.ParserCreate`.
        **kwargs: Keyword arguments forwarded to :func:`pyexpat.ParserCreate`.

    Returns:
        A new parser created by the standard library.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    return _pyexpat_module().ParserCreate(*args, **kwargs)


__all__: List[str] = [
    "CurrentPosition",
    "EXPAT_VERSION",
    "ElementAttributes",
    "ErrorPosition",
    "ExpatError",
    "ParserCreate",
    "XML_PARAM_ENTITY_PARSING_ALWAYS",
    "XML_PARAM_ENTITY_PARSING_NEVER",
    "XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE",
    "attribute_mapping",
    "create_parser",
    "current_position",
    "error_position",
    "error_string",
    "external_entity_parser",
    "get_base",
    "is_available",
    "parse",
    "parse_file",
    "parse_text",
    "set_base",
    "set_character_data_handler",
    "set_element_handlers",
    "set_end_element_handler",
    "set_param_entity_parsing",
    "set_processing_instruction_handler",
    "set_start_element_handler",
    "version_info",
]


def _pyexpat_module() -> Any:
    """Return the standard library ``pyexpat`` module.

    Returns:
        The imported :mod:`pyexpat` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    if _pyexpat is None:  # pragma: no cover - pyexpat ships with every CPython
        raise RuntimeError(
            "the standard library module 'pyexpat' is not available on this interpreter"
        )
    return _pyexpat


def _require_bool(value: Any, name: str) -> bool:
    """Return *value* as a boolean, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a boolean.

    Raises:
        TypeError: If *value* is not a boolean.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as text.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_path(value: Any, name: str) -> str:
    """Return *value* as the path of a file.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The path as text.

    Raises:
        TypeError: If *value* is neither a string nor a path.
        ValueError: If *value* is an empty path.
    """
    if not isinstance(value, (str, os.PathLike)):
        raise TypeError(f"{name} must be a path, got {type(value).__name__}")
    text = os.fspath(value)
    if not isinstance(text, str):
        raise TypeError(f"{name} must be a text path, got {type(value).__name__}")
    if not text:
        raise ValueError(f"{name} must not be empty")
    return text


def _require_count(value: Any, name: str = "count") -> int:
    """Return *value* as a non-negative integer.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as an integer.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def _require_handler(
    value: Any, name: str
) -> Optional[Callable[..., Any]]:
    """Return *value* as a handler of the parser.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The handler, or ``None`` when the handler is removed.

    Raises:
        TypeError: If *value* is neither ``None`` nor callable.
    """
    if value is None:
        return None
    if not callable(value):
        raise TypeError(f"{name} must be callable or None, got {type(value).__name__}")
    return cast(Callable[..., Any], value)


def is_available() -> bool:
    """Report whether the interpreter ships the :mod:`pyexpat` module.

    Returns:
        True when the standard library module is importable, False otherwise.
    """
    return _pyexpat is not None


def version_info() -> Tuple[int, ...]:
    """Return the version of the expat library.

    Returns:
        The version of the expat library as a tuple of integers.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    info = _pyexpat_module().version_info
    return tuple(int(part) for part in info)


def error_string(code: Any) -> str:
    """Return the text that describes the error code *code*.

    Args:
        code: The error code returned by the parser.

    Returns:
        The text that describes the error.

    Raises:
        TypeError: If *code* is not an integer.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    number = _require_count(code, "code")
    return str(_pyexpat_module().ErrorString(number))


def create_parser(
    namespace_prefixes: bool = False,
    ordered_attributes: bool = False,
    specified_attributes: bool = False,
    buffer_size: int = 8192,
) -> Any:
    """Create a parser with the options of expat behind one validated call.

    The parser is ready to parse documents once it is configured with the
    handlers of the caller.

    Args:
        namespace_prefixes: Whether the parser reports the namespace prefixes
            of the element and attribute names.
        ordered_attributes: Whether the parser reports the attributes of an
            element in the order they appear in the document.
        specified_attributes: Whether the parser reports only the attributes
            that are specified in the document.
        buffer_size: The size of the buffer the parser uses.

    Returns:
        A parser ready to be configured and to parse documents.

    Raises:
        TypeError: If an option has the wrong type.
        ValueError: If *buffer_size* is not positive.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    parser = _pyexpat_module().ParserCreate()
    parser.namespace_prefixes = _require_bool(namespace_prefixes, "namespace_prefixes")
    parser.ordered_attributes = _require_bool(ordered_attributes, "ordered_attributes")
    parser.specified_attributes = _require_bool(specified_attributes, "specified_attributes")
    size = _require_count(buffer_size, "buffer_size")
    if size == 0:
        raise ValueError("buffer_size must be positive, got 0")
    parser.buffer_size = size
    return parser


def parse(parser: Any, data: Any, is_final: bool = True) -> int:
    """Parse the document *data* with *parser*.

    Args:
        parser: The parser to parse with.
        data: The document as text.
        is_final: Whether *data* is the last piece of the document.

    Returns:
        The result of the parse call of the standard library.

    Raises:
        TypeError: If *data* is not a string.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
        ExpatError: If the document is not well-formed.
    """
    text = _require_text(data, "data")
    final = _require_bool(is_final, "is_final")
    return parser.Parse(text, final)  # type: ignore[no-any-return]


def parse_text(parser: Any, text: Any) -> int:
    """Parse the document *text* with *parser*.

    The whole document is parsed in one call, so *is_final* is ``True``.

    Args:
        parser: The parser to parse with.
        text: The document as text.

    Returns:
        The result of the parse call of the standard library.

    Raises:
        TypeError: If *text* is not a string.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
        ExpatError: If the document is not well-formed.
    """
    return parse(parser, text, True)


def parse_file(parser: Any, filename: Any) -> int:
    """Parse the document in the file *filename* with *parser*.

    The file is opened by the helper, so a caller never has to open it
    themselves.

    Args:
        parser: The parser to parse with.
        filename: The path of the file that holds the document.

    Returns:
        The result of the parse call of the standard library.

    Raises:
        TypeError: If *filename* is not a path.
        ValueError: If *filename* is an empty path.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
        OSError: If the file cannot be opened.
        ExpatError: If the document is not well-formed.
    """
    path = _require_path(filename, "filename")
    with open(path, "rb") as handle:
        return parser.ParseFile(handle)  # type: ignore[no-any-return]


def set_base(parser: Any, base: Any) -> str:
    """Set the base of the parser and return it.

    The base is used to resolve relative paths of external entities.

    Args:
        parser: The parser to configure.
        base: The base as text.

    Returns:
        The base that was set.

    Raises:
        TypeError: If *base* is not a string.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    text = _require_text(base, "base")
    parser.SetBase(text)
    return text


def get_base(parser: Any) -> Optional[str]:
    """Return the base of the parser.

    Args:
        parser: The parser to inspect.

    Returns:
        The base of the parser, or ``None`` when no base is set.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    base = parser.GetBase()
    return None if base is None else str(base)


def set_param_entity_parsing(parser: Any, parsing: Any) -> int:
    """Set the parameter entity parsing of *parser* and return the previous value.

    Args:
        parser: The parser to configure.
        parsing: One of the ``XML_PARAM_ENTITY_PARSING_*`` constants.

    Returns:
        The previous value of the parameter entity parsing.

    Raises:
        TypeError: If *parsing* is not an integer.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    value = _require_count(parsing, "parsing")
    return int(parser.SetParamEntityParsing(value))


def external_entity_parser(parser: Any, encoding: Any = "") -> Any:
    """Return a parser for the external entity with *encoding*.

    Args:
        parser: The parser to create the external entity parser from.
        encoding: The encoding of the external entity.

    Returns:
        A parser for the external entity.

    Raises:
        TypeError: If *encoding* is not a string.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    text = _require_text(encoding, "encoding")
    return parser.ExternalEntityParserCreate(text)


def set_start_element_handler(parser: Any, handler: Any) -> None:
    """Set the handler that is called when an element starts.

    The handler is called with the name of the element and the mapping of its
    attributes.  Passing ``None`` removes the handler.

    Args:
        parser: The parser to configure.
        handler: The handler, or ``None``.

    Raises:
        TypeError: If *handler* is neither ``None`` nor callable.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    func = _require_handler(handler, "handler")
    parser.StartElementHandler = func


def set_end_element_handler(parser: Any, handler: Any) -> None:
    """Set the handler that is called when an element ends.

    The handler is called with the name of the element.  Passing ``None``
    removes the handler.

    Args:
        parser: The parser to configure.
        handler: The handler, or ``None``.

    Raises:
        TypeError: If *handler* is neither ``None`` nor callable.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    func = _require_handler(handler, "handler")
    parser.EndElementHandler = func


def set_element_handlers(
    parser: Any, start_handler: Any, end_handler: Any
) -> None:
    """Set the handlers that are called when an element starts and ends.

    Args:
        parser: The parser to configure.
        start_handler: The handler for the start of an element, or ``None``.
        end_handler: The handler for the end of an element, or ``None``.

    Raises:
        TypeError: If a handler is neither ``None`` nor callable.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    set_start_element_handler(parser, start_handler)
    set_end_element_handler(parser, end_handler)


def set_character_data_handler(parser: Any, handler: Any) -> None:
    """Set the handler that is called with the character data of an element.

    The handler is called with the text.  Passing ``None`` removes the handler.

    Args:
        parser: The parser to configure.
        handler: The handler, or ``None``.

    Raises:
        TypeError: If *handler* is neither ``None`` nor callable.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    func = _require_handler(handler, "handler")
    parser.CharacterDataHandler = func


def set_processing_instruction_handler(parser: Any, handler: Any) -> None:
    """Set the handler that is called with a processing instruction.

    The handler is called with the target and the data of the instruction.
    Passing ``None`` removes the handler.

    Args:
        parser: The parser to configure.
        handler: The handler, or ``None``.

    Raises:
        TypeError: If *handler* is neither ``None`` nor callable.
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    func = _require_handler(handler, "handler")
    parser.ProcessingInstructionHandler = func


def error_position(parser: Any) -> ErrorPosition:
    """Return the position of the last error of *parser* as one record.

    The standard library reports the position of an error with three separate
    attributes.  The wrapper returns them as one record.

    Args:
        parser: The parser to inspect.

    Returns:
        The position of the last error.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    return ErrorPosition(
        line=int(parser.ErrorLineNumber),
        column=int(parser.ErrorColumnNumber),
        code=int(parser.ErrorCode),
        byte_index=int(parser.ErrorByteIndex),
    )


def current_position(parser: Any) -> CurrentPosition:
    """Return the current position of *parser* as one record.

    Args:
        parser: The parser to inspect.

    Returns:
        The current position of the parser.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pyexpat`` module.
    """
    return CurrentPosition(
        byte_index=int(parser.CurrentByteIndex),
        line_number=int(parser.CurrentLineNumber),
        column_number=int(parser.CurrentColumnNumber),
    )


def attribute_mapping(attributes: Any) -> ElementAttributes:
    """Return the attributes of an element as a mapping.

    The standard library already reports the attributes as a mapping, but a
    caller can use this helper to normalize the value into a plain dictionary.

    Args:
        attributes: The attributes of an element.

    Returns:
        The attributes as a mapping from names to values.

    Raises:
        TypeError: If *attributes* is not a mapping.
    """
    if not isinstance(attributes, Mapping):
        raise TypeError(
            f"attributes must be a mapping, got {type(attributes).__name__}"
        )
    return {str(key): str(value) for key, value in attributes.items()}
