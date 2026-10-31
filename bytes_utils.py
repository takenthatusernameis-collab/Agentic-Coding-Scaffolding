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
        data: Bytes or bytearray to test.
        suffix: Bytes or bytearray suffix.

    Returns:
        True if *data* ends with *suffix*.

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
