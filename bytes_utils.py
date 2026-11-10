"""Utilities for working with bytes and binary data."""

from __future__ import annotations

from typing import Literal

__all__: list[str] = [
    "to_hex",
    "from_hex",
    "xor",
    "chunk",
    "concat",
    "repeat",
    "reverse",
    "contains",
    "not_contains",
    "index",
    "index_of",
    "partition",
    "starts_with",
    "ends_with",
    "split",
    "find",
    "rfind",
    "rindex",
    "rpartition",
    "rsplit",
    "replace",
    "count",
    "count_digits",
    "decode_utf8",
    "encode_utf8",
    "rstrip",
    "lstrip",
    "strip",
    "center",
    "ljust",
    "rjust",
    "zfill",
    "removeprefix",
    "removesuffix",
    "splitlines",
    "upper",
    "lower",
    "capitalize",
    "title",
    "swapcase",
    "casefold",
    "isalnum",
    "count_alnum",
    "has_alnum",
    "isalpha",
    "count_alpha",
    "has_alpha",
    "isascii",
    "count_ascii",
    "has_ascii",
    "isdigit",
    "islower",
    "count_lower",
    "has_lower",
    "isspace",
    "count_space",
    "has_space",
    "istitle",
    "count_title",
    "has_title",
    "isupper",
    "count_upper",
    "has_upper",
    "isprintable",
    "count_printable",
    "has_printable",
    "isidentifier",
    "join",
    "expandtabs",
    "decode_ascii",
    "encode_ascii",
    "maketrans",
    "translate",
    "to_int",
    "from_int",
    "bit_count",
    "has_digits",
    "has_set_bits",
    "is_power_of_two",
    "is_zero",
    "is_all_ones",
    "count_null_bytes",
    "count_null_byte",
    "has_null_byte",
    "has_null_bytes",
    "count_non_null_bytes",
    "count_non_null_byte",
    "has_non_null_byte",
    "has_non_null_bytes",
    "lowest_set_bit",
    "highest_set_bit",
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
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
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
    if isinstance(count, bool) or not isinstance(count, int) or count < 0:
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


def not_contains(data: bytes, sub: bytes) -> bool:
    """Return True if *sub* is not contained within *data*.

    This is the boolean negation companion to :func:`contains`.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray to search for.

    Returns:
        True if *sub* is not contained in *data*.

    Raises:
        TypeError: If *data* or *sub* is not bytes or bytearray.

    Examples:
        >>> not_contains(b"hello", b"world")
        True
        >>> not_contains(b"hello", b"ll")
        False
    """
    return not contains(data, sub)


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


def index(data: bytes, sub: bytes, start: int = 0, end: int | None = None) -> int:
    """Return the first index of *sub* in *data*, raising ValueError if not found.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray subsequence to search for.
        start: Optional starting index for the search.
        end: Optional ending index for the search.

    Returns:
        The lowest index in *data* where *sub* is found.

    Raises:
        TypeError: If *data* or *sub* is not bytes or bytearray, or if
            *start*/*end* is not an int.
        ValueError: If *sub* is not found in *data*.

    Examples:
        >>> index(b"hello world", b"world")
        6
        >>> index(b"hello world", b"hello")
        0
        >>> index(b"abcabc", b"bc", 2)
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
    return bytes(data).index(bytes(sub), start, end)


def starts_with(
    data: bytes,
    prefix: bytes,
    start: int = 0,
    end: int | None = None,
) -> bool:
    """Return True if *data* starts with *prefix* in the given slice.

    Args:
        data: Bytes or bytearray to inspect.
        prefix: Bytes or bytearray prefix to match.
        start: Optional starting index for the search slice.
        end: Optional ending index for the search slice.

    Returns:
        True if the selected slice starts with *prefix*, otherwise False.

    Raises:
        TypeError: If *data*/*prefix* are not bytes-like, or if *start*/*end*
            are not valid integers (bool is rejected).
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(prefix, (bytes, bytearray)):
        raise TypeError("prefix must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).startswith(bytes(prefix), start, end)


def ends_with(
    data: bytes,
    suffix: bytes,
    start: int = 0,
    end: int | None = None,
) -> bool:
    """Return True if *data* ends with *suffix* in the given slice.

    Args:
        data: Bytes or bytearray to inspect.
        suffix: Bytes or bytearray suffix to match.
        start: Optional starting index for the search slice.
        end: Optional ending index for the search slice.

    Returns:
        True if the selected slice ends with *suffix*, otherwise False.

    Raises:
        TypeError: If *data*/*suffix* are not bytes-like, or if *start*/*end*
            are not valid integers (bool is rejected).
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(suffix, (bytes, bytearray)):
        raise TypeError("suffix must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).endswith(bytes(suffix), start, end)


def split(data: bytes, sep: bytes | None = None, maxsplit: int = -1) -> list[bytes]:
    """Split *data* on *sep*, at most *maxsplit* times.

    Args:
        data: Bytes or bytearray to split.
        sep: Separator bytes, or ``None`` to split on whitespace runs.
        maxsplit: Maximum number of splits (-1 for no limit). Bool rejected.

    Returns:
        List of byte chunks.

    Raises:
        TypeError: If *data* is not bytes/bytearray, *sep* invalid, or
            *maxsplit* is not an int.
    """
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
    """Return the lowest index of *sub* in *data*, or -1 if not found.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray subsequence to search for.
        start: Optional starting index for the search.
        end: Optional ending index for the search.

    Returns:
        The lowest index where *sub* is found, or -1.

    Raises:
        TypeError: If *data*/*sub* not bytes-like or *start*/*end* invalid.
    """
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
    """Replace occurrences of *old* with *new* in *data*.

    Args:
        data: Bytes or bytearray to transform.
        old: Bytes or bytearray to replace.
        new: Replacement bytes or bytearray.
        count: Maximum replacements (-1 for all). Bool rejected.

    Returns:
        Bytes with replacements applied.

    Raises:
        TypeError: If any argument has an invalid type.
    """
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
    """Count non-overlapping occurrences of *sub* in *data*.

    Args:
        data: Bytes or bytearray to search in.
        sub: Bytes or bytearray subsequence to count.
        start: Optional starting index for the search.
        end: Optional ending index for the search.

    Returns:
        Number of occurrences.

    Raises:
        TypeError: If *data*/*sub* not bytes-like or *start*/*end* invalid.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sub, (bytes, bytearray)):
        raise TypeError("sub must be bytes or bytearray")
    if not isinstance(start, int) or isinstance(start, bool):
        raise TypeError("start must be an int")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool)):
        raise TypeError("end must be an int or None")
    return bytes(data).count(bytes(sub), start, end)


