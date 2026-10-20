"""SMTP client utilities (wrapping :mod:`smtplib`).

The :mod:`smtplib` module implements an SMTP client as described in
:rfc:`821`, :rfc:`1869` (ESMTP), :rfc:`2554` (authentication) and :rfc:`2487`
(SMTP over TLS).  It ships the :class:`~smtplib.SMTP`,
:class:`~smtplib.SMTP_SSL` and :class:`~smtplib.LMTP` clients, the exception
hierarchy they raise, and a handful of address helpers.

This wrapper keeps the standard library as the single source of truth and adds
three conveniences:

* every argument is validated before the standard library is reached, so a
  mistake raises :class:`TypeError` or :class:`ValueError` instead of failing
  deep inside the client,
* :func:`build_message` assembles a complete
  :class:`email.message.EmailMessage` from plain values, which the standard
  library leaves to the caller,
* :func:`parse_response` and :func:`parse_ehlo_features` parse captured
  server replies without needing a connection.

The wrapper never opens a connection on its own: :func:`create_smtp`,
:func:`create_smtp_ssl` and :func:`create_lmtp` build the standard library
clients, and it is up to the caller to decide when to connect.  The
:func:`send_message` and :func:`send_text` helpers operate on a client the
caller already owns.
"""

from __future__ import annotations

import email.message
import email.utils
import mimetypes
import re
import smtplib as _smtplib
import socket
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

__all__ = [
    "CRLF",
    "LMTP",
    "LMTP_PORT",
    "RefusedRecipients",
    "SMTP",
    "SMTPAuthenticationError",
    "SMTPConnectError",
    "SMTPDataError",
    "SMTPHeloError",
    "SMTPNotSupportedError",
    "SMTPRecipientsRefused",
    "SMTPSenderRefused",
    "SMTPServerDisconnected",
    "SMTPResponseException",
    "SMTPException",
    "SMTP_PORT",
    "SMTP_SSL",
    "SMTP_SSL_PORT",
    "address_only",
    "build_message",
    "create_lmtp",
    "create_smtp",
    "create_smtp_ssl",
    "format_address",
    "getfqdn",
    "is_smtp_authentication_error",
    "is_smtp_data_error",
    "is_smtp_error",
    "is_smtp_helo_error",
    "is_smtp_not_supported",
    "is_smtp_recipients_refused",
    "is_smtp_response_error",
    "is_smtp_sender_refused",
    "is_smtp_server_disconnected",
    "parse_address",
    "parse_ehlo_features",
    "parse_response",
    "quote_data",
    "quote_string",
    "quoteaddr",
    "send_message",
    "send_text",
]

#: The line ending every SMTP command uses.
CRLF: str = _smtplib.CRLF

#: The default port of a plain SMTP server.
SMTP_PORT: int = _smtplib.SMTP_PORT

#: The default port of an SMTP server that speaks TLS from the first byte.
SMTP_SSL_PORT: int = _smtplib.SMTP_SSL_PORT

#: The default port of a local mail transfer agent.
LMTP_PORT: int = _smtplib.LMTP_PORT

#: The standard library plain SMTP client, re-exported for convenience.
SMTP = _smtplib.SMTP

#: The standard library SMTP over TLS client, re-exported for convenience.
SMTP_SSL = _smtplib.SMTP_SSL

#: The standard library local mail transfer client, re-exported for convenience.
LMTP = _smtplib.LMTP

#: The base error of the standard library, re-exported for convenience.
SMTPException = _smtplib.SMTPException

#: The standard library "command not supported" error.
SMTPNotSupportedError = _smtplib.SMTPNotSupportedError

#: The standard library "server disconnected" error.
SMTPServerDisconnected = _smtplib.SMTPServerDisconnected

#: The standard library "unexpected reply" error.
SMTPResponseException = _smtplib.SMTPResponseException

#: The standard library "sender refused" error.
SMTPSenderRefused = _smtplib.SMTPSenderRefused

#: The standard library "recipients refused" error.
SMTPRecipientsRefused = _smtplib.SMTPRecipientsRefused

#: The standard library "data refused" error.
SMTPDataError = _smtplib.SMTPDataError

#: The standard library "connection failed" error.
SMTPConnectError = _smtplib.SMTPConnectError

