"""XDR (eXternal Data Representation) utilities wrapping the standard library :mod:`xdrlib`.

XDR is the binary wire format described in :rfc:`1014` and used by RPC
protocols such as ONC RPC and NFS.  Every value is encoded in big-endian
order, integers occupy four bytes, opaque data is padded to a multiple of four
bytes, and variable-length data is prefixed with its length.

The :mod:`xdrlib` module implements a subset of that format with a
:class:`~xdrlib.Packer` that writes into an internal buffer and an
:class:`~xdrlib.Unpacker` that reads from one.  This wrapper exposes one
function per XDR type, so callers never have to manage a packer themselves:
every helper takes and returns plain Python values.  The wrapper also adds the
two conveniences the standard library lacks — every argument is validated
before the standard library is reached, and a truncated payload raises
:class:`ValueError` instead of :class:`EOFError`.

.. note::

   The :mod:`xdrlib` module was deprecated in Python 3.12 and removed in
   Python 3.13 as part of :pep:`594`.  The import below degrades gracefully:
   when the interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that points at the :mod:`struct_utils` replacements.

The encoding is pure computation: no helper opens a network connection, reads
a file, or spawns a process.
"""

from __future__ import annotations

import warnings
from typing import Any, Callable, List, Sequence, TypeVar, Union

__all__ = [
    "BytesLike",
    "ConversionError",
    "Error",
    "FLOAT_MAX",
    "HYPER_MAX",
    "HYPER_MIN",
    "INT_MAX",
    "INT_MIN",
    "Packer",
    "PackerCallback",
    "UHYPER_MAX",
    "UINT_MAX",
    "Unpacker",
    "UnpackerCallback",
    "pack_array",
    "pack_bool",
    "pack_bytes",
    "pack_double",
    "pack_enum",
    "pack_farray",
    "pack_float",
    "pack_fopaque",
    "pack_fstring",
    "pack_hyper",
    "pack_int",
    "pack_list",
    "pack_opaque",
    "pack_string",
    "pack_uhyper",
    "pack_uint",
    "pack_uint_array",
    "unpack_array",
    "unpack_bool",
    "unpack_bytes",
    "unpack_double",
    "unpack_enum",
    "unpack_farray",
    "unpack_float",
    "unpack_fopaque",
    "unpack_fstring",
    "unpack_hyper",
    "unpack_int",
    "unpack_list",
    "unpack_opaque",
    "unpack_string",
    "unpack_uhyper",
    "unpack_uint",
    "unpack_uint_array",
]

#: Largest value that fits in an XDR unsigned integer.
UINT_MAX = 2**32 - 1

#: Smallest value that fits in an XDR signed integer.
INT_MIN = -(2**31)

#: Largest value that fits in an XDR signed integer.
INT_MAX = 2**31 - 1

#: Largest value that fits in an XDR unsigned 64-bit integer.
UHYPER_MAX = 2**64 - 1

#: Smallest value that fits in an XDR signed 64-bit integer.
HYPER_MIN = -(2**63)

#: Largest value that fits in an XDR signed 64-bit integer.
HYPER_MAX = 2**63 - 1

#: Largest magnitude that fits in an XDR single precision float.
FLOAT_MAX = 3.4028234663852886e38

_REMOVED_MESSAGE = (
    "the standard library 'xdrlib' module was removed in Python 3.13; "
    "use struct_utils for the big-endian binary encoding it implemented"
)

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import xdrlib as _xdrlib
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _xdrlib = None  # type: ignore[assignment]

if _xdrlib is not None:
    #: The standard library packer, re-exported for convenience.
    Packer = _xdrlib.Packer
    #: The standard library unpacker, re-exported for convenience.
    Unpacker = _xdrlib.Unpacker
    #: The standard library base error, re-exported for convenience.
    Error = _xdrlib.Error
    #: The standard library conversion error, re-exported for convenience.
    ConversionError = _xdrlib.ConversionError
