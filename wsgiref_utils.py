"""WSGI utilities wrapping the standard library :mod:`wsgiref` package.

The :mod:`wsgiref` package is the reference implementation of the Web Server
Gateway Interface (:pep:`3333`).  It holds the helpers that build and inspect
the environment of a request, the collection of the headers of a response, the
middleware that checks an application against the specification, and a small
server that serves an application on the local machine.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  The classes of the standard library are re-exported, so a
caller does not have to import :mod:`wsgiref` itself.

The module never opens a connection.  The helpers of the environment of a
request work on a dictionary, the helpers of the headers of a response work on
a list, and a server is only created when a caller asks for one.
"""

from __future__ import annotations

import warnings
from typing import IO, Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple
from wsgiref import simple_server as _simple_server
from wsgiref import util as _util
from wsgiref import validate as _validate
from wsgiref.headers import Headers
from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
from wsgiref.validate import WSGIWarning

__all__: list[str] = [
    "Application",
    "Environment",
    "FileWrapper",
    "HOP_BY_HOP_HEADERS",
    "Headers",
    "WSGIRequestHandler",
    "WSGIServer",
    "WSGIWarning",
    "application_uri",
    "build_headers",
    "check_environ",
    "demo_app",
    "encode_headers",
    "environ_errors",
    "file_wrapper",
    "guess_scheme",
    "header_values",
    "is_hop_by_hop",
    "make_server",
    "request_uri",
    "setup_testing_defaults",
    "shift_path_info",
    "validator",
]

#: The environment of a request, the variables of the specification as a mapping.
Environment = Dict[str, Any]

#: The application of a request, a callable that answers with an iterable of bytes.
Application = Callable[..., Any]

#: The headers of RFC 2616, section 13.5.1, that a proxy must not forward.
HOP_BY_HOP_HEADERS = frozenset(
    {
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
    }
)

#: The wrapper of the standard library that turns a file into an iterable.
FileWrapper = _util.FileWrapper


def _require_str(value: object, name: str) -> str:
    """Return the value when it is a string.

    Args:
        value: The value to validate.
        name: The name of the parameter for error messages.

    Returns:
        The validated string.

    Raises:
        TypeError: If the value is not a string.
    """
    if isinstance(value, bool) or not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_bool(value: object, name: str) -> bool:
    """Return the value when it is a boolean.

    Raises:
        TypeError: If the value is not a boolean.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_int(value: object, name: str) -> int:
    """Return the value when it is an integer.

    Raises:
        TypeError: If the value is not an integer.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_callable(value: object, name: str) -> Application:
    """Return the value when it is callable.

    Raises:
        TypeError: If the value is not callable.
    """
    if not callable(value):
        raise TypeError(f"{name} must be callable, got {type(value).__name__}")
    return value


def _require_environment(value: object, name: str = "environ") -> Environment:
    """Return the environment of a request when it is a dictionary.

    The specification of the interface requires a plain dictionary, so a
    mapping of another type is refused.

    Raises:
        TypeError: If the value is not a dictionary.
    """
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict, got {type(value).__name__}")
    return value


def _require_keys(environ: Environment, keys: Sequence[str], name: str) -> None:
    """Raise when the environment of a request misses one of the keys.

    Raises:
        ValueError: If one of the keys is missing.
    """
    missing = [key for key in keys if key not in environ]
    if missing:
        raise ValueError(f"{name} is missing the key {', '.join(missing)}")


def _require_request_keys(environ: Environment) -> None:
    """Raise when the environment misses the keys a request URI is built from."""
    _require_keys(environ, ("wsgi.url_scheme",), "environ")
    if not environ.get("HTTP_HOST"):
        _require_keys(environ, ("SERVER_NAME", "SERVER_PORT"), "environ")


def setup_testing_defaults(environ: Environment) -> Environment:
    """Fill the environment of a request with the defaults of the standard library.

    The defaults are the ones a test needs: the name and the port of the
    server, the method of the request, the variables of the specification, and
    the streams of the request.  The settings that the environment already
    holds are kept, the way the standard library keeps them.

    Args:
        environ: The environment of a request.  It is changed in place.

    Returns:
        The environment of the request, so a caller can use the result.
    """
    environment = _require_environment(environ)
    _util.setup_testing_defaults(environment)
    return environment


