"""Utilities for working with bytes and binary data."""

from __future__ import annotations

__all__: list[str] = [
    "to_hex",
    "from_hex",
    "xor",
    "chunk",
    "concat",
    "repeat",
    "reverse",
    "contains",
    "index_of",
    "starts_with",
    "ends_with",
    "split",
    "find",
    "rfind",
    "rindex",
    "replace",
    "count",
    "decode_utf8",
    "encode_utf8",
    "rstrip",
    "lstrip",
    "strip",
    "center",
    "ljust",
    "rjust",
    "zfill",
]


def to_hex(data: bytes) -> str:
    """Return the hexadecimal representation of *data*.

    Args:
        data: Bytes or bytearray to encode.

    Returns:
        Hexadecimal string representation of *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).hex()


def from_hex(text: str) -> bytes:
    """Decode a hex string into bytes.

    Args:
        text: Hexadecimal string to decode.

    Returns:
        Decoded bytes.

    Raises:
        TypeError: If *text* is not a str.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return bytes.fromhex(text)


def xor(data: bytes, key: bytes) -> bytes:
    """XOR *data* with a repeating *key*.

    Args:
        data: Bytes or bytearray to transform.
        key: Non-empty bytes or bytearray key.

    Returns:
        Result of XORing *data* with *key*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.
        ValueError: If *key* is empty or not bytes-like.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(key, (bytes, bytearray)) or not key:
        raise ValueError("key must be non-empty bytes or bytearray")
    key_bytes = bytes(key)
    return bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))


def chunk(data: bytes, size: int) -> list[bytes]:
    """Split *data* into chunks of *size* bytes.

    Args:
        data: Bytes or bytearray to split.
        size: Positive chunk size in bytes.

    Returns:
        List of byte chunks.

    Raises:
        TypeError: If *data* is not bytes or bytearray.
        ValueError: If *size* is not a positive integer.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer")
    data = bytes(data)
    return [data[i : i + size] for i in range(0, len(data), size)]


def concat(*parts: bytes) -> bytes:
    """Concatenate one or more bytes-like objects into a single ``bytes``.

    Args:
        *parts: Bytes or bytearray objects to concatenate.

    Returns:
        Concatenated bytes.

    Raises:
        TypeError: If any part is not bytes or bytearray.

    Examples:
        >>> concat(b"ab", b"cd")
        b'abcd'
        >>> concat(b"ab", bytearray(b"ef"))
        b'abef'
        >>> concat()
        b''
    """
    result = bytearray()
    for part in parts:
        if not isinstance(part, (bytes, bytearray)):
            raise TypeError("parts must be bytes or bytearray")
        result.extend(part)
    return bytes(result)


def repeat(data: bytes, count: int) -> bytes:
    """Repeat *data* *count* times.

    Args:
        data: Bytes or bytearray to repeat.
        count: Non-negative repetition count.

    Returns:
        Repeated bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.
        ValueError: If *count* is negative or not an int.

    Examples:
        >>> repeat(b"ab", 3)
        b'ababab'
        >>> repeat(b"x", 0)
        b''
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(count, int) or count < 0:
        raise ValueError("count must be a non-negative integer")
    return bytes(data) * count


def reverse(data: bytes) -> bytes:
    """Return a reversed copy of *data*.

    Args:
        data: Bytes or bytearray to reverse.

    Returns:
        Reversed bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> reverse(b"abc")
        b'cba'
        >>> reverse(bytearray(b"ab"))
        b'ba'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(reversed(bytes(data)))


def contains(data: bytes, sub: bytes) -> bool:
    """Return True if *sub* is contained within *data*.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray to search for.

    Returns:
        True if *sub* is contained in *data*.

    Raises:
        TypeError: If *data* or *sub* is not bytes or bytearray.

    Examples:
        >>> contains(b"hello", b"ll")
        True
        >>> contains(b"hello", b"world")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    return bytes(sub) in bytes(data)


def index_of(data: bytes, sub: bytes) -> int:
    """Return the first index of *sub* in *data*, or -1 if not found.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray subsequence to search for.

    Returns:
        The lowest index in *data* where *sub* is found, or -1 if *sub* is
        not present.

    Raises:
        TypeError: If *data* or *sub* is not bytes or bytearray.

    Examples:
        >>> index_of(b"hello world", b"world")
        6
        >>> index_of(b"hello", b"x")
        -1
        >>> index_of(b"aaaa", b"aa")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    return bytes(data).find(bytes(sub))


def starts_with(data: bytes, prefix: bytes) -> bool:
    """Return True if *data* starts with *prefix*.

    Args:
        data: Bytes or bytearray to test.
        prefix: Bytes or bytearray prefix.

    Returns:
        True if *data* starts with *prefix*.

    Raises:
        TypeError: If *data* or *prefix* is not bytes or bytearray.

    Examples:
        >>> starts_with(b"hello", b"he")
        True
        >>> starts_with(b"hello", b"lo")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(prefix, (bytes, bytearray)):
        raise TypeError("prefix must be bytes or bytearray")
    return bytes(data).startswith(bytes(prefix))


def ends_with(data: bytes, suffix: bytes) -> bool:
    """Return True if *data* ends with *suffix*.

    Args:
        data: Bytes or bytearray to check.
        suffix: Suffix to look for.

    Returns:
        True if *data* ends with *suffix*, False otherwise.

    Raises:
        TypeError: If *data* or *suffix* is not bytes or bytearray.

    Examples:
        >>> ends_with(b"hello", b"lo")
        True
        >>> ends_with(b"hello", b"he")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(suffix, (bytes, bytearray)):
        raise TypeError("suffix must be bytes or bytearray")
    return bytes(data).endswith(bytes(suffix))


