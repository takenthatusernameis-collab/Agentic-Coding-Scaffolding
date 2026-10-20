"""IMAP4 client utilities (wrapping :mod:`imaplib`).

The :mod:`imaplib` module defines three classes, ``IMAP4``, ``IMAP4_SSL`` and
``IMAP4_stream``, which encapsulate a connection to an IMAP4 server and
implement a large subset of the IMAP4rev1 client commands. It also exposes a
handful of module level helpers that translate between IMAP4 wire formats and
Python values.

This wrapper exposes validated constructors for the client classes plus the
pure helpers used to parse and format capability lists, message flags and
``INTERNALDATE`` timestamps. The connection helpers only build the standard
library clients; they never open a socket on their own, so callers stay in
control of when (and if) a connection is attempted.
"""

from __future__ import annotations

import imaplib as _imaplib
import re
import time
from datetime import datetime
from typing import Any, Iterable, List, Optional, Sequence, Tuple, Union

__all__ = [
    "CRLF",
    "IMAP4",
    "IMAP4_SSL",
    "IMAP4_SSL_PORT",
    "IMAP4_PORT",
    "IMAP4_stream",
    "IMAP4AbortError",
    "IMAP4Error",
    "IMAP4ReadOnlyError",
    "create_imap4",
    "create_imap4_ssl",
    "create_imap4_stream",
    "format_flags",
    "format_internaldate",
    "has_capability",
    "int_to_ap",
    "is_imap4_abort",
    "is_imap4_error",
    "is_imap4_readonly",
    "parse_capabilities",
    "parse_fetch_flags",
    "parse_flags",
    "parse_internaldate",
]

CRLF: bytes = _imaplib.CRLF  # type: ignore[attr-defined]
IMAP4_PORT: int = _imaplib.IMAP4_PORT  # type: ignore[attr-defined]
IMAP4_SSL_PORT: int = _imaplib.IMAP4_SSL_PORT  # type: ignore[attr-defined]

IMAP4 = _imaplib.IMAP4
IMAP4_SSL = _imaplib.IMAP4_SSL
IMAP4_stream = _imaplib.IMAP4_stream

IMAP4Error = _imaplib.IMAP4.error
IMAP4AbortError = _imaplib.IMAP4.abort
IMAP4ReadOnlyError = _imaplib.IMAP4.readonly

_RESPONSE_CODES = frozenset({"OK", "NO", "BAD", "BYE", "PREAUTH"})

_CAPABILITY_BRACKET = re.compile(r"\[CAPABILITY(?P<caps>[^\]]*)\]", re.IGNORECASE)
_FLAGS_SECTION = re.compile(r"FLAGS\s*\((?P<flags>[^)]*)\)", re.IGNORECASE)


def _require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_bytes(value: Any, name: str) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes, got {type(value).__name__}")
    return value


