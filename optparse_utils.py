"""Command-line option parsing utilities wrapping the standard library :mod:`optparse`.

The :mod:`optparse` module implements the venerable GNU-style command-line
parser.  It predates :mod:`argparse`, is not deprecated, and is still the parser
of choice for tools that want the classic ``-f value`` / ``--file=value``
behaviour without the argparse defaults.

This wrapper exposes validated helpers around the standard library classes.  The
helpers never touch the network, never spawn a process, and never modify the
interpreter state, so they are safe to use from a test suite.

The two conveniences the standard library does not offer are:

* **Validated arguments.**  Every helper checks the types of its arguments and
  raises :class:`TypeError` or :class:`ValueError` before the standard library
  is reached, instead of failing with a less specific error later on.
* **Errors as exceptions.**  The standard library prints a usage message and
  terminates the interpreter when the command line cannot be parsed.  The
  :func:`parse_args` helper can be told to raise :class:`OptionParseError`
  instead, which keeps a failed parse from tearing down the caller.

.. note::

   The standard library is used as the single source of truth: the wrapper never
   re-implements the parsing rules, it only validates the input and, when
   asked, converts the standard library's :class:`SystemExit` into an
   :class:`OptionError`.
"""

from __future__ import annotations

import inspect
import io
import optparse
from contextlib import redirect_stderr
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

__all__ = [
    "BadOptionError",
    "Option",
    "OptionConflictError",
    "OptionContainer",
    "OptionError",
    "OptionGroup",
    "OptionParseError",
    "OptionParser",
    "OptionValueError",
    "SUPPRESS_HELP",
    "SUPPRESS_USAGE",
    "Values",
    "add_count_option",
    "add_flag",
    "add_option",
    "add_option_group",
    "choice_type",
    "dest_for",
    "float_type",
    "format_help",
    "format_option_help",
    "format_usage",
    "get_default_values",
    "get_option",
    "get_prog_name",
    "get_usage",
    "has_option",
    "int_type",
    "make_parser",
    "parse_args",
    "remove_option",
    "set_defaults",
    "string_type",
    "values_to_dict",
]

#: The standard library parser re-exported for convenience.
OptionParser = optparse.OptionParser

#: The standard library option container re-exported for convenience.
OptionContainer = optparse.OptionContainer

#: The standard library option group re-exported for convenience.
OptionGroup = optparse.OptionGroup

#: The standard library option re-exported for convenience.
Option = optparse.Option

#: The standard library parsed values re-exported for convenience.
Values = optparse.Values

#: The standard library option error re-exported for convenience.
OptionError = optparse.OptionError

#: The standard library option value error re-exported for convenience.
OptionValueError = optparse.OptionValueError

#: The standard library option conflict error re-exported for convenience.
OptionConflictError = optparse.OptionConflictError

#: The standard library bad option error re-exported for convenience.
BadOptionError = optparse.BadOptionError


class OptionParseError(OptionError):
    """Raised when a command line cannot be parsed.

    The standard library reports a failed parse by printing a usage message
    and terminating the interpreter.  This error carries the same message but
    keeps the program alive, and it derives from :class:`optparse.OptionError`
    so that ``except OptionError`` still catches it.
    """

    def __init__(self, message: str) -> None:
        """Store *message* as the error message.

        Args:
            message: The message describing why the command line was rejected.
        """
        self.msg = message
        self.option = None
        self.option_id = ""
        Exception.__init__(self, message)

    def __str__(self) -> str:
        """Return the message without the option prefix."""
        return self.msg

#: Hide an option from the generated help text.
SUPPRESS_HELP = optparse.SUPPRESS_HELP

#: Hide the usage line from the generated help text.
SUPPRESS_USAGE = optparse.SUPPRESS_USAGE

#: A converter that turns the raw string of an option into a value.
TypeConverter = Callable[[str], Any]

#: The supported values of the ``on_error`` argument of :func:`parse_args`.
ERROR_MODES = ("exit", "raise")


class _Unset:
    """Sentinel marking an argument that was not supplied by the caller."""

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return "<unset>"

    def __bool__(self) -> bool:
        return False


#: Marker for arguments that were not supplied.
UNSET = _Unset()