def partition(data: bytes, sep: bytes) -> tuple[bytes, bytes, bytes]:
    """Split *data* at the first occurrence of *sep*.

    Args:
        data: Bytes or bytearray to split.
        sep: Bytes or bytearray separator to search for.

    Returns:
        A 3-tuple ``(before, sep, after)`` containing the part before the
        first occurrence of *sep*, *sep* itself, and the part after it. If
        *sep* is not found, returns ``(data, b"", b"")``.

    Raises:
        TypeError: If *data* or *sep* is not bytes or bytearray.

    Examples:
        >>> partition(b"hello world", b" ")
        (b'hello', b' ', b'world')
        >>> partition(b"hello", b"x")
        (b'hello', b'', b'')
        >>> partition(b"abcabc", b"ab")
        (b'', b'ab', b'cabc')
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes or bytearray")
    return bytes(data).partition(bytes(sep))


def rpartition(data: bytes, sep: bytes) -> tuple[bytes, bytes, bytes]:
    """Split *data* at the last occurrence of *sep*.

    Args:
        data: Bytes or bytearray to split.
        sep: Bytes or bytearray separator to search for.

    Returns:
        A 3-tuple ``(before, sep, after)`` containing the part before the
        last occurrence of *sep*, *sep* itself, and the part after it. If
        *sep* is not found, returns ``(b"", b"", data)``.

    Raises:
        TypeError: If *data* or *sep* is not bytes or bytearray.

    Examples:
        >>> rpartition(b"hello world", b" ")
        (b'hello', b' ', b'world')
        >>> rpartition(b"hello", b"x")
        (b'', b'', b'hello')
        >>> rpartition(b"ababab", b"ab")
        (b'abab', b'ab', b'')
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes or bytearray")
    return bytes(data).rpartition(bytes(sep))


def decode_utf8(data: bytes, errors: str = "strict") -> str:
    """Decode *data* as UTF-8.

    Args:
        data: Bytes or bytearray to decode.
        errors: Decode error handler name.

    Returns:
        Decoded string.

    Raises:
        TypeError: If *data* is not bytes/bytearray or *errors* is not a str.
        UnicodeDecodeError: If decoding fails with the selected handler.
        LookupError: If *errors* is not a known handler.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(errors, str):
        raise TypeError("errors must be a string")
    return bytes(data).decode("utf-8", errors=errors)


def encode_utf8(s: str, errors: str = "strict") -> bytes:
    """Encode *s* as UTF-8.

    Args:
        s: Text to encode.
        errors: Encode error handler name.

    Returns:
        Encoded bytes.

    Raises:
        TypeError: If *s* or *errors* is not a str.
        UnicodeEncodeError: If encoding fails with the selected handler.
        LookupError: If *errors* is not a known handler.
    """
    if not isinstance(s, str):
        raise TypeError("s must be a string")
    if not isinstance(errors, str):
        raise TypeError("errors must be a string")
    return s.encode("utf-8", errors=errors)


def rstrip(data: bytes, chars: bytes | None = None) -> bytes:
    """Strip trailing *chars* (or whitespace) from *data*.

    Args:
        data: Bytes or bytearray to strip.
        chars: Bytes/bytearray of chars to strip, or ``None`` for whitespace.

    Returns:
        Stripped bytes.

    Raises:
        TypeError: If *data* is not bytes/bytearray or *chars* invalid.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if chars is not None and not isinstance(chars, (bytes, bytearray)):
        raise TypeError("chars must be bytes, bytearray, or None")
    if chars is None:
        return bytes(data).rstrip()
    return bytes(data).rstrip(bytes(chars))


def lstrip(data: bytes, chars: bytes | None = None) -> bytes:
    """Strip leading *chars* (or whitespace) from *data*.

    Args:
        data: Bytes or bytearray to strip.
        chars: Bytes/bytearray of chars to strip, or ``None`` for whitespace.

    Returns:
        Stripped bytes.

    Raises:
        TypeError: If *data* is not bytes/bytearray or *chars* invalid.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if chars is not None and not isinstance(chars, (bytes, bytearray)):
        raise TypeError("chars must be bytes, bytearray, or None")
    if chars is None:
        return bytes(data).lstrip()
    return bytes(data).lstrip(bytes(chars))


def strip(data: bytes, chars: bytes | None = None) -> bytes:
    """Strip leading/trailing *chars* (or whitespace) from *data*.

    Args:
        data: Bytes or bytearray to strip.
        chars: Bytes/bytearray of chars to strip, or ``None`` for whitespace.

    Returns:
        Stripped bytes.

    Raises:
        TypeError: If *data* is not bytes/bytearray or *chars* invalid.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if chars is not None and not isinstance(chars, (bytes, bytearray)):
        raise TypeError("chars must be bytes, bytearray, or None")
    if chars is None:
        return bytes(data).strip()
    return bytes(data).strip(bytes(chars))


def center(data: bytes, width: int, fillbyte: bytes = b" ") -> bytes:
    """Center *data* in a field of *width* bytes.

    Args:
        data: Bytes or bytearray to pad.
        width: Target width in bytes. Bool is rejected.
        fillbyte: Single-byte padding value (bytes or bytearray).

    Returns:
        Centered bytes.

    Raises:
        TypeError: If *data*/*fillbyte* types are invalid or *width* is not int.
        ValueError: If *fillbyte* is not exactly one byte.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an int")
    if not isinstance(fillbyte, (bytes, bytearray)):
        raise TypeError("fillbyte must be bytes or bytearray")
    fb = bytes(fillbyte)
    if len(fb) != 1:
        raise ValueError("fillbyte must be a single byte")
    return bytes(data).center(width, fb)


def ljust(data: bytes, width: int, fillbyte: bytes = b" ") -> bytes:
    """Left-justify *data* in a field of *width* bytes.

    Args:
        data: Bytes or bytearray to pad.
        width: Target width in bytes. Bool is rejected.
        fillbyte: Single-byte padding value (bytes or bytearray).

    Returns:
        Left-justified bytes.

    Raises:
        TypeError: If *data*/*fillbyte* types are invalid or *width* is not int.
        ValueError: If *fillbyte* is not exactly one byte.
    """
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
    """Right-justify *data* in a field of *width* bytes.

    Args:
        data: Bytes or bytearray to pad.
        width: Target width in bytes. Bool is rejected.
        fillbyte: Single-byte padding value (bytes or bytearray).

    Returns:
        Right-justified bytes.

    Raises:
        TypeError: If *data*/*fillbyte* types are invalid or *width* is not int.
        ValueError: If *fillbyte* is not exactly one byte.
    """
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
    """Pad numeric *data* on the left with ASCII ``0`` digits.

    Args:
        data: Bytes or bytearray to pad.
        width: Target width in bytes. Bool is rejected.

    Returns:
        Zero-filled bytes.

    Raises:
        TypeError: If *data* type is invalid or *width* is not int.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(width, int) or isinstance(width, bool):
        raise TypeError("width must be an int")
    return bytes(data).zfill(width)


