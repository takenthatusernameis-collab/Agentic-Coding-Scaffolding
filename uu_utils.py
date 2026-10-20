"""Uuencode utilities wrapping the standard library :mod:`uu` module.

The :mod:`uu` module implements the historical uuencode format, an ASCII-only
encoding that carries a binary payload inside plain text.  A payload opens with
a ``begin <mode> <name>`` header, continues with one encoded line per 45 input
bytes, and closes with an ``end`` line.

This wrapper exposes validated helpers for encoding and decoding payloads both
in memory and on disk, plus small utilities for inspecting the header of an
encoded payload.

.. note::

   The :mod:`uu` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that points at the :mod:`binascii_utils` replacements.

The helpers never write to the current working directory behind the caller's
back.  The standard library decoder derives an output filename from the header
when no destination is supplied; this wrapper always decodes into memory and
only touches the filesystem when an explicit destination is given.
"""

from __future__ import annotations

import io
import os
import warnings
from typing import Any, Dict, Optional, Union

__all__ = [
    "DEFAULT_FILE_MODE",
    "decode_uu",
    "encode_uu",
    "is_uuencoded",
    "parse_uu_header",
    "uu_decode",
    "uu_encode",
]

#: Permission mask recorded in the header when the caller does not pick one.
DEFAULT_FILE_MODE = 0o666

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import uu as _uu
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _uu = None  # type: ignore[assignment]


def _uu_module() -> Any:
    """Return the standard library ``uu`` module.

    Returns:
        The imported :mod:`uu` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``uu`` module.
    """
    if _uu is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'uu' module was removed in Python 3.13; "
            "use binascii_utils.b2a_uu and binascii_utils.a2b_uu instead"
        )
    return _uu


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes, raising ``TypeError`` for other types."""
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for other types."""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray, memoryview)):
        return bytes(value).decode("ascii", errors="replace")
    raise TypeError(f"{name} must be str or bytes, got {type(value).__name__}")


def _require_path(value: Any, name: str) -> str:
    """Return *value* as a filesystem path string."""
    if isinstance(value, str):
        return value
    if isinstance(value, os.PathLike):
        return os.fspath(value)  # type: ignore[no-any-return]
    raise TypeError(f"{name} must be str or os.PathLike, got {type(value).__name__}")


def _require_optional_str(value: Any, name: str) -> Optional[str]:
    """Return *value* when it is a string or ``None``."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str or None, got {type(value).__name__}")
    return value


def _require_optional_mode(value: Any, name: str) -> Optional[int]:
    """Return *value* when it is a permission mask or ``None``."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int or None, got {type(value).__name__}")
    if not 0 <= value <= 0o7777:
        raise ValueError(f"{name} must be a permission mask, got {value}")
    return value


def _split_header(text: str) -> Optional[list[str]]:
    """Return the fields of the uuencoded ``begin`` header, or ``None``."""
    for line in text.splitlines():
        if not line.strip():
            continue
        if not line.startswith("begin "):
            return None
        fields = line.split(" ", 2)
        if len(fields) != 3:
            return None
        try:
            int(fields[1], 8)
        except ValueError:
            return None
        return fields
    return None


def encode_uu(data: Any, name: str = "data", mode: Optional[int] = None) -> str:
    """Return the uuencoded representation of *data* as ASCII text.

    Args:
        data: The binary payload to encode.
        name: The file name recorded in the ``begin`` header.
        mode: The permission mask recorded in the header.  Defaults to
            :data:`DEFAULT_FILE_MODE`.

    Returns:
        The uuencoded payload, including its header and terminator.

    Raises:
        TypeError: If *data* is not bytes-like, *name* is not a string, or
            *mode* is not an integer.
        ValueError: If *mode* is not a valid permission mask.
        RuntimeError: If the interpreter no longer ships the ``uu`` module.
    """
    payload = _require_bytes(data, "data")
    file_name = _require_optional_str(name, "name") or "data"
    permission = DEFAULT_FILE_MODE if mode is None else _require_optional_mode(mode, "mode")
    uu_module = _uu_module()
    source = io.BytesIO(payload)
    target = io.BytesIO()
    uu_module.encode(source, target, name=file_name, mode=permission)
    return target.getvalue().decode("ascii")


