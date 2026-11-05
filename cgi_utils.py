"""CGI utilities wrapping the standard library :mod:`cgi`."""

from __future__ import annotations

import cgi as _cgi
from html import escape as _html_escape
from urllib.parse import parse_qs as _parse_qs
from urllib.parse import parse_qsl as _parse_qsl
from typing import Any

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

FieldStorage = _cgi.FieldStorage
MiniFieldStorage = _cgi.MiniFieldStorage


def escape(s, quote: bool = True):  # type: ignore[no-untyped-def]
    if hasattr(_cgi, "escape"):
        try:
            return _cgi.escape(s, quote)  # type: ignore[attr-defined]
        except Exception:
            pass
    return _html_escape(str(s), quote)


parse = getattr(_cgi, "parse", _parse_qs)
parse_header = _cgi.parse_header
parse_multipart = getattr(_cgi, "parse_multipart", lambda *a, **k: {})
parse_qs = _parse_qs
parse_qsl = _parse_qsl


def is_available() -> bool:
    """Return True if the standard library :mod:`cgi` module is available."""
    return True