else:  # pragma: no cover - Python 3.13 removed the module

    class Packer:  # type: ignore[no-redef]
        """Placeholder for the standard library packer.

        The class only exists so that the module keeps importing on
        interpreters that no longer ship :mod:`xdrlib`; instantiating it
        raises a :class:`RuntimeError`.
        """

        def __init__(self) -> None:
            raise RuntimeError(_REMOVED_MESSAGE)

    class Unpacker:  # type: ignore[no-redef]
        """Placeholder for the standard library unpacker.

        The class only exists so that the module keeps importing on
        interpreters that no longer ship :mod:`xdrlib`; instantiating it
        raises a :class:`RuntimeError`.
        """

        def __init__(self, data: bytes) -> None:
            raise RuntimeError(_REMOVED_MESSAGE)

    class Error(Exception):  # type: ignore[no-redef]
        """Placeholder for the standard library error class."""

    class ConversionError(Error):  # type: ignore[no-redef]
        """Placeholder for the standard library conversion error class."""


#: Callback that writes a single value into a packer.
PackerCallback = Callable[["Packer", Any], None]

#: Callback that reads a single value from an unpacker.
UnpackerCallback = Callable[["Unpacker"], Any]

#: Every object the helpers accept as binary payload.
BytesLike = Union[bytes, bytearray, memoryview]

_T = TypeVar("_T")


def _xdrlib_module() -> Any:
    """Return the standard library :mod:`xdrlib` module.

    Returns:
        The imported :mod:`xdrlib` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``xdrlib`` module.
    """
    if _xdrlib is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(_REMOVED_MESSAGE)
    return _xdrlib


def _packer() -> Packer:
    """Return a fresh standard library packer.

    Returns:
        An empty :class:`Packer`.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``xdrlib`` module.
    """
    _xdrlib_module()
    return Packer()


def _unpacker(data: bytes) -> Unpacker:
    """Return a standard library unpacker reading from *data*.

    Args:
        data: The payload the unpacker reads from.

    Returns:
        An :class:`Unpacker` positioned at the start of *data*.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``xdrlib`` module.
    """
    _xdrlib_module()
    return Unpacker(data)


def _require_int(value: Any, name: str) -> int:
    """Return *value* when it is an integer.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated integer.

    Raises:
        TypeError: If *value* is not an integer.  Booleans are rejected because
            they are integers in Python but never a meaningful XDR value.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_range(value: float, name: str, minimum: float, maximum: float) -> None:
    """Raise ``ValueError`` when *value* lies outside the given inclusive range.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.
        minimum: The smallest accepted value.
        maximum: The largest accepted value.

    Raises:
        ValueError: If *value* lies outside the range.
    """
    if not minimum <= value <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}, got {value}")


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated payload.

    Raises:
        TypeError: If *value* is not a bytes-like object.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_float(value: Any, name: str) -> float:
    """Return *value* as a float.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated float.

    Raises:
        TypeError: If *value* is not an integer or a float.
        ValueError: If *value* cannot be represented as a float.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be an int or a float, got {type(value).__name__}")
    try:
        return float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is too large to be represented as a float") from exc


def _require_sequence(value: Any, name: str) -> Sequence[Any]:
    """Return *value* when it is a sequence of values.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Returns:
        The validated sequence.

    Raises:
        TypeError: If *value* is not a sequence, or is a string or bytes
            object, which are sequences of characters rather than of values.
    """
    if isinstance(value, (str, bytes, bytearray, memoryview)):
        raise TypeError(f"{name} must be a sequence of values, not {type(value).__name__}")
    if not isinstance(value, Sequence):
        raise TypeError(f"{name} must be a sequence of values, got {type(value).__name__}")
    return value


def _require_callable(value: Any, name: str) -> None:
    """Raise ``TypeError`` when *value* is not callable.

    Args:
        name: The name of the argument, used in the error message.
        value: The value to check.

    Raises:
        TypeError: If *value* is not callable.
    """
    if not callable(value):
        raise TypeError(f"{name} must be callable, got {type(value).__name__}")


