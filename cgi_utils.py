"""CGI utilities wrapping the standard library :mod:`cgi` module.

This wrapper provides utilities for parsing CGI forms and headers.
It validates arguments before passing them to the standard library and adds
conveniences where helpful.

.. note::

   The :mod:`cgi` module was deprecated in Python 3.11 and removed in
   Python 3.13 as part of :pep:`594`. The import below degrades gracefully:
   when the interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, List, Optional, Tuple, cast

__all__ = [
    "FieldStorage",
    "MiniFieldStorage",
    "escape",
    "is_available",
    "parse",
    "parse_header",
    "parse_multipart",
    "parse_qs",
    "parse_qsl",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import cgi as _cgi
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _cgi = None  # type: ignore[assignment]

# ``cgi.parse_qs`` and ``cgi.parse_qsl`` were only added in Python 3.13, so on
# the interpreters that still ship the ``cgi`` module the helpers fall back to
# the equivalent functions of :mod:`urllib.parse`, which share the signature.
try:
    import urllib.parse as _urlparse
except ImportError:  # pragma: no cover - urllib.parse is part of the core
    _urlparse = None  # type: ignore[assignment]


def _parse_qs(qs: str, keep_blank_values: int = 0, strict_parsing: int = 0,
              encoding: str = "utf-8", errors: str = "replace",
              max_num_fields: Optional[int] = None,
              separator: str = "&") -> Dict[str, List[str]]:
    """Parse a query string into a dictionary, preferring ``cgi`` when present."""
    module = _cgi_module()
    func = getattr(module, "parse_qs", None)
    if func is not None:
        try:
            return cast(Dict[str, List[str]], func(
                qs, keep_blank_values=keep_blank_values,
                strict_parsing=strict_parsing, encoding=encoding,
                errors=errors, max_num_fields=max_num_fields, separator=separator,
            ))
        except TypeError:
            return cast(Dict[str, List[str]], func(
                qs, keep_blank_values=keep_blank_values,
                strict_parsing=strict_parsing,
            ))
    if _urlparse is None:  # pragma: no cover - urllib.parse is always present
        raise RuntimeError(
            "neither 'cgi.parse_qs' nor 'urllib.parse.parse_qs' is available"
        )
    return cast(Dict[str, List[str]], _urlparse.parse_qs(
        qs, keep_blank_values=bool(keep_blank_values),
        strict_parsing=bool(strict_parsing), encoding=encoding,
        errors=errors, max_num_fields=max_num_fields, separator=separator,
    ))


def _parse_qsl(qs: str, keep_blank_values: int = 0, strict_parsing: int = 0,
               encoding: str = "utf-8", errors: str = "replace",
               max_num_fields: Optional[int] = None,
               separator: str = "&") -> List[Tuple[str, str]]:
    """Parse a query string into a list of tuples, preferring ``cgi`` when present."""
    module = _cgi_module()
    func = getattr(module, "parse_qsl", None)
    if func is not None:
        try:
            return cast(List[Tuple[str, str]], func(
                qs, keep_blank_values=keep_blank_values,
                strict_parsing=strict_parsing, encoding=encoding,
                errors=errors, max_num_fields=max_num_fields, separator=separator,
            ))
        except TypeError:
            return cast(List[Tuple[str, str]], func(
                qs, keep_blank_values=keep_blank_values,
                strict_parsing=strict_parsing,
            ))
    if _urlparse is None:  # pragma: no cover - urllib.parse is always present
        raise RuntimeError(
            "neither 'cgi.parse_qsl' nor 'urllib.parse.parse_qsl' is available"
        )
    return cast(List[Tuple[str, str]], _urlparse.parse_qsl(
        qs, keep_blank_values=bool(keep_blank_values),
        strict_parsing=bool(strict_parsing), encoding=encoding,
        errors=errors, max_num_fields=max_num_fields, separator=separator,
    ))


def _cgi_module() -> Any:
    """Return the standard library ``cgi`` module."""
    if _cgi is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'cgi' module was removed in Python 3.13; "
            "use html.parser, urllib.parse, and email.parser instead"
        )
    return _cgi


def is_available() -> bool:
    """Return whether the standard library :mod:`cgi` module is available."""
    return _cgi is not None


# Re-export classes if available
if _cgi is not None:
    FieldStorage = _cgi.FieldStorage
    MiniFieldStorage = _cgi.MiniFieldStorage
else:  # pragma: no cover
    class FieldStorage:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _cgi_module()

    class MiniFieldStorage:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _cgi_module()


def parse(fp: Any = None, environ: Optional[Dict[str, str]] = None,
          keep_blank_values: int = 0, strict_parsing: int = 0,
          separator: str = "&") -> Dict[str, List[Any]]:
    """Parse a query string or form data."""
    _require_mapping_or_none(environ, "environ")
    if not isinstance(keep_blank_values, int) or isinstance(keep_blank_values, bool):
        raise TypeError("keep_blank_values must be an int")
    if not isinstance(strict_parsing, int) or isinstance(strict_parsing, bool):
        raise TypeError("strict_parsing must be an int")
    if not isinstance(separator, str):
        raise TypeError("separator must be a str")
    module = _cgi_module()
    result = module.parse(
        fp,
        environ=environ,
        keep_blank_values=keep_blank_values,
        strict_parsing=strict_parsing,
        separator=separator,
    )
    return cast(Dict[str, List[Any]], result)


def parse_qs(qs: Any, keep_blank_values: int = 0, strict_parsing: int = 0,
            encoding: str = "utf-8", errors: str = "replace",
            max_num_fields: Optional[int] = None, separator: str = "&") -> Dict[str, List[str]]:
    """Parse a query string and return a dictionary."""
    qs = _require_text(qs, "qs")
    if not isinstance(keep_blank_values, int) or isinstance(keep_blank_values, bool):
        raise TypeError("keep_blank_values must be an int")
    if not isinstance(strict_parsing, int) or isinstance(strict_parsing, bool):
        raise TypeError("strict_parsing must be an int")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a str")
    if not isinstance(errors, str):
        raise TypeError("errors must be a str")
    if max_num_fields is not None:
        if not isinstance(max_num_fields, int) or isinstance(max_num_fields, bool):
            raise TypeError("max_num_fields must be an int or None")
        if max_num_fields < 1:
            raise ValueError("max_num_fields must be at least 1")
    if not isinstance(separator, str):
        raise TypeError("separator must be a str")
    return _parse_qs(
        qs, keep_blank_values=keep_blank_values, strict_parsing=strict_parsing,
        encoding=encoding, errors=errors, max_num_fields=max_num_fields,
        separator=separator,
    )


def parse_qsl(qs: Any, keep_blank_values: int = 0, strict_parsing: int = 0,
              encoding: str = "utf-8", errors: str = "replace",
              max_num_fields: Optional[int] = None, separator: str = "&") -> List[Tuple[str, str]]:
    """Parse a query string and return a list of tuples."""
    qs = _require_text(qs, "qs")
    if not isinstance(keep_blank_values, int) or isinstance(keep_blank_values, bool):
        raise TypeError("keep_blank_values must be an int")
    if not isinstance(strict_parsing, int) or isinstance(strict_parsing, bool):
        raise TypeError("strict_parsing must be an int")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a str")
    if not isinstance(errors, str):
        raise TypeError("errors must be a str")
    if max_num_fields is not None:
        if not isinstance(max_num_fields, int) or isinstance(max_num_fields, bool):
            raise TypeError("max_num_fields must be an int or None")
        if max_num_fields < 1:
            raise ValueError("max_num_fields must be at least 1")
    if not isinstance(separator, str):
        raise TypeError("separator must be a str")
    return _parse_qsl(
        qs, keep_blank_values=keep_blank_values, strict_parsing=strict_parsing,
        encoding=encoding, errors=errors, max_num_fields=max_num_fields,
        separator=separator,
    )


def parse_header(line: Any) -> Tuple[str, Dict[str, str]]:
    """Parse a MIME header line."""
    line = _require_text(line, "line")
    module = _cgi_module()
    return cast(Tuple[str, Dict[str, str]], module.parse_header(line))


def parse_multipart(fp: Any, pdict: Dict[str, Any], encoding: str = "utf-8",
                    errors: str = "replace", separator: str = "&") -> Dict[str, List[Any]]:
    """Parse multipart/form-data."""
    if not isinstance(pdict, dict):
        raise TypeError("pdict must be a dict")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a str")
    if not isinstance(errors, str):
        raise TypeError("errors must be a str")
    if not isinstance(separator, str):
        raise TypeError("separator must be a str")
    module = _cgi_module()
    try:
        result = module.parse_multipart(
            fp, pdict, encoding=encoding, errors=errors, separator=separator
        )
        return cast(Dict[str, List[Any]], result)
    except TypeError:
        result = module.parse_multipart(fp, pdict)
        return cast(Dict[str, List[Any]], result)


def escape(s: Any, quote: bool = False) -> str:
    """Replace special characters in HTML."""
    if not isinstance(s, str):
        raise TypeError(f"s must be a str, got {type(s).__name__}")
    if not isinstance(quote, bool):
        raise TypeError("quote must be a bool")
    try:
        import html as _html
        if quote:
            return _html.escape(s, quote=True)
        return _html.escape(s, quote=False)
    except Exception:
        module = _cgi_module()
        return cast(str, module.escape(s, quote=quote))


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_mapping_or_none(value: Any, name: str) -> Optional[Dict[str, str]]:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict or None, got {type(value).__name__}")
    return value
