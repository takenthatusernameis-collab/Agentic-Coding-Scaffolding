"""IFF chunk utilities wrapping the standard library :mod:`chunk` module.

The :mod:`chunk` module reads the chunks of an IFF file, the container format
of AIFF, AIFF-C, TIFF, and RMFF.  A chunk starts with a four character
identifier and a four byte size, both stored in big endian order, and holds the
payload that follows.  The size covers the payload only, and a chunk whose
payload has an odd length is padded with a single zero byte.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the standard library.  It adds the conveniences the
standard library leaves to the caller: a chunk is returned as one record that
carries its identifier, its size, and its payload, a file is iterated chunk by
chunk, the identifier of a chunk is decoded as text, the next chunk can be
inspected without consuming it, and a chunk can be written again, which the
standard library cannot do at all.

.. note::

   The :mod:`chunk` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers that read a chunk raise
   a :class:`RuntimeError` that names the missing module, while the helpers
   that only encode a chunk and :func:`is_available` keep working.

The wrapper only touches the files and the streams it is given.  It never
writes to the current working directory behind the caller's back.
"""

from __future__ import annotations

import io
import os
import struct
import warnings
from typing import Any, Iterator, List, NamedTuple, Union

__all__ = [
    "ChunkRecord",
    "build_chunk",
    "chunk_name",
    "is_available",
    "iter_chunks",
    "open_chunk",
    "peek_chunk",
    "read_chunk",
    "read_chunks",
    "skip_chunk",
    "write_chunk",
]

#: The number of bytes of the identifier of a chunk.
NAME_SIZE = 4

#: The number of bytes of the header of a chunk.
HEADER_SIZE = 8

#: The largest payload a chunk can hold, because its size is a 32 bit number.
MAX_CHUNK_SIZE = 0xFFFFFFFF

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import chunk as _chunk
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _chunk = None  # type: ignore[assignment]


class ChunkRecord(NamedTuple):
    """One chunk of an IFF file.

    Attributes:
        name: The four character identifier of the chunk.
        size: The number of payload bytes the header of the chunk declares.
        data: The payload bytes that were read from the file.
    """

    name: bytes
    size: int
    data: bytes

    @property
    def text_name(self) -> str:
        """The identifier of the chunk as text."""
        return _decode_name(self.name)


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
            "read the IFF chunk header of the file yourself instead"
        )
    return _chunk


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as bytes.

    Raises:
        TypeError: If *value* is not bytes-like.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_name(value: Any, name: str) -> bytes:
    """Return *value* as the four bytes of the identifier of a chunk.

    Args:
        value: The identifier to check.
        name: The name of the argument, used in the error message.

    Returns:
        The identifier as four bytes.

    Raises:
        TypeError: If *value* is neither bytes nor text.
        ValueError: If *value* is not four characters long, or is not ASCII.
    """
    if isinstance(value, str):
        if len(value) != NAME_SIZE:
            raise ValueError(
                f"{name} must be {NAME_SIZE} characters long, got {len(value)}"
            )
        try:
            return value.encode("ascii")
        except UnicodeEncodeError:
            raise ValueError(f"{name} must be ASCII, got {value!r}") from None
    raw = _require_bytes(value, name)
    if len(raw) != NAME_SIZE:
        raise ValueError(f"{name} must be {NAME_SIZE} bytes long, got {len(raw)}")
    return raw


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


def _require_reader(value: Any, name: str) -> None:
    """Raise ``TypeError`` unless *value* is a readable binary stream.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Raises:
        TypeError: If *value* is not a readable binary stream.
    """
    if isinstance(value, io.TextIOBase):
        raise TypeError(f"{name} must be a binary stream, got a text stream")
    if not hasattr(value, "read"):
        raise TypeError(
            f"{name} must be a binary stream, got {type(value).__name__}"
        )


def _require_writer(value: Any, name: str) -> None:
    """Raise ``TypeError`` unless *value* is a writable binary stream.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Raises:
        TypeError: If *value* is not a writable binary stream.
    """
    if isinstance(value, io.TextIOBase):
        raise TypeError(f"{name} must be a binary stream, got a text stream")
    if not hasattr(value, "write"):
        raise TypeError(
            f"{name} must be a binary stream, got {type(value).__name__}"
        )