#: The standard library "greeting refused" error.
SMTPHeloError = _smtplib.SMTPHeloError

#: The standard library "authentication failed" error.
SMTPAuthenticationError = _smtplib.SMTPAuthenticationError

#: The recipients a server refused, mapped to the reason it gave.
RefusedRecipients = Dict[str, Tuple[int, bytes]]

#: The sentinel the standard library uses for "use the global socket timeout".
_GLOBAL_DEFAULT_TIMEOUT: Any = getattr(socket, "_GLOBAL_DEFAULT_TIMEOUT", None)

_FEATURE = re.compile(r"(?P<feature>[A-Za-z0-9][A-Za-z0-9\-]*) ?")

_DEFAULT_MAINTYPE = "application"
_DEFAULT_SUBTYPE = "octet-stream"


def _require_str(value: Any, name: str) -> str:
    """Return *value* when it is a string.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated string.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_optional_str(value: Any, name: str) -> Optional[str]:
    """Return *value* when it is a string or ``None``.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated string, or ``None``.

    Raises:
        TypeError: If *value* is neither a string nor ``None``.
    """
    if value is None:
        return None
    return _require_str(value, name)


def _require_int(value: Any, name: str) -> int:
    """Return *value* when it is an integer.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated integer.

    Raises:
        TypeError: If *value* is not an integer.  Booleans are rejected because
            they are integers in Python but never a meaningful port or count.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_port(value: Any, name: str) -> int:
    """Return *value* when it is a usable port number.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated port.  Zero means "use the default port of the client".

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is negative or above 65535.
    """
    port = _require_int(value, name)
    if port < 0 or port > 65535:
        raise ValueError(f"{name} must be between 0 and 65535, got {port}")
    return port


def _require_timeout(value: Any) -> Optional[float]:
    """Return *value* when it is a usable socket timeout.

    Args:
        value: The value to check.

    Returns:
        The validated timeout, or ``None`` for "use the global default".

    Raises:
        TypeError: If *value* is neither a number nor ``None``.
        ValueError: If *value* is not positive.  The standard library rejects
            a non-blocking socket, so a timeout of zero is refused as well.
    """
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"timeout must be a number or None, got {type(value).__name__}")
    timeout = float(value)
    if timeout <= 0:
        raise ValueError(f"timeout must be positive, got {timeout}")
    return timeout


def _require_source_address(
    value: Any,
) -> Optional[Tuple[str, int]]:
    """Return *value* when it is a usable source address.

    Args:
        value: The value to check.

    Returns:
        The validated ``(host, port)`` pair, or ``None``.

    Raises:
        TypeError: If *value* is neither a pair nor ``None``.
        ValueError: If the port of the pair is out of range.
    """
    if value is None:
        return None
    if not isinstance(value, (tuple, list)) or len(value) != 2:
        raise TypeError(
            "source_address must be a (host, port) pair or None, "
            f"got {type(value).__name__}"
        )
    host = _require_str(value[0], "source_address[0]")
    port = _require_port(value[1], "source_address[1]")
    return (host, port)


def _require_addresses(value: Any, name: str) -> List[str]:
    """Return *value* as a list of non-empty addresses.

    Args:
        value: A single address, or an iterable of addresses.
        name: The name of the argument, used in the error message.

    Returns:
        The validated addresses.

    Raises:
        TypeError: If *value* is not a string or an iterable of strings.
        ValueError: If one of the addresses is empty.
    """
    if isinstance(value, str):
        candidates: List[str] = [value]
    else:
        try:
            collected = list(value)
        except TypeError as exc:
            raise TypeError(
                f"{name} must be a str or an iterable of str, "
                f"got {type(value).__name__}"
            ) from exc
        candidates = []
        for index, item in enumerate(collected):
            if not isinstance(item, str):
                raise TypeError(
                    f"{name}[{index}] must be a str, got {type(item).__name__}"
                )
            candidates.append(item)
    for index, candidate in enumerate(candidates):
        if not candidate.strip():
            raise ValueError(f"{name}[{index}] must not be empty")
    return candidates


