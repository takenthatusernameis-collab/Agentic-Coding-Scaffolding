"""CGI utilities wrapping the standard library :mod:`cgi`."""

from __future__ import annotations

from collections.abc import Callable
from html import escape as _html_escape
from typing import Any
from urllib.parse import parse_qs as _parse_qs
from urllib.parse import parse_qsl as _parse_qsl

try:
    import cgi as _cgi
    _CGI_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when cgi is unavailable
    _cgi = None  # type: ignore[assignment]
    _CGI_AVAILABLE = False

__all__: list[str] = [
    "FieldStorage",
    "MiniFieldStorage",
    "escape",
    "parse",
    "parse_header",
    "parse_multipart",
    "parse_qs",
    "parse_qsl",
    "is_available",
]


def escape(s: Any, quote: bool = True) -> str:
    if hasattr(_cgi, "escape"):
        try:
            return _cgi.escape(s, quote)  # type: ignore[attr-defined,no-any-return]
        except Exception:
            pass
    return _html_escape(str(s), quote)


if _CGI_AVAILABLE:
    FieldStorage = _cgi.FieldStorage
    MiniFieldStorage = _cgi.MiniFieldStorage
    parse_header: Callable[..., Any] = _cgi.parse_header
    parse_multipart: Callable[..., Any] = getattr(
        _cgi, "parse_multipart", lambda *args, **kwargs: {}
    )
else:  # pragma: no cover - exercised when cgi is unavailable
    class FieldStorage:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("cgi module is not available")

    class MiniFieldStorage(FieldStorage):  # type: ignore[no-redef]
        pass

    def parse_header(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        raise RuntimeError("cgi module is not available")

    def parse_multipart(*args: Any, **kwargs: Any) -> Any:  # type: ignore[no-redef]
        raise RuntimeError("cgi module is not available")


parse = getattr(_cgi, "parse", _parse_qs)
parse_qs = _parse_qs
parse_qsl = _parse_qsl


def is_available() -> bool:
    """Return True if the standard library :mod:`cgi` module is available."""
    return _CGI_AVAILABLE
