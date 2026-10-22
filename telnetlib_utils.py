"""Telnet client utilities wrapping the standard library :mod:`telnetlib` module.

The :mod:`telnetlib` module implements a client of the telnet protocol as it is
described in :rfc:`854`.  It opens a connection, negotiates the options of the
protocol, and reads the data of the connection as bytes.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It adds the conveniences the standard
library leaves to the caller: the data of a connection can be read as text, a
line can be sent in one call, the number of bytes that reached the peer is
reported, the telnet commands can be removed from a payload or escaped in one,
and the name of a command or an option can be looked up.

.. note::

   The :mod:`telnetlib` module was deprecated in Python 3.11 and removed in
   Python 3.13 as part of :pep:`594`.  The import below degrades gracefully:
   when the interpreter no longer ships the module, the helpers that need it
   raise a :class:`RuntimeError` that names the missing module, while the
   helpers that only work on the protocol itself keep working.
"""

from __future__ import annotations

import re
import socket
import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Tuple, Union, cast

if TYPE_CHECKING:
    # The module is imported at runtime with a guard, so the name only exists
    # for the type checker.
    import telnetlib

__all__ = [
    "AO",
    "AYT",
    "BRK",
    "DM",
    "DO",
    "DONT",
    "EC",
    "EL",
    "GA",
    "IAC",
    "IP",
    "NOP",
    "SB",
    "SE",
    "TELNET_PORT",
    "WILL",
    "WONT",
    "Telnet",
    "close",
    "command_name",
    "connect_telnet",
    "create_telnet",
    "escape_iac",
    "expect",
    "expect_text",
    "is_available",
    "option_name",
    "read_all",
    "read_eager",
    "read_lazy",
    "read_sb_data",
    "read_some",
    "read_until",
    "read_until_text",
    "read_very_eager",
    "read_very_lazy",
    "send_line",
    "strip_iac",
    "theNULL",
    "write",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import telnetlib as _telnetlib
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _telnetlib = None  # type: ignore[assignment]


def _constant(name: str, default: bytes) -> bytes:
    """Return the constant *name* of the standard library, or *default*.

    Args:
        name: The name of the constant.
        default: The value to use when the interpreter no longer ships the
            module.

    Returns:
        The value of the constant as a single byte.
    """
    return bytes(getattr(_telnetlib, name, default))


#: Interpret as command, the byte that introduces a telnet command.
IAC = _constant("IAC", b"\xff")
#: Refuse to perform the option that follows.
DONT = _constant("DONT", b"\xfe")
#: Ask to perform the option that follows.
DO = _constant("DO", b"\xfd")
#: Refuse to perform the option that follows.
WONT = _constant("WONT", b"\xfc")
#: Offer to perform the option that follows.
WILL = _constant("WILL", b"\xfb")
#: End of a subnegotiation.
SE = _constant("SE", b"\xf0")
#: No operation.
NOP = _constant("NOP", b"\xf1")
#: Data mark.
DM = _constant("DM", b"\xf2")
#: Break.
BRK = _constant("BRK", b"\xf3")
#: Interrupt process.
IP = _constant("IP", b"\xf4")
#: Abort output.
AO = _constant("AO", b"\xf5")
#: Are you there.
AYT = _constant("AYT", b"\xf6")
#: Erase character.
EC = _constant("EC", b"\xf7")
#: Erase line.
EL = _constant("EL", b"\xf8")
#: Go ahead.
GA = _constant("GA", b"\xf9")
#: Begin of a subnegotiation.
SB = _constant("SB", b"\xfa")
#: The null byte, which carries no data.
theNULL = _constant("theNULL", b"\x00")

#: The port the telnet protocol uses by default.
TELNET_PORT = int(getattr(_telnetlib, "TELNET_PORT", 23))

#: The sentinel the standard library uses for "use the global socket timeout".
_GLOBAL_DEFAULT_TIMEOUT: Any = getattr(socket, "_GLOBAL_DEFAULT_TIMEOUT", None)

#: The telnet commands of :rfc:`854`, by the value of the command byte.
COMMANDS: Dict[int, str] = {
    240: "SE",
    241: "NOP",
    242: "DM",
    243: "BRK",
    244: "IP",
    245: "AO",
    246: "AYT",
    247: "EC",
    248: "EL",
    249: "GA",
    250: "SB",
    251: "WILL",
    252: "WONT",
    253: "DO",
    254: "DONT",
    255: "IAC",
}

#: The telnet options, by the value of the option byte.
OPTIONS: Dict[int, str] = {
    0: "BINARY",
    1: "ECHO",
    2: "RCP",
    3: "SGA",
    4: "NAMS",
    5: "STATUS",
    6: "TM",
    7: "RCTE",
    8: "NAOL",
    9: "NAOP",
    10: "NAOCRD",
    11: "NAOHTS",
    12: "NAOHTD",
    13: "NAOFFD",
    14: "NAOVTS",
    15: "NAOVTD",
    16: "NAOLFD",
    17: "XASCII",
    18: "LOGOUT",
    19: "BM",
    20: "DET",
    21: "SUPDUP",
    22: "SUPDUPOUTPUT",
    23: "SNDLOC",
    24: "TTYPE",
    25: "EOR",
    26: "TUID",
    27: "OUTMRK",
    28: "TTYLOC",
    29: "VT3270REGIME",
    30: "X3PAD",
    31: "NAWS",
    32: "TSPEED",
    33: "LFLOW",
    34: "LINEMODE",
    35: "XDISPLOC",
    36: "OLD_ENVIRON",
    37: "AUTHENTICATION",
    38: "ENCRYPT",
    39: "NEW_ENVIRON",
    40: "TN3270E",
    41: "XAUTH",
    42: "CHARSET",
    43: "RSP",
    44: "COM_PORT_OPTION",
    45: "SUPPRESS_LOCAL_ECHO",
    46: "TLS",
    47: "KERMIT",
    48: "SEND_URL",
    49: "FORWARD_X",
    138: "PRAGMA_LOGON",
    139: "SSPI_LOGON",
    140: "PRAGMA_HEARTBEAT",
    255: "EXOPL",
}


def _telnetlib_module() -> Any:
    """Return the standard library ``telnetlib`` module.

    Returns:
        The imported :mod:`telnetlib` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    if _telnetlib is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'telnetlib' module was removed in Python 3.13; "
            "use the 'telnetlib3' package instead"
        )
    return _telnetlib


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for every other type.

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


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes, raising ``TypeError`` for every other type.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as bytes.

    Raises:
        TypeError: If *value* is not a bytes-like object.
    """
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_timeout(timeout: Any, name: str = "timeout") -> Optional[float]:
    """Return *timeout* as a number of seconds, or ``None``.

    Args:
        timeout: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The timeout in seconds, or ``None`` when no timeout was given.

    Raises:
        TypeError: If *timeout* is neither a number nor ``None``.
    """
    if timeout is None:
        return None
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError(f"{name} must be a number or None, got {type(timeout).__name__}")
    return float(timeout)


def _require_port(port: Any) -> int:
    """Return *port* as a port number.

    Args:
        port: The value to check.

    Returns:
        The port number.

    Raises:
        TypeError: If *port* is not an integer.
        ValueError: If *port* is out of the range of a port number.
    """
    if isinstance(port, bool) or not isinstance(port, int):
        raise TypeError(f"port must be an int, got {type(port).__name__}")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    return port


def _require_client(client: Any) -> Any:
    """Return *client* when it is a telnet client.

    Args:
        client: The value to check.

    Returns:
        The client of the standard library.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    telnetlib_module = _telnetlib_module()
    if not isinstance(client, telnetlib_module.Telnet):
        raise TypeError(f"client must be a telnetlib.Telnet, got {type(client).__name__}")
    return client


def _require_byte(value: Any, name: str) -> int:
    """Return *value* as the number of a single byte.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The number of the byte.

    Raises:
        TypeError: If *value* is neither an integer nor a single byte.
        ValueError: If *value* is out of the range of a byte.
    """
    if isinstance(value, (bytes, bytearray)):
        if len(value) != 1:
            raise ValueError(f"{name} must be a single byte, got {len(value)} bytes")
        return int(value[0])
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int or a single byte, got {type(value).__name__}")
    if value < 0 or value > 255:
        raise ValueError(f"{name} must be between 0 and 255, got {value}")
    return value


def _timeout_value(timeout: Optional[float]) -> Any:
    """Return the timeout the standard library expects.

    Args:
        timeout: The timeout in seconds, or ``None`` for the default of the
            interpreter.

    Returns:
        The timeout to hand to the standard library.
    """
    if timeout is None:
        return _GLOBAL_DEFAULT_TIMEOUT
    return timeout


def is_available() -> bool:
    """Report whether the interpreter ships the standard library ``telnetlib`` module.

    Returns:
        ``True`` when the module is importable, ``False`` otherwise.
    """
    return _telnetlib is not None


def create_telnet(
    host: Optional[str] = None,
    port: int = 0,
    timeout: Optional[float] = None,
) -> "telnetlib.Telnet":
    """Create a telnet client.

    Args:
        host: The host to connect to.  The client stays unconnected when no
            host is given.
        port: The port to connect to.  The standard library uses the port of
            the protocol when no port is given.
        timeout: The timeout of the connection in seconds.  The default of the
            interpreter is used when no timeout is given.

    Returns:
        The client of the standard library.

    Raises:
        TypeError: If *host* is not a string, *port* is not an integer, or
            *timeout* is not a number.
        ValueError: If *port* is out of the range of a port number.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    if host is not None:
        _require_text(host, "host")
    _require_port(port)
    _require_timeout(timeout)
    telnetlib_module = _telnetlib_module()
    client = telnetlib_module.Telnet(host, port, _timeout_value(timeout))
    return cast("telnetlib.Telnet", client)


def connect_telnet(
    host: str,
    port: int = TELNET_PORT,
    timeout: Optional[float] = None,
) -> "telnetlib.Telnet":
    """Create a telnet client and connect it to *host*.

    Args:
        host: The host to connect to.
        port: The port to connect to.
        timeout: The timeout of the connection in seconds.  The default of the
            interpreter is used when no timeout is given.

    Returns:
        The connected client of the standard library.

    Raises:
        TypeError: If *host* is not a string, *port* is not an integer, or
            *timeout* is not a number.
        ValueError: If *port* is out of the range of a port number.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        OSError: If the connection cannot be opened.
    """
    _require_text(host, "host")
    _require_port(port)
    _require_timeout(timeout)
    telnetlib_module = _telnetlib_module()
    client = telnetlib_module.Telnet()
    client.open(host, port, _timeout_value(timeout))
    return cast("telnetlib.Telnet", client)


def read_until(
    client: Any,
    match: bytes,
    timeout: Optional[float] = None,
) -> bytes:
    """Read from *client* until *match* was received.

    Args:
        client: The telnet client to read from.
        match: The byte sequence to read until.
        timeout: The timeout of the read in seconds.  The read blocks until the
            data arrives when no timeout is given.

    Returns:
        The data that was read, including the match.

    Raises:
        TypeError: If *client* is not a telnet client, *match* is not bytes, or
            *timeout* is not a number.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        EOFError: If the connection is closed before any data arrives.
    """
    _require_client(client)
    _require_bytes(match, "match")
    _require_timeout(timeout)
    return cast(bytes, client.read_until(match, timeout))


def read_until_text(
    client: Any,
    match: str,
    timeout: Optional[float] = None,
    *,
    encoding: str = "utf-8",
    errors: str = "replace",
) -> str:
    """Read from *client* until *match* was received, and return the data as text.

    Args:
        client: The telnet client to read from.
        match: The text to read until.
        timeout: The timeout of the read in seconds.  The read blocks until the
            data arrives when no timeout is given.
        encoding: The encoding of the data of the connection.
        errors: The way undecodable bytes are handled.

    Returns:
        The data that was read, including the match, as text.

    Raises:
        TypeError: If *client* is not a telnet client, *match* is not text, or
            *timeout* is not a number.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        EOFError: If the connection is closed before any data arrives.
    """
    _require_text(match, "match")
    _require_text(encoding, "encoding")
    _require_text(errors, "errors")
    data = read_until(client, match.encode(encoding), timeout)
    return data.decode(encoding, errors)


def read_all(client: Any) -> bytes:
    """Read from *client* until the connection is closed.

    Args:
        client: The telnet client to read from.

    Returns:
        The data that was read.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    _require_client(client)
    return cast(bytes, client.read_all())


def read_some(client: Any) -> bytes:
    """Read at least one byte from *client* unless the connection is closed.

    Args:
        client: The telnet client to read from.

    Returns:
        The data that was read, which is empty when the connection is closed.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    _require_client(client)
    return cast(bytes, client.read_some())


def read_eager(client: Any) -> bytes:
    """Read from *client* without blocking for more than one round trip.

    Args:
        client: The telnet client to read from.

    Returns:
        The data that was read.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    _require_client(client)
    return cast(bytes, client.read_eager())


def read_lazy(client: Any) -> bytes:
    """Read from *client* without blocking, unless the data is already there.

    Args:
        client: The telnet client to read from.

    Returns:
        The data that was read.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    _require_client(client)
    return cast(bytes, client.read_lazy())


def read_very_eager(client: Any) -> bytes:
    """Read from *client* without blocking, and raise on a closed connection.

    Args:
        client: The telnet client to read from.

    Returns:
        The data that was read.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        EOFError: If the connection is closed.
    """
    _require_client(client)
    return cast(bytes, client.read_very_eager())


def read_very_lazy(client: Any) -> bytes:
    """Read from *client* without blocking and without raising.

    Args:
        client: The telnet client to read from.

    Returns:
        The data that was read.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    _require_client(client)
    return cast(bytes, client.read_very_lazy())


def read_sb_data(client: Any) -> bytes:
    """Read the data of a subnegotiation from *client*.

    Args:
        client: The telnet client to read from.

    Returns:
        The data of the subnegotiation.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        EOFError: If the connection is closed before the data arrives.
    """
    _require_client(client)
    return cast(bytes, client.read_sb_data())


def write(client: Any, data: bytes) -> int:
    """Write *data* to *client* and report the number of bytes that were sent.

    The standard library escapes the byte that introduces a telnet command
    before it writes, so the number of bytes that reach the peer can be larger
    than the number of bytes that were given.

    Args:
        client: The telnet client to write to.
        data: The data to write.

    Returns:
        The number of bytes that reached the peer.

    Raises:
        TypeError: If *client* is not a telnet client or *data* is not bytes.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        OSError: If the connection is closed.
    """
    _require_client(client)
    payload = _require_bytes(data, "data")
    client.write(payload)
    return len(payload) + payload.count(IAC)


def send_line(
    client: Any,
    text: str,
    *,
    encoding: str = "utf-8",
    terminator: str = "\r\n",
) -> int:
    """Write *text* to *client* and end the line with *terminator*.

    Args:
        client: The telnet client to write to.
        text: The line to write.
        encoding: The encoding of the line.
        terminator: The bytes that end the line.

    Returns:
        The number of bytes that reached the peer.

    Raises:
        TypeError: If *client* is not a telnet client, *text* is not text, or
            *terminator* is not text.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        OSError: If the connection is closed.
    """
    _require_text(text, "text")
    _require_text(encoding, "encoding")
    _require_text(terminator, "terminator")
    payload = text.encode(encoding) + terminator.encode(encoding)
    return write(client, payload)


def expect(
    client: Any,
    patterns: Sequence[Union[bytes, "re.Pattern[bytes]"]],
    timeout: Optional[float] = None,
) -> Tuple[int, Optional["re.Match[bytes]"], bytes]:
    """Read from *client* until one of *patterns* matched.

    Args:
        client: The telnet client to read from.
        patterns: The patterns to look for.  The data of a telnet connection is
            a byte string, so the patterns have to match bytes.
        timeout: The timeout of the read in seconds.  The read blocks until the
            data arrives when no timeout is given.

    Returns:
        The number of the pattern that matched, the match of that pattern, and
        the data that was read up to and including the match.  The number is
        ``-1`` and the match is ``None`` when no pattern matched.

    Raises:
        TypeError: If *client* is not a telnet client, a pattern does not match
            bytes, or *timeout* is not a number.
        ValueError: If no pattern was given.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        EOFError: If the connection is closed before any data arrives.
    """
    _require_client(client)
    _require_timeout(timeout)
    compiled = _compile_patterns(patterns)
    index, match, data = client.expect(compiled, timeout)
    return int(index), cast(Optional["re.Match[bytes]"], match), cast(bytes, data)


def expect_text(
    client: Any,
    patterns: Sequence[str],
    timeout: Optional[float] = None,
    *,
    encoding: str = "utf-8",
    errors: str = "replace",
) -> Tuple[int, Optional["re.Match[str]"], str]:
    """Read from *client* until one of *patterns* matched, and return the data as text.

    Args:
        client: The telnet client to read from.
        patterns: The patterns to look for.
        timeout: The timeout of the read in seconds.  The read blocks until the
            data arrives when no timeout is given.
        encoding: The encoding of the data of the connection.
        errors: The way undecodable bytes are handled.

    Returns:
        The number of the pattern that matched, the match of that pattern, and
        the data that was read up to and including the match, as text.  The
        number is ``-1`` and the match is ``None`` when no pattern matched.

    Raises:
        TypeError: If *client* is not a telnet client, a pattern is not text, or
            *timeout* is not a number.
        ValueError: If no pattern was given.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
        EOFError: If the connection is closed before any data arrives.
    """
    _require_text(encoding, "encoding")
    _require_text(errors, "errors")
    text_patterns: List["re.Pattern[str]"] = []
    byte_patterns: List["re.Pattern[bytes]"] = []
    for pattern in patterns:
        text = _require_text(pattern, "pattern")
        text_patterns.append(re.compile(text))
        byte_patterns.append(re.compile(text.encode(encoding)))
    index, _, data = expect(client, byte_patterns, timeout)
    decoded = cast(bytes, data).decode(encoding, errors)
    match: Optional["re.Match[str]"] = None
    if index >= 0:
        for candidate in text_patterns:
            found = candidate.search(decoded)
            if found is not None:
                match = found
                break
    return index, match, decoded


def close(client: Any) -> None:
    """Close the connection of *client*.

    Args:
        client: The telnet client to close.

    Raises:
        TypeError: If *client* is not a telnet client.
        RuntimeError: If the interpreter no longer ships the ``telnetlib`` module.
    """
    _require_client(client)
    client.close()


def escape_iac(data: bytes) -> bytes:
    """Return *data* with every byte that introduces a command doubled.

    A payload byte of 255 is escaped as two bytes of 255, so the peer can tell
    it apart from a command.

    Args:
        data: The data to escape.

    Returns:
        The escaped data.

    Raises:
        TypeError: If *data* is not bytes.
    """
    payload = _require_bytes(data, "data")
    return payload.replace(IAC, IAC + IAC)


def strip_iac(data: bytes) -> bytes:
    """Return *data* without the telnet commands it holds.

    The commands of the protocol are removed, a subnegotiation is removed as a
    whole, and a payload byte of 255 is restored from the pair of bytes that
    escaped it.

    Args:
        data: The data to strip.

    Returns:
        The payload of the data.

    Raises:
        TypeError: If *data* is not bytes.
    """
    payload = _require_bytes(data, "data")
    result = bytearray()
    index = 0
    length = len(payload)
    while index < length:
        if payload[index] != IAC[0]:
            result.append(payload[index])
            index += 1
            continue
        if index + 1 >= length:
            # A byte of 255 at the end of the data is an unfinished command.
            break
        command = payload[index + 1]
        if command == IAC[0]:
            result.append(IAC[0])
            index += 2
            continue
        index += 2
        if command in (WILL[0], WONT[0], DO[0], DONT[0]):
            # A negotiation names the option it negotiates.
            index += 1
            continue
        if command == SB[0]:
            index = _skip_subnegotiation(payload, index)
    return bytes(result)


def _skip_subnegotiation(data: bytes, index: int) -> int:
    """Return the offset behind the subnegotiation that starts at *index*.

    Args:
        data: The data that holds the subnegotiation.
        index: The offset of the first byte of the subnegotiation.

    Returns:
        The offset behind the subnegotiation.
    """
    length = len(data)
    while index < length:
        if data[index] != IAC[0]:
            index += 1
            continue
        if index + 1 >= length:
            return length
        following = data[index + 1]
        if following == IAC[0]:
            # A pair of bytes of 255 carries a payload byte of 255.
            index += 2
            continue
        if following == SE[0]:
            return index + 2
        index += 2
    return length


def command_name(value: Union[int, bytes]) -> Optional[str]:
    """Return the name of the telnet command *value* names.

    Args:
        value: The number of the command, or the command as a single byte.

    Returns:
        The name of the command, such as ``"WILL"``, or ``None`` when the value
        does not name a command.

    Raises:
        TypeError: If *value* is neither an integer nor a single byte.
        ValueError: If *value* is out of the range of a byte.
    """
    return COMMANDS.get(_require_byte(value, "value"))


def option_name(value: Union[int, bytes]) -> Optional[str]:
    """Return the name of the telnet option *value* names.

    Args:
        value: The number of the option, or the option as a single byte.

    Returns:
        The name of the option, such as ``"ECHO"``, or ``None`` when the value
        does not name an option.

    Raises:
        TypeError: If *value* is neither an integer nor a single byte.
        ValueError: If *value* is out of the range of a byte.
    """
    return OPTIONS.get(_require_byte(value, "value"))


def _compile_patterns(
    patterns: Sequence[Union[bytes, "re.Pattern[bytes]"]],
) -> List["re.Pattern[bytes]"]:
    """Return *patterns* as the compiled patterns of the standard library.

    Args:
        patterns: The patterns to compile.

    Returns:
        The compiled patterns.

    Raises:
        TypeError: If *patterns* is not a sequence, or a pattern does not match
            bytes.
        ValueError: If no pattern was given.
    """
    if isinstance(patterns, (str, bytes, bytearray)) or not isinstance(patterns, Sequence):
        raise TypeError("patterns must be a sequence of patterns")
    if not patterns:
        raise ValueError("patterns must not be empty")
    compiled: List["re.Pattern[bytes]"] = []
    for index, pattern in enumerate(patterns):
        if isinstance(pattern, (bytes, bytearray)):
            compiled.append(re.compile(bytes(pattern)))
            continue
        source = getattr(pattern, "pattern", None)
        if not isinstance(source, bytes):
            raise TypeError(f"patterns[{index}] must be a pattern that matches bytes")
        compiled.append(cast("re.Pattern[bytes]", pattern))
    return compiled


class _TelnetProxy:
    """Stand-in for the client of the standard library when the module is missing."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Raise a :class:`RuntimeError` because the standard library is missing."""
        _telnetlib_module()


if _telnetlib is not None:
    Telnet = _telnetlib.Telnet  # type: ignore[misc,assignment]
else:  # pragma: no cover - Python 3.13 removed the module
    Telnet = _TelnetProxy  # type: ignore[misc,assignment]
