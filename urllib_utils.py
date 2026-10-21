"""URL parsing utilities wrapping the standard library :mod:`urllib.parse` module.

The :mod:`urllib.parse` module takes URLs apart and puts them back together:
it splits a URL into its scheme, netloc, path, parameters, query, and fragment,
joins a base URL with a relative reference, and percent-encodes and decodes
query strings and form data.

Every helper validates its arguments before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure.  The wrappers are pure computation: they never open a network
connection.
"""

from __future__ import annotations

import urllib.parse as _urllib_parse
from typing import Any, Mapping, Optional, Sequence, Tuple, Union, cast

__all__: list[str] = [
    "defrag",
    "join_url",
    "parse_qs",
    "parse_qsl",
    "parse_url",
    "quote",
    "quote_plus",
    "unquote",
    "unquote_plus",
    "unquote_to_bytes",
    "urlencode",
    "urlsplit",
    "urlunsplit",
]

#: The characters that :func:`quote` leaves untouched by default.
_DEFAULT_SAFE = "/"

#: The encoding used to turn text into bytes before percent-encoding.
_DEFAULT_ENCODING = "utf-8"


def _require_str(value: object, name: str) -> str:
    """Return *value* when it is a string.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The string value.

    Raises:
        TypeError: If the value is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_mapping_or_pairs(
    value: object, name: str
) -> Union[Mapping[str, Any], Sequence[Tuple[str, Any]]]:
    """Return *value* when it is a mapping or a sequence of pairs.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value unchanged.

    Raises:
        TypeError: If the value is not a mapping or a sequence of pairs.
    """
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{name} must be a mapping or a sequence of pairs, not a single string")
    if isinstance(value, Mapping):
        return value
    if isinstance(value, Sequence):
        for entry in value:
            if not isinstance(entry, (tuple, list)) or len(entry) != 2:
                raise TypeError(f"{name} entries must be pairs of two items, got {entry!r}")
            key, item = entry
            if not isinstance(key, str):
                raise TypeError(f"{name} keys must be strings, got {type(key).__name__}")
        return value
    raise TypeError(f"{name} must be a mapping or a sequence of pairs, got {type(value).__name__}")


def parse_url(url: str) -> _urllib_parse.ParseResult:
    """Split a URL into its components.

    Args:
        url: The URL to split.

    Returns:
        The parsed components of the URL.

    Raises:
        TypeError: If *url* is not a string.
    """
    _require_str(url, "url")
    return _urllib_parse.urlparse(url)


def build_url(components: Sequence[str]) -> str:
    """Build a URL from its components.

    Args:
        components: The scheme, netloc, path, parameters, query, and fragment
            of the URL.

    Returns:
        The assembled URL.

    Raises:
        TypeError: If *components* is not a sequence of strings.
        ValueError: If *components* does not hold exactly six items.
    """
    if isinstance(components, str):
        raise TypeError("components must be a sequence of strings, not a single string")
    if not isinstance(components, (list, tuple)) or len(components) != 6:
        raise ValueError("components must hold exactly six items")
    for index, item in enumerate(components):
        if not isinstance(item, str):
            raise TypeError(f"components entry {index} must be a str, got {type(item).__name__}")
    return cast(str, _urllib_parse.urlunparse(tuple(components)))


def urlsplit(url: str) -> _urllib_parse.SplitResult:
    """Split a URL into its components without separating the parameters.

    Args:
        url: The URL to split.

    Returns:
        The split components of the URL.

    Raises:
        TypeError: If *url* is not a string.
    """
    _require_str(url, "url")
    return _urllib_parse.urlsplit(url)


def urlunsplit(components: Sequence[str]) -> str:
    """Build a URL from its split components.

    Args:
        components: The scheme, netloc, path, query, and fragment of the URL.

    Returns:
        The assembled URL.

    Raises:
        TypeError: If *components* is not a sequence of strings.
        ValueError: If *components* does not hold exactly five items.
    """
    if isinstance(components, str):
        raise TypeError("components must be a sequence of strings, not a single string")
    if not isinstance(components, (list, tuple)) or len(components) != 5:
        raise ValueError("components must hold exactly five items")
    for index, item in enumerate(components):
        if not isinstance(item, str):
            raise TypeError(f"components entry {index} must be a str, got {type(item).__name__}")
    return cast(str, _urllib_parse.urlunsplit(tuple(components)))


def join_url(base: str, url: str) -> str:
    """Join a base URL with a relative URL.

    Args:
        base: The base URL.
        url: The relative URL to resolve against the base.

    Returns:
        The absolute URL.

    Raises:
        TypeError: If an argument is not a string.
    """
    base_text = _require_str(base, "base")
    url_text = _require_str(url, "url")
    return _urllib_parse.urljoin(base_text, url_text)


def quote(
    text: str,
    safe: str = _DEFAULT_SAFE,
    encoding: str = _DEFAULT_ENCODING,
    errors: str = "replace",
) -> str:
    """Percent-encode a string.

    Args:
        text: The string to encode.
        safe: The ASCII characters that should never be encoded.
        encoding: The encoding used to turn the string into bytes.
        errors: The error handler used when encoding the string.

    Returns:
        The percent-encoded string.

    Raises:
        TypeError: If *text* or *safe* is not a string.
    """
    text_value = _require_str(text, "text")
    safe_value = _require_str(safe, "safe")
    return _urllib_parse.quote(text_value, safe=safe_value, encoding=encoding, errors=errors)


def quote_plus(
    text: str,
    safe: str = "",
    encoding: str = _DEFAULT_ENCODING,
    errors: str = "replace",
) -> str:
    """Percent-encode a string, replacing spaces with plus signs.

    Args:
        text: The string to encode.
        safe: The ASCII characters that should never be encoded.
        encoding: The encoding used to turn the string into bytes.
        errors: The error handler used when encoding the string.

    Returns:
        The percent-encoded string.

    Raises:
        TypeError: If *text* or *safe* is not a string.
    """
    text_value = _require_str(text, "text")
    safe_value = _require_str(safe, "safe")
    return _urllib_parse.quote_plus(text_value, safe=safe_value, encoding=encoding, errors=errors)


def unquote(text: str, encoding: str = _DEFAULT_ENCODING, errors: str = "replace") -> str:
    """Decode a percent-encoded string.

    Args:
        text: The string to decode.
        encoding: The encoding used to turn bytes back into text.
        errors: The error handler used when decoding the bytes.

    Returns:
        The decoded string.

    Raises:
        TypeError: If *text* is not a string.
    """
    _require_str(text, "text")
    return _urllib_parse.unquote(text, encoding=encoding, errors=errors)


def unquote_plus(text: str, encoding: str = _DEFAULT_ENCODING, errors: str = "replace") -> str:
    """Decode a percent-encoded string, turning plus signs into spaces.

    Args:
        text: The string to decode.
        encoding: The encoding used to turn bytes back into text.
        errors: The error handler used when decoding the bytes.

    Returns:
        The decoded string.

    Raises:
        TypeError: If *text* is not a string.
    """
    _require_str(text, "text")
    return _urllib_parse.unquote_plus(text, encoding=encoding, errors=errors)


def unquote_to_bytes(text: str) -> bytes:
    """Decode a percent-encoded string into bytes.

    Args:
        text: The string to decode.

    Returns:
        The decoded bytes.

    Raises:
        TypeError: If *text* is not a string.
    """
    _require_str(text, "text")
    return _urllib_parse.unquote_to_bytes(text)


def urlencode(
    query: Union[Mapping[str, Any], Sequence[Tuple[str, Any]]],
    doseq: bool = False,
    safe: str = "",
    encoding: Optional[str] = None,
    errors: Optional[str] = None,
) -> str:
    """Encode a mapping or a sequence of pairs into a query string.

    Args:
        query: The mapping or sequence of pairs to encode.
        doseq: Whether to encode sequences of values as repeated keys.
        safe: The ASCII characters that should never be encoded.
        encoding: The encoding used to turn text into bytes.
        errors: The error handler used when encoding text.

    Returns:
        The encoded query string.

    Raises:
        TypeError: If *query* or *safe* is not of the expected type.
    """
    resolved = _require_mapping_or_pairs(query, "query")
    _require_str(safe, "safe")
    return _urllib_parse.urlencode(
        resolved, doseq=doseq, safe=safe, encoding=encoding, errors=errors
    )


def parse_qs(qs: str, **kwargs: Any) -> dict[str, list[Any]]:
    """Parse a query string into a mapping of names to lists of values.

    Args:
        qs: The query string to parse.
        kwargs: Additional options forwarded to the standard library.

    Returns:
        A mapping of names to lists of values.

    Raises:
        TypeError: If *qs* is not a string.
    """
    _require_str(qs, "qs")
    return _urllib_parse.parse_qs(qs, **kwargs)


def parse_qsl(qs: str, **kwargs: Any) -> list[tuple[str, str]]:
    """Parse a query string into a list of name/value pairs.

    Args:
        qs: The query string to parse.
        kwargs: Additional options forwarded to the standard library.

    Returns:
        A list of name/value pairs.

    Raises:
        TypeError: If *qs* is not a string.
    """
    _require_str(qs, "qs")
    return _urllib_parse.parse_qsl(qs, **kwargs)


def defrag(url: str) -> Tuple[str, Optional[str]]:
    """Remove the fragment from a URL.

    Args:
        url: The URL to defragment.

    Returns:
        The URL without its fragment and the fragment itself, or ``None`` when
        the URL has no fragment.

    Raises:
        TypeError: If *url* is not a string.
    """
    _require_str(url, "url")
    result = _urllib_parse.urldefrag(url)
    fragment: Optional[str] = result.fragment if result.fragment else None
    return result.url, fragment
