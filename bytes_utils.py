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
