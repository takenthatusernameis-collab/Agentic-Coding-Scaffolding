"""XML-RPC utilities wrapping the standard library :mod:`xmlrpc` package.

The module covers both halves of the protocol: the client half
(:mod:`xmlrpc.client`) and the server half (:mod:`xmlrpc.server`).  Every
helper validates its arguments before the standard library is reached, so a
caller gets a clear ``TypeError`` or ``ValueError`` instead of a malformed
request.

The encoding helpers are pure computation and never touch the network.  The
helpers that would open a connection (``create_proxy``) or bind a socket
(``create_server``, ``create_multi_path_server``) only build the standard
library objects, so the caller stays in control of when a connection is
attempted.
"""

from __future__ import annotations

from typing import Any, Sequence
from xmlrpc import client as _client
from xmlrpc import server as _server

__all__: list[str] = [
    "Binary",
    "DateTime",
    "Error",
    "Fault",
    "Marshaller",
    "MultiCall",
    "MultiCallIterator",
    "ProtocolError",
    "ResponseError",
    "SafeTransport",
    "ServerProxy",
    "Transport",
    "Unmarshaller",
    "CGIXMLRPCRequestHandler",
    "MultiPathXMLRPCServer",
    "SimpleXMLRPCDispatcher",
    "SimpleXMLRPCRequestHandler",
    "SimpleXMLRPCServer",
    "build_request",
    "create_dispatcher",
    "create_marshaller",
    "create_multi_path_server",
    "create_proxy",
    "create_server",
    "create_transport",
    "dumps_value",
    "list_public_methods",
    "loads_value",
    "marshal_params",
    "parse_method_call",
    "parse_method_response",
    "register_function",
    "register_instance",
    "register_introspection_functions",
    "register_multicall_functions",
    "resolve_dotted_attribute",
    "unmarshal_params",
]

Error = _client.Error
Fault = _client.Fault
ProtocolError = _client.ProtocolError
ResponseError = _client.ResponseError
Binary = _client.Binary
DateTime = _client.DateTime
Marshaller = _client.Marshaller
Unmarshaller = _client.Unmarshaller
Transport = _client.Transport
SafeTransport = _client.SafeTransport
ServerProxy = _client.ServerProxy
MultiCall = _client.MultiCall
MultiCallIterator = _client.MultiCallIterator

SimpleXMLRPCServer = _server.SimpleXMLRPCServer
MultiPathXMLRPCServer = _server.MultiPathXMLRPCServer
SimpleXMLRPCRequestHandler = _server.SimpleXMLRPCRequestHandler
CGIXMLRPCRequestHandler = _server.CGIXMLRPCRequestHandler
SimpleXMLRPCDispatcher = _server.SimpleXMLRPCDispatcher


def _require_params(params: object) -> tuple[Any, ...]:
    """Return *params* as a tuple of XML-RPC arguments."""
    if isinstance(params, (str, bytes, bytearray)):
        raise TypeError("params must be a list or tuple, not a string")
    if not isinstance(params, (list, tuple)):
        raise TypeError(f"params must be a list or tuple, got {type(params).__name__}")
    return tuple(params)


def _require_document(document: object) -> str | bytes:
    """Return *document* as the text or bytes of an XML-RPC document."""
    if isinstance(document, (str, bytes, bytearray)):
        return bytes(document) if isinstance(document, bytearray) else document
    raise TypeError(f"document must be a str or bytes, got {type(document).__name__}")


def _require_name(name: object, label: str) -> str:
    """Return *name* when it is a usable, non-empty identifier."""
    if not isinstance(name, str):
        raise TypeError(f"{label} must be a str, got {type(name).__name__}")
    if not name:
        raise ValueError(f"{label} must not be empty")
    return name


def _require_bool(value: object, label: str) -> bool:
    """Return *value* when it is a boolean."""
    if not isinstance(value, bool):
        raise TypeError(f"{label} must be a bool, got {type(value).__name__}")
    return value


def dumps_value(
    params: Sequence[Any],
    methodname: str | None = None,
    methodresponse: bool | None = None,
    encoding: str | None = None,
    allow_none: bool = False,
) -> str:
    """Encode XML-RPC arguments into a request or response document.

    Args:
        params: The arguments of the call or the result of the response.
        methodname: The name of the method being called.
        methodresponse: Whether the document is a response.
        encoding: The text encoding of the document.
        allow_none: Whether ``None`` may be marshalled.

    Returns:
        The encoded document.
    """
    values = _require_params(params)
    if methodname is not None:
        _require_name(methodname, "methodname")
    if methodresponse is not None:
        _require_bool(methodresponse, "methodresponse")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    _require_bool(allow_none, "allow_none")
    if methodresponse and len(values) != 1:
        raise ValueError("a response document must carry exactly one value")
    return _client.dumps(
        values,
        methodname=methodname,
        methodresponse=methodresponse,
        encoding=encoding,
        allow_none=allow_none,
    )