def _read(reader: Callable[[], _T], description: str) -> _T:
    """Return the result of *reader*, translating a short payload into an error.

    Args:
        reader: The standard library call that reads the next value.
        description: What the reader reads, used in the error message.

    Returns:
        The value read from the payload.

    Raises:
        ValueError: If the payload ends before the value could be read.
    """
    try:
        return reader()
    except EOFError as exc:
        raise ValueError(f"data is too short to contain {description}") from exc


def pack_uint(value: int) -> bytes:
    """Pack *value* as an XDR unsigned integer.

    Args:
        value: The integer to pack.  It must fit in four unsigned bytes.

    Returns:
        The four byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* does not fit in an unsigned 32-bit integer.

    Examples:
        >>> pack_uint(1)
        b'\\x00\\x00\\x00\\x01'
    """
    number = _require_int(value, "value")
    _require_range(number, "value", 0, UINT_MAX)
    packer = _packer()
    packer.pack_uint(number)
    return packer.get_buffer()


def unpack_uint(data: BytesLike) -> int:
    """Unpack an XDR unsigned integer from *data*.

    Args:
        data: The payload to read from.  Four bytes are required.

    Returns:
        The unsigned integer that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than four bytes.

    Examples:
        >>> unpack_uint(b'\\x00\\x00\\x00\\x01')
        1
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_uint, "an unsigned integer")


def pack_int(value: int) -> bytes:
    """Pack *value* as an XDR signed integer.

    Args:
        value: The integer to pack.  It must fit in four signed bytes.

    Returns:
        The four byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* does not fit in a signed 32-bit integer.

    Examples:
        >>> pack_int(-1)
        b'\\xff\\xff\\xff\\xff'
    """
    number = _require_int(value, "value")
    _require_range(number, "value", INT_MIN, INT_MAX)
    packer = _packer()
    packer.pack_int(number)
    return packer.get_buffer()


def unpack_int(data: BytesLike) -> int:
    """Unpack an XDR signed integer from *data*.

    Args:
        data: The payload to read from.  Four bytes are required.

    Returns:
        The signed integer that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than four bytes.

    Examples:
        >>> unpack_int(b'\\xff\\xff\\xff\\xff')
        -1
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_int, "a signed integer")


def pack_enum(value: int) -> bytes:
    """Pack *value* as an XDR enumeration.

    The standard library encodes an enumeration as a signed 32-bit integer,
    so this helper is equivalent to :func:`pack_int`.

    Args:
        value: The enumeration value to pack.

    Returns:
        The four byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* does not fit in a signed 32-bit integer.
    """
    return pack_int(value)


def unpack_enum(data: BytesLike) -> int:
    """Unpack an XDR enumeration from *data*.

    The standard library decodes an enumeration as a signed 32-bit integer,
    so this helper is equivalent to :func:`unpack_int`.

    Args:
        data: The payload to read from.  Four bytes are required.

    Returns:
        The enumeration value that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than four bytes.
    """
    return unpack_int(data)


def pack_bool(value: bool) -> bytes:
    """Pack *value* as an XDR boolean.

    Args:
        value: The boolean to pack.

    Returns:
        The four byte representation of *value*.

    Raises:
        TypeError: If *value* is not a boolean.

    Examples:
        >>> pack_bool(True)
        b'\\x00\\x00\\x00\\x01'
    """
    if not isinstance(value, bool):
        raise TypeError(f"value must be a bool, got {type(value).__name__}")
    packer = _packer()
    packer.pack_bool(value)
    return packer.get_buffer()


