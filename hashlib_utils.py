"""Hash utilities (wrapping :mod:`hashlib`).

This module provides convenient helpers for common hashing operations using
Python's standard library :mod:`hashlib`. All functions validate inputs and
raise :class:`TypeError` or :class:`ValueError` for invalid arguments.
"""

from hashlib import (
    blake2b,
    blake2s,
    md5,
    sha1,
    sha3_224,
    sha3_256,
    sha3_384,
    sha3_512,
    sha224,
    sha256,
    sha384,
    sha512,
)
from typing import Any, Callable


def _ensure_bytes(data: bytes) -> None:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes-like")


def _hash_callable(fn: Callable[..., Any], data: bytes, **kwargs) -> bytes:
    _ensure_bytes(data)
    h = fn(data, **kwargs)
    digest = h.digest()
    return bytes(digest)


def md5_hash(data: bytes) -> bytes:
    """Compute MD5 digest of ``data``."""
    return _hash_callable(md5, data)


def sha1_hash(data: bytes) -> bytes:
    """Compute SHA1 digest of ``data``."""
    return _hash_callable(sha1, data)


def sha256_hash(data: bytes) -> bytes:
    """Compute SHA256 digest of ``data``."""
    return _hash_callable(sha256, data)


def sha512_hash(data: bytes) -> bytes:
    """Compute SHA512 digest of ``data``."""
    return _hash_callable(sha512, data)


def sha3_256_hash(data: bytes) -> bytes:
    """Compute SHA3-256 digest of ``data``."""
    return _hash_callable(sha3_256, data)


def sha3_512_hash(data: bytes) -> bytes:
    """Compute SHA3-512 digest of ``data``."""
    return _hash_callable(sha3_512, data)


def blake2b_hash(data: bytes, **kwargs) -> bytes:
    """Compute BLAKE2b digest of ``data``."""
    return _hash_callable(blake2b, data, **kwargs)


def blake2s_hash(data: bytes, **kwargs) -> bytes:
    """Compute BLAKE2s digest of ``data``."""
    return _hash_callable(blake2s, data, **kwargs)


def file_hash(path: str, algorithm: str = "sha256", chunk_size: int = 8192) -> bytes:
    """Compute hash of file contents using ``algorithm``.

    Args:
        path: Path to the file to hash.
        algorithm: Name of hashlib algorithm (default ``"sha256"``).
        chunk_size: Size of chunks to read (default 8192).

    Returns:
        Digest bytes.

    Raises:
        TypeError: If inputs are of wrong type.
        ValueError: If ``chunk_size`` is not positive.
        FileNotFoundError: If ``path`` does not exist.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not isinstance(algorithm, str):
        raise TypeError("algorithm must be a string")
    if not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an int")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    import hashlib
    import os

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.digest()


__all__ = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
    "md5_hash",
    "sha1_hash",
    "sha256_hash",
    "sha512_hash",
    "sha3_256_hash",
    "sha3_512_hash",
    "blake2b_hash",
    "blake2s_hash",
    "file_hash",
]
