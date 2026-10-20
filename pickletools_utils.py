"""Pickletools utility functions.

Thin, validated wrappers around the standard library :mod:`pickletools` module.
The helpers disassemble, optimise, and inspect pickle byte streams; they never
unpickle anything and never execute the code a pickle describes.

.. note::

   The standard library changed two details over the lifetime of the supported
   interpreters, and this wrapper hides both of them:

   * ``pickletools.OpcodeInfo`` was a named tuple up to Python 3.11 and became
     a plain class in Python 3.12.  :func:`get_opcode_info` therefore reports
     the opcode name and the fields the standard library documents instead of
     relying on the concrete type.
   * ``pickletools.decode_long`` used to expect a length-prefixed payload and
     decodes raw little-endian bytes since Python 3.11.  :func:`encode_long`
     inspects the interpreter at import time and always produces a payload the
     running interpreter can decode again.
"""

from __future__ import annotations

import pickle
import pickletools
from typing import IO, Any, Dict, Iterator, List, Optional, Tuple, Union, cast

__all__ = [
    "decode_long",
    "dis",
    "encode_long",
    "genops",
    "get_opcode_info",
    "get_pickle_size",
    "is_opcode",
    "list_opcodes",
    "optimize",
]

#: The payload accepted by the standard library ``dis`` and ``genops`` helpers.
PickleData = Union[bytes, bytearray, IO[bytes]]


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes, raising ``TypeError`` for other types."""
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_pickle_data(value: Any, name: str) -> PickleData:
    """Return *value* as a pickle payload the standard library accepts."""
    if isinstance(value, (bytes, bytearray)):
        return value
    if hasattr(value, "read"):
        return cast(PickleData, value)
    raise TypeError(
        f"{name} must be bytes or a binary file object, got {type(value).__name__}"
    )


def _require_out(value: Any) -> Optional[IO[str]]:
    """Return *value* as a text stream, raising ``TypeError`` for other types."""
    if value is None:
        return None
    if hasattr(value, "write"):
        return cast(IO[str], value)
    raise TypeError(f"out must be a text stream or None, got {type(value).__name__}")


def _require_memo(value: Any) -> Optional[Dict[Any, Any]]:
    """Return *value* as a memo dictionary, raising ``TypeError`` otherwise."""
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    raise TypeError(f"memo must be a dict or None, got {type(value).__name__}")


def _require_indentlevel(value: Any) -> int:
    """Return *value* as an indentation level, raising for invalid values."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"indentlevel must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"indentlevel must be >= 0, got {value}")
    return value


