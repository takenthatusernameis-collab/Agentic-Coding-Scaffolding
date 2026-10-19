"""Ctypes utility functions wrapping the standard library ``ctypes`` module."""

from __future__ import annotations

import ctypes as _ctypes
from ctypes.util import find_library as _find_library
from typing import Any

__all__: list[str] = [
    "c_byte",
    "c_ubyte",
    "c_short",
    "c_ushort",
    "c_int",
    "c_uint",
    "c_long",
    "c_ulong",
    "c_longlong",
    "c_ulonglong",
    "c_float",
    "c_double",
    "c_longdouble",
    "c_char",
    "c_wchar",
    "c_bool",
    "c_void_p",
    "c_char_p",
    "c_wchar_p",
    "c_size_t",
    "c_ssize_t",
    "c_int8",
    "c_uint8",
    "c_int16",
    "c_uint16",
    "c_int32",
    "c_uint32",
    "c_int64",
    "c_uint64",
    "Structure",
    "Union",
    "POINTER",
    "Array",
    "CFUNCTYPE",
    "sizeof",
    "alignment",
    "addressof",
    "pointer",
    "byref",
    "cast",
    "memmove",
    "memset",
    "string_at",
    "create_string_buffer",
    "create_unicode_buffer",
    "get_errno",
    "set_errno",
    "get_last_error",
    "set_last_error",
    "find_library",
]


c_byte = _ctypes.c_byte
c_ubyte = _ctypes.c_ubyte
c_short = _ctypes.c_short
c_ushort = _ctypes.c_ushort
c_int = _ctypes.c_int
c_uint = _ctypes.c_uint
c_long = _ctypes.c_long
c_ulong = _ctypes.c_ulong
c_longlong = _ctypes.c_longlong
c_ulonglong = _ctypes.c_ulonglong
c_float = _ctypes.c_float
c_double = _ctypes.c_double
c_longdouble = _ctypes.c_longdouble
c_char = _ctypes.c_char
c_wchar = _ctypes.c_wchar
c_bool = _ctypes.c_bool
c_void_p = _ctypes.c_void_p
c_char_p = _ctypes.c_char_p
c_wchar_p = _ctypes.c_wchar_p
c_size_t = _ctypes.c_size_t
c_ssize_t = _ctypes.c_ssize_t
c_int8 = _ctypes.c_int8
c_uint8 = _ctypes.c_uint8
c_int16 = _ctypes.c_int16
c_uint16 = _ctypes.c_uint16
c_int32 = _ctypes.c_int32
c_uint32 = _ctypes.c_uint32
c_int64 = _ctypes.c_int64
c_uint64 = _ctypes.c_uint64

Structure = _ctypes.Structure
Union = _ctypes.Union
POINTER = _ctypes.POINTER
Array = _ctypes.Array
CFUNCTYPE = _ctypes.CFUNCTYPE


def sizeof(obj: Any) -> int:
    """Return the size in bytes of a ctypes type or instance.

    Args:
        obj: A ctypes type or instance.

    Returns:
        The size in bytes of *obj*.

    See :func:`ctypes.sizeof`.
    """
    return _ctypes.sizeof(obj)


def alignment(obj_or_type: Any) -> int:
    """Return the alignment in bytes of a ctypes type or instance.

    Args:
        obj_or_type: A ctypes type or instance.

    Returns:
        The alignment in bytes of *obj_or_type*.

    See :func:`ctypes.alignment`.
    """
    return _ctypes.alignment(obj_or_type)


def addressof(obj: Any) -> int:
    """Return the address of a ctypes instance as an integer.

    Args:
        obj: A ctypes instance.

    Returns:
        The memory address of *obj*.

    See :func:`ctypes.addressof`.
    """
    return _ctypes.addressof(obj)


def pointer(obj: Any) -> Any:
    """Return a ctypes pointer to *obj*.

    Args:
        obj: A ctypes instance or type.

    Returns:
        A ctypes pointer referencing *obj*.

    See :func:`ctypes.pointer`.
    """
    return _ctypes.pointer(obj)


def byref(obj: Any, offset: int = 0) -> Any:
    """Return a lightweight pointer to *obj* as a ctypes byref object.

    Args:
        obj: A ctypes instance.
        offset: An optional byte offset added to the address.

    Returns:
        A ctypes byref object for *obj*.

    See :func:`ctypes.byref`.
    """
    return _ctypes.byref(obj, offset)