def guess_scheme(environ: Environment) -> str:
    """Return the scheme of the request.

    Args:
        environ: The environment of a request.

    Returns:
        ``"https"`` when the environment reports a secure request, and
        ``"http"`` otherwise.
    """
    environment = _require_environment(environ)
    return _util.guess_scheme(environment)


def application_uri(environ: Environment) -> str:
    """Return the base URI of the application.

    The base URI holds the scheme, the host, the port, and the name of the
    script, but neither the path of the request nor its query string.

    Args:
        environ: The environment of a request.

    Returns:
        The base URI of the application.

    Raises:
        ValueError: If the environment misses one of the keys the URI is
            built from.
    """
    environment = _require_environment(environ)
    _require_request_keys(environment)
    return _util.application_uri(environment)


def request_uri(environ: Environment, include_query: bool = True) -> str:
    """Return the full URI of the request.

    Args:
        environ: The environment of a request.
        include_query: Whether the query string of the request is part of the
            URI.

    Returns:
        The URI of the request.

    Raises:
        ValueError: If the environment misses one of the keys the URI is
            built from.
    """
    environment = _require_environment(environ)
    query = _require_bool(include_query, "include_query")
    _require_request_keys(environment)
    return _util.request_uri(environment, query)


def shift_path_info(environ: Environment) -> Optional[str]:
    """Move the first segment of the path of the request to the name of the script.

    The environment is changed in place, the way the standard library changes
    it, so a caller that needs the original values keeps a copy of them.

    Args:
        environ: The environment of a request.  It is changed in place.

    Returns:
        The segment that was moved, or ``None`` when the path of the request
        is empty.
    """
    environment = _require_environment(environ)
    return _util.shift_path_info(environment)


def is_hop_by_hop(name: str) -> bool:
    """Report whether a header is a hop-by-hop header.

    A hop-by-hop header belongs to a single connection, so a proxy must not
    forward it.  The standard library provides the check from Python 3.9 on;
    the wrapper falls back to the list of RFC 2616, section 13.5.1, on the
    interpreters that do not ship it.

    Args:
        name: The name of the header.

    Returns:
        ``True`` when the header is a hop-by-hop header, ``False`` otherwise.
    """
    text = _require_str(name, "name").lower()
    checker = getattr(_util, "is_hop_by_hop", None)
    if checker is None:
        return text in HOP_BY_HOP_HEADERS
    return bool(checker(text))


def build_headers(items: Sequence[Tuple[str, str]]) -> Headers:
    """Build the collection of the headers of a response.

    Args:
        items: The headers of the response as a sequence of pairs of a name
            and a value.

    Returns:
        The collection of the headers.

    Raises:
        TypeError: If the items are not a sequence of pairs of strings.
        ValueError: If a name or a value holds a control character.
    """
    if isinstance(items, (str, bytes)) or not isinstance(items, (list, tuple)):
        raise TypeError(f"items must be a list or a tuple, got {type(items).__name__}")
    pairs: List[Tuple[str, str]] = []
    for item in items:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise TypeError("items entries must be pairs of a name and a value")
        name = _require_str(item[0], "header name")
        value = _require_str(item[1], "header value")
        pairs.append((name, value))
    return Headers(pairs)


def header_values(headers: Headers, name: str) -> List[str]:
    """Return every value of a header of a response.

    A header may appear more than once in a response, so the first value
    alone is often not enough.

    Args:
        headers: The collection of the headers of a response.
        name: The name of the header.

    Returns:
        The values of the header, in the order they were added.
    """
    collection = _require_headers(headers)
    text = _require_str(name, "name")
    return list(collection.get_all(text))


def encode_headers(headers: Headers) -> bytes:
    """Return the headers of a response in the form that is sent over the wire.

    Args:
        headers: The collection of the headers of a response.

    Returns:
        The headers of the response, every line ended by a carriage return
        and a line feed.
    """
    collection = _require_headers(headers)
    return bytes(collection)


def _require_headers(value: object) -> Headers:
    """Return the collection of the headers when it is one.

    Raises:
        TypeError: If the value is not a collection of the headers.
    """
    if not isinstance(value, Headers):
        raise TypeError(f"headers must be a Headers instance, got {type(value).__name__}")
    return value


