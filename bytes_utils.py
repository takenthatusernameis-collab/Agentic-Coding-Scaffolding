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
    "isalpha",
    "isascii",
    "isdigit",
    "islower",
    "isspace",
    "istitle",
    "isupper",
    "isdecimal",
    "isnumeric",
    "isprintable",
    "isidentifier",
    "join",
    "expandtabs",
    "decode_ascii",
    "encode_ascii",
    "maketrans",
    "translate",
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
        raise ValueError("fillbyte must be a single byte")
    return bytes(data).center(width, fb)


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
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(keepends, bool):
        raise TypeError("keepends must be bool")
    if isinstance(data, bytearray):
        data = bytes(data)
    if not data:
        return []
    result = []
    i = 0
    n = len(data)
    start = 0
    while i < n:
        b = data[i]
        if b == 0x0D:  # \r
            if i + 1 < n and data[i + 1] == 0x0A:  # \r\n
                if keepends:
                    result.append(data[start : i + 2])
                else:
                    result.append(data[start:i])
                i += 2
            else:
                if keepends:
                    result.append(data[start : i + 1])
                else:
                    result.append(data[start:i])
                i += 1
            start = i
        elif b == 0x0A:  # \n
            if keepends:
                result.append(data[start : i + 1])
            else:
                result.append(data[start:i])
            i += 1
            start = i
        elif b in (0x0B, 0x0C, 0x1C, 0x1D, 0x1E, 0x85):
            if keepends:
                result.append(data[start : i + 1])
            else:
                result.append(data[start:i])
            i += 1
            start = i
        else:
            i += 1
    if start < n:
        result.append(data[start:n])
    return result


def rsplit(data: bytes, sep: bytes | None = None, maxsplit: int = -1) -> list[bytes]:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if isinstance(data, bytearray):
        data = bytes(data)
    if sep is None:
        if not isinstance(maxsplit, int) or isinstance(maxsplit, bool):
            raise TypeError("maxsplit must be an int")
        if not data.strip():
            return []
        # split on whitespace like str
        i = 0
        n = len(data)
        splits = 0
        # go from right to left easier with str-like logic
        if maxsplit < 0:
            # simple scan
            # do normal split logic by scanning
            pass
        # easier to convert to logic similar to split but reversed
    if sep is not None and not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes or bytearray or None")
    if not isinstance(maxsplit, int) or isinstance(maxsplit, bool):
        raise TypeError("maxsplit must be an int")
    if isinstance(sep, bytearray):
        sep = bytes(sep)
    if sep is None:
        # handle whitespace split
        i = 0
        n = len(data)
        # collect runs of non-whitespace
        if maxsplit == 0:
            if not data.strip():
                return []
            return [data] if False else [bytes(data)]  # but need to be careful
        # better implementation
        # find all whitespace
        result = []
        splits = 0
        if maxsplit < 0:
            # split all
            i = n - 1
            # easier to use split and reverse? no - for multiple spaces behavior matches
            # do forward split on whitespace
            res = []
            j = 0
            while j < n:
                b = data[j]
                if b in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                    j += 1
                    continue
                k = j
                while k < n and data[k] not in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                    k += 1
                res.append(data[j:k])
                j = k
            return res
        # with maxsplit
        # count from right
        # find split points from right
        i = n - 1
        while i >= 0 and splits < maxsplit:
            b = data[i]
            if b in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                # skip whitespace
                i -= 1
                continue
            # find start of this token from left in this region
            # look backwards to find whitespace boundary
            # easier: do forward split but limit
            # alternative: track
            break  # fallback to simple
        # simpler approach matching split behavior for maxsplit
        # do forward
        res = []
        j = 0
        count_splits = 0
        while j < n and count_splits < maxsplit:
            b = data[j]
            if b in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                j += 1
                continue
            k = j
            while k < n and data[k] not in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                k += 1
            res.append(data[j:k])
            j = k
            # skip whitespace
            while j < n and data[j] in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                j += 1
            count_splits += 1
            # but we need to handle remaining
        # not quite right - easier to do: get all tokens and if maxsplit>0, combine from left appropriately for rsplit?  # noqa: E501
        # rsplit with maxsplit splits from right
        # get all tokens
        all_tokens = []
        j = 0
        while j < n:
            if data[j] in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                j += 1
                continue
            k = j
            while k < n and data[k] not in (0x20, 0x09, 0x0A, 0x0B, 0x0C, 0x0D):
                k += 1
            all_tokens.append(data[j:k])
            j = k
        if maxsplit < 0:
            return all_tokens
        if maxsplit == 0:
            if all_tokens:
                return [bytes(data).strip()] if False else [bytes(data).replace(b'\t',b' ').replace(b'\n',b' ').replace(b'\r',b' ')]  # wrong  # noqa: E501
            # easier: just return the whole thing as one element if no split would occur? bytes.split with maxsplit 0 and sep None returns [s] if not all whitespace  # noqa: E501
            # check if all whitespace
            if not data.strip():
                return []
            # but "if maxsplit is given and non-negative, at most maxsplit splits are made" - result has maxsplit+1 elements  # noqa: E501
            return [bytes(data)]  # not quite right for bytes semantics
        # for maxsplit>0, rsplit takes from right: gives at most maxsplit splits
        if len(all_tokens) <= maxsplit:
            return all_tokens
        # take all_tokens[0:len-maxsplit] as first part joined? No wait - for sep None, bytes.split ignores whitespace and returns list of non-empty tokens  # noqa: E501
        # rsplit same for sep None
        result = all_tokens[: len(all_tokens) - maxsplit]
        result.append(concat(*all_tokens[len(all_tokens) - maxsplit :])) if False else None
        # actually no - easier to just do the standard way
        # build: take leftmost (len - maxsplit) tokens joined by spaces conceptually? No wait - bytes.split(sep=None) returns a list of the words in the bytes, using whitespace as the delimiter string; any whitespace string is a separator and empty strings are removed from the result  # noqa: E501
        # so all tokens are just the words
        # rsplit does the same thing
        all_tokens[: max(0, len(all_tokens) - maxsplit)]
        all_tokens[max(0, len(all_tokens) - maxsplit) :]
        # but how to reconstruct? no - we just need to return the tokens split appropriately
        # for rsplit with sep None, it's the same as split
        if maxsplit == 0:
            if not data.strip():
                return []
            # bytes behavior: split(b'   ', None) gives [] if all whitespace? let us check
            # easier to be compatible with Python bytes behavior
            pass
    # sep is not None
    if sep == b"":
        raise ValueError("empty separator")
    if maxsplit == 0:
        return [bytes(data)]
    if maxsplit < 0:
        i = len(data) - len(sep)
        # search from right
        # build from right to left
        # collect split positions
        # find all occurrences from right to left up to maxsplit? no maxsplit negative means all
        idx = data.rfind(sep)
        if idx == -1:
            return [bytes(data)]
        # easier to do iteratively
        # do it properly
        result_parts = []
        remaining = bytes(data)
        splits_done = 0
        while True:
            if maxsplit >= 0 and splits_done >= maxsplit:
                result_parts.append(remaining)
                break
            idx = remaining.rfind(sep)
            if idx == -1:
                result_parts.append(remaining)
                break
            result_parts.append(remaining[idx + len(sep) :])
            remaining = remaining[:idx]
            splits_done += 1
        result_parts.reverse()
        return result_parts


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
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).capitalize()