def cast(obj: Any, type: Any) -> Any:
    """Cast a ctypes object to a different ctypes type.

    Args:
        obj: A ctypes instance or pointer.
        type: A ctypes type to cast to.

    Returns:
        A ctypes object of type *type* referencing the same memory.

    See :func:`ctypes.cast`.
    """
    return _ctypes.cast(obj, type)


def memmove(dst: Any, src: Any, count: int) -> None:
    """Copy *count* bytes from *src* to *dst*.

    Args:
        dst: Destination buffer (ctypes instance or integer address).
        src: Source buffer (ctypes instance or integer address).
        count: Number of bytes to copy.

    Returns:
        None; memory is copied in place.

    See :func:`ctypes.memmove`.
    """
    _ctypes.memmove(dst, src, count)


def memset(dst: Any, char: int, count: int) -> None:
    """Fill *count* bytes of *dst* with the byte value *char*.

    Args:
        dst: Destination buffer (ctypes instance or integer address).
        char: Byte value (0-255) to fill with.
        count: Number of bytes to fill.

    Returns:
        None; memory is filled in place.

    See :func:`ctypes.memset`.
    """
    _ctypes.memset(dst, char, count)


def string_at(addr: int, size: int = -1) -> bytes:
    """Return the C string at memory address *addr* as ``bytes``.

    Args:
        addr: Memory address of the string.
        size: Maximum number of bytes to read. A negative value reads
            up to the first null byte.

    Returns:
        The string at *addr* as ``bytes``.

    See :func:`ctypes.string_at`.
    """
    return _ctypes.string_at(addr, size)


def create_string_buffer(init_or_size: Any, size: int | None = None) -> Any:
    """Create a mutable character buffer.

    Args:
        init_or_size: An initial bytes-like value or the buffer size.
        size: An optional explicit buffer size.

    Returns:
        A mutable ctypes character buffer.

    See :func:`ctypes.create_string_buffer`.
    """
    if size is None:
        return _ctypes.create_string_buffer(init_or_size)
    return _ctypes.create_string_buffer(init_or_size, size)


def create_unicode_buffer(init_or_size: Any, size: int | None = None) -> Any:
    """Create a mutable unicode character buffer.

    Args:
        init_or_size: An initial string or the buffer size in characters.
        size: An optional explicit buffer size in characters.

    Returns:
        A mutable ctypes unicode buffer.

    See :func:`ctypes.create_unicode_buffer`.
    """
    if size is None:
        return _ctypes.create_unicode_buffer(init_or_size)
    return _ctypes.create_unicode_buffer(init_or_size, size)


def get_errno() -> int:
    """Return the current value of the ctypes errno variable.

    Returns:
        The current errno value.

    See :func:`ctypes.get_errno`.
    """
    return _ctypes.get_errno()


def set_errno(errno: int) -> None:
    """Set the current value of the ctypes errno variable.

    Args:
        errno: The errno value to set.

    Returns:
        None.

    See :func:`ctypes.set_errno`.
    """
    _ctypes.set_errno(errno)


def get_last_error() -> int:
    """Return the current value of the ctypes last-error variable.

    Available on Windows. On other platforms this raises ``AttributeError``.

    Returns:
        The current last-error value.

    Raises:
        AttributeError: If last-error is not supported on this platform.

    See :func:`ctypes.get_last_error`.
    """
    return int(getattr(_ctypes, "get_last_error")())


def set_last_error(errno: int) -> None:
    """Set the current value of the ctypes last-error variable.

    Available on Windows. On other platforms this raises ``AttributeError``.

    Args:
        errno: The last-error value to set.

    Returns:
        None.

    Raises:
        AttributeError: If last-error is not supported on this platform.

    See :func:`ctypes.set_last_error`.
    """
    getattr(_ctypes, "set_last_error")(errno)


def find_library(name: str) -> str | None:
    """Locate a shared library by name.

    Args:
        name: The library name to locate (e.g. ``"c"`` or ``"m"``).

    Returns:
        The path to the library, or ``None`` if it cannot be found.

    See :func:`ctypes.util.find_library`.
    """
    return _find_library(name)