def _require_parser(parser: Any) -> OptionParser:
    """Return *parser* when it is an :class:`optparse.OptionParser`.

    Args:
        parser: The object to check.

    Returns:
        The validated parser.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser`.
    """
    if not isinstance(parser, OptionParser):
        raise TypeError(
            f"parser must be an optparse.OptionParser, got {type(parser).__name__}"
        )
    return parser


def _require_container(container: Any) -> OptionContainer:
    """Return *container* when it can hold options.

    Both :class:`optparse.OptionParser` and :class:`optparse.OptionGroup`
    derive from :class:`optparse.OptionContainer`, which is the class that
    actually implements :meth:`~optparse.OptionContainer.add_option`.

    Args:
        container: The object to check.

    Returns:
        The validated container.

    Raises:
        TypeError: If *container* cannot hold options.
    """
    if not isinstance(container, OptionContainer):
        raise TypeError(
            "container must be an optparse.OptionParser or an optparse.OptionGroup, "
            f"got {type(container).__name__}"
        )
    return container


def _require_optional_str(name: str, value: Optional[str]) -> Optional[str]:
    """Return *value* when it is a string or ``None``.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated value.

    Raises:
        TypeError: If *value* is neither a string nor ``None``.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    return value


def _require_str(name: str, value: Any) -> str:
    """Return *value* when it is a string.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated value.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _validate_flags(flags: Sequence[str]) -> List[str]:
    """Return the option strings of *flags* after checking them.

    The rules are the ones the standard library applies: a short option string
    is a dash followed by a single non-dash character, and a long option string
    is two dashes followed by a non-dash character.

    Args:
        flags: The option strings to check.

    Returns:
        The validated option strings.

    Raises:
        TypeError: If an option string is not a string.
        ValueError: If no option string was given or an option string is
            malformed.
    """
    if not flags:
        raise ValueError("at least one option string must be supplied")
    validated: List[str] = []
    for flag in flags:
        if not isinstance(flag, str):
            raise TypeError(f"option strings must be str, got {type(flag).__name__}")
        if len(flag) < 2:
            raise ValueError(
                f"invalid option string {flag!r}: must be at least two characters long"
            )
        if len(flag) == 2:
            if flag[0] != "-" or flag[1] == "-":
                raise ValueError(
                    f"invalid short option string {flag!r}: must be of the form -x"
                )
        elif not flag.startswith("--") or flag[2] == "-":
            raise ValueError(
                f"invalid long option string {flag!r}: must start with -- "
                "followed by a non-dash character"
            )
        validated.append(flag)
    return validated


def _validate_choices(choices: Sequence[str]) -> List[str]:
    """Return *choices* as a list of strings.

    Args:
        choices: The accepted values.

    Returns:
        The validated choices.

    Raises:
        TypeError: If *choices* is a string or contains a non-string entry.
        ValueError: If *choices* is empty.
    """
    if isinstance(choices, (str, bytes)):
        raise TypeError("choices must be a sequence of strings, not a single string")
    try:
        entries = list(choices)
    except TypeError as exc:
        raise TypeError(
            f"choices must be an iterable of strings, got {type(choices).__name__}"
        ) from exc
    if not entries:
        raise ValueError("choices must not be empty")
    for entry in entries:
        if not isinstance(entry, str):
            raise TypeError(f"choices entries must be str, got {type(entry).__name__}")
    return entries


def _type_converter(converter: Callable[..., Any]) -> Callable[..., Any]:
    """Return *converter* in the calling convention the standard library expects.

    The standard library calls a custom converter with three arguments
    ``(option, opt, value)``.  A converter that takes a single value, such as
    :func:`int`, is adapted so that it can be used as an option type.

    Args:
        converter: The converter to adapt.

    Returns:
        A callable that follows the standard library calling convention.
    """
    try:
        signature = inspect.signature(converter)
    except (TypeError, ValueError):  # pragma: no cover - builtins without signature
        signature = None
    if signature is not None:
        parameters = list(signature.parameters.values())
        positional = [
            parameter
            for parameter in parameters
            if parameter.kind in (parameter.POSITIONAL_ONLY, parameter.POSITIONAL_OR_KEYWORD)
        ]
        variadic = any(
            parameter.kind is parameter.VAR_POSITIONAL for parameter in parameters
        )
        if variadic or len(positional) >= 3:
            return converter

    def _convert(option: Option, opt: str, value: str) -> Any:
        return converter(value)

    return _convert