def split(data: bytes, sep: bytes | None = None, maxsplit: int = -1) -> list[bytes]:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if sep is not None and not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes, bytearray, or None")
    if not isinstance(maxsplit, int) or isinstance(maxsplit, bool):
        raise TypeError("maxsplit must be an int")
    if sep is None:
        return bytes(data).split(maxsplit=maxsplit)
    return bytes(data).split(bytes(sep), maxsplit)


def find(data: bytes, sub: bytes, start: int = 0, end: int | None = None) -> int:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).find(bytes(sub), start, end)


def rfind(data: bytes, sub: bytes, start: int = 0, end: int | None = None) -> int:
    """Return the highest index of *sub* in *data*, or -1 if not found.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray subsequence to search for.
        start: Optional starting index for the search.
        end: Optional ending index for the search.

    Returns:
        The highest index in *data* where *sub* is found, or -1 if *sub* is
        not present.

    Raises:
        TypeError: If *data* or *sub* is not bytes or bytearray, or if
            *start*/*end* is not an int.

    Examples:
        >>> rfind(b"hello world", b"o")
        7
        >>> rfind(b"hello", b"x")
        -1
        >>> rfind(b"ababab", b"ab")
        4
        >>> rfind(b"hello world", b"o", 0, 5)
        4
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).rfind(bytes(sub), start, end)


def rindex(data: bytes, sub: bytes, start: int = 0, end: int | None = None) -> int:
    """Return the highest index of *sub* in *data*, raising ValueError if not found.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray subsequence to search for.
        start: Optional starting index for the search.
        end: Optional ending index for the search.

    Returns:
        The highest index in *data* where *sub* is found.

    Raises:
        TypeError: If *data* or *sub* is not bytes or bytearray, or if
            *start*/*end* is not an int.
        ValueError: If *sub* is not found in *data*.

    Examples:
        >>> rindex(b"hello world", b"o")
        7
        >>> rindex(b"ababab", b"ab")
        4
        >>> rindex(b"hello world", b"o", 0, 5)
        4
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).rindex(bytes(sub), start, end)


def replace(data: bytes, old: bytes, new: bytes, count: int = -1) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(old, (bytes, bytearray)):
        raise TypeError("old must be bytes or bytearray")
    if not isinstance(new, (bytes, bytearray)):
        raise TypeError("new must be bytes or bytearray")
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("count must be an int")
    return bytes(data).replace(bytes(old), bytes(new), count)


def count(data: bytes, sub: bytes, start: int = 0, end: int | None = None) -> int:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).count(bytes(sub), start, end)


def decode_utf8(data: bytes, errors: str = "strict") -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(errors, str):
        raise TypeError("errors must be a string")
    return bytes(data).decode("utf-8", errors=errors)


def encode_utf8(s: str, errors: str = "strict") -> bytes:
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    if not isinstance(errors, str):
        raise TypeError("errors must be a string")
    return s.encode("utf-8", errors=errors)


def rstrip(data: bytes, chars: bytes | None = None) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if chars is not None and not isinstance(chars, (bytes, bytearray)):
        raise TypeError("chars must be bytes, bytearray, or None")
    if chars is None:
        return bytes(data).rstrip()
    return bytes(data).rstrip(bytes(chars))


def lstrip(data: bytes, chars: bytes | None = None) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if chars is not None and not isinstance(chars, (bytes, bytearray)):
        raise TypeError("chars must be bytes, bytearray, or None")
    if chars is None:
        return bytes(data).lstrip()
    return bytes(data).lstrip(bytes(chars))


def strip(data: bytes, chars: bytes | None = None) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if chars is not None and not isinstance(chars, (bytes, bytearray)):
        raise TypeError("chars must be bytes, bytearray, or None")
    if chars is None:
        return bytes(data).strip()
    return bytes(data).strip(bytes(chars))


def center(data: bytes, width: int, fillbyte: bytes = b" ") -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an int")
    if not isinstance(fillbyte, (bytes, bytearray)):
        raise TypeError("fillbyte must be bytes or bytearray")
    fb = bytes(fillbyte)
    if len(fb) != 1:
        fb = fb[:1] or b" "
    else:
        fb = fb
    return bytes(data).center(width, fb[:1]) if len(fb) != 1 else bytes(data).center(width, fb)


def ljust(data: bytes, width: int, fillbyte: bytes = b" ") -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an int")
    if not isinstance(fillbyte, (bytes, bytearray)):
        raise TypeError("fillbyte must be bytes or bytearray")
    fb = bytes(fillbyte)
    if len(fb) != 1:
        raise ValueError("fillbyte must be a single byte")
    return bytes(data).ljust(width, fb)


def rjust(data: bytes, width: int, fillbyte: bytes = b" ") -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an int")
    if not isinstance(fillbyte, (bytes, bytearray)):
        raise TypeError("fillbyte must be bytes or bytearray")
    fb = bytes(fillbyte)
    if len(fb) != 1:
        raise ValueError("fillbyte must be a single byte")
    return bytes(data).rjust(width, fb)


def zfill(data: bytes, width: int) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an int")
    return bytes(data).zfill(width)
