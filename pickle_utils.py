"""Utilities for object serialization (wrapping :mod:`pickle`)."""

import pickle as _pickle
from typing import Any

_PROTOCOLS = (-1, 0, 1, 2, 3, 4, 5)


def dump(obj, file, protocol=None, *, fix_imports=True, buffer_callback=None):
    """Pickle *obj* into an open binary *file*.

    Args:
        obj: The object to serialize.
        file: A binary-mode file-like object opened for writing.
        protocol: Pickle protocol to use (defaults to ``pickle.HIGHEST_PROTOCOL``).

    Returns:
        ``None``; the object is written to *file*.

    See :func:`pickle.dump`.
    """
    return _pickle.dump(
        obj,
        file,
        protocol,
        fix_imports=fix_imports,
        buffer_callback=buffer_callback,
    )


def dumps(obj, protocol=None, *, fix_imports=True, buffer_callback=None) -> bytes:
    """Return the pickled representation of *obj* as ``bytes``.

    Args:
        obj: The object to serialize.
        protocol: Pickle protocol to use (defaults to ``pickle.HIGHEST_PROTOCOL``).

    Returns:
        The pickled bytes.

    See :func:`pickle.dumps`.
    """
    return _pickle.dumps(
        obj,
        protocol,
        fix_imports=fix_imports,
        buffer_callback=buffer_callback,
    )


def load(file, *, fix_imports=True, buffers=()) -> Any:
    """Unpickle an object from an open binary *file*.

    Args:
        file: A binary-mode file-like object opened for reading.
        fix_imports: Whether to translate ``2to3``-style pickle names.

    Returns:
        The unpickled object.

    See :func:`pickle.load`.
    """
    return _pickle.load(file, fix_imports=fix_imports, buffers=buffers)


def loads(data, *, fix_imports=True, buffers=()) -> Any:
    """Unpickle an object from a ``bytes`` buffer.

    Args:
        data: The pickled bytes.
        fix_imports: Whether to translate ``2to3``-style pickle names.

    Returns:
        The unpickled object.

    See :func:`pickle.loads`.
    """
    return _pickle.loads(data, fix_imports=fix_imports, buffers=buffers)


def pickler(file, protocol=None, *, fix_imports=True) -> _pickle.Pickler:
    """Return a :class:`pickle.Pickler` for streaming serialization.

    Args:
        file: A binary-mode file-like object opened for writing.
        protocol: Pickle protocol to use (defaults to ``pickle.HIGHEST_PROTOCOL``).

    Returns:
        A configured :class:`pickle.Pickler`.

    See :class:`pickle.Pickler`.
    """
    return _pickle.Pickler(file, protocol=protocol, fix_imports=fix_imports)


def unpickler(file, *, fix_imports=True, buffers=()) -> _pickle.Unpickler:
    """Return a :class:`pickle.Unpickler` for streaming deserialization.

    Args:
        file: A binary-mode file-like object opened for reading.
        fix_imports: Whether to translate ``2to3``-style pickle names.

    Returns:
        A configured :class:`pickle.Unpickler`.

    See :class:`pickle.Unpickler`.
    """
    return _pickle.Unpickler(file, fix_imports=fix_imports, buffers=buffers)


def is_valid_protocol(protocol) -> bool:
    """Return ``True`` if *protocol* is a valid pickle protocol number.

    Args:
        protocol: Candidate protocol value to validate.

    Returns:
        ``True`` when *protocol* is one of ``-1`` through ``5``.
    """
    return protocol in _PROTOCOLS


def validate_protocol(protocol) -> int:
    """Validate and normalize a pickle *protocol* argument.

    Args:
        protocol: A protocol number or ``None`` (defaults to highest).

    Returns:
        The validated protocol number.

    Raises:
        TypeError: If *protocol* is not an int.
        ValueError: If *protocol* is outside the supported range.
    """
    if protocol is None:
        return _pickle.HIGHEST_PROTOCOL
    if not isinstance(protocol, int) or isinstance(protocol, bool):
        raise TypeError("protocol must be an int or None")
    if protocol not in _PROTOCOLS:
        raise ValueError(f"protocol must be one of {_PROTOCOLS}, got {protocol!r}")
    return protocol