def _install_converter(option: Option, converter: Callable[..., Any]) -> None:
    """Make *option* convert its raw value with *converter*.

    The standard library only knows a fixed set of option types, so a custom
    converter is installed on the option itself: the option keeps the string
    type of the standard library and the converter takes over the conversion.

    Args:
        option: The option to change.
        converter: The converter, in the calling convention of the standard
            library.
    """

    def _check_value(opt: str, value: str) -> Any:
        return converter(option, opt, value)

    setattr(option, "check_value", _check_value)


def _normalize_type(type_: Optional[Union[str, Callable[..., Any]]]) -> Optional[str]:
    """Return the option type the standard library understands.

    Args:
        type_: The requested type: a name such as ``"int"``, a type such as
            :class:`int`, or a callable that converts the raw string.

    Returns:
        The type name understood by the standard library, or ``None`` when a
        callable was given.

    Raises:
        TypeError: If *type_* is neither a string, a type, nor a callable.
        ValueError: If *type_* names an unsupported type.
    """
    if type_ is None:
        return None
    if isinstance(type_, str):
        name = "string" if type_ == "str" else type_
        if name not in Option.TYPES:
            raise ValueError(f"invalid option type: {type_!r}")
        return name
    if isinstance(type_, type):
        name = "string" if type_.__name__ == "str" else type_.__name__
        if name not in Option.TYPES:
            raise ValueError(f"unsupported option type: {type_.__name__!r}")
        return name
    if callable(type_):
        return None
    raise TypeError(
        "type must be a str, a type, or a callable, "
        f"got {type(type_).__name__}"
    )


def make_parser(
    usage: Optional[str] = None,
    description: Optional[str] = None,
    prog: Optional[str] = None,
    version: Optional[str] = None,
    epilog: Optional[str] = None,
    add_help_option: bool = True,
    conflict_handler: str = "error",
) -> OptionParser:
    """Create an :class:`optparse.OptionParser` with validated arguments.

    Args:
        usage: The usage line of the program.
        description: The description shown in the help text.
        prog: The name of the program; defaults to the interpreter's script name.
        version: The version string; when given, a ``--version`` option is added.
        epilog: The text shown after the options in the help text.
        add_help_option: Whether the parser accepts ``-h`` and ``--help``.
        conflict_handler: Either ``"error"`` or ``"resolve"``.

    Returns:
        The new parser.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *conflict_handler* is not a supported handler.
    """
    _require_optional_str("usage", usage)
    _require_optional_str("description", description)
    _require_optional_str("prog", prog)
    _require_optional_str("version", version)
    _require_optional_str("epilog", epilog)
    if not isinstance(add_help_option, bool):
        raise TypeError(
            f"add_help_option must be a bool, got {type(add_help_option).__name__}"
        )
    if conflict_handler not in ("error", "resolve"):
        raise ValueError(
            f"invalid conflict handler: {conflict_handler!r}, expected 'error' or 'resolve'"
        )
    return OptionParser(
        usage=usage,
        description=description,
        prog=prog,
        version=version,
        epilog=epilog,
        add_help_option=add_help_option,
        conflict_handler=conflict_handler,
    )