def _require_annotate(value: Any) -> int:
    """Return *value* as an annotation level, raising for invalid values."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"annotate must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"annotate must be >= 0, got {value}")
    return value


def _uses_length_prefix() -> bool:
    """Return ``True`` when the standard library expects a length prefix.

    Python 3.10 and earlier decode a payload whose first byte holds the
    number of payload bytes; later interpreters decode the raw little-endian
    bytes.  The two formats are told apart by a payload that is valid in
    exactly one of them.
    """
    return pickle.decode_long(b"\x02\x05\x00") != 0x000502


def _payload_length(value: int) -> int:
    """Return the number of bytes needed to store *value* as a signed integer."""
    return max(1, (value.bit_length() + 8) // 8)


def dis(
    pickle_data: PickleData,
    out: Optional[IO[str]] = None,
    memo: Optional[Dict[Any, Any]] = None,
    indentlevel: int = 4,
    annotate: int = 0,
) -> None:
    """Write the symbolic disassembly of a pickle.

    Args:
        pickle_data: The pickle to disassemble, as bytes or a binary file.
        out: The text stream the disassembly is written to.  Defaults to
            standard output.
        memo: The memo dictionary the disassembly refers to.
        indentlevel: The number of spaces one nesting level adds.
        annotate: The annotation level; ``1`` adds the opcode argument names.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *indentlevel* or *annotate* is negative.
    """
    data = _require_pickle_data(pickle_data, "pickle_data")
    stream = _require_out(out)
    memo_dict = _require_memo(memo)
    level = _require_indentlevel(indentlevel)
    annotation = _require_annotate(annotate)
    pickletools.dis(data, out=stream, memo=memo_dict, indentlevel=level, annotate=annotation)


def genops(pickle_data: PickleData) -> Iterator[Any]:
    """Return an iterator over the opcodes of a pickle.

    Args:
        pickle_data: The pickle to scan, as bytes or a binary file.

    Returns:
        An iterator of ``(opcode, argument, position)`` triples.

    Raises:
        TypeError: If *pickle_data* is neither bytes nor a binary file.
    """
    data = _require_pickle_data(pickle_data, "pickle_data")
    return pickletools.genops(data)


def optimize(pickle_data: bytes) -> bytes:
    """Return an optimized copy of a pickle.

    Args:
        pickle_data: The pickle to optimize.

    Returns:
        The optimized pickle.

    Raises:
        TypeError: If *pickle_data* is not bytes.
    """
    data = _require_bytes(pickle_data, "pickle_data")
    return pickletools.optimize(data)


def get_opcode_info(opcode_name: str) -> Tuple[Any, ...]:
    """Return the description of a pickle opcode.

    Args:
        opcode_name: The symbolic name of the opcode, such as ``"PROTO"``.

    Returns:
        A tuple with the opcode name, its byte code, its argument descriptor,
        the stack before and after the opcode, the protocol that introduced it,
        and its documentation.

    Raises:
        TypeError: If *opcode_name* is not a string.
        KeyError: If no opcode carries that name.
    """
    if not isinstance(opcode_name, str):
        raise TypeError(f"opcode_name must be a str, got {type(opcode_name).__name__}")
    for opcode in pickletools.opcodes:
        if opcode.name == opcode_name:
            return (
                opcode.name,
                opcode.code,
                opcode.arg,
                tuple(opcode.stack_before),
                tuple(opcode.stack_after),
                opcode.proto,
                opcode.doc,
            )
    raise KeyError(f"unknown pickle opcode: {opcode_name}")


def list_opcodes() -> List[str]:
    """Return the names of every pickle opcode.

    Returns:
        The opcode names in the order the standard library declares them.
    """
    return [opcode.name for opcode in pickletools.opcodes]


def is_opcode(name: str) -> bool:
    """Report whether *name* is a pickle opcode.

    Args:
        name: The symbolic name of the opcode.

    Returns:
        ``True`` when the standard library knows the opcode.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    return any(opcode.name == name for opcode in pickletools.opcodes)


def get_pickle_size(pickle_data: bytes) -> int:
    """Return the size of a pickle in bytes.

    Args:
        pickle_data: The pickle to measure.

    Returns:
        The number of bytes the pickle occupies.

    Raises:
        TypeError: If *pickle_data* is not bytes.
    """
    data = _require_bytes(pickle_data, "pickle_data")
    return len(data)


def decode_long(data: bytes) -> int:
    """Decode an integer from its two's complement little-endian form.

    Args:
        data: The bytes to decode.

    Returns:
        The decoded integer.

    Raises:
        TypeError: If *data* is not bytes.
        ValueError: If the standard library rejects the payload.
    """
    payload = _require_bytes(data, "data")
    return pickle.decode_long(payload)


def encode_long(value: int) -> bytes:
    """Encode an integer in the form the standard library decodes again.

    Args:
        value: The integer to encode.

    Returns:
        The encoded payload.

    Raises:
        TypeError: If *value* is not an integer.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"value must be an int, got {type(value).__name__}")
    payload = value.to_bytes(_payload_length(value), "little", signed=True)
    if not _uses_length_prefix():
        return payload
    if len(payload) >= 0xFF:
        return b"\xff" + payload
    return bytes([len(payload)]) + payload
