"""Utilities for MIME type detection (wrapping :mod:`mimetypes`).

The :mod:`mimetypes` module maps file name extensions to MIME types and MIME
types back to extensions. This wrapper exposes a small, validated surface over
that functionality so callers can detect the type of a file, look up the
extensions registered for a MIME type, and register custom mappings without
repeating the usual type checks.
"""

from __future__ import annotations

import mimetypes as _mimetypes
import re
from typing import List, Optional, Sequence, Tuple

__all__ = [
    "guess_type",
    "guess_extension",
    "guess_all_extensions",
    "type_for_extension",
    "add_type",
    "init_database",
    "normalize_extension",
    "is_valid_mime_type",
    "mime_category",
    "is_text_mime_type",
]

# MIME types that carry textual payloads even though their top level type is
# not "text".
_TEXT_APPLICATION_TYPES = frozenset(
    {
        "application/json",
        "application/ld+json",
        "application/xml",
        "application/xhtml+xml",
        "application/javascript",
        "application/x-javascript",
        "application/x-www-form-urlencoded",
        "application/yaml",
        "application/x-yaml",
        "application/toml",
        "application/csv",
        "application/sql",
    }
)

# A MIME type is a "type/subtype" pair built from the characters allowed in
# an RFC 2045 token.
_MIME_TYPE_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*/[A-Za-z0-9][A-Za-z0-9!#$&^_.+-]*$"
)