def file_wrapper(stream: IO[bytes], block_size: int = 8192) -> Iterator[bytes]:
    """Return an iterator that reads a stream in blocks.

    The stream has to be opened in binary mode, because the iterator yields
    the bytes of the stream.

    Args:
        stream: The stream that is read.
        block_size: The number of bytes that are read at a time.

    Returns:
        An iterator over the bytes of the stream.

    Raises:
        TypeError: If the stream has no read method.
        ValueError: If the size of a block is not positive.
    """
    if not hasattr(stream, "read"):
        raise TypeError("stream must have a read method")
    size = _require_int(block_size, "block_size")
    if size <= 0:
        raise ValueError(f"block_size must be positive, got {size}")
    return iter(FileWrapper(stream, size))


def check_environ(environ: Environment) -> None:
    """Check the environment of a request against the specification.

    The check of the standard library reports the first problem of an
    environment by raising an :class:`AssertionError`.

    Args:
        environ: The environment of a request.

    Raises:
        AssertionError: If the environment does not follow the specification.
    """
    environment = _require_environment(environ)
    checker = getattr(_validate, "check_environ", None)
    if checker is None:  # pragma: no cover - the standard library always ships it
        raise RuntimeError(
            "the standard library of this interpreter does not provide "
            "wsgiref.validate.check_environ"
        )
    checker(environment)


def environ_errors(environ: Environment) -> List[str]:
    """Return the problems of the environment of a request.

    The standard library reports the first problem of an environment by
    raising an :class:`AssertionError`, and it reports the suspicious
    settings of an environment with a warning.  This helper collects both in
    a list, so a caller can report every problem of an environment at once.

    Args:
        environ: The environment of a request.

    Returns:
        The messages of the problems of the environment.  The list is empty
        when the environment follows the specification.
    """
    environment = _require_environment(environ)
    messages: List[str] = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            check_environ(environment)
        except AssertionError as error:
            messages.append(str(error))
    messages.extend(str(entry.message) for entry in caught)
    return messages


def validator(application: Application) -> Application:
    """Return the middleware that checks an application against the specification.

    The middleware does not change the request or the response, it raises an
    :class:`AssertionError` when the application breaks the specification.

    Args:
        application: The application that is checked.

    Returns:
        The middleware that checks the application.
    """
    checked = _require_callable(application, "application")
    return _validate.validator(checked)


def demo_app(environ: Environment, start_response: Application) -> List[bytes]:
    """Return the answer of the demonstration application of the standard library.

    The application answers with the variables of the environment of the
    request, so a caller sees what a server hands to an application.

    Args:
        environ: The environment of a request.
        start_response: The callable that starts the response.

    Returns:
        The body of the response.
    """
    environment = _require_environment(environ)
    responder = _require_callable(start_response, "start_response")
    return list(_simple_server.demo_app(environment, responder))


def make_server(
    host: str,
    port: int,
    app: Application,
    server_class: type = WSGIServer,
    handler_class: type = WSGIRequestHandler,
) -> WSGIServer:
    """Create a server that serves an application on a host and a port.

    The server is not started, the caller decides when it accepts requests
    and when it is closed.

    Args:
        host: The host the server listens on.  An empty string listens on
            every host of the machine.
        port: The port the server listens on.  The port zero lets the
            operating system choose a free port.
        app: The application the server serves.
        server_class: The class of the server.
        handler_class: The class of the handler of the requests.

    Returns:
        The server that serves the application.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If the port is outside the range of the ports.
    """
    address = _require_str(host, "host")
    number = _require_int(port, "port")
    if not 0 <= number <= 65535:
        raise ValueError(f"port must be between 0 and 65535, got {number}")
    application = _require_callable(app, "app")
    server = _require_class(server_class, "server_class")
    handler = _require_class(handler_class, "handler_class")
    return _simple_server.make_server(address, number, application, server, handler)


def _require_class(value: object, name: str) -> type:
    """Return the value when it is a class.

    Raises:
        TypeError: If the value is not a class.
    """
    if not isinstance(value, type):
        raise TypeError(f"{name} must be a class, got {type(value).__name__}")
    return value