def removeprefix(data: bytes, prefix: bytes) -> bytes:
    """Return *data* with *prefix* removed from the start, if present.

    Args:
        data: Bytes or bytearray to transform.
        prefix: Bytes or bytearray prefix to remove.

    Returns:
        *data* with *prefix* removed from the start if it starts with
        *prefix*; otherwise *data* unchanged.

    Raises:
        TypeError: If *data* or *prefix* is not bytes or bytearray.

    Examples:
        >>> removeprefix(b"hello", b"he")
        b'llo'
        >>> removeprefix(b"hello", b"lo")
        b'hello'
        >>> removeprefix(b"", b"x")
        b''
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(prefix, (bytes, bytearray)):
        raise TypeError("prefix must be bytes or bytearray")
    return bytes(data).removeprefix(bytes(prefix))


def removesuffix(data: bytes, suffix: bytes) -> bytes:
    """Return *data* with *suffix* removed from the end, if present.

    Args:
        data: Bytes or bytearray to transform.
        suffix: Bytes or bytearray suffix to remove.

    Returns:
        *data* with *suffix* removed from the end if it ends with
        *suffix*; otherwise *data* unchanged.

    Raises:
        TypeError: If *data* or *suffix* is not bytes or bytearray.

    Examples:
        >>> removesuffix(b"hello", b"lo")
        b'hel'
        >>> removesuffix(b"hello", b"he")
        b'hello'
        >>> removesuffix(b"", b"x")
        b''
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(suffix, (bytes, bytearray)):
        raise TypeError("suffix must be bytes or bytearray")
    return bytes(data).removesuffix(bytes(suffix))


def splitlines(data: bytes, keepends: bool = False) -> list[bytes]:
    """Split *data* on universal newline boundaries.

    This mirrors :meth:`bytes.splitlines` for bytes-like input, recognizing
    ``\\n``, ``\\r``, and ``\\r\\n``. Other single-byte separators (such as
    vertical tab, form feed, file/group/record separators, and NEL) are not
    treated as line boundaries.

    Args:
        data: Bytes or bytearray to split.
        keepends: If ``True``, keep line ending bytes in the results.

    Returns:
        A list of lines.

    Raises:
        TypeError: If *data* is not bytes/bytearray or *keepends* is not bool.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(keepends, bool):
        raise TypeError("keepends must be bool")
    if isinstance(data, bytearray):
        data = bytes(data)
    if not data:
        return []
    result: list[bytes] = []
    i = 0
    n = len(data)
    start = 0
    while i < n:
        b = data[i]
        if b == 0x0D:  # \r
            if i + 1 < n and data[i + 1] == 0x0A:  # \r\n
                end = i + 2
            else:
                end = i + 1
            result.append(data[start:end] if keepends else data[start:i])
            i = end
            start = i
        elif b == 0x0A:  # \n
            end = i + 1
            result.append(data[start:end] if keepends else data[start:i])
            i = end
            start = i
        else:
            i += 1
    if start < n:
        result.append(data[start:n])
    return result


def rsplit(data: bytes, sep: bytes | None = None, maxsplit: int = -1) -> list[bytes]:
    """Split *data* from the right, using *sep* as the delimiter.

    Behaves like :meth:`bytes.rsplit`.

    Args:
        data: Bytes or bytearray to split.
        sep: Delimiter bytes, or ``None`` to split on whitespace runs.
        maxsplit: Maximum number of splits to perform. ``-1`` means no limit.

    Returns:
        List of byte chunks.

    Raises:
        TypeError: If *data* is not bytes/bytearray, *sep* is not
            bytes/bytearray/None, or *maxsplit* is not an int.
        ValueError: If *sep* is an empty bytes-like object.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if sep is not None and not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes, bytearray, or None")
    if not isinstance(maxsplit, int) or isinstance(maxsplit, bool):
        raise TypeError("maxsplit must be an int")
    if sep is None:
        return bytes(data).rsplit(None, maxsplit)
    sep_bytes = bytes(sep)
    if sep_bytes == b"":
        raise ValueError("empty separator")
    return bytes(data).rsplit(sep_bytes, maxsplit)


def upper(data: bytes) -> bytes:
    """Return an uppercased copy of *data*.

    Args:
        data: Bytes or bytearray to convert.

    Returns:
        Uppercased bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> upper(b"abc")
        b'ABC'
        >>> upper(bytearray(b"ab"))
        b'AB'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).upper()


def lower(data: bytes) -> bytes:
    """Return a lowercased copy of *data*.

    Args:
        data: Bytes or bytearray to convert.

    Returns:
        Lowercased bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> lower(b"ABC")
        b'abc'
        >>> lower(bytearray(b"AB"))
        b'ab'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).lower()


def capitalize(data: bytes) -> bytes:
    """Return a copy with first byte uppercased and rest lowercased.

    Args:
        data: Bytes or bytearray to convert.

    Returns:
        Capitalized bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> capitalize(b"hello")
        b'Hello'
        >>> capitalize(bytearray(b"hELLO"))
        b'Hello'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).capitalize()


def title(data: bytes) -> bytes:
    """Return titlecased bytes.

    Args:
        data: Bytes or bytearray to convert.

    Returns:
        Titlecased bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> title(b"hello world")
        b'Hello World'
        >>> title(bytearray(b"hello WORLD"))
        b'Hello World'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).title()