def _require_text(value: object, name: str) -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_flag(value: object, name: str) -> bool:
    """Return *value* when it is a boolean, otherwise raise ``TypeError``."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def guess_type(url: str, strict: bool = True) -> Tuple[Optional[str], Optional[str]]:
    """Guess the MIME type of the file behind *url*.

    Args:
        url: File name or URL to inspect.
        strict: Whether only the standard MIME types are considered.

    Returns:
        A tuple of the MIME type and the content encoding. Both entries are
        ``None`` when the type cannot be guessed.

    Raises:
        TypeError: If *url* is not a string or *strict* is not a boolean.
    """
    target = _require_text(url, "url")
    strict_flag = _require_flag(strict, "strict")
    mime_type, encoding = _mimetypes.guess_type(target, strict=strict_flag)
    return mime_type, encoding


def guess_extension(mime_type: str, strict: bool = True) -> Optional[str]:
    """Guess the file extension of *mime_type*.

    Args:
        mime_type: MIME type to look up, such as ``"text/html"``.
        strict: Whether only the standard MIME types are considered.

    Returns:
        The extension, including the leading dot, or ``None`` when the type is
        unknown.

    Raises:
        TypeError: If *mime_type* is not a string or *strict* is not a boolean.
    """
    value = _require_text(mime_type, "mime_type")
    strict_flag = _require_flag(strict, "strict")
    return _mimetypes.guess_extension(value, strict=strict_flag)


def guess_all_extensions(mime_type: str, strict: bool = True) -> List[str]:
    """Guess every file extension registered for *mime_type*.

    Args:
        mime_type: MIME type to look up, such as ``"text/html"``.
        strict: Whether only the standard MIME types are considered.

    Returns:
        The matching extensions, including the leading dot. The list is empty
        when the type is unknown.

    Raises:
        TypeError: If *mime_type* is not a string or *strict* is not a boolean.
    """
    value = _require_text(mime_type, "mime_type")
    strict_flag = _require_flag(strict, "strict")
    return list(_mimetypes.guess_all_extensions(value, strict=strict_flag))


def normalize_extension(extension: str) -> str:
    """Return *extension* in the canonical form used by the MIME database.

    The canonical form is lower case and includes the leading dot, so
    ``"HTML"`` and ``".html"`` both normalize to ``".html"``.

    Args:
        extension: Extension to normalize, with or without a leading dot.

    Returns:
        The normalized extension.

    Raises:
        TypeError: If *extension* is not a string.
        ValueError: If *extension* is empty or only whitespace.
    """
    value = _require_text(extension, "extension").strip()
    if not value:
        raise ValueError("extension must not be empty")
    if not value.startswith("."):
        value = f".{value}"
    return value.lower()


def type_for_extension(extension: str, strict: bool = True) -> Optional[str]:
    """Return the MIME type registered for *extension*.

    Args:
        extension: Extension to look up, with or without a leading dot.
        strict: Whether only the standard MIME types are considered.

    Returns:
        The MIME type, or ``None`` when the extension is unknown.

    Raises:
        TypeError: If *extension* is not a string or *strict* is not a boolean.
        ValueError: If *extension* is empty or only whitespace.
    """
    suffix = normalize_extension(extension)
    strict_flag = _require_flag(strict, "strict")
    mime_type, _encoding = _mimetypes.guess_type(f"file{suffix}", strict=strict_flag)
    return mime_type


def add_type(mime_type: str, extension: str, strict: bool = True) -> None:
    """Register *extension* as an additional suffix of *mime_type*.

    The mapping is added to the database shared by the standard library, so it
    is visible to later calls of :func:`guess_type` and :func:`guess_extension`.

    Args:
        mime_type: MIME type to register, such as ``"application/x-kilo"``.
        extension: Extension to register, with or without a leading dot.
        strict: Whether the mapping replaces an already known extension.

    Raises:
        TypeError: If an argument has an unsupported type.
        ValueError: If *extension* is empty or only whitespace.
    """
    value = _require_text(mime_type, "mime_type")
    suffix = normalize_extension(extension)
    strict_flag = _require_flag(strict, "strict")
    _mimetypes.add_type(value, suffix, strict=strict_flag)


def init_database(files: Optional[Sequence[str]] = None) -> None:
    """Initialize the MIME type database.

    Calling the function without arguments restores the platform defaults.
    Passing file names reads those files in addition to the current database.

    Args:
        files: Paths of ``mime.types`` files to read, or ``None``.

    Raises:
        TypeError: If *files* is not a sequence of strings or ``None``.
    """
    if files is None:
        _mimetypes.init()
        return
    if isinstance(files, (str, bytes)):
        raise TypeError("files must be a sequence of strings or None")
    paths: List[str] = []
    for index, item in enumerate(files):
        if not isinstance(item, str):
            raise TypeError(f"files[{index}] must be a string, got {type(item).__name__}")
        paths.append(item)
    _mimetypes.init(files=paths)


def is_valid_mime_type(mime_type: str) -> bool:
    """Return ``True`` when *mime_type* is a well formed ``type/subtype`` value.

    Args:
        mime_type: MIME type to check.

    Returns:
        ``True`` when the value consists of a type and a subtype separated by
        a slash.

    Raises:
        TypeError: If *mime_type* is not a string.
    """
    value = _require_text(mime_type, "mime_type")
    return bool(_MIME_TYPE_PATTERN.match(value))


def mime_category(mime_type: str) -> str:
    """Return the top level type of *mime_type*.

    Args:
        mime_type: MIME type to inspect, such as ``"text/html"``.

    Returns:
        The top level type in lower case, such as ``"text"``. The empty
        string is returned when the MIME type is malformed.

    Raises:
        TypeError: If *mime_type* is not a string.
    """
    value = _require_text(mime_type, "mime_type")
    if not is_valid_mime_type(value):
        return ""
    return value.split("/", 1)[0].lower()


def is_text_mime_type(mime_type: str) -> bool:
    """Return ``True`` when *mime_type* describes textual content.

    Beside the ``text/*`` types the known textual application types, such as
    ``"application/json"``, are reported as text as well.

    Args:
        mime_type: MIME type to inspect.

    Returns:
        ``True`` when the payload of the type is text.

    Raises:
        TypeError: If *mime_type* is not a string.
    """
    value = _require_text(mime_type, "mime_type")
    if mime_category(value) == "text":
        return True
    return value.lower() in _TEXT_APPLICATION_TYPES