def loads_value(
    document: str | bytes,
    use_datetime: bool = False,
    use_builtin_types: bool = False,
) -> tuple[tuple[Any, ...], str | None]:
    """Decode an XML-RPC document into its arguments and method name.

    Args:
        document: The document to decode.
        use_datetime: Whether dates are decoded as ``datetime`` objects.
        use_builtin_types: Whether binary and date values use builtin types.

    Returns:
        A tuple of the decoded arguments and the method name.  The method name
        is ``None`` for a response document.
    """
    payload = _require_document(document)
    _require_bool(use_datetime, "use_datetime")
    _require_bool(use_builtin_types, "use_builtin_types")
    params, methodname = _client.loads(
        payload,
        use_datetime=use_datetime,
        use_builtin_types=use_builtin_types,
    )
    return params, methodname


def build_request(methodname: str, params: Sequence[Any] = ()) -> str:
    """Build an XML-RPC method call document.

    Args:
        methodname: The name of the method to call.
        params: The arguments of the call.

    Returns:
        The encoded method call document.
    """
    name = _require_name(methodname, "methodname")
    values = _require_params(params)
    return _client.dumps(values, methodname=name)


def parse_method_call(document: str | bytes) -> tuple[str, tuple[Any, ...]]:
    """Parse an XML-RPC method call document.

    Args:
        document: The method call document.

    Returns:
        A tuple of the method name and the call arguments.
    """
    payload = _require_document(document)
    params, methodname = _client.loads(payload)
    if not methodname:
        raise ValueError("document does not contain a method call")
    return methodname, params


def parse_method_response(document: str | bytes) -> tuple[Any, ...]:
    """Parse an XML-RPC method response document.

    Args:
        document: The method response document.

    Returns:
        The result of the call.

    Raises:
        Fault: When the document carries a fault instead of a result.
    """
    payload = _require_document(document)
    params, methodname = _client.loads(payload)
    if methodname:
        raise ValueError("document contains a method call, not a method response")
    return params


def marshal_params(params: Sequence[Any]) -> str:
    """Encode XML-RPC arguments as a ``<params>`` document.

    Args:
        params: The arguments to encode.

    Returns:
        The encoded ``<params>`` document.
    """
    values = _require_params(params)
    marshaller = _client.Marshaller()
    return marshaller.dumps(values)


def unmarshal_params(document: str | bytes) -> tuple[Any, ...]:
    """Decode a ``<params>`` document into its arguments.

    Args:
        document: The document to decode.

    Returns:
        The decoded arguments.
    """
    payload = _require_document(document)
    params, _methodname = _client.loads(payload)
    return params


def create_marshaller(encoding: str | None = None, allow_none: bool = False) -> Marshaller:
    """Create a marshaller for XML-RPC values.

    Args:
        encoding: The text encoding of the produced documents.
        allow_none: Whether ``None`` may be marshalled.
    """
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    _require_bool(allow_none, "allow_none")
    return _client.Marshaller(encoding=encoding, allow_none=allow_none)


def create_transport(
    use_datetime: bool = False,
    use_builtin_types: bool = False,
    *,
    headers: Sequence[tuple[str, str]] = (),
) -> Transport:
    """Create the transport used by a client proxy.

    Args:
        use_datetime: Whether dates are decoded as ``datetime`` objects.
        use_builtin_types: Whether binary and date values use builtin types.
        headers: Extra HTTP headers sent with every request.
    """
    _require_bool(use_datetime, "use_datetime")
    _require_bool(use_builtin_types, "use_builtin_types")
    if not isinstance(headers, (list, tuple)):
        raise TypeError(f"headers must be a list or tuple, got {type(headers).__name__}")
    return _client.Transport(
        use_datetime=use_datetime,
        use_builtin_types=use_builtin_types,
        headers=tuple(headers),
    )