def _require_optional_str(value: Any, name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    return value


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_optional_float(value: Any, name: str) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number or None, got {type(value).__name__}")
    return float(value)


def _require_port(value: Any, name: str) -> int:
    port = _require_int(value, name)
    if port < 0 or port > 65535:
        raise ValueError(f"{name} must be between 0 and 65535")
    return port


def _require_timeout(value: Any) -> Optional[float]:
    timeout = _require_optional_float(value, "timeout")
    if timeout is not None and timeout < 0:
        raise ValueError("timeout must be non-negative")
    return timeout


def create_imap4(
    host: str = "",
    port: int = IMAP4_PORT,
    timeout: Optional[float] = None,
) -> _imaplib.IMAP4:
    """Create an IMAP4 client for *host*.

    Args:
        host: The server hostname or address.
        port: The server port.
        timeout: Optional socket timeout in seconds.

    Returns:
        A connected :class:`imaplib.IMAP4` instance.

    Raises:
        TypeError: If *host* is not a string, *port* is not an int, or
            *timeout* is not a number.
        ValueError: If *port* is out of range or *timeout* is negative.
        imaplib.IMAP4.error: If the server cannot be reached.
    """
    _require_str(host, "host")
    port_value = _require_port(port, "port")
    timeout_value = _require_timeout(timeout)
    return _imaplib.IMAP4(host, port_value, timeout=timeout_value)


def create_imap4_ssl(
    host: str = "",
    port: int = IMAP4_SSL_PORT,
    keyfile: Optional[str] = None,
    certfile: Optional[str] = None,
    ssl_context: Any = None,
    timeout: Optional[float] = None,
) -> _imaplib.IMAP4_SSL:
    """Create an IMAP4 over SSL client for *host*.

    Args:
        host: The server hostname or address.
        port: The server port.
        keyfile: Optional path to a private key file.
        certfile: Optional path to a certificate file.
        ssl_context: Optional :class:`ssl.SSLContext` to use.
        timeout: Optional socket timeout in seconds.

    Returns:
        A connected :class:`imaplib.IMAP4_SSL` instance.

    Raises:
        TypeError: If *host*, *port*, *keyfile* or *certfile* have the wrong
            type, or *timeout* is not a number.
        ValueError: If *port* is out of range or *timeout* is negative.
        imaplib.IMAP4.error: If the server cannot be reached.
    """
    _require_str(host, "host")
    port_value = _require_port(port, "port")
    keyfile_value = _require_optional_str(keyfile, "keyfile")
    certfile_value = _require_optional_str(certfile, "certfile")
    timeout_value = _require_timeout(timeout)
    try:
        return _imaplib.IMAP4_SSL(
            host,
            port_value,
            keyfile=keyfile_value,
            certfile=certfile_value,
            ssl_context=ssl_context,
            timeout=timeout_value,
        )
    except TypeError:
        return _imaplib.IMAP4_SSL(host, port_value, keyfile_value, certfile_value)


def create_imap4_stream(command: str) -> _imaplib.IMAP4_stream:
    """Create an IMAP4 client that talks to a local command.

    Args:
        command: The command to run, as a string or a list of arguments.

    Returns:
        An :class:`imaplib.IMAP4_stream` instance.

    Raises:
        TypeError: If *command* is not a string.
    """
    _require_str(command, "command")
    return _imaplib.IMAP4_stream(command)


def parse_capabilities(response: str) -> List[str]:
    """Parse the capability names advertised by an IMAP4 server.

    Handles the untagged ``CAPABILITY`` response as well as the bracketed
    capability list that appears in a greeting.

    Args:
        response: The raw server response.

    Returns:
        The advertised capability names, in the order they were reported.

    Raises:
        TypeError: If *response* is not a string.

    Examples:
        >>> parse_capabilities("* CAPABILITY IMAP4rev1 STARTTLS")
        ['IMAP4rev1', 'STARTTLS']
        >>> parse_capabilities("* OK [CAPABILITY IMAP4rev1 AUTH=PLAIN] Ready")
        ['IMAP4rev1', 'AUTH=PLAIN']
    """
    text = _require_str(response, "response").strip()
    bracket = _CAPABILITY_BRACKET.search(text)
    if bracket is not None:
        return [token for token in bracket.group("caps").split() if token]
    tokens = text.split()
    tagged = False
    if tokens and tokens[0] == "*":
        tokens = tokens[1:]
        tagged = True
    if tokens and tokens[0].upper() in _RESPONSE_CODES:
        tokens = tokens[1:]
        tagged = True
    if tokens and tokens[0].upper() == "CAPABILITY":
        tokens = tokens[1:]
    elif tagged:
        # An untagged response that is not a capability response.
        return []
    return [token for token in tokens if token]


def has_capability(capabilities: Union[str, Sequence[str]], name: str) -> bool:
    """Return ``True`` when *name* is among the advertised capabilities.

    Args:
        capabilities: A space separated capability string, or a sequence of
            capability names.
        name: The capability to look for; the comparison ignores case.

    Returns:
        ``True`` when the capability is advertised.

    Raises:
        TypeError: If *capabilities* is not a string or sequence of strings,
            or *name* is not a string.

    Examples:
        >>> has_capability("IMAP4rev1 STARTTLS", "starttls")
        True
        >>> has_capability(["IMAP4rev1"], "STARTTLS")
        False
    """
    _require_str(name, "name")
    if isinstance(capabilities, str):
        names: List[str] = capabilities.split()
    elif isinstance(capabilities, (list, tuple)):
        for index, item in enumerate(capabilities):
            if not isinstance(item, str):
                raise TypeError(
                    f"capabilities[{index}] must be a str, got {type(item).__name__}"
                )
        names = list(capabilities)
    else:
        raise TypeError(
            "capabilities must be a str or a sequence of str, "
            f"got {type(capabilities).__name__}"
        )
    wanted = name.upper()
    return any(candidate.upper() == wanted for candidate in names)


def parse_flags(response: bytes) -> Tuple[bytes, ...]:
    """Parse a ``FLAGS`` response into the individual flags it carries.

    Args:
        response: The raw server response, for example
            ``b"* 1 FETCH (FLAGS (\\\\Seen \\\\Deleted))"``.

    Returns:
        The flags reported by the server, or an empty tuple when the
        response does not contain a flag list.

    Raises:
        TypeError: If *response* is not bytes.

    Examples:
        >>> parse_flags(b"* 1 FETCH (FLAGS (\\\\Seen \\\\Deleted))")
        (b'\\\\Seen', b'\\\\Deleted')
    """
    raw = _require_bytes(response, "response")
    return _imaplib.ParseFlags(raw)


def parse_fetch_flags(response: str) -> List[str]:
    """Extract the message flags from a ``FETCH`` response.

    Args:
        response: The raw server response, for example
            ``"* 1 FETCH (UID 12 FLAGS (\\\\Seen \\\\Deleted))"``.

    Returns:
        The flags in the order they were reported; an empty list when the
        response carries no ``FLAGS`` section.

    Raises:
        TypeError: If *response* is not a string.

    Examples:
        >>> parse_fetch_flags("* 1 FETCH (FLAGS (\\\\Seen \\\\Deleted))")
        ['\\\\Seen', '\\\\Deleted']
    """
    text = _require_str(response, "response")
    section = _FLAGS_SECTION.search(text)
    if section is None:
        return []
    return [flag for flag in section.group("flags").split() if flag]


def format_flags(flags: Union[str, Iterable[str]]) -> str:
    """Format message flags the way an IMAP4 server expects them.

    Args:
        flags: A space separated flag string, or an iterable of flag names.

    Returns:
        The flags wrapped in parentheses, for example ``"(\\\\Seen)"``.

    Raises:
        TypeError: If *flags* is not a string or an iterable of strings.

    Examples:
        >>> format_flags(["\\\\Seen", "\\\\Draft"])
        '(\\\\Seen \\\\Draft)'
        >>> format_flags("  \\\\Seen   \\\\Seen ")
        '(\\\\Seen)'
    """
    if isinstance(flags, str):
        candidates = flags.split()
    else:
        collected: List[str] = []
        for index, item in enumerate(flags):
            if not isinstance(item, str):
                raise TypeError(
                    f"flags[{index}] must be a str, got {type(item).__name__}"
                )
            collected.append(item)
        candidates = [item.strip() for item in collected]
    unique: List[str] = []
    for candidate in candidates:
        cleaned = candidate.strip()
        if cleaned and cleaned not in unique:
            unique.append(cleaned)
    return "(" + " ".join(unique) + ")"


def parse_internaldate(response: bytes) -> Optional[time.struct_time]:
    """Parse an IMAP4 ``INTERNALDATE`` value into a local time tuple.

    Args:
        response: The raw ``INTERNALDATE`` value, for example
            ``b'INTERNALDATE "05-Feb-2024 10:20:30 +0100"'``.

    Returns:
        The corresponding local time, or ``None`` when *response* is not a
        valid ``INTERNALDATE`` value.

    Raises:
        TypeError: If *response* is not bytes.

    Examples:
        >>> parse_internaldate(b'INTERNALDATE "05-Feb-2024 10:20:30 +0100"').tm_year
        2024
    """
    raw = _require_bytes(response, "response")
    return _imaplib.Internaldate2tuple(raw)


def format_internaldate(date_time: Any) -> str:
    """Format a timestamp the way an IMAP4 server expects it.

    Args:
        date_time: A POSIX timestamp, a :class:`time.struct_time`, a
            :class:`datetime.datetime`, or an already formatted string.

    Returns:
        The ``INTERNALDATE`` representation, for example
        ``'"05-Feb-2024 10:20:30 +0100"'``.

    Raises:
        TypeError: If *date_time* has an unsupported type.
        ValueError: If *date_time* is a naive :class:`datetime.datetime`.
    """
    if isinstance(date_time, (int, float)) and not isinstance(date_time, bool):
        return _imaplib.Time2Internaldate(float(date_time))
    if isinstance(date_time, time.struct_time):
        return _imaplib.Time2Internaldate(date_time)
    if isinstance(date_time, datetime):
        return _imaplib.Time2Internaldate(date_time)
    if isinstance(date_time, str):
        return _imaplib.Time2Internaldate(date_time)
    raise TypeError(
        "date_time must be a number, a time.struct_time, a datetime, or a str, "
        f"got {type(date_time).__name__}"
    )


def int_to_ap(num: int) -> bytes:
    """Convert an integer into its ``A``-``P`` digit representation.

    Args:
        num: The integer to convert.

    Returns:
        The ``A``-``P`` encoded bytes; an empty result for zero.

    Raises:
        TypeError: If *num* is not an int.

    Examples:
        >>> int_to_ap(26)
        b'BK'
    """
    value = _require_int(num, "num")
    return _imaplib.Int2AP(value)


def is_imap4_error(exc: Any) -> bool:
    """Return ``True`` when *exc* is an IMAP4 error."""
    return isinstance(exc, _imaplib.IMAP4.error)


def is_imap4_abort(exc: Any) -> bool:
    """Return ``True`` when *exc* is an IMAP4 abort error."""
    return isinstance(exc, _imaplib.IMAP4.abort)


def is_imap4_readonly(exc: Any) -> bool:
    """Return ``True`` when *exc* is an IMAP4 readonly error."""
    return isinstance(exc, _imaplib.IMAP4.readonly)