def unpack_bool(data: BytesLike) -> bool:
    """Unpack an XDR boolean from *data*.

    Args:
        data: The payload to read from.  Four bytes are required.

    Returns:
        The boolean that was packed.  Every non-zero value decodes to ``True``.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than four bytes.

    Examples:
        >>> unpack_bool(b'\\x00\\x00\\x00\\x01')
        True
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_bool, "a boolean")


def pack_uhyper(value: int) -> bytes:
    """Pack *value* as an XDR unsigned 64-bit integer.

    Args:
        value: The integer to pack.  It must fit in eight unsigned bytes.

    Returns:
        The eight byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* does not fit in an unsigned 64-bit integer.
    """
    number = _require_int(value, "value")
    _require_range(number, "value", 0, UHYPER_MAX)
    packer = _packer()
    packer.pack_uhyper(number)
    return packer.get_buffer()


def unpack_uhyper(data: BytesLike) -> int:
    """Unpack an XDR unsigned 64-bit integer from *data*.

    Args:
        data: The payload to read from.  Eight bytes are required.

    Returns:
        The unsigned 64-bit integer that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than eight bytes.
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_uhyper, "an unsigned 64-bit integer")


def pack_hyper(value: int) -> bytes:
    """Pack *value* as an XDR signed 64-bit integer.

    Args:
        value: The integer to pack.  It must fit in eight signed bytes.

    Returns:
        The eight byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* does not fit in a signed 64-bit integer.

    Examples:
        >>> pack_hyper(-1)
        b'\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff'
    """
    number = _require_int(value, "value")
    _require_range(number, "value", HYPER_MIN, HYPER_MAX)
    packer = _packer()
    packer.pack_hyper(number)
    return packer.get_buffer()


def unpack_hyper(data: BytesLike) -> int:
    """Unpack an XDR signed 64-bit integer from *data*.

    Args:
        data: The payload to read from.  Eight bytes are required.

    Returns:
        The signed 64-bit integer that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than eight bytes.
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_hyper, "a signed 64-bit integer")


def pack_float(value: float) -> bytes:
    """Pack *value* as an XDR single precision float.

    Args:
        value: The number to pack.  It must fit in a single precision float.

    Returns:
        The four byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer or a float.
        ValueError: If *value* is too large for a single precision float.

    Examples:
        >>> pack_float(1.0)
        b'\\x3f\\x80\\x00\\x00'
    """
    number = _require_float(value, "value")
    _require_range(number, "value", -FLOAT_MAX, FLOAT_MAX)
    packer = _packer()
    packer.pack_float(number)
    return packer.get_buffer()


def unpack_float(data: BytesLike) -> float:
    """Unpack an XDR single precision float from *data*.

    Args:
        data: The payload to read from.  Four bytes are required.

    Returns:
        The single precision float that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than four bytes.

    Examples:
        >>> unpack_float(b'\\x3f\\x80\\x00\\x00')
        1.0
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_float, "a single precision float")


def pack_double(value: float) -> bytes:
    """Pack *value* as an XDR double precision float.

    Args:
        value: The number to pack.

    Returns:
        The eight byte big-endian representation of *value*.

    Raises:
        TypeError: If *value* is not an integer or a float.
        ValueError: If *value* cannot be represented as a float.

    Examples:
        >>> pack_double(1.0)
        b'\\x3f\\xf0\\x00\\x00\\x00\\x00\\x00\\x00'
    """
    number = _require_float(value, "value")
    packer = _packer()
    packer.pack_double(number)
    return packer.get_buffer()


def unpack_double(data: BytesLike) -> float:
    """Unpack an XDR double precision float from *data*.

    Args:
        data: The payload to read from.  Eight bytes are required.

    Returns:
        The double precision float that was packed.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* holds fewer than eight bytes.
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_double, "a double precision float")


def pack_string(value: BytesLike) -> bytes:
    """Pack *value* as an XDR string.

    The payload is prefixed with its length and padded to a multiple of four
    bytes.

    Args:
        value: The payload to pack.

    Returns:
        The encoded string.

    Raises:
        TypeError: If *value* is not a bytes-like object.

    Examples:
        >>> pack_string(b'ab')
        b'\\x00\\x00\\x00\\x02ab\\x00\\x00'
    """
    payload = _require_bytes(value, "value")
    packer = _packer()
    packer.pack_string(payload)
    return packer.get_buffer()


def unpack_string(data: BytesLike) -> bytes:
    """Unpack an XDR string from *data*.

    Args:
        data: The payload to read from.

    Returns:
        The string that was packed, without its length prefix or padding.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* ends before the string could be read.

    Examples:
        >>> unpack_string(b'\\x00\\x00\\x00\\x02ab\\x00\\x00')
        b'ab'
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_string, "a string")


