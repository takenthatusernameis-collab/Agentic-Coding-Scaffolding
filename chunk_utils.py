"""Chunked transfer encoding utilities wrapping the standard library :mod:`chunk` module.

The :mod:`chunk` module reads the chunked transfer encoding used by file
formats such as AIFF and AIFF-C.  A chunk holds a four character name, a
size, and a payload, and the standard library reads the payload through a
:class:`~chunk.Chunk` object.

This wrapper validates every argument before the standard library is
reached, so a caller gets a clear :class:`TypeError` or :class:`ValueError`
instead of an opaque failure from the standard library.  It adds the
conveniences the standard library leaves to the caller: the payload of a
chunk is read in one call, and the position of a stream is restored after
the chunk is read.

.. note::

   The :mod:`chunk` module was deprecated in Python 3.11 and removed in
   Python 3.13 as part of :pep:`594`.  The import below degrades
   gracefully: when the interpreter no longer ships the module, the helpers
   raise a :class:`RuntimeError` that names the missing module, while
   :func:`is_available` still reports whether the module is shipped.

The wrapper only reads the file it is given and never writes to the
filesystem.
"""

from __future__ import annotations

import os
import warnings
from typing import Any, Union, cast

__all__ = [
    "Chunk",
    "is_available",
    "open_chunk",
    "read_chunk",
]

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import chunk as _chunk
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _chunk = None  # type: ignore[assignment]


Chunk = _chunk.Chunk if _chunk is not None else None  # type: ignore[assignment]


def _chunk_module() -> Any:
    """Return the standard library ``chunk`` module.

    Returns:
        The imported :mod:`chunk` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``chunk``
            module.
    """
    if _chunk is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'chunk' module was removed in Python 3.13; "
            "parse the chunked transfer encoding from the file header instead"
        )
    return _chunk


def _require_stream(value: Any, name: str) -> None:
    """Raise ``TypeError`` unless *value* is a readable binary stream.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Raises:
        TypeError: If *value* has no ``read`` method.
    """
    if not hasattr(value, "read"):
        raise TypeError(
            f"{name} must be a binary stream, got {type(value).__name__}"
        )


def _require_source(value: Any, name: str) -> None:
    """Raise ``TypeError`` unless *value* is a path or a binary stream.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Raises:
        TypeError: If *value* is neither a path nor a readable stream.
    """
    if isinstance(value, (str, os.PathLike)):
        return
    if hasattr(value, "read"):
        return
    raise TypeError(
        f"{name} must be a path or a binary stream, got {type(value).__name__}"
    )


def _require_bool(value: Any, name: str) -> bool:
    """Return *value* as a bool, rejecting other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a bool.

    Raises:
        TypeError: If *value* is not a bool.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def is_available() -> bool:
    """Return ``True`` if the interpreter ships the ``chunk`` module.

    Returns:
        ``True`` when the standard library module could be imported.
    """
    return _chunk is not None


def open_chunk(
    stream: Any,
    bigendian: bool = True,
    align: bool = True,
    inclheader: bool = False,
) -> Any:
    """Open the next chunk of a binary stream and return a :class:`Chunk`.

    The standard library reads the four character name and the size of the
    chunk while it is opened, so the returned object is positioned at the
    start of the payload.

    Args:
        stream: An open binary stream positioned at the start of a chunk.
        bigendian: Whether the size of the chunk is stored big-endian.
        align: Whether the chunks are padded to even sizes.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        A :class:`~chunk.Chunk` object positioned at the start of the
        payload.

    Raises:
        TypeError: If *stream* is not a binary stream, or if *bigendian*,
            *align*, or *inclheader* is not a bool.
        EOFError: If the stream holds fewer than eight bytes.
        RuntimeError: If the interpreter does not ship the ``chunk``
            module.
    """
    _require_stream(stream, "stream")
    _require_bool(bigendian, "bigendian")
    _require_bool(align, "align")
    _require_bool(inclheader, "inclheader")
    module = _chunk_module()
    return cast(Any, module.Chunk(stream, bigendian=bigendian, align=align, inclheader=inclheader))


def read_chunk(
    file: Union[PathLike, Any],
    bigendian: bool = True,
    align: bool = True,
    inclheader: bool = False,
) -> bytes:
    """Return the payload of the next chunk of a file or byte stream.

    The position of a stream is restored, so reading a chunk never changes
    what the caller reads next.  When *file* is a path, the file is opened
    and closed again, so the caller never leaks a handle.

    Args:
        file: The path of the file, or an open binary stream positioned at
            the start of a chunk.
        bigendian: Whether the size of the chunk is stored big-endian.
        align: Whether the chunks are padded to even sizes.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The payload bytes of the chunk.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if
            *bigendian*, *align*, or *inclheader* is not a bool.
        EOFError: If the stream holds fewer than eight bytes.
        RuntimeError: If the interpreter does not ship the ``chunk``
            module.
    """
    _require_source(file, "file")
    _require_bool(bigendian, "bigendian")
    _require_bool(align, "align")
    _require_bool(inclheader, "inclheader")
    module = _chunk_module()
    if isinstance(file, (str, os.PathLike)):
        with open(cast(str, os.fspath(file)), "rb") as handle:
            chunk = module.Chunk(
                handle, bigendian=bigendian, align=align, inclheader=inclheader
            )
            try:
                return cast(bytes, chunk.read())
            finally:
                chunk.close()
    stream = cast(Any, file)
    location = stream.tell()
    chunk = module.Chunk(
        stream, bigendian=bigendian, align=align, inclheader=inclheader
    )
    try:
        return cast(bytes, chunk.read())
    finally:
        chunk.close()
        stream.seek(location)