def _require_source(value: Any, name: str) -> None:
    """Raise ``TypeError`` unless *value* is a path or a binary stream.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Raises:
        TypeError: If *value* is neither a path nor a readable binary stream.
    """
    if isinstance(value, (str, os.PathLike)):
        return
    _require_reader(value, name)


def _decode_name(name: bytes) -> str:
    """Return the identifier of a chunk as text.

    Every byte maps to exactly one character, so an identifier that is not
    printable is still reported instead of raising an error.

    Args:
        name: The identifier of the chunk.

    Returns:
        The identifier as text.
    """
    return name.decode("latin-1")


def _record(chunk: Any) -> ChunkRecord:
    """Return the record of an open chunk of the standard library.

    Args:
        chunk: The :class:`chunk.Chunk` object of the standard library.

    Returns:
        The record of the chunk.
    """
    name = chunk.getname()
    size = chunk.getsize()
    data = chunk.read()
    return ChunkRecord(name=name, size=size, data=data)


def _iter_chunks(
    module: Any,
    stream: Any,
    align: bool,
    bigendian: bool,
    inclheader: bool,
) -> Iterator[ChunkRecord]:
    """Yield the chunks of a stream until it holds no chunk anymore.

    Args:
        module: The :mod:`chunk` module of the standard library.
        stream: The binary stream to read.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Yields:
        The record of every chunk of the stream.
    """
    while True:
        try:
            chunk = module.Chunk(
                stream, align=align, bigendian=bigendian, inclheader=inclheader
            )
        except EOFError:
            return
        try:
            yield _record(chunk)
        finally:
            chunk.close()


def _iter_file_chunks(
    module: Any,
    path: PathLike,
    align: bool,
    bigendian: bool,
    inclheader: bool,
) -> Iterator[ChunkRecord]:
    """Yield the chunks of a file until it holds no chunk anymore.

    The file is opened and closed by this helper, so the caller never leaks a
    handle.

    Args:
        module: The :mod:`chunk` module of the standard library.
        path: The path of the file.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Yields:
        The record of every chunk of the file.
    """
    with open(os.fspath(path), "rb") as handle:
        yield from _iter_chunks(module, handle, align, bigendian, inclheader)


def is_available() -> bool:
    """Return ``True`` if the interpreter ships the ``chunk`` module.

    Returns:
        ``True`` when the standard library module could be imported.
    """
    return _chunk is not None


def chunk_name(name: Union[bytes, str]) -> str:
    """Return the identifier of a chunk as text.

    The identifier of an IFF chunk is four characters, and the characters that
    are not printable are reported as they are.

    Args:
        name: The identifier of the chunk, as bytes or as text.

    Returns:
        The identifier of the chunk as text.

    Raises:
        TypeError: If *name* is neither bytes nor text.
        ValueError: If *name* is not four characters long, or is not ASCII.
    """
    return _decode_name(_require_name(name, "name"))


def build_chunk(
    name: Union[bytes, str],
    data: Any,
    bigendian: bool = True,
    align: bool = True,
    inclheader: bool = False,
) -> bytes:
    """Return the bytes of a chunk.

    The bytes are the identifier of the chunk, the size of its payload, and the
    payload itself.  A payload of an odd length is padded with a single zero
    byte, the way the standard library expects it.

    Args:
        name: The identifier of the chunk, as bytes or as text.
        data: The payload of the chunk.
        bigendian: Whether the size of the chunk is stored big-endian.
        align: Whether the payload is padded to an even length.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The bytes of the chunk.

    Raises:
        TypeError: If *name* is neither bytes nor text, if *data* is not
            bytes-like, or if a flag is not a bool.
        ValueError: If *name* is not four characters long, is not ASCII, or if
            the payload is too large for the size field of a chunk.
    """
    raw_name = _require_name(name, "name")
    payload = _require_bytes(data, "data")
    _require_bool(bigendian, "bigendian")
    _require_bool(align, "align")
    _require_bool(inclheader, "inclheader")
    size = len(payload) + (HEADER_SIZE if inclheader else 0)
    if size > MAX_CHUNK_SIZE:
        raise ValueError(
            f"the payload of a chunk must not exceed {MAX_CHUNK_SIZE} bytes, "
            f"got {len(payload)}"
        )
    prefix = ">" if bigendian else "<"
    body = raw_name + struct.pack(prefix + "L", size) + payload
    if align and len(payload) % 2:
        body += b"\x00"
    return body