def pack_bytes(value: BytesLike) -> bytes:
    """Pack *value* as an XDR byte string.

    The encoding is identical to :func:`pack_string`: the payload is prefixed
    with its length and padded to a multiple of four bytes.

    Args:
        value: The payload to pack.

    Returns:
        The encoded byte string.

    Raises:
        TypeError: If *value* is not a bytes-like object.
    """
    payload = _require_bytes(value, "value")
    packer = _packer()
    packer.pack_bytes(payload)
    return packer.get_buffer()


def unpack_bytes(data: BytesLike) -> bytes:
    """Unpack an XDR byte string from *data*.

    Args:
        data: The payload to read from.

    Returns:
        The byte string that was packed, without its length prefix or padding.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* ends before the byte string could be read.
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_bytes, "a byte string")


def pack_opaque(value: BytesLike) -> bytes:
    """Pack *value* as XDR opaque data.

    The encoding is identical to :func:`pack_string`: the payload is prefixed
    with its length and padded to a multiple of four bytes.

    Args:
        value: The payload to pack.

    Returns:
        The encoded opaque data.

    Raises:
        TypeError: If *value* is not a bytes-like object.
    """
    payload = _require_bytes(value, "value")
    packer = _packer()
    packer.pack_opaque(payload)
    return packer.get_buffer()


def unpack_opaque(data: BytesLike) -> bytes:
    """Unpack XDR opaque data from *data*.

    Args:
        data: The payload to read from.

    Returns:
        The opaque data that was packed, without its length prefix or padding.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* ends before the opaque data could be read.
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(unpacker.unpack_opaque, "opaque data")


def pack_fstring(length: int, value: BytesLike) -> bytes:
    """Pack *value* as a fixed length XDR string.

    The payload is truncated to *length* bytes and padded to a multiple of
    four bytes.  No length prefix is written.

    Args:
        length: The number of bytes the string occupies.
        value: The payload to pack.

    Returns:
        The encoded fixed length string.

    Raises:
        TypeError: If *length* is not an integer or *value* is not a bytes-like
            object.
        ValueError: If *length* is negative.

    Examples:
        >>> pack_fstring(4, b'ab')
        b'ab\\x00\\x00'
    """
    size = _require_int(length, "length")
    if size < 0:
        raise ValueError(f"length must not be negative, got {size}")
    payload = _require_bytes(value, "value")
    packer = _packer()
    packer.pack_fstring(size, payload)
    return packer.get_buffer()


def unpack_fstring(length: int, data: BytesLike) -> bytes:
    """Unpack a fixed length XDR string from *data*.

    Args:
        length: The number of bytes the string occupies.
        data: The payload to read from.

    Returns:
        The string that was packed, without its padding.

    Raises:
        TypeError: If *length* is not an integer or *data* is not a bytes-like
            object.
        ValueError: If *length* is negative or *data* holds fewer bytes than
            the padded string occupies.

    Examples:
        >>> unpack_fstring(2, b'ab\\x00\\x00')
        b'ab'
    """
    size = _require_int(length, "length")
    if size < 0:
        raise ValueError(f"length must not be negative, got {size}")
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(lambda: unpacker.unpack_fstring(size), "a fixed length string")


def pack_fopaque(length: int, value: BytesLike) -> bytes:
    """Pack *value* as fixed length XDR opaque data.

    The payload is truncated to *length* bytes and padded to a multiple of
    four bytes.  No length prefix is written.

    Args:
        length: The number of bytes the opaque data occupies.
        value: The payload to pack.

    Returns:
        The encoded fixed length opaque data.

    Raises:
        TypeError: If *length* is not an integer or *value* is not a bytes-like
            object.
        ValueError: If *length* is negative.
    """
    size = _require_int(length, "length")
    if size < 0:
        raise ValueError(f"length must not be negative, got {size}")
    payload = _require_bytes(value, "value")
    packer = _packer()
    packer.pack_fopaque(size, payload)
    return packer.get_buffer()