def add_option(
    container: OptionContainer,
    *flags: str,
    action: str = "store",
    dest: Optional[str] = None,
    type_: Optional[Union[str, Callable[..., Any]]] = None,
    default: Any = UNSET,
    help_text: Optional[str] = None,
    metavar: Optional[str] = None,
    choices: Optional[Sequence[str]] = None,
    nargs: Optional[int] = None,
    const: Any = UNSET,
) -> Option:
    """Add an option to a parser or to an option group.

    Args:
        container: The parser or the option group the option belongs to.
        flags: The option strings, for example ``"--file"`` or ``"-f"``.
        action: The action the option performs.
        dest: The attribute the parsed value is stored in; the standard library
            derives it from the option strings when omitted.
        type_: The type of the value: a name such as ``"int"``, a type such as
            :class:`int`, or a callable that converts the raw string.
        default: The value used when the option is not given.
        help_text: The help text of the option.
        metavar: The placeholder shown in the help text.
        choices: The accepted values; implies the ``"choice"`` type.
        nargs: The number of values the option consumes.
        const: The value used by the ``"store_const"`` and ``"append_const"``
            actions.

    Returns:
        The newly created option.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an argument has an unsupported value.
        OptionError: If the standard library rejects the combination of
            arguments.
    """
    target = _require_container(container)
    option_strings = _validate_flags(flags)
    _require_str("action", action)
    if action not in Option.ACTIONS:
        raise ValueError(f"invalid action: {action!r}")
    _require_optional_str("dest", dest)
    _require_optional_str("help_text", help_text)
    _require_optional_str("metavar", metavar)
    if nargs is not None:
        if isinstance(nargs, bool) or not isinstance(nargs, int):
            raise TypeError(f"nargs must be an int or None, got {type(nargs).__name__}")
        if nargs < 0:
            raise ValueError("nargs must not be negative")
    normalized_type = _normalize_type(type_)
    converter: Optional[Callable[..., Any]] = None
    if type_ is not None and not isinstance(type_, (str, type)) and callable(type_):
        converter = _type_converter(type_)
    if choices is not None:
        choice_list = _validate_choices(choices)
        normalized_type = "choice"
    else:
        choice_list = None
    if normalized_type == "choice" and choice_list is None:
        raise ValueError("must supply a list of choices for type 'choice'")

    attrs: Dict[str, Any] = {"action": action}
    if dest is not None:
        attrs["dest"] = dest
    if normalized_type is not None:
        attrs["type"] = normalized_type
    if default is not UNSET:
        attrs["default"] = default
    if help_text is not None:
        attrs["help"] = help_text
    if metavar is not None:
        attrs["metavar"] = metavar
    if choice_list is not None:
        attrs["choices"] = choice_list
    if nargs is not None:
        attrs["nargs"] = nargs
    if const is not UNSET:
        attrs["const"] = const
    option = target.add_option(*option_strings, **attrs)
    if converter is not None:
        _install_converter(option, converter)
    return option


def add_flag(
    container: OptionContainer,
    *flags: str,
    dest: Optional[str] = None,
    help_text: Optional[str] = None,
    default: bool = False,
) -> Option:
    """Add a boolean flag to a parser or to an option group.

    A flag with a default of ``False`` stores ``True`` when it is given, and a
    flag with a default of ``True`` stores ``False`` when it is given.

    Args:
        container: The parser or the option group the option belongs to.
        flags: The option strings of the flag.
        dest: The attribute the parsed value is stored in.
        help_text: The help text of the flag.
        default: The value used when the flag is not given.

    Returns:
        The newly created option.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an option string is malformed.
    """
    if not isinstance(default, bool):
        raise TypeError(f"default must be a bool, got {type(default).__name__}")
    action = "store_false" if default else "store_true"
    return add_option(
        container,
        *flags,
        action=action,
        dest=dest,
        default=default,
        help_text=help_text,
    )


def add_count_option(
    container: OptionContainer,
    *flags: str,
    dest: Optional[str] = None,
    help_text: Optional[str] = None,
) -> Option:
    """Add an option that counts how often it is given.

    Args:
        container: The parser or the option group the option belongs to.
        flags: The option strings of the option.
        dest: The attribute the parsed value is stored in.
        help_text: The help text of the option.

    Returns:
        The newly created option.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an option string is malformed.
    """
    return add_option(
        container,
        *flags,
        action="count",
        dest=dest,
        default=0,
        help_text=help_text,
    )


