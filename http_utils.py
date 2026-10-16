"""HTTP utility functions for status codes and response handling."""

from typing import Dict, Optional

# HTTP status code category prefixes (1xx through 5xx)
HTTP_INFORMATIONAL = 1
HTTP_SUCCESS = 2
HTTP_REDIRECTION = 3
HTTP_CLIENT_ERROR = 4
HTTP_SERVER_ERROR = 5


STATUS_CODES: Dict[int, str] = {
    # 1xx Informational
    100: "Continue",
    101: "Switching Protocols",
    102: "Processing",
    # 2xx Success
    200: "OK",
    201: "Created",
    202: "Accepted",
    203: "Non-Authoritative Information",
    204: "No Content",
    205: "Reset Content",
    206: "Partial Content",
    207: "Multi-Status",
    # 3xx Redirection
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    305: "Use Proxy",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    # 4xx Client Error
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    411: "Length Required",
    412: "Precondition Failed",
    413: "Payload Too Large",
    414: "URI Too Long",
    415: "Unsupported Media Type",
    416: "Range Not Satisfiable",
    417: "Expectation Failed",
    418: "I'm a teapot",
    421: "Misdirected Request",
    422: "Unprocessable Entity",
    423: "Locked",
    424: "Failed Dependency",
    425: "Too Early",
    426: "Upgrade Required",
    428: "Precondition Required",
    429: "Too Many Requests",
    431: "Request Header Fields Too Large",
    451: "Unavailable For Legal Reasons",
    # 5xx Server Error
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    505: "HTTP Version Not Supported",
    506: "Variant Also Negotiates",
    507: "Insufficient Storage",
    508: "Loop Detected",
    510: "Not Extended",
    511: "Network Authentication Required",
}


def status_code_category(code: int) -> int:
    """Return the HTTP status code category (1-5) for a given code.

    Args:
        code: The HTTP status code.

    Returns:
        The leading digit of the status code (1 through 5).
    """
    return code // 100


def status_message(code: int) -> Optional[str]:
    """Return the standard reason phrase for an HTTP status code.

    Args:
        code: The HTTP status code.

    Returns:
        The standard reason phrase, or ``None`` if the code is unknown.
    """
    return STATUS_CODES.get(code)


def is_informational(code: int) -> bool:
    """Return ``True`` if the status code is a 1xx informational response."""
    return status_code_category(code) == HTTP_INFORMATIONAL


def is_success(code: int) -> bool:
    """Return ``True`` if the status code is a 2xx success response."""
    return status_code_category(code) == HTTP_SUCCESS


def is_redirection(code: int) -> bool:
    """Return ``True`` if the status code is a 3xx redirection response."""
    return status_code_category(code) == HTTP_REDIRECTION


def is_client_error(code: int) -> bool:
    """Return ``True`` if the status code is a 4xx client error response."""
    return status_code_category(code) == HTTP_CLIENT_ERROR


def is_server_error(code: int) -> bool:
    """Return ``True`` if the status code is a 5xx server error response."""
    return status_code_category(code) == HTTP_SERVER_ERROR


def is_error(code: int) -> bool:
    """Return ``True`` if the status code is a 4xx or 5xx error response."""
    category = status_code_category(code)
    return category in (HTTP_CLIENT_ERROR, HTTP_SERVER_ERROR)