def write_chunk(
    file: Union[PathLike, Any],
    name: Union[bytes, str],
    data: Any,
    bigendian: bool = True,
    align: bool = True,
    inclheader: bool = False,
) -> int:
    """Write a chunk to a file or a binary stream.

    The standard library can only read a chunk, so the bytes of the chunk are
    built by :func:`build_chunk`.

    Args:
        file: The path of the file, or an open binary stream.
        name: The identifier of the chunk, as bytes or as text.
        data: The payload of the chunk.
        bigendian: Whether the size of the chunk is stored big-endian.
        align: Whether the payload is padded to an even length.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The number of bytes that were written.

    Raises:
        TypeError: If *file* is neither a path nor a writable binary stream, if
            *name* is neither bytes nor text, if *data* is not bytes-like, or
            if a flag is not a bool.
        ValueError: If *name* is not four characters long, is not ASCII, or if
            the payload is too large for the size field of a chunk.
    """
    body = build_chunk(
        name, data, bigendian=bigendian, align=align, inclheader=inclheader
    )
    if isinstance(file, (str, os.PathLike)):
        with open(os.fspath(file), "wb") as handle:
            handle.write(body)
        return len(body)
    _require_writer(file, "file")
    file.write(body)
    return len(body)


def open_chunk(
    stream: Any,
    align: bool = True,
    bigendian: bool = True,
    inclheader: bool = False,
) -> Any:
    """Open the next chunk of a binary stream and return it.

    The standard library reads the identifier and the size of the chunk while
    it is opened, so the returned object is positioned at the start of the
    payload.  The object is a :class:`chunk.Chunk` of the standard library, so
    it offers ``read``, ``skip``, ``seek``, ``tell``, ``getname``,
    ``getsize``, and ``close``.

    Args:
        stream: An open binary stream positioned at the start of a chunk.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The :class:`chunk.Chunk` object of the standard library.

    Raises:
        TypeError: If *stream* is not a binary stream, or if a flag is not a
            bool.
        EOFError: If the stream holds fewer than eight bytes.
        RuntimeError: If the interpreter does not ship the ``chunk`` module.
    """
    _require_reader(stream, "stream")
    _require_bool(align, "align")
    _require_bool(bigendian, "bigendian")
    _require_bool(inclheader, "inclheader")
    module = _chunk_module()
    return module.Chunk(
        stream, align=align, bigendian=bigendian, inclheader=inclheader
    )


def read_chunk(
    file: Union[PathLike, Any],
    align: bool = True,
    bigendian: bool = True,
    inclheader: bool = False,
) -> ChunkRecord:
    """Return the next chunk of a file or a byte stream.

    The record carries the identifier of the chunk, the size its header
    declares, and its payload.  A file that ends in the middle of a chunk
    yields fewer payload bytes than the header declares.

    Args:
        file: The path of the file, or an open binary stream positioned at the
            start of a chunk.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The record of the chunk.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if a
            flag is not a bool.
        EOFError: If the stream holds fewer than eight bytes.
        RuntimeError: If the interpreter does not ship the ``chunk`` module.
    """
    _require_source(file, "file")
    _require_bool(align, "align")
    _require_bool(bigendian, "bigendian")
    _require_bool(inclheader, "inclheader")
    module = _chunk_module()
    if isinstance(file, (str, os.PathLike)):
        with open(os.fspath(file), "rb") as handle:
            chunk = module.Chunk(
                handle, align=align, bigendian=bigendian, inclheader=inclheader
            )
            try:
                return _record(chunk)
            finally:
                chunk.close()
    chunk = module.Chunk(
        file, align=align, bigendian=bigendian, inclheader=inclheader
    )
    try:
        return _record(chunk)
    finally:
        chunk.close()


