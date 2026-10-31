"""Utilities for working with bytes and binary data."""


def to_hex(data: bytes) -> str:
    """Return the hexadecimal representation of *data*."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    return bytes(data).hex()


def from_hex(text: str) -> bytes:
    """Decode a hex string into bytes."""
    if not isinstance(text, str):
        raise TypeError("text must be a str")
    return bytes.fromhex(text)


def xor(data: bytes, key: bytes) -> bytes:
    """XOR *data* with a repeating *key*."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(key, (bytes, bytearray)) or not key:
        raise ValueError("key must be non-empty bytes or bytearray")
    key_bytes = bytes(key)
    return bytes(b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data))


def chunk(data: bytes, size: int) -> list[bytes]:
    """Split *data* into chunks of *size* bytes."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes or bytearray")
    if not isinstance(size, int) or size <= 0:
        raise ValueError("size must be a positive integer")
    data = bytes(data)
    return [data[i : i + size] for i in range(0, len(data), size)]


def concat(*parts: bytes) -> bytes:
    """Concatenate one or more bytes-like objects into a single ``bytes``."""
    result = bytearray()
    for part in parts:
        if not isinstance(part, (bytes, bytearray)):
            raise TypeError("parts must be bytes or bytearray")
        result.extend(part)
    return bytes(result)