def create_proxy(
    uri: str,
    transport: Transport | None = None,
    encoding: str | None = None,
    verbose: bool = False,
    allow_none: bool = False,
    use_datetime: bool = False,
    use_builtin_types: bool = False,
    *,
    headers: Sequence[tuple[str, str]] = (),
    context: Any = None,
) -> ServerProxy:
    """Create a client proxy for an XML-RPC server.

    The proxy is lazy: no connection is opened until a remote method is
    called.

    Args:
        uri: The URI of the server.
        transport: The transport used for the requests.
        encoding: The text encoding of the requests.
        verbose: Whether the requests are logged.
        allow_none: Whether ``None`` may be sent.
        use_datetime: Whether dates are decoded as ``datetime`` objects.
        use_builtin_types: Whether binary and date values use builtin types.
        headers: Extra HTTP headers sent with every request.
        context: The SSL context used for an ``https`` URI.
    """
    _require_name(uri, "uri")
    if transport is not None and not isinstance(transport, Transport):
        raise TypeError(f"transport must be a Transport or None, got {type(transport).__name__}")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    _require_bool(verbose, "verbose")
    _require_bool(allow_none, "allow_none")
    _require_bool(use_datetime, "use_datetime")
    _require_bool(use_builtin_types, "use_builtin_types")
    if not isinstance(headers, (list, tuple)):
        raise TypeError(f"headers must be a list or tuple, got {type(headers).__name__}")
    return _client.ServerProxy(
        uri,
        transport=transport,
        encoding=encoding,
        verbose=verbose,
        allow_none=allow_none,
        use_datetime=use_datetime,
        use_builtin_types=use_builtin_types,
        headers=tuple(headers),
        context=context,
    )


def create_dispatcher(
    allow_none: bool = False,
    encoding: str | None = None,
    use_builtin_types: bool = False,
) -> SimpleXMLRPCDispatcher:
    """Create a dispatcher that maps remote calls onto local callables.

    The dispatcher is a plain mixin and does not open a socket, so it can be
    exercised without a server.

    Args:
        allow_none: Whether ``None`` may be sent.
        encoding: The text encoding of the responses.
        use_builtin_types: Whether binary and date values use builtin types.
    """
    _require_bool(allow_none, "allow_none")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    _require_bool(use_builtin_types, "use_builtin_types")
    return _server.SimpleXMLRPCDispatcher(
        allow_none=allow_none,
        encoding=encoding,
        use_builtin_types=use_builtin_types,
    )


def _require_dispatcher(dispatcher: object) -> SimpleXMLRPCDispatcher:
    """Return *dispatcher* when it is a dispatcher of the standard library."""
    if not isinstance(dispatcher, SimpleXMLRPCDispatcher):
        raise TypeError(
            f"dispatcher must be a SimpleXMLRPCDispatcher, got {type(dispatcher).__name__}"
        )
    return dispatcher


def register_function(
    dispatcher: SimpleXMLRPCDispatcher,
    function: Any = None,
    name: str | None = None,
) -> None:
    """Register a callable so that it can be called remotely.

    Args:
        dispatcher: The dispatcher the function is registered with.
        function: The callable to register.
        name: The name the function is registered under.
    """
    _require_dispatcher(dispatcher)
    if function is not None and not callable(function):
        raise TypeError(f"function must be callable or None, got {type(function).__name__}")
    if name is not None:
        _require_name(name, "name")
    dispatcher.register_function(function, name)


def register_instance(
    dispatcher: SimpleXMLRPCDispatcher,
    instance: Any,
    allow_dotted_names: bool = False,
) -> None:
    """Register an object so that its methods can be called remotely.

    Args:
        dispatcher: The dispatcher the instance is registered with.
        instance: The object to register.
        allow_dotted_names: Whether dotted method names are allowed.
    """
    _require_dispatcher(dispatcher)
    if instance is None:
        raise ValueError("instance must not be None")
    _require_bool(allow_dotted_names, "allow_dotted_names")
    dispatcher.register_instance(instance, allow_dotted_names)


def register_introspection_functions(dispatcher: SimpleXMLRPCDispatcher) -> None:
    """Register the ``system.*`` introspection methods with a dispatcher."""
    _require_dispatcher(dispatcher)
    dispatcher.register_introspection_functions()


def register_multicall_functions(dispatcher: SimpleXMLRPCDispatcher) -> None:
    """Register the ``system.multicall`` method with a dispatcher."""
    _require_dispatcher(dispatcher)
    dispatcher.register_multicall_functions()


def resolve_dotted_attribute(obj: Any, attr: str, allow_dotted_names: bool = True) -> Any:
    """Resolve a possibly dotted attribute path on *obj*.

    Args:
        obj: The object the attribute is resolved on.
        attr: The attribute path.
        allow_dotted_names: Whether dotted names are resolved step by step.

    Returns:
        The resolved attribute.
    """
    if obj is None:
        raise ValueError("obj must not be None")
    _require_name(attr, "attr")
    _require_bool(allow_dotted_names, "allow_dotted_names")
    return _server.resolve_dotted_attribute(obj, attr, allow_dotted_names)