def peek_chunk(
    file: Union[PathLike, Any],
    align: bool = True,
    bigendian: bool = True,
    inclheader: bool = False,
) -> ChunkRecord:
    """Return the next chunk of a file or a byte stream without consuming it.

    The position of a stream is restored, so the chunk can be read again
    afterwards.

    Args:
        file: The path of the file, or an open binary stream positioned at the
            start of a chunk.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The record of the chunk.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if a
            flag is not a bool.
        ValueError: If *file* is a stream that cannot be seeked.
        EOFError: If the stream holds fewer than eight bytes.
        RuntimeError: If the interpreter does not ship the ``chunk`` module.
    """
    _require_source(file, "file")
    if isinstance(file, (str, os.PathLike)):
        return read_chunk(
            file, align=align, bigendian=bigendian, inclheader=inclheader
        )
    try:
        location = file.tell()
    except (OSError, ValueError) as error:
        raise ValueError(
            "the stream cannot be seeked, so the next chunk cannot be peeked at"
        ) from error
    try:
        return read_chunk(
            file, align=align, bigendian=bigendian, inclheader=inclheader
        )
    finally:
        file.seek(location)


def iter_chunks(
    file: Union[PathLike, Any],
    align: bool = True,
    bigendian: bool = True,
    inclheader: bool = False,
) -> Iterator[ChunkRecord]:
    """Return an iterator over the chunks of a file or a byte stream.

    The chunks are read one after another, and the iterator stops at the end of
    the file.  The position of a stream moves to the end of the file.

    Args:
        file: The path of the file, or an open binary stream positioned at the
            start of a chunk.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        An iterator over the records of the chunks.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if a
            flag is not a bool.
        RuntimeError: If the interpreter does not ship the ``chunk`` module.
    """
    _require_source(file, "file")
    _require_bool(align, "align")
    _require_bool(bigendian, "bigendian")
    _require_bool(inclheader, "inclheader")
    module = _chunk_module()
    if isinstance(file, (str, os.PathLike)):
        return _iter_file_chunks(module, file, align, bigendian, inclheader)
    return _iter_chunks(module, file, align, bigendian, inclheader)


def read_chunks(
    file: Union[PathLike, Any],
    align: bool = True,
    bigendian: bool = True,
    inclheader: bool = False,
) -> List[ChunkRecord]:
    """Return every chunk of a file or a byte stream.

    Args:
        file: The path of the file, or an open binary stream positioned at the
            start of a chunk.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The records of the chunks, in the order they are stored in the file.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if a
            flag is not a bool.
        RuntimeError: If the interpreter does not ship the ``chunk`` module.
    """
    return list(iter_chunks(file, align=align, bigendian=bigendian, inclheader=inclheader))


def skip_chunk(
    file: Union[PathLike, Any],
    align: bool = True,
    bigendian: bool = True,
    inclheader: bool = False,
) -> int:
    """Skip the payload of the next chunk of a file or a byte stream.

    The position of a stream moves to the start of the next chunk, so the
    chunks that are of no interest can be passed over quickly.

    Args:
        file: The path of the file, or an open binary stream positioned at the
            start of a chunk.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The number of payload bytes that were skipped.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if a
            flag is not a bool.
        EOFError: If the stream holds fewer than eight bytes.
        RuntimeError: If the interpreter does not ship the ``chunk`` module.
    """
    _require_source(file, "file")
    _require_bool(align, "align")
    _require_bool(bigendian, "bigendian")
    _require_bool(inclheader, "inclheader")
    module = _chunk_module()
    if isinstance(file, (str, os.PathLike)):
        with open(os.fspath(file), "rb") as handle:
            return _skip_chunk(module, handle, align, bigendian, inclheader)
    return _skip_chunk(module, file, align, bigendian, inclheader)


def _skip_chunk(
    module: Any,
    stream: Any,
    align: bool,
    bigendian: bool,
    inclheader: bool,
) -> int:
    """Skip the payload of the next chunk of a stream.

    Args:
        module: The :mod:`chunk` module of the standard library.
        stream: The binary stream to read.
        align: Whether the chunks are padded to even sizes.
        bigendian: Whether the size of the chunk is stored big-endian.
        inclheader: Whether the size includes the eight byte header.

    Returns:
        The number of payload bytes that were skipped.
    """
    chunk = module.Chunk(
        stream, align=align, bigendian=bigendian, inclheader=inclheader
    )
    size: int = chunk.getsize()
    chunk.skip()
    return size