def swapcase(data: bytes) -> bytes:
    """Return bytes with case swapped.

    Args:
        data: Bytes or bytearray to convert.

    Returns:
        Case-swapped bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> swapcase(b"Hello")
        b'hELLO'
        >>> swapcase(bytearray(b"aBc"))
        b'AbC'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).swapcase()


def casefold(data: bytes) -> bytes:
    """Return a casefolded copy of *data*.

    For ASCII bytes, uses bytearray casefold semantics via UTF-8 decode/encode
    when possible; falls back to ``lower()`` for invalid UTF-8.

    Args:
        data: Bytes or bytearray to convert.

    Returns:
        Casefolded bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> casefold(b"Hello")
        b'hello'
        >>> casefold(bytearray(b"HELLO"))
        b'hello'
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    try:
        return bytes(data).decode("utf-8").casefold().encode("utf-8")
    except UnicodeError:
        return bytes(data).lower()


def isalnum(data: bytes) -> bool:
    """Return ``True`` if all bytes are alphanumeric and there is at least one.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).isalnum()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isalnum(b"abc123")
        True
        >>> isalnum(bytearray(b"abc123"))
        True
        >>> isalnum(b"abc 123")
        False
        >>> isalnum(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isalnum()


def count_alnum(data: bytes) -> int:
    """Return the number of ASCII alphanumeric bytes in *data*.

    This is the integer companion to :func:`isalnum`. An alphanumeric byte is
    any byte that passes :meth:`bytes.isalnum` (ASCII letters ``a``-``z``,
    ``A``-``Z`` and digits ``0``-``9``). Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of alphanumeric bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_alnum(b"abc123")
        6
        >>> count_alnum(b"ABC")
        3
        >>> count_alnum(b"abc 123")
        6
        >>> count_alnum(b"!@#")
        0
        >>> count_alnum(b"")
        0
        >>> count_alnum(bytearray(b"a1b2"))
        4
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if bytes([b]).isalnum())


def has_alnum(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII alphanumeric byte.

    This is the boolean companion to :func:`count_alnum`. It returns ``True``
    when at least one byte is alphanumeric and ``False`` otherwise (empty input
    is ``False``), reusing :func:`count_alnum` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if *data* contains an alphanumeric byte.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_alnum(b"abc123")
        True
        >>> has_alnum(b"!@#")
        False
        >>> has_alnum(b"1a2")
        True
        >>> has_alnum(bytearray(b"ABC"))
        True
        >>> has_alnum(b"")
        False
    """
    return count_alnum(data) > 0


def isalpha(data: bytes) -> bool:
    """Return ``True`` if all bytes are alphabetic and there is at least one.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).isalpha()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isalpha(b"abc")
        True
        >>> isalpha(bytearray(b"ABC"))
        True
        >>> isalpha(b"abc123")
        False
        >>> isalpha(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isalpha()


def count_alpha(data: bytes) -> int:
    """Return the number of ASCII alphabetic bytes in *data*.

    This is the integer companion to :func:`isalpha`. An alphabetic byte is
    any byte that passes :meth:`bytes.isalpha` (ASCII letters ``a``-``z`` and
    ``A``-``Z``). Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of alphabetic bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_alpha(b"abc")
        3
        >>> count_alpha(b"ABC")
        3
        >>> count_alpha(b"abc123")
        3
        >>> count_alpha(b"123")
        0
        >>> count_alpha(b"")
        0
        >>> count_alpha(bytearray(b"a1b2"))
        2
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if bytes([b]).isalpha())


def has_alpha(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII alphabetic byte.

    This is the boolean companion to :func:`count_alpha`. It returns ``True``
    when at least one byte is alphabetic and ``False`` otherwise (empty input
    is ``False``), reusing :func:`count_alpha` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if *data* contains an alphabetic byte.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_alpha(b"abc")
        True
        >>> has_alpha(b"123")
        False
        >>> has_alpha(b"a1b2")
        True
        >>> has_alpha(bytearray(b"ABC"))
        True
        >>> has_alpha(b"")
        False
    """
    return count_alpha(data) > 0


def isascii(data: bytes) -> bool:
    """Return ``True`` if *data* is empty or all bytes are in ``0x00``–``0x7F``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).isascii()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isascii(b"abc")
        True
        >>> isascii(bytearray(b"123"))
        True
        >>> isascii(b"\\x80")
        False
        >>> isascii(b"")
        True
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isascii()


def count_ascii(data: bytes) -> int:
    """Return the number of ASCII bytes (``0x00``-``0x7F``) in *data*.

    This is the integer companion to :func:`isascii`. An ASCII byte is any
    byte whose value is in the ASCII range ``0x00``-``0x7F``. Empty input
    returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of ASCII bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_ascii(b"abc")
        3
        >>> count_ascii(b"\\x80")
        0
        >>> count_ascii(b"a\\x80b")
        2
        >>> count_ascii(b"")
        0
        >>> count_ascii(bytearray(b"ABC"))
        3
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if 0x00 <= b <= 0x7F)


