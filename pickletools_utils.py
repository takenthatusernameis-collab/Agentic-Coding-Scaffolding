"""Pickletools utility functions."""

import io
import pickle
import pickletools
from typing import Any, IO


def dis(pickle_data: bytes | bytearray | IO[bytes], out: IO[str] | None = None,
        memo: dict[Any, Any] | None = None, indentlevel: int = 4,
        annotate: int = 0) -> None:
    """Disassemble a pickle and output the symbolic disassembly."""
    pickletools.dis(pickle_data, out=out, memo=memo, indentlevel=indentlevel, annotate=annotate)


def genops(pickle_data: bytes | bytearray | IO[bytes]) -> Any:
    """Generate all the opcode proto-objects in pickle."""
    return pickletools.genops(pickle_data)


def optimize(pickle_data: bytes) -> bytes:
    """Return an optimized version of the pickle."""
    return pickletools.optimize(pickle_data)


def get_opcode_info(opcode_name: str) -> Any:
    """Return information about a pickle opcode."""
    for op in pickletools.opcodes:
        if op.name == opcode_name:
            return op
    raise KeyError(opcode_name)


def list_opcodes() -> list[str]:
    """Return a list of all opcode names."""
    return [op.name for op in pickletools.opcodes]


def is_opcode(name: str) -> bool:
    """Check if a name is a valid pickle opcode."""
    return any(op.name == name for op in pickletools.opcodes)


def get_pickle_size(pickle_data: bytes) -> int:
    """Get the size of a pickle in bytes."""
    return len(pickle_data)


def decode_long(data: bytes) -> int:
    """Decode a long integer from a bytes object."""
    return pickletools.decode_long(data)


def encode_long(x: int) -> bytes:
    """Encode a long integer as a bytes object."""
    if hasattr(pickletools, 'encode_long'):
        return pickletools.encode_long(x)
    # Fallback: use pickle's encoding
    f = io.BytesIO()
    p = pickle._Pickler(f, protocol=2)
    p.dump(x)
    return f.getvalue()


def __getattr__(name: str) -> Any:
    """Delegate unknown attributes to the pickletools module."""
    return getattr(pickletools, name)