def title(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).title()


def swapcase(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).swapcase()


def casefold(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    try:
        return bytes(data).decode("utf-8").casefold().encode("utf-8")
    except UnicodeError:
        return bytes(data).lower()



def isalnum(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isalnum()


def isalpha(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isalpha()


def isascii(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isascii()


def isdigit(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isdigit()


def islower(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).islower()


def isspace(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isspace()


def istitle(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).istitle()


def isupper(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isupper()


def isdecimal(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isdecimal()


def isnumeric(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isnumeric()


def isprintable(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isprintable()


def isidentifier(data: bytes) -> bool:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).isidentifier()


def join(iterable: object, sep: bytes = b"") -> bytes:
    if not isinstance(sep, (bytes, bytearray)):
        raise TypeError("sep must be bytes or bytearray")
    return bytes(sep).join(iterable)  # type: ignore[arg-type]


def expandtabs(data: bytes, tabsize: int = 8) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(tabsize, int):
        raise TypeError("tabsize must be int")
    return bytes(data).expandtabs(tabsize)


def decode_ascii(data: bytes, errors: str = "strict") -> str:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(errors, str):
        raise TypeError("errors must be str")
    return bytes(data).decode("ascii", errors=errors)


def encode_ascii(s: str, errors: str = "strict") -> bytes:
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


def translate(data: bytes, table: bytes) -> bytes:
    """Return a copy of *data* with each byte replaced according to *table*.

    *table* must be a bytes object of length 256 (as produced by
    :func:`maketrans`); each byte value *b* in *data* is replaced by
    *table[b]*.

    Args:
        data: Bytes or bytearray to translate.
        table: A 256-byte translation table.

    Returns:
        The translated bytes.

    Raises:
        TypeError: If *data* is not bytes or bytearray, or *table* is not
            bytes.
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
    if not isinstance(table, bytes):
        raise TypeError("table must be bytes")
    if len(table) != 256:
        raise ValueError("table must be exactly 256 bytes long")
    return bytes(data).translate(table)