def _require_message(value: Any, name: str) -> email.message.Message:
    """Return *value* when it is an email message.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated message.

    Raises:
        TypeError: If *value* is not an :class:`email.message.Message`.
    """
    if not isinstance(value, email.message.Message):
        raise TypeError(
            f"{name} must be an email.message.Message, got {type(value).__name__}"
        )
    return value


def _require_client(value: Any, name: str) -> _smtplib.SMTP:
    """Return *value* when it looks like an SMTP client.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated client.

    Raises:
        TypeError: If *value* is not an SMTP client.
    """
    if not isinstance(value, _smtplib.SMTP):
        raise TypeError(
            f"{name} must be an smtplib.SMTP instance, got {type(value).__name__}"
        )
    return value


def _require_options(value: Any, name: str) -> List[str]:
    """Return *value* as a list of SMTP options.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The validated options.

    Raises:
        TypeError: If *value* is not an iterable of strings.
        ValueError: If one of the options is empty or holds a line break.
    """
    options: List[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise TypeError(
                f"{name}[{index}] must be a str, got {type(item).__name__}"
            )
        if not item:
            raise ValueError(f"{name}[{index}] must not be empty")
        if "\r" in item or "\n" in item:
            raise ValueError(f"{name}[{index}] must not contain a line break")
        options.append(item)
    return options


def _response_text(value: Any, name: str) -> str:
    """Return *value* as the text of a server reply.

    Args:
        value: A reply as a string or as bytes.
        name: The name of the argument, used in the error message.

    Returns:
        The reply as text.

    Raises:
        TypeError: If *value* is neither a string nor bytes.
    """
    if isinstance(value, bytes):
        return value.decode("latin-1")
    if isinstance(value, str):
        return value
    raise TypeError(f"{name} must be a str or bytes, got {type(value).__name__}")


def quoteaddr(address: str) -> str:
    """Quote an address the way an SMTP server expects it.

    Args:
        address: The address, optionally with a display name.

    Returns:
        The address in angle brackets, for example ``"<user@example.com>"``.

    Raises:
        TypeError: If *address* is not a string.

    Examples:
        >>> quoteaddr("user@example.com")
        '<user@example.com>'
    """
    return _smtplib.quoteaddr(_require_str(address, "address"))


def quote_string(text: str) -> str:
    """Quote a string so that it can be used inside a header.

    Backslashes and double quotes are escaped, and the result is wrapped in
    double quotes.

    Args:
        text: The string to quote.

    Returns:
        The quoted string, for example ``'"say \\"hi\\""'``.

    Raises:
        TypeError: If *text* is not a string.

    Examples:
        >>> quote_string('say "hi"')
        '"say \\\\"hi\\\\""'
    """
    return '"' + email.utils.quote(_require_str(text, "text")) + '"'


def quote_data(data: str) -> str:
    """Quote the body of a message the way SMTP expects it.

    Leading periods are doubled and every line ending becomes a CRLF, so the
    body cannot terminate the message early.

    Args:
        data: The message body.

    Returns:
        The quoted body.

    Raises:
        TypeError: If *data* is not a string.

    Examples:
        >>> quote_data("one\\ntwo")
        'one\\r\\ntwo'
    """
    return _smtplib.quotedata(_require_str(data, "data"))


def parse_address(address: str) -> Tuple[str, str]:
    """Split an address into its display name and its address.

    Args:
        address: The address, optionally with a display name.

    Returns:
        A ``(display name, address)`` pair.  Both parts are empty when the
        address cannot be parsed.

    Raises:
        TypeError: If *address* is not a string.

    Examples:
        >>> parse_address("Alice <alice@example.com>")
        ('Alice', 'alice@example.com')
    """
    return email.utils.parseaddr(_require_str(address, "address"))


def address_only(address: str) -> str:
    """Return an address without its display name.

    Args:
        address: The address, optionally with a display name.

    Returns:
        The bare address, for example ``"alice@example.com"``.

    Raises:
        TypeError: If *address* is not a string.

    Examples:
        >>> address_only("Alice <alice@example.com>")
        'alice@example.com'
    """
    display_name, parsed = email.utils.parseaddr(_require_str(address, "address"))
    if not display_name and not parsed:
        return address
    return parsed


def format_address(display_name: str, address: str) -> str:
    """Format a display name and an address as a single header value.

    A display name that is not plain ASCII is encoded as described in
    :rfc:`2047`.

    Args:
        display_name: The display name of the address.
        address: The address itself.

    Returns:
        The formatted value, for example ``"Alice <alice@example.com>"``.

    Raises:
        TypeError: If *display_name* or *address* is not a string.

    Examples:
        >>> format_address("Alice", "alice@example.com")
        'Alice <alice@example.com>'
    """
    name = _require_str(display_name, "display_name")
    target = _require_str(address, "address")
    return email.utils.formataddr((name, target))


def getfqdn(name: str = "") -> str:
    """Return the fully qualified domain name of a host.

    Args:
        name: The host name to resolve.  An empty name resolves the local
            host.

    Returns:
        The fully qualified domain name.

    Raises:
        TypeError: If *name* is not a string.
    """
    return socket.getfqdn(_require_str(name, "name"))


def parse_response(response: Union[str, bytes]) -> Tuple[int, str]:
    """Parse a raw SMTP reply into its code and its message.

    A multiline reply keeps every line but the last one in the message, joined
    with a newline, exactly like the standard library client does.

    Args:
        response: The reply as it was received from the server.

    Returns:
        A ``(code, message)`` pair.  The code is ``-1`` when the reply does not
        start with a three digit code.

    Raises:
        TypeError: If *response* is neither a string nor bytes.
        ValueError: If *response* holds no line at all.

    Examples:
        >>> parse_response("250 OK")
        (250, 'OK')
        >>> parse_response("250-First\\n250 Second")
        (250, 'First\\nSecond')
    """
    text = _response_text(response, "response")
    lines = text.splitlines()
    if not lines:
        raise ValueError("response must not be empty")
    code = -1
    messages: List[str] = []
    for line in lines:
        stripped = line.rstrip("\r\n")
        try:
            code = int(stripped[:3])
        except ValueError:
            code = -1
        messages.append(stripped[4:].strip())
        if stripped[3:4] != "-":
            break
    return code, "\n".join(messages)


def _has_code_prefix(line: str) -> bool:
    """Return ``True`` when *line* starts with an SMTP reply code.

    Args:
        line: The line to inspect.

    Returns:
        ``True`` when the line starts with three digits followed by a space or
        a hyphen.
    """
    return len(line) >= 4 and line[:3].isdigit() and line[3] in "- "


def parse_ehlo_features(
    response: Union[str, bytes],
    skip_greeting: bool = True,
) -> Dict[str, str]:
    """Parse the service extensions a server announced in its EHLO reply.

    Args:
        response: The reply, either the message of a reply or the complete
            raw reply.  Both the message of a reply, which is what
            :meth:`smtplib.SMTP.ehlo` returns, and a raw reply are accepted.
        skip_greeting: Whether the first line is the greeting of the server
            and therefore not a service extension.  The standard library
            behaves the same way.

    Returns:
        The announced service extensions, mapped to their parameters.  The
        names are lower case, again like the standard library.

    Raises:
        TypeError: If *response* is neither a string nor bytes.

    Examples:
        >>> parse_ehlo_features("mail.example.com Hello\\nSIZE 100\\n8BITMIME")
        {'size': '100', '8bitmime': ''}
    """
    text = _response_text(response, "response")
    lines = text.splitlines()
    if not lines:
        return {}
    if skip_greeting:
        lines = lines[1:]
    features: Dict[str, str] = {}
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if _has_code_prefix(stripped):
            stripped = stripped[4:].strip()
        match = _FEATURE.match(stripped)
        if match is None:
            continue
        name = match.group("feature").lower()
        params = stripped[match.end("feature") :].strip()
        if name == "auth":
            features[name] = (features.get(name, "") + " " + params).strip()
        else:
            features[name] = params
    return features


def build_message(
    sender: str,
    recipients: Iterable[str],
    subject: str,
    body: str,
    cc: Optional[Iterable[str]] = None,
    bcc: Optional[Iterable[str]] = None,
    reply_to: Optional[str] = None,
    html: Optional[str] = None,
    attachments: Optional[Sequence[Tuple[str, bytes]]] = None,
) -> email.message.EmailMessage:
    """Build a complete message from plain values.

    The standard library only offers the low level ``sendmail`` and
    ``send_message`` methods, so building the message is left to the caller.
    This helper assembles a :class:`email.message.EmailMessage` instead.

    Args:
        sender: The address the message is sent from.
        recipients: The addresses the message is sent to.
        subject: The subject of the message.
        body: The plain text body of the message.
        cc: Optional addresses that receive a copy of the message.
        bcc: Optional addresses that receive a hidden copy of the message.
            They are part of the envelope but never appear in the headers.
        reply_to: Optional address replies are sent to.
        html: Optional HTML body.  When it is given, the message carries both
            a plain text and an HTML alternative.
        attachments: Optional ``(file name, payload)`` pairs.  The media type
            of an attachment is guessed from its file name.

    Returns:
        The assembled message.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an address is empty or an attachment is malformed.

    Examples:
        >>> message = build_message("alice@example.com", ["bob@example.com"], "Hi", "Hello")
        >>> message["Subject"]
        'Hi'
    """
    from_address = _require_str(sender, "sender")
    if not from_address.strip():
        raise ValueError("sender must not be empty")
    to_addresses = _require_addresses(recipients, "recipients")
    if not to_addresses:
        raise ValueError("recipients must not be empty")
    title = _require_str(subject, "subject")
    text = _require_str(body, "body")
    cc_addresses = _require_addresses(cc, "cc") if cc is not None else []
    if bcc is not None:
        _require_addresses(bcc, "bcc")
    reply = _require_optional_str(reply_to, "reply_to")
    if reply is not None and not reply.strip():
        raise ValueError("reply_to must not be empty")

    message = email.message.EmailMessage()
    message["From"] = from_address
    message["To"] = ", ".join(to_addresses)
    if cc_addresses:
        message["Cc"] = ", ".join(cc_addresses)
    message["Subject"] = title
    if reply is not None:
        message["Reply-To"] = reply
    message.set_content(text)
    if html is not None:
        message.add_alternative(_require_str(html, "html"), subtype="html")
    for index, attachment in enumerate(attachments or ()):
        if not isinstance(attachment, (tuple, list)) or len(attachment) != 2:
            raise TypeError(
                f"attachments[{index}] must be a (file name, payload) pair, "
                f"got {type(attachment).__name__}"
            )
        file_name = _require_str(attachment[0], f"attachments[{index}][0]")
        payload = attachment[1]
        if not isinstance(payload, bytes):
            raise TypeError(
                f"attachments[{index}][1] must be bytes, got {type(payload).__name__}"
            )
        if not file_name:
            raise ValueError(f"attachments[{index}][0] must not be empty")
        maintype, subtype = _guess_media_type(file_name)
        message.add_attachment(
            payload,
            maintype=maintype,
            subtype=subtype,
            filename=file_name,
        )
    return message


def _guess_media_type(file_name: str) -> Tuple[str, str]:
    """Return the media type of a file name.

    Args:
        file_name: The name of the file.

    Returns:
        A ``(main type, sub type)`` pair.  Unknown file names fall back to
        ``("application", "octet-stream")``.
    """
    guessed = mimetypes.guess_type(file_name)[0]
    if not guessed:
        return (_DEFAULT_MAINTYPE, _DEFAULT_SUBTYPE)
    maintype, _, subtype = guessed.partition("/")
    if not maintype or not subtype:
        return (_DEFAULT_MAINTYPE, _DEFAULT_SUBTYPE)
    return (maintype, subtype)


def create_smtp(
    host: str = "",
    port: int = 0,
    local_hostname: Optional[str] = None,
    timeout: Optional[float] = None,
    source_address: Optional[Tuple[str, int]] = None,
) -> _smtplib.SMTP:
    """Create a plain SMTP client.

    The client connects right away when *host* is not empty, so the caller
    stays in control of when a connection is attempted.

    Args:
        host: The server to connect to.  An empty host builds a client that
            is not connected yet.
        port: The port of the server.  Zero uses the default port of the
            client.
        local_hostname: The name the client announces in its greeting.  When
            it is omitted the standard library looks the name up.
        timeout: The socket timeout in seconds.  ``None`` uses the global
            socket default.
        source_address: Optional ``(host, port)`` pair the socket binds to.

    Returns:
        A :class:`smtplib.SMTP` instance.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *port* is out of range or *timeout* is not positive.
    """
    server = _require_str(host, "host")
    port_number = _require_port(port, "port")
    hostname = _require_optional_str(local_hostname, "local_hostname")
    timeout_value = _require_timeout(timeout)
    address = _require_source_address(source_address)
    if timeout_value is None:
        timeout_argument: Any = _GLOBAL_DEFAULT_TIMEOUT
    else:
        timeout_argument = timeout_value
    return _smtplib.SMTP(
        server,
        port_number,
        local_hostname=hostname,
        timeout=timeout_argument,
        source_address=address,
    )


def create_smtp_ssl(
    host: str = "",
    port: int = 0,
    local_hostname: Optional[str] = None,
    context: Optional[Any] = None,
    timeout: Optional[float] = None,
    source_address: Optional[Tuple[str, int]] = None,
) -> _smtplib.SMTP_SSL:
    """Create an SMTP client that speaks TLS from the first byte.

    Args:
        host: The server to connect to.  An empty host builds a client that
            is not connected yet.
        port: The port of the server.  Zero uses the default port of the
            client.
        local_hostname: The name the client announces in its greeting.
        context: Optional :class:`ssl.SSLContext` to use.  When it is
            omitted the standard library builds a default context.
        timeout: The socket timeout in seconds.  ``None`` uses the global
            socket default.
        source_address: Optional ``(host, port)`` pair the socket binds to.

    Returns:
        An :class:`smtplib.SMTP_SSL` instance.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *port* is out of range or *timeout* is not positive.
    """
    server = _require_str(host, "host")
    port_number = _require_port(port, "port")
    hostname = _require_optional_str(local_hostname, "local_hostname")
    timeout_value = _require_timeout(timeout)
    address = _require_source_address(source_address)
    if timeout_value is None:
        timeout_argument: Any = _GLOBAL_DEFAULT_TIMEOUT
    else:
        timeout_argument = timeout_value
    return _smtplib.SMTP_SSL(
        server,
        port_number,
        local_hostname=hostname,
        context=context,
        timeout=timeout_argument,
        source_address=address,
    )


def create_lmtp(
    host: str = "",
    port: int = LMTP_PORT,
    local_hostname: Optional[str] = None,
    timeout: Optional[float] = None,
    source_address: Optional[Tuple[str, int]] = None,
) -> _smtplib.LMTP:
    """Create a local mail transfer client.

    Args:
        host: The server to connect to.  A host that starts with a slash is
            treated as a Unix socket by the standard library.
        port: The port of the server.
        local_hostname: The name the client announces in its greeting.
        timeout: The socket timeout in seconds.  ``None`` uses the global
            socket default.
        source_address: Optional ``(host, port)`` pair the socket binds to.

    Returns:
        A :class:`smtplib.LMTP` instance.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *port* is out of range or *timeout* is not positive.
    """
    server = _require_str(host, "host")
    port_number = _require_port(port, "port")
    hostname = _require_optional_str(local_hostname, "local_hostname")
    timeout_value = _require_timeout(timeout)
    address = _require_source_address(source_address)
    if timeout_value is None:
        timeout_argument: Any = _GLOBAL_DEFAULT_TIMEOUT
    else:
        timeout_argument = timeout_value
    return _smtplib.LMTP(
        server,
        port_number,
        local_hostname=hostname,
        source_address=address,
        timeout=timeout_argument,
    )


def send_message(
    smtp: _smtplib.SMTP,
    message: email.message.Message,
    from_addr: Optional[str] = None,
    to_addrs: Optional[Iterable[str]] = None,
    mail_options: Sequence[str] = (),
    rcpt_options: Sequence[str] = (),
) -> RefusedRecipients:
    """Send a message with a client the caller owns.

    Args:
        smtp: The client to send the message with.
        message: The message to send.
        from_addr: The envelope sender.  When it is omitted the ``From``
            header of the message is used.
        to_addrs: The envelope recipients.  When it is omitted the ``To``,
            ``Cc`` and ``Bcc`` headers of the message are used.
        mail_options: Options for the ``MAIL`` command, for example
            ``("SIZE=1000",)``.
        rcpt_options: Options for the ``RCPT`` command.

    Returns:
        The recipients the server refused, mapped to the reason it gave.  An
        empty mapping means that every recipient was accepted.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an option is empty or holds a line break.
    """
    client = _require_client(smtp, "smtp")
    payload = _require_message(message, "message")
    sender = _require_optional_str(from_addr, "from_addr")
    recipients = _require_addresses(to_addrs, "to_addrs") if to_addrs is not None else None
    mail = _require_options(mail_options, "mail_options")
    rcpt = _require_options(rcpt_options, "rcpt_options")
    return client.send_message(payload, sender, recipients, mail, rcpt)


def send_text(
    smtp: _smtplib.SMTP,
    sender: str,
    recipients: Iterable[str],
    subject: str,
    body: str,
    cc: Optional[Iterable[str]] = None,
    bcc: Optional[Iterable[str]] = None,
    reply_to: Optional[str] = None,
    html: Optional[str] = None,
    attachments: Optional[Sequence[Tuple[str, bytes]]] = None,
    mail_options: Sequence[str] = (),
    rcpt_options: Sequence[str] = (),
) -> RefusedRecipients:
    """Build a message and send it with a client the caller owns.

    Args:
        smtp: The client to send the message with.
        sender: The address the message is sent from.
        recipients: The addresses the message is sent to.
        subject: The subject of the message.
        body: The plain text body of the message.
        cc: Optional addresses that receive a copy of the message.
        bcc: Optional addresses that receive a hidden copy of the message.
        reply_to: Optional address replies are sent to.
        html: Optional HTML body.
        attachments: Optional ``(file name, payload)`` pairs.
        mail_options: Options for the ``MAIL`` command.
        rcpt_options: Options for the ``RCPT`` command.

    Returns:
        The recipients the server refused, mapped to the reason it gave.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an address is empty or an option is malformed.
    """
    client = _require_client(smtp, "smtp")
    message = build_message(
        sender,
        recipients,
        subject,
        body,
        cc=cc,
        bcc=bcc,
        reply_to=reply_to,
        html=html,
        attachments=attachments,
    )
    envelope = list(_require_addresses(recipients, "recipients"))
    if cc is not None:
        envelope.extend(_require_addresses(cc, "cc"))
    if bcc is not None:
        envelope.extend(_require_addresses(bcc, "bcc"))
    return send_message(
        client,
        message,
        from_addr=sender,
        to_addrs=envelope,
        mail_options=mail_options,
        rcpt_options=rcpt_options,
    )


def is_smtp_error(exc: Any) -> bool:
    """Return ``True`` when *exc* is any SMTP error."""
    return isinstance(exc, _smtplib.SMTPException)


def is_smtp_response_error(exc: Any) -> bool:
    """Return ``True`` when *exc* is an unexpected SMTP reply."""
    return isinstance(exc, _smtplib.SMTPResponseException)


def is_smtp_sender_refused(exc: Any) -> bool:
    """Return ``True`` when *exc* reports a refused sender."""
    return isinstance(exc, _smtplib.SMTPSenderRefused)


def is_smtp_recipients_refused(exc: Any) -> bool:
    """Return ``True`` when *exc* reports refused recipients."""
    return isinstance(exc, _smtplib.SMTPRecipientsRefused)


def is_smtp_data_error(exc: Any) -> bool:
    """Return ``True`` when *exc* reports a refused message body."""
    return isinstance(exc, _smtplib.SMTPDataError)


def is_smtp_helo_error(exc: Any) -> bool:
    """Return ``True`` when *exc* reports a refused greeting."""
    return isinstance(exc, _smtplib.SMTPHeloError)


def is_smtp_not_supported(exc: Any) -> bool:
    """Return ``True`` when *exc* reports an unsupported command."""
    return isinstance(exc, _smtplib.SMTPNotSupportedError)


def is_smtp_server_disconnected(exc: Any) -> bool:
    """Return ``True`` when *exc* reports a closed connection."""
    return isinstance(exc, _smtplib.SMTPServerDisconnected)


def is_smtp_authentication_error(exc: Any) -> bool:
    """Return ``True`` when *exc* reports a failed authentication."""
    return isinstance(exc, _smtplib.SMTPAuthenticationError)