def decode_uu(text: Any) -> bytes:
    """Return the binary payload carried by the uuencoded *text*.

    Args:
        text: The uuencoded payload, as text or bytes.

    Returns:
        The decoded binary payload.

    Raises:
        TypeError: If *text* is neither text nor bytes.
        uu.Error: If *text* does not hold a valid uuencoded payload.
        RuntimeError: If the interpreter no longer ships the ``uu`` module.
    """
    raw = _require_text(text, "text").encode("ascii", errors="replace")
    uu_module = _uu_module()
    target = io.BytesIO()
    uu_module.decode(io.BytesIO(raw), target)
    return target.getvalue()


def parse_uu_header(text: Any) -> Dict[str, str]:
    """Return the header recorded by a uuencoded payload.

    Args:
        text: The uuencoded payload, as text or bytes.

    Returns:
        A dictionary with the octal ``mode`` string and the ``name`` recorded
        in the ``begin <mode> <name>`` header.

    Raises:
        TypeError: If *text* is neither text nor bytes.
        ValueError: If *text* does not start with a valid ``begin`` header.
    """
    fields = _split_header(_require_text(text, "text"))
    if fields is None:
        raise ValueError("no valid 'begin <mode> <name>' header found")
    return {"mode": fields[1], "name": fields[2].strip()}


def is_uuencoded(text: Any) -> bool:
    """Return ``True`` when *text* opens with a valid uuencoded header.

    Args:
        text: The candidate payload, as text or bytes.

    Returns:
        ``True`` when the payload starts with a ``begin <mode> <name>`` header.

    Raises:
        TypeError: If *text* is neither text nor bytes.
    """
    return _split_header(_require_text(text, "text")) is not None


def uu_encode(
    data: Any,
    out_path: PathLike,
    name: Optional[str] = None,
    mode: Optional[int] = None,
) -> str:
    """Write the uuencoded representation of *data* to *out_path*.

    Args:
        data: The binary payload to encode.
        out_path: The path of the file to write.
        name: The file name recorded in the ``begin`` header.  Defaults to the
            base name of *out_path*.
        mode: The permission mask recorded in the header.  Defaults to
            :data:`DEFAULT_FILE_MODE`.

    Returns:
        The uuencoded payload that was written.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *mode* is not a valid permission mask.
        OSError: If the destination cannot be written.
        RuntimeError: If the interpreter no longer ships the ``uu`` module.
    """
    target_path = _require_path(out_path, "out_path")
    file_name = _require_optional_str(name, "name")
    if file_name is None:
        file_name = os.path.basename(target_path) or "data"
    encoded = encode_uu(data, name=file_name, mode=mode)
    with open(target_path, "w", encoding="ascii", newline="\n") as handle:
        handle.write(encoded)
    return encoded


def uu_decode(
    in_path: PathLike,
    out_path: Optional[PathLike] = None,
    mode: Optional[int] = None,
) -> bytes:
    """Decode the uuencoded file *in_path* and return the binary payload.

    The payload is always decoded into memory first, so the standard library
    decoder never derives an output filename from the header on its own.

    Args:
        in_path: The path of the uuencoded file to read.
        out_path: The path of the file to write.  When omitted, nothing is
            written to disk.
        mode: The permission mask applied to *out_path*.  When omitted, the
            mode recorded in the uuencoded header is used.  Setuid, setgid,
            and sticky bits are always masked off.

    Returns:
        The decoded binary payload.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *mode* is not a valid permission mask.
        OSError: If the source cannot be read or the destination written.
        uu.Error: If *in_path* does not hold a valid uuencoded payload.
        RuntimeError: If the interpreter no longer ships the ``uu`` module.
    """
    source_path = _require_path(in_path, "in_path")
    destination = None if out_path is None else _require_path(out_path, "out_path")
    permission = _require_optional_mode(mode, "mode")
    uu_module = _uu_module()
    with open(source_path, "rb") as handle:
        raw = handle.read()
    target = io.BytesIO()
    uu_module.decode(io.BytesIO(raw), target)
    payload = target.getvalue()
    if destination is not None:
        with open(destination, "wb") as handle:
            handle.write(payload)
        effective = permission if permission is not None else _recorded_mode(raw)
        os.chmod(destination, effective & 0o777)
    return payload


def _recorded_mode(raw: bytes) -> int:
    """Return the permission mask recorded in the header of *raw*."""
    try:
        header = parse_uu_header(raw)
    except ValueError:
        return DEFAULT_FILE_MODE
    return int(header["mode"], 8)