def has_ascii(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII byte.

    This is the boolean companion to :func:`count_ascii`. It returns ``True``
    when at least one byte is in the ASCII range ``0x00``-``0x7F`` and
    ``False`` otherwise (empty input is ``False``), reusing
    :func:`count_ascii` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if *data* contains an ASCII byte.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_ascii(b"abc")
        True
        >>> has_ascii(b"\\x80\\x9f")
        False
        >>> has_ascii(b"a\\x80")
        True
        >>> has_ascii(bytearray(b"ABC"))
        True
        >>> has_ascii(b"")
        False
    """
    return count_ascii(data) > 0


def isdigit(data: bytes) -> bool:
    """Return ``True`` if all bytes are ASCII digits and there is at least one.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).isdigit()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isdigit(b"123")
        True
        >>> isdigit(bytearray(b"0"))
        True
        >>> isdigit(b"12a")
        False
        >>> isdigit(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isdigit()


def count_digits(data: bytes) -> int:
    """Return the number of ASCII digit bytes (``0``-``9``) in *data*.

    Counts every byte whose value is in the ASCII digit range ``0x30``-``0x39``.
    An empty input has no digit bytes and returns zero.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The number of ASCII digit bytes as a non-negative integer.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_digits(b"123")
        3
        >>> count_digits(b"abc")
        0
        >>> count_digits(b"a1b2c3")
        3
        >>> count_digits(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if 0x30 <= b <= 0x39)


def has_digits(data: bytes) -> bool:
    """Return True if *data* contains at least one ASCII digit byte.

    This is the boolean companion to :func:`count_digits`. It returns
    ``True`` when *data* contains at least one ASCII digit byte
    (``0``-``9``) and ``False`` otherwise (empty input is ``False``),
    reusing :func:`count_digits` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is an ASCII digit, False otherwise (empty input
        is False).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_digits(b"123")
        True
        >>> has_digits(bytearray(b"0"))
        True
        >>> has_digits(b"abc")
        False
        >>> has_digits(b"a1b2c3")
        True
        >>> has_digits(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_digits(data) > 0


def islower(data: bytes) -> bool:
    """Return ``True`` if there is at least one cased byte and all cased bytes are lowercase.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).islower()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> islower(b"abc")
        True
        >>> islower(bytearray(b"abc123"))
        True
        >>> islower(b"Abc")
        False
        >>> islower(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).islower()


def count_lower(data: bytes) -> int:
    """Return the number of ASCII lowercase bytes (``a``-``z``) in *data*.

    This is the integer companion to :func:`islower`. A lowercase byte is any
    byte for which :meth:`bytes.islower` is true. Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of lowercase bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_lower(b"abc")
        3
        >>> count_lower(b"ABC")
        0
        >>> count_lower(b"AbC")
        1
        >>> count_lower(b"123")
        0
        >>> count_lower(b"")
        0
        >>> count_lower(bytearray(b"a1b2"))
        2
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if bytes([b]).islower())


def has_lower(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII lowercase byte.

    This is the boolean companion to :func:`count_lower`. It returns ``True``
    when at least one byte is lowercase and ``False`` otherwise (empty input
    is ``False``), reusing :func:`count_lower` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is a lowercase ASCII letter, False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_lower(b"abc")
        True
        >>> has_lower(b"ABC")
        False
        >>> has_lower(bytearray(b"1a"))
        True
        >>> has_lower(b"123")
        False
        >>> has_lower(b"a1b2c3")
        True
        >>> has_lower(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_lower(data) > 0


def isspace(data: bytes) -> bool:
    """Return ``True`` if all bytes are whitespace and there is at least one.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).isspace()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isspace(b"   ")
        True
        >>> isspace(bytearray(b"\\t\\n"))
        True
        >>> isspace(b"a")
        False
        >>> isspace(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isspace()


def count_space(data: bytes) -> int:
    """Return the number of ASCII whitespace bytes in *data*.

    This is the integer companion to :func:`isspace`. A whitespace byte is any
    byte for which :meth:`bytes.isspace` is true (space, tab, newline,
    carriage return, form feed, vertical tab). Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of whitespace bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_space(b"   ")
        3
        >>> count_space(b"\\t\\n")
        2
        >>> count_space(b"a b")
        1
        >>> count_space(b"abc")
        0
        >>> count_space(b"")
        0
        >>> count_space(bytearray(b"x\\ty"))
        1
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if bytes([b]).isspace())


def has_space(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII whitespace byte.

    This is the boolean companion to :func:`count_space`. It returns ``True``
    when at least one byte is whitespace and ``False`` otherwise (empty input
    is ``False``), reusing :func:`count_space` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is an ASCII whitespace byte, False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_space(b"   ")
        True
        >>> has_space(b"\\t")
        True
        >>> has_space(bytearray(b"x y"))
        True
        >>> has_space(b"abc")
        False
        >>> has_space(b"a b c")
        True
        >>> has_space(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_space(data) > 0


def istitle(data: bytes) -> bool:
    """Return ``True`` if *data* is titlecased and there is at least one cased byte.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).istitle()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> istitle(b"Hello World")
        True
        >>> istitle(bytearray(b"Hello"))
        True
        >>> istitle(b"hello world")
        False
        >>> istitle(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).istitle()


def count_title(data: bytes) -> int:
    """Return the number of titlecase bytes in *data*.

    A titlecase byte is an uppercase ASCII letter (``A``-``Z``) that appears at a
    word boundary (start of data or after a non-alphabetic byte) and is followed
    by a lowercase letter, a non-alphabetic byte, or the end of the data. This
    mirrors the uppercase positions in a titlecased string (as produced by
    :meth:`bytes.title`). Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of titlecase bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_title(b"Hello World")
        2
        >>> count_title(b"Hello")
        1
        >>> count_title(b"hello world")
        0
        >>> count_title(b"HelloWorld")
        1
        >>> count_title(b"")
        0
        >>> count_title(bytearray(b"Hi There"))
        2
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    raw = bytes(data)
    count = 0
    n = len(raw)
    for i, b in enumerate(raw):
        if 0x41 <= b <= 0x5A:  # 'A'-'Z'
            # Check if at word boundary: position 0 or previous is non-alphabetic
            at_boundary = i == 0 or not (0x41 <= raw[i - 1] <= 0x5A or 0x61 <= raw[i - 1] <= 0x7A)
            if at_boundary:
                # Check if followed by lowercase, non-alphabetic, or end of data
                if i + 1 == n:
                    count += 1
                else:
                    next_b = raw[i + 1]
                    if not (0x41 <= next_b <= 0x5A):  # not uppercase
                        count += 1
    return count


def has_title(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one titlecase byte.

    This is the boolean companion to :func:`count_title`. It returns ``True``
    when at least one byte is a titlecase byte and ``False`` otherwise (empty
    input is ``False``), reusing :func:`count_title` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if *data* contains a titlecase byte.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_title(b"Hello World")
        True
        >>> has_title(b"hello world")
        False
        >>> has_title(bytearray(b"Hi"))
        True
        >>> has_title(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_title(data) > 0


def isupper(data: bytes) -> bool:
    """Return ``True`` if there is at least one cased byte and all cased bytes are uppercase.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if ``bytes(data).isupper()`` is true.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isupper(b"ABC")
        True
        >>> isupper(bytearray(b"ABC123"))
        True
        >>> isupper(b"Abc")
        False
        >>> isupper(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isupper()


def count_upper(data: bytes) -> int:
    """Return the number of ASCII uppercase bytes (``A``-``Z``) in *data*.

    This is the integer companion to :func:`isupper`. An uppercase byte is any
    byte for which :meth:`bytes.isupper` is true. Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of uppercase bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_upper(b"ABC")
        3
        >>> count_upper(b"abc")
        0
        >>> count_upper(b"AbC")
        2
        >>> count_upper(b"123")
        0
        >>> count_upper(b"")
        0
        >>> count_upper(bytearray(b"A1B2"))
        2
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if bytes([b]).isupper())


def has_upper(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII uppercase byte.

    This is the boolean companion to :func:`count_upper`. It returns ``True``
    when at least one byte is uppercase and ``False`` otherwise (empty input
    is ``False``), reusing :func:`count_upper` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is an uppercase ASCII letter, False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_upper(b"ABC")
        True
        >>> has_upper(b"abc")
        False
        >>> has_upper(bytearray(b"1A"))
        True
        >>> has_upper(b"123")
        False
        >>> has_upper(b"aBc")
        True
        >>> has_upper(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_upper(data) > 0


def isprintable(data: bytes) -> bool:
    """Return True if *data* contains only printable bytes.

    A byte is printable when it is in the ASCII printable range
    (0x20-0x7E, including the space). An empty input is considered
    printable and returns ``True``, matching :meth:`str.isprintable`.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        ``True`` if every byte is printable (including empty input),
        ``False`` otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isprintable(b"hello")
        True
        >>> isprintable(b"hi there")
        True
        >>> isprintable(b"")
        True
        >>> isprintable(b"no\\ttabs")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    raw = bytes(data)
    return all(0x20 <= b <= 0x7E for b in raw)


def count_printable(data: bytes) -> int:
    """Return the number of ASCII printable bytes in *data*.

    This is the integer companion to :func:`isprintable`. A printable byte is
    any byte in the ASCII printable range ``0x20``-``0x7E`` (including the
    space). Empty input returns ``0``.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        Count of printable bytes in *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_printable(b"hello")
        5
        >>> count_printable(b"hi there")
        8
        >>> count_printable(b"")
        0
        >>> count_printable(b"no\\ttabs")
        6
        >>> count_printable(b"\\x1b\\x01")
        0
        >>> count_printable(bytearray(b"A1!"))
        3
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if 0x20 <= b <= 0x7E)


def has_printable(data: bytes) -> bool:
    """Return ``True`` if *data* contains at least one ASCII printable byte.

    This is the boolean companion to :func:`count_printable`. It returns
    ``True`` when at least one byte is printable and ``False`` otherwise
    (empty input is ``False``), reusing :func:`count_printable` for
    consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is ASCII printable, False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_printable(b"hello")
        True
        >>> has_printable(b"\\x1b\\x01")
        False
        >>> has_printable(bytearray(b"A1!"))
        True
        >>> has_printable(b"")
        False
        >>> has_printable(b"  ")
        True
        >>> has_printable(b"\\x7f")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_printable(data) > 0


def isidentifier(data: bytes) -> bool:
    """Return True if *data* is a valid ASCII Python identifier.

    The bytes are decoded as ASCII and tested with
    :meth:`str.isidentifier`. Non-ASCII or undecodable bytes make the
    result False.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if *data* decodes to a valid identifier, False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> isidentifier(b"foo_bar")
        True
        >>> isidentifier(b"9abc")
        False
        >>> isidentifier(b"")
        False
        >>> isidentifier(b"caf\\xc3\\xa9")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    try:
        return bytes(data).decode("ascii").isidentifier()
    except UnicodeDecodeError:
        return False


def join(iterable: object, sep: bytes = b"") -> bytes:
    """Join bytes-like items from *iterable* with *sep*.

    Args:
        iterable: Iterable yielding bytes or bytearray objects.
        sep: Separator bytes or bytearray.

    Returns:
        Joined bytes.

    Raises:
        TypeError: If *sep* is not bytes/bytearray, *iterable* is not
            iterable, or items are not bytes-like.
    """
    if not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes or bytearray")
    return bytes(sep).join(iterable)  # type: ignore[arg-type]


def expandtabs(data: bytes, tabsize: int = 8) -> bytes:
    """Expand tab characters in *data* using *tabsize* spaces.

    Args:
        data: Bytes or bytearray to transform.
        tabsize: Tab stop size. Bool is rejected.

    Returns:
        Bytes with tabs expanded.

    Raises:
        TypeError: If *data* type is invalid or *tabsize* is not int.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(tabsize, int) or isinstance(tabsize, bool):
        raise TypeError("tabsize must be int")
    return bytes(data).expandtabs(tabsize)


def decode_ascii(data: bytes, errors: str = "strict") -> str:
    """Decode *data* as ASCII.

    Args:
        data: Bytes or bytearray to decode.
        errors: Decode error handler name.

    Returns:
        Decoded string.

    Raises:
        TypeError: If *data* is not bytes/bytearray or *errors* is not a str.
        UnicodeDecodeError: If decoding fails with the selected handler.
        LookupError: If *errors* is not a known handler.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(errors, str):
        raise TypeError("errors must be str")
    return bytes(data).decode("ascii", errors=errors)


def encode_ascii(s: str, errors: str = "strict") -> bytes:
    """Encode *s* as ASCII.

    Args:
        s: Text to encode.
        errors: Encode error handler name.

    Returns:
        Encoded bytes.

    Raises:
        TypeError: If *s* or *errors* is not a str.
        UnicodeEncodeError: If encoding fails with the selected handler.
        LookupError: If *errors* is not a known handler.
    """
    if not isinstance(s, str):
        raise TypeError("s must be str")
    if not isinstance(errors, str):
        raise TypeError("errors must be str")
    return s.encode("ascii", errors=errors)


def maketrans(frm: bytes, to: bytes) -> bytes:
    """Return a 256-byte translation table for :func:`translate`.

    Each byte of *frm* is mapped to the byte at the same position in *to*;
    all other byte values map to themselves. The result can be passed to
    :func:`translate` to replace bytes in a bytes-like object.

    Args:
        frm: Bytes or bytearray whose bytes are mapped to replacements.
        to: Bytes or bytearray of the same length as *frm* giving the
            replacement bytes.

    Returns:
        A bytes object of length 256 suitable for :func:`translate`.

    Raises:
        TypeError: If *frm* or *to* is not bytes or bytearray.
        ValueError: If *frm* and *to* do not have the same length.

    Examples:
        >>> table = maketrans(b"ab", b"xy")
        >>> table[97]  # ord('a')
        120
        >>> table[98]  # ord('b')
        121
        >>> maketrans(b"", b"") == bytes(range(256))
        True
    """
    if not isinstance(frm, (bytes, bytearray)):
        raise TypeError("frm must be bytes or bytearray")
    if not isinstance(to, (bytes, bytearray)):
        raise TypeError("to must be bytes or bytearray")
    if len(frm) != len(to):
        raise ValueError("frm and to must have the same length")
    table = bytearray(range(256))
    for b_from, b_to in zip(frm, to):
        table[b_from] = b_to
    return bytes(table)


def translate(data: bytes, table: bytes | bytearray) -> bytes:
    """Return a copy of *data* with each byte replaced according to *table*.

    *table* must be a bytes-like object of length 256 (as produced by
    :func:`maketrans`); each byte value *b* in *data* is replaced by
    *table[b]*.

    Args:
        data: Bytes or bytearray to translate.
        table: A 256-byte translation table.

    Returns:
        The translated bytes.

    Raises:
        TypeError: If *data* or *table* is not bytes or bytearray.
        ValueError: If *table* is not exactly 256 bytes long.

    Examples:
        >>> translate(b"abc", maketrans(b"ab", b"xy"))
        b'xyc'
        >>> translate(b"abc", bytes(range(256)))
        b'abc'
        >>> translate(b"", maketrans(b"ab", b"xy"))
        b''
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(table, (bytes, bytearray)):
        raise TypeError("table must be bytes or bytearray")
    if len(table) != 256:
        raise ValueError("table must be exactly 256 bytes long")
    return bytes(data).translate(bytes(table))


def to_int(data: bytes, byteorder: Literal["big", "little"] = "big", signed: bool = False) -> int:
    """Interpret *data* as an integer using the given byte order.

    The conversion mirrors :func:`int.from_bytes`: *data* is treated as the
    byte representation of a non-negative integer in the chosen *byteorder*
    ("big" or "little"), and *signed* controls whether the value is interpreted
    in two's-complement form (so the most significant bit is the sign bit).
    Empty input yields ``0``.

    Args:
        data: Bytes or bytearray to interpret.
        byteorder: "big" (most significant byte first) or "little" (least
            significant byte first).
        signed: If True, interpret the bytes as a two's-complement signed
            integer.

    Returns:
        The integer value of *data*.

    Raises:
        TypeError: If *data* is not bytes or bytearray, or *byteorder* is not
            a str.
        ValueError: If *byteorder* is not "big" or "little".

    Examples:
        >>> to_int(from_hex("0100"))
        256
        >>> to_int(from_hex("0001"), byteorder="little")
        256
        >>> to_int(from_hex("ff"), signed=True)
        -1
        >>> to_int(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(byteorder, str):
        raise TypeError("byteorder must be a str")
    if byteorder not in ("big", "little"):
        raise ValueError("byteorder must be 'big' or 'little'")
    if not isinstance(signed, bool):
        raise TypeError("signed must be a bool")
    return int.from_bytes(bytes(data), byteorder=byteorder, signed=signed)


def from_int(
    value: int,
    length: int,
    byteorder: Literal["big", "little"] = "big",
    signed: bool = False,
) -> bytes:
    """Encode the integer *value* into a fixed-length bytes object.

    The result is exactly *length* bytes long. If *value* fits in the requested
    representation it is encoded directly; otherwise a :class:`OverflowError`
    is raised (matching :meth:`int.to_bytes`).

    Args:
        value: The integer to encode.
        length: The number of bytes in the result (must be >= 0).
        byteorder: "big" (most significant byte first) or "little" (least
            significant byte first).
        signed: If True, encode the value in two's-complement form so that
            negative values are representable.

    Returns:
        The *length*-byte representation of *value*.

    Raises:
        TypeError: If *value* is not an int (a bool is rejected), *length* is
            not an int, *byteorder* is not a str, or *signed* is not a bool.
        ValueError: If *length* is negative, or *byteorder* is not "big" or
            "little".
        OverflowError: If *value* does not fit in *length* bytes with the
            requested signedness.

    Examples:
        >>> to_hex(from_int(256, 2))
        '0100'
        >>> to_hex(from_int(256, 2, byteorder="little"))
        '0001'
        >>> to_hex(from_int(-1, 1, signed=True))
        'ff'
        >>> len(from_int(0, 4))
        4
        >>> from_int(0, 0)
        b''
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("value must be an int")
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an int")
    if length < 0:
        raise ValueError("length must be non-negative")
    if not isinstance(byteorder, str):
        raise TypeError("byteorder must be a str")
    if byteorder not in ("big", "little"):
        raise ValueError("byteorder must be 'big' or 'little'")
    if not isinstance(signed, bool):
        raise TypeError("signed must be a bool")
    return value.to_bytes(length, byteorder=byteorder, signed=signed)


def bit_count(data: bytes) -> int:
    """Return the total number of set (1) bits in *data*.

    Counts every bit with value 1 across all bytes. An empty input has no
    set bits and returns 0.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The number of set bits as a non-negative integer.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> bit_count(from_hex("00"))
        0
        >>> bit_count(from_hex("ff"))
        8
        >>> bit_count(from_hex("0f00"))
        4
        >>> bit_count(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(b.bit_count() for b in bytes(data))


def has_set_bits(data: bytes) -> bool:
    """Return True if *data* contains at least one set (1) bit.

    This is the boolean companion to :func:`bit_count`. It returns ``True``
    when any bit in *data* is set and ``False`` otherwise (an empty input
    has no set bits and is ``False``), reusing :func:`bit_count` for
    consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any bit is set, False otherwise (empty input is False).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_set_bits(from_hex("00"))
        False
        >>> has_set_bits(from_hex("01"))
        True
        >>> has_set_bits(from_hex("ff"))
        True
        >>> has_set_bits(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bit_count(data) > 0


def is_zero(data: bytes) -> bool:
    """Return True if *data* contains only zero bytes.

    An empty input is considered all-zero and returns True.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if every byte is 0 (or *data* is empty), False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> is_zero(from_hex("000000"))
        True
        >>> is_zero(from_hex("000100"))
        False
        >>> is_zero(b"")
        True
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return all(b == 0 for b in bytes(data))


def is_power_of_two(data: bytes) -> bool:
    """Return True if *data* has exactly one set bit across all bytes.

    A power-of-two value has exactly one bit set. An empty input has no set
    bits and returns False.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if exactly one bit is set in *data*, False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> is_power_of_two(from_hex("01"))
        True
        >>> is_power_of_two(from_hex("80"))
        True
        >>> is_power_of_two(from_hex("0f"))
        False
        >>> is_power_of_two(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bit_count(data) == 1


def is_all_ones(data: bytes) -> bool:
    """Return True if *data* contains only 0xff bytes.

    An empty input is considered all-ones and returns True.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if every byte is 0xff (or *data* is empty), False otherwise.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> is_all_ones(from_hex("ffffff"))
        True
        >>> is_all_ones(from_hex("fffeff"))
        False
        >>> is_all_ones(b"")
        True
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return all(b == 0xff for b in bytes(data))


def count_null_bytes(data: bytes) -> int:
    """Return the number of zero bytes in *data*.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The count of bytes equal to 0 (empty input returns 0).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_null_bytes(from_hex("000000"))
        3
        >>> count_null_bytes(from_hex("010203"))
        0
        >>> count_null_bytes(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if b == 0)


def count_null_byte(data: bytes) -> int:
    """Alias for :func:`count_null_bytes` (singular form).

    Returns the number of zero bytes in *data*.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The count of bytes equal to 0 (empty input returns 0).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_null_byte(from_hex("000000"))
        3
        >>> count_null_byte(from_hex("010203"))
        0
        >>> count_null_byte(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_null_bytes(data)


def has_null_byte(data: bytes) -> bool:
    """Return True if *data* contains at least one zero byte.

    This is the boolean companion to :func:`count_null_bytes`. It returns
    ``True`` when *data* contains at least one zero byte and ``False``
    otherwise (empty input is ``False``), reusing :func:`count_null_bytes`
    for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is 0, False otherwise (empty input is False).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_null_byte(from_hex("000000"))
        True
        >>> has_null_byte(from_hex("010203"))
        False
        >>> has_null_byte(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_null_bytes(data) > 0


def has_null_bytes(data: bytes) -> bool:
    """Alias for :func:`has_null_byte` (plural form).

    Returns ``True`` if *data* contains at least one zero byte.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is 0, False otherwise (empty input is False).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_null_bytes(from_hex("000000"))
        True
        >>> has_null_bytes(from_hex("010203"))
        False
        >>> has_null_bytes(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_null_bytes(data) > 0


def count_non_null_bytes(data: bytes) -> int:
    """Return the number of non-zero bytes in *data*.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The count of bytes not equal to 0 (empty input returns 0).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_non_null_bytes(from_hex("000000"))
        0
        >>> count_non_null_bytes(from_hex("010203"))
        3
        >>> count_non_null_bytes(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return sum(1 for b in bytes(data) if b != 0)


def count_non_null_byte(data: bytes) -> int:
    """Alias for :func:`count_non_null_bytes` (singular form).

    Returns the number of non-zero bytes in *data*.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The count of bytes not equal to 0 (empty input returns 0).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> count_non_null_byte(from_hex("000000"))
        0
        >>> count_non_null_byte(from_hex("010203"))
        3
        >>> count_non_null_byte(b"")
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_non_null_bytes(data)


def has_non_null_byte(data: bytes) -> bool:
    """Return True if *data* contains at least one non-zero byte.

    This is the boolean companion to :func:`count_non_null_bytes`. It returns
    ``True`` when *data* contains at least one byte that is not zero and
    ``False`` otherwise (empty input is ``False``), reusing
    :func:`count_non_null_bytes` for consistency.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is non-zero, False otherwise (empty input is False).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_non_null_byte(from_hex("000000"))
        False
        >>> has_non_null_byte(from_hex("010203"))
        True
        >>> has_non_null_byte(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_non_null_bytes(data) > 0


def has_non_null_bytes(data: bytes) -> bool:
    """Alias for :func:`has_non_null_byte` (plural form).

    Returns ``True`` if *data* contains at least one non-zero byte.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        True if any byte is non-zero, False otherwise (empty input is False).

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> has_non_null_bytes(from_hex("000000"))
        False
        >>> has_non_null_bytes(from_hex("010203"))
        True
        >>> has_non_null_bytes(b"")
        False
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return count_non_null_bytes(data) > 0


def lowest_set_bit(data: bytes) -> int:
    """Return the position of the least significant set bit in *data*, or -1.

    The bytes are interpreted as a big-endian unsigned integer, so the first
    byte is the most significant. The least significant set bit is the lowest
    bit position (0-based) whose value is 1. An empty input, or an input with
    no set bits, returns -1.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The 0-based position of the least significant set bit, or -1 if
        *data* has no set bits.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> lowest_set_bit(from_hex("00"))
        -1
        >>> lowest_set_bit(from_hex("01"))
        0
        >>> lowest_set_bit(from_hex("02"))
        1
        >>> lowest_set_bit(from_hex("80"))
        7
        >>> lowest_set_bit(from_hex("0100"))
        8
        >>> lowest_set_bit(from_hex("ff"))
        0
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    value = int.from_bytes(bytes(data), "big")
    if value == 0:
        return -1
    return (value & -value).bit_length() - 1


def highest_set_bit(data: bytes) -> int:
    """Return the position of the most significant set bit in *data*, or -1.

    The bytes are interpreted as a big-endian unsigned integer, so the first
    byte is the most significant. The most significant set bit is the highest
    bit position (0-based) whose value is 1. An empty input, or an input with
    no set bits, returns -1.

    Args:
        data: Bytes or bytearray to inspect.

    Returns:
        The 0-based position of the most significant set bit, or -1 if *data*
        has no set bits.

    Raises:
        TypeError: If *data* is not bytes or bytearray.

    Examples:
        >>> highest_set_bit(from_hex("00"))
        -1
        >>> highest_set_bit(from_hex("01"))
        0
        >>> highest_set_bit(from_hex("02"))
        1
        >>> highest_set_bit(from_hex("80"))
        7
        >>> highest_set_bit(from_hex("ff"))
        7
        >>> highest_set_bit(from_hex("0100"))
        8
        >>> highest_set_bit(b"")
        -1
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    value = int.from_bytes(bytes(data), "big")
    if value == 0:
        return -1
    return value.bit_length() - 1