def add_option_group(
    parser: OptionParser,
    title: str,
    description: Optional[str] = None,
) -> OptionGroup:
    """Add an option group to a parser.

    Args:
        parser: The parser the group belongs to.
        title: The heading of the group in the help text.
        description: The description of the group in the help text.

    Returns:
        The newly created group.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    target = _require_parser(parser)
    _require_str("title", title)
    _require_optional_str("description", description)
    return target.add_option_group(title, description=description)


def _validate_args(args: Optional[Sequence[str]]) -> Optional[List[str]]:
    """Return *args* as a list of strings.

    Args:
        args: The command line to parse, or ``None`` to use :data:`sys.argv`.

    Returns:
        The validated command line, or ``None`` when the interpreter's own
        command line should be used.

    Raises:
        TypeError: If *args* is a string or contains a non-string entry.
    """
    if args is None:
        return None
    if isinstance(args, (str, bytes)):
        raise TypeError("args must be a sequence of strings, not a single string")
    try:
        entries = list(args)
    except TypeError as exc:
        raise TypeError(
            f"args must be a sequence of strings, got {type(args).__name__}"
        ) from exc
    for entry in entries:
        if not isinstance(entry, str):
            raise TypeError(f"args entries must be str, got {type(entry).__name__}")
    return entries


def parse_args(
    parser: OptionParser,
    args: Optional[Sequence[str]] = None,
    *,
    on_error: str = "exit",
) -> Tuple[Values, List[str]]:
    """Parse a command line with *parser*.

    Args:
        parser: The parser that reads the command line.
        args: The command line to parse, or ``None`` to use :data:`sys.argv`.
        on_error: Either ``"exit"``, which keeps the standard library behaviour
            of printing a usage message and terminating the interpreter, or
            ``"raise"``, which raises :class:`OptionParseError` instead.

    Returns:
        A tuple of the parsed values and the remaining arguments.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *on_error* is not a supported mode.
        OptionParseError: If the command line is invalid and *on_error* is
            ``"raise"``.
        SystemExit: If the command line is invalid and *on_error* is ``"exit"``,
            or when ``--help`` or ``--version`` is requested.
    """
    target = _require_parser(parser)
    if on_error not in ERROR_MODES:
        raise ValueError(
            f"invalid error mode: {on_error!r}, expected 'exit' or 'raise'"
        )
    command_line = _validate_args(args)
    if on_error == "exit":
        options, remaining = target.parse_args(command_line)
        return options, remaining
    buffer = io.StringIO()
    try:
        with redirect_stderr(buffer):
            options, remaining = target.parse_args(command_line)
    except SystemExit as exc:
        status = exc.code if isinstance(exc.code, int) else 1
        if status == 0:
            raise
        message = buffer.getvalue().strip()
        raise OptionParseError(
            message or f"option parsing failed with status {status}"
        ) from exc
    return options, remaining


def get_option(parser: OptionParser, option_string: str) -> Optional[Option]:
    """Return the option registered under *option_string*.

    Args:
        parser: The parser to search.
        option_string: The option string, for example ``"--file"``.

    Returns:
        The option, or ``None`` when the parser does not know it.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *option_string* is malformed.
    """
    target = _require_parser(parser)
    _require_str("option_string", option_string)
    if len(option_string) < 2 or not option_string.startswith("-"):
        raise ValueError(
            f"invalid option string {option_string!r}: must start with a dash"
        )
    return target.get_option(option_string)


def has_option(parser: OptionParser, option_string: str) -> bool:
    """Report whether *parser* knows *option_string*.

    Args:
        parser: The parser to search.
        option_string: The option string, for example ``"--file"``.

    Returns:
        ``True`` when the option is registered, ``False`` otherwise.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *option_string* is malformed.
    """
    target = _require_parser(parser)
    _require_str("option_string", option_string)
    if len(option_string) < 2 or not option_string.startswith("-"):
        raise ValueError(
            f"invalid option string {option_string!r}: must start with a dash"
        )
    return target.has_option(option_string)


def remove_option(parser: OptionParser, option_string: str) -> None:
    """Remove the option registered under *option_string*.

    Args:
        parser: The parser to change.
        option_string: The option string, for example ``"--file"``.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If the option string is malformed or unknown.
    """
    target = _require_parser(parser)
    _require_str("option_string", option_string)
    if len(option_string) < 2 or not option_string.startswith("-"):
        raise ValueError(
            f"invalid option string {option_string!r}: must start with a dash"
        )
    target.remove_option(option_string)


def get_default_values(parser: OptionParser) -> Values:
    """Return the default values of *parser*.

    Args:
        parser: The parser to read.

    Returns:
        The values every option falls back to.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser`.
    """
    target = _require_parser(parser)
    return target.get_default_values()


def set_defaults(parser: OptionParser, **defaults: Any) -> None:
    """Set the default values of *parser*.

    Args:
        parser: The parser to change.
        **defaults: The default values, keyed by destination attribute.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser` or a
            default name is not a string.
    """
    target = _require_parser(parser)
    for name in defaults:
        _require_str("default name", name)
    target.set_defaults(**defaults)


def get_usage(parser: OptionParser) -> str:
    """Return the usage line of *parser*.

    Args:
        parser: The parser to read.

    Returns:
        The usage line.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser`.
    """
    target = _require_parser(parser)
    return target.get_usage()


def format_usage(parser: OptionParser) -> str:
    """Return the formatted usage line of *parser*.

    The standard library formats the usage line in :func:`get_usage`; this
    helper is an alias that keeps the naming of the other helpers symmetric.

    Args:
        parser: The parser to read.

    Returns:
        The formatted usage line.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser`.
    """
    target = _require_parser(parser)
    return target.get_usage()


def format_help(parser: OptionParser) -> str:
    """Return the help text of *parser*.

    Args:
        parser: The parser to read.

    Returns:
        The formatted help text.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser`.
    """
    target = _require_parser(parser)
    return target.format_help()


def format_option_help(parser: OptionParser, option: Option) -> str:
    """Return the help text of a single option.

    Args:
        parser: The parser that owns the option.
        option: The option to describe.

    Returns:
        The formatted help text of the option.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    target = _require_parser(parser)
    if not isinstance(option, Option):
        raise TypeError(f"option must be an optparse.Option, got {type(option).__name__}")
    target.format_option_help()
    return target.formatter.format_option(option)


def get_prog_name(parser: OptionParser) -> str:
    """Return the program name *parser* uses in its help text.

    Args:
        parser: The parser to read.

    Returns:
        The program name.

    Raises:
        TypeError: If *parser* is not an :class:`optparse.OptionParser`.
    """
    target = _require_parser(parser)
    return target.get_prog_name()


def dest_for(*flags: str) -> str:
    """Return the destination attribute the standard library derives from *flags*.

    The standard library uses the first long option string, or the first short
    option string when there is none, strips the leading dashes, and replaces
    the remaining dashes with underscores.

    Args:
        flags: The option strings of an option.

    Returns:
        The destination attribute.

    Raises:
        TypeError: If an option string is not a string.
        ValueError: If no option string was given or an option string is
            malformed.
    """
    option_strings = _validate_flags(flags)
    long_options = [flag for flag in option_strings if flag.startswith("--")]
    short_options = [flag for flag in option_strings if not flag.startswith("--")]
    if long_options:
        dest = long_options[0][2:]
    else:
        dest = short_options[0][1:]
    return dest.replace("-", "_")


def string_type(value: str) -> str:
    """Return *value* unchanged.

    Args:
        value: The raw string of an option.

    Returns:
        The same string.

    Raises:
        TypeError: If *value* is not a string.
    """
    return _require_str("value", value)


def int_type(value: str) -> int:
    """Convert *value* to an integer.

    Args:
        value: The raw string of an option.

    Returns:
        The integer the string holds.

    Raises:
        TypeError: If *value* is not a string.
        OptionValueError: If *value* is not a valid integer.
    """
    text = _require_str("value", value)
    try:
        return int(text)
    except ValueError as exc:
        raise OptionValueError(f"invalid integer value: {value!r}") from exc


def float_type(value: str) -> float:
    """Convert *value* to a float.

    Args:
        value: The raw string of an option.

    Returns:
        The float the string holds.

    Raises:
        TypeError: If *value* is not a string.
        OptionValueError: If *value* is not a valid float.
    """
    text = _require_str("value", value)
    try:
        return float(text)
    except ValueError as exc:
        raise OptionValueError(f"invalid float value: {value!r}") from exc


def choice_type(choices: Sequence[str]) -> TypeConverter:
    """Return a converter that only accepts one of *choices*.

    Args:
        choices: The accepted values.

    Returns:
        A converter that raises :class:`OptionValueError` for any other value.

    Raises:
        TypeError: If *choices* is a string or contains a non-string entry.
        ValueError: If *choices* is empty.
    """
    accepted = _validate_choices(choices)

    def _convert(value: str) -> str:
        text = _require_str("value", value)
        if text not in accepted:
            listed = ", ".join(repr(choice) for choice in accepted)
            raise OptionValueError(f"invalid choice: {value!r} (choose from {listed})")
        return text

    return _convert


def values_to_dict(options: Values) -> Dict[str, Any]:
    """Return the parsed values as a plain dictionary.

    Args:
        options: The values returned by :func:`parse_args`.

    Returns:
        A dictionary of the parsed values.

    Raises:
        TypeError: If *options* is not an :class:`optparse.Values` instance.
    """
    if not isinstance(options, Values):
        raise TypeError(f"options must be an optparse.Values, got {type(options).__name__}")
    return dict(vars(options))