def unpack_fopaque(length: int, data: BytesLike) -> bytes:
    """Unpack fixed length XDR opaque data from *data*.

    Args:
        length: The number of bytes the opaque data occupies.
        data: The payload to read from.

    Returns:
        The opaque data that was packed, without its padding.

    Raises:
        TypeError: If *length* is not an integer or *data* is not a bytes-like
            object.
        ValueError: If *length* is negative or *data* holds fewer bytes than
            the padded opaque data occupies.
    """
    size = _require_int(length, "length")
    if size < 0:
        raise ValueError(f"length must not be negative, got {size}")
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    return _read(lambda: unpacker.unpack_fopaque(size), "fixed length opaque data")


def pack_array(items: Sequence[Any], pack_item: PackerCallback) -> bytes:
    """Pack *items* as an XDR array.

    The array is prefixed with the number of items it holds.  The callback is
    handed the packer and the item, so it can use any of the standard library
    packing methods.

    Args:
        items: The items to pack.
        pack_item: The callback that writes a single item into the packer.

    Returns:
        The encoded array.

    Raises:
        TypeError: If *items* is not a sequence of values or *pack_item* is
            not callable.

    Examples:
        >>> pack_array([1, 2], lambda packer, item: packer.pack_uint(item))
        b'\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02'
    """
    values = _require_sequence(items, "items")
    _require_callable(pack_item, "pack_item")
    packer = _packer()
    packer.pack_uint(len(values))
    for item in values:
        pack_item(packer, item)
    return packer.get_buffer()


def unpack_array(data: BytesLike, unpack_item: UnpackerCallback) -> List[Any]:
    """Unpack an XDR array from *data*.

    The callback is handed the unpacker and returns the item it read.

    Args:
        data: The payload to read from.
        unpack_item: The callback that reads a single item from the unpacker.

    Returns:
        The items of the array.

    Raises:
        TypeError: If *data* is not a bytes-like object or *unpack_item* is
            not callable.
        ValueError: If *data* ends before the array could be read.

    Examples:
        >>> unpack_array(b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x07', lambda u: u.unpack_uint())
        [7]
    """
    payload = _require_bytes(data, "data")
    _require_callable(unpack_item, "unpack_item")
    unpacker = _unpacker(payload)
    count = _read(unpacker.unpack_uint, "the length of an array")
    items: List[Any] = []
    for _ in range(count):
        items.append(_read(lambda: unpack_item(unpacker), "an array item"))
    return items


def pack_farray(count: int, items: Sequence[Any], pack_item: PackerCallback) -> bytes:
    """Pack *items* as a fixed length XDR array.

    No length prefix is written, so the reader has to know how many items the
    array holds.

    Args:
        count: The number of items the array holds.
        items: The items to pack.
        pack_item: The callback that writes a single item into the packer.

    Returns:
        The encoded array.

    Raises:
        TypeError: If *count* is not an integer, *items* is not a sequence of
            values, or *pack_item* is not callable.
        ValueError: If *count* is negative or does not match the number of
            items.
    """
    size = _require_int(count, "count")
    if size < 0:
        raise ValueError(f"count must not be negative, got {size}")
    values = _require_sequence(items, "items")
    _require_callable(pack_item, "pack_item")
    if len(values) != size:
        raise ValueError(f"count must match the number of items, got {size} and {len(values)}")
    packer = _packer()
    for item in values:
        pack_item(packer, item)
    return packer.get_buffer()