def list_public_methods(obj: Any) -> list[str]:
    """Return the public methods of *obj*.

    Args:
        obj: The object to inspect.
    """
    if obj is None:
        raise ValueError("obj must not be None")
    return _server.list_public_methods(obj)


def create_server(
    addr: tuple[str, int],
    request_handler: type[SimpleXMLRPCRequestHandler] = SimpleXMLRPCRequestHandler,
    log_requests: bool = True,
    allow_none: bool = False,
    encoding: str | None = None,
    bind_and_activate: bool = True,
    use_builtin_types: bool = False,
) -> SimpleXMLRPCServer:
    """Create an XML-RPC server bound to *addr*.

    The server binds its socket unless ``bind_and_activate`` is false, so the
    caller stays in control of when the port is opened.

    Args:
        addr: The ``(host, port)`` address the server listens on.
        request_handler: The request handler class.
        log_requests: Whether requests are logged.
        allow_none: Whether ``None`` may be sent.
        encoding: The text encoding of the responses.
        bind_and_activate: Whether the socket is bound immediately.
        use_builtin_types: Whether binary and date values use builtin types.
    """
    if not isinstance(addr, tuple) or len(addr) != 2:
        raise TypeError("addr must be a (host, port) tuple")
    if not isinstance(addr[0], str):
        raise TypeError(f"addr host must be a str, got {type(addr[0]).__name__}")
    if not isinstance(addr[1], int) or isinstance(addr[1], bool):
        raise TypeError(f"addr port must be an int, got {type(addr[1]).__name__}")
    if not 0 <= addr[1] <= 65535:
        raise ValueError(f"addr port must be between 0 and 65535, got {addr[1]}")
    if not isinstance(request_handler, type) or not issubclass(
        request_handler, SimpleXMLRPCRequestHandler
    ):
        raise TypeError("request_handler must be a SimpleXMLRPCRequestHandler subclass")
    _require_bool(log_requests, "log_requests")
    _require_bool(allow_none, "allow_none")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    _require_bool(bind_and_activate, "bind_and_activate")
    _require_bool(use_builtin_types, "use_builtin_types")
    return _server.SimpleXMLRPCServer(
        addr,
        requestHandler=request_handler,
        logRequests=log_requests,
        allow_none=allow_none,
        encoding=encoding,
        bind_and_activate=bind_and_activate,
        use_builtin_types=use_builtin_types,
    )


def create_multi_path_server(
    addr: tuple[str, int],
    paths: Any,
    request_handler: type[SimpleXMLRPCRequestHandler] = SimpleXMLRPCRequestHandler,
    log_requests: bool = True,
    allow_none: bool = False,
    encoding: str | None = None,
    bind_and_activate: bool = True,
    use_builtin_types: bool = False,
) -> MultiPathXMLRPCServer:
    """Create an XML-RPC server that dispatches on the request path.

    Args:
        addr: The ``(host, port)`` address the server listens on.
        paths: A mapping of request paths onto dispatchers.
        request_handler: The request handler class.
        log_requests: Whether requests are logged.
        allow_none: Whether ``None`` may be sent.
        encoding: The text encoding of the responses.
        bind_and_activate: Whether the socket is bound immediately.
        use_builtin_types: Whether binary and date values use builtin types.
    """
    if not isinstance(addr, tuple) or len(addr) != 2:
        raise TypeError("addr must be a (host, port) tuple")
    if not isinstance(addr[0], str):
        raise TypeError(f"addr host must be a str, got {type(addr[0]).__name__}")
    if not isinstance(addr[1], int) or isinstance(addr[1], bool):
        raise TypeError(f"addr port must be an int, got {type(addr[1]).__name__}")
    if not 0 <= addr[1] <= 65535:
        raise ValueError(f"addr port must be between 0 and 65535, got {addr[1]}")
    if paths is None:
        raise ValueError("paths must not be None")
    if not isinstance(request_handler, type) or not issubclass(
        request_handler, SimpleXMLRPCRequestHandler
    ):
        raise TypeError("request_handler must be a SimpleXMLRPCRequestHandler subclass")
    _require_bool(log_requests, "log_requests")
    _require_bool(allow_none, "allow_none")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    _require_bool(bind_and_activate, "bind_and_activate")
    _require_bool(use_builtin_types, "use_builtin_types")
    return _server.MultiPathXMLRPCServer(
        addr,
        requestHandler=request_handler,
        logRequests=log_requests,
        allow_none=allow_none,
        encoding=encoding,
        bind_and_activate=bind_and_activate,
        use_builtin_types=use_builtin_types,
    )