def unpack_farray(count: int, data: BytesLike, unpack_item: UnpackerCallback) -> List[Any]:
    """Unpack a fixed length XDR array from *data*.

    Args:
        count: The number of items the array holds.
        data: The payload to read from.
        unpack_item: The callback that reads a single item from the unpacker.

    Returns:
        The items of the array.

    Raises:
        TypeError: If *count* is not an integer, *data* is not a bytes-like
            object, or *unpack_item* is not callable.
        ValueError: If *count* is negative or *data* ends before the array
            could be read.
    """
    size = _require_int(count, "count")
    if size < 0:
        raise ValueError(f"count must not be negative, got {size}")
    payload = _require_bytes(data, "data")
    _require_callable(unpack_item, "unpack_item")
    unpacker = _unpacker(payload)
    items: List[Any] = []
    for _ in range(size):
        items.append(_read(lambda: unpack_item(unpacker), "an array item"))
    return items


def pack_list(items: Sequence[Any], pack_item: PackerCallback) -> bytes:
    """Pack *items* as an XDR list.

    Every item is preceded by a flag of one and the list is terminated by a
    flag of zero, so a reader can stop at the end of the list without knowing
    its length in advance.

    Args:
        items: The items to pack.
        pack_item: The callback that writes a single item into the packer.

    Returns:
        The encoded list.

    Raises:
        TypeError: If *items* is not a sequence of values or *pack_item* is
            not callable.

    Examples:
        >>> pack_list([1], lambda packer, item: packer.pack_uint(item))
        b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x00'
    """
    values = _require_sequence(items, "items")
    _require_callable(pack_item, "pack_item")
    packer = _packer()
    for item in values:
        packer.pack_uint(1)
        pack_item(packer, item)
    packer.pack_uint(0)
    return packer.get_buffer()


def unpack_list(data: BytesLike, unpack_item: UnpackerCallback) -> List[Any]:
    """Unpack an XDR list from *data*.

    Args:
        data: The payload to read from.
        unpack_item: The callback that reads a single item from the unpacker.

    Returns:
        The items of the list.

    Raises:
        TypeError: If *data* is not a bytes-like object or *unpack_item* is
            not callable.
        ValueError: If *data* ends before the list could be read.
        ConversionError: If the payload holds a flag other than zero or one.
    """
    payload = _require_bytes(data, "data")
    _require_callable(unpack_item, "unpack_item")
    unpacker = _unpacker(payload)
    items: List[Any] = []
    while True:
        flag = _read(unpacker.unpack_uint, "a list flag")
        if flag == 0:
            return items
        if flag != 1:
            raise ConversionError(f"0 or 1 expected, got {flag!r}")
        items.append(_read(lambda: unpack_item(unpacker), "a list item"))


def pack_uint_array(items: Sequence[int]) -> bytes:
    """Pack *items* as an XDR array of unsigned integers.

    The array is prefixed with the number of items it holds.

    Args:
        items: The integers to pack.  Every item must fit in an unsigned
            32-bit integer.

    Returns:
        The encoded array.

    Raises:
        TypeError: If *items* is not a sequence or an item is not an integer.
        ValueError: If an item does not fit in an unsigned 32-bit integer.

    Examples:
        >>> pack_uint_array([1, 2])
        b'\\x00\\x00\\x00\\x02\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x02'
    """
    values = _require_sequence(items, "items")
    packer = _packer()
    packer.pack_uint(len(values))
    for index, item in enumerate(values):
        number = _require_int(item, f"items[{index}]")
        _require_range(number, f"items[{index}]", 0, UINT_MAX)
        packer.pack_uint(number)
    return packer.get_buffer()


def unpack_uint_array(data: BytesLike) -> List[int]:
    """Unpack an XDR array of unsigned integers from *data*.

    Args:
        data: The payload to read from.

    Returns:
        The integers of the array.

    Raises:
        TypeError: If *data* is not a bytes-like object.
        ValueError: If *data* ends before the array could be read.

    Examples:
        >>> unpack_uint_array(b'\\x00\\x00\\x00\\x01\\x00\\x00\\x00\\x07')
        [7]
    """
    payload = _require_bytes(data, "data")
    unpacker = _unpacker(payload)
    count = _read(unpacker.unpack_uint, "the length of an array")
    items: List[int] = []
    for _ in range(count):
        items.append(_read(unpacker.unpack_uint, "an array item"))
    return items
