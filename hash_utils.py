"""Hashing and checksum utility functions for computing and verifying hashes.

This module provides utilities for computing common cryptographic hashes
(MD5, SHA1, SHA256, SHA512) and CRC32 checksums, with support for both
string and bytes inputs.
"""

from __future__ import annotations

import hashlib
import zlib
from typing import Union

__all__: list[str] = [
    "md5",
    "sha1",
    "sha256",
    "sha512",
    "crc32",
    "hash_file",
]


def _normalize_input(data: Union[str, bytes]) -> bytes:
    """Normalize input to bytes."""
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, bytes):
        return data
    raise TypeError("data must be str or bytes")


def md5(data: Union[str, bytes]) -> str:
    """Compute the MD5 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the MD5 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.md5(normalized).hexdigest()


def sha1(data: Union[str, bytes]) -> str:
    """Compute the SHA1 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the SHA1 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.sha1(normalized).hexdigest()


def sha256(data: Union[str, bytes]) -> str:
    """Compute the SHA256 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the SHA256 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.sha256(normalized).hexdigest()


def sha512(data: Union[str, bytes]) -> str:
    """Compute the SHA512 hash of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Hexadecimal digest of the SHA512 hash.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return hashlib.sha512(normalized).hexdigest()


def crc32(data: Union[str, bytes]) -> int:
    """Compute the CRC32 checksum of the input.

    Args:
        data: Input string or bytes.

    Returns:
        Integer CRC32 checksum.

    Raises:
        TypeError: If data is not str or bytes.
    """
    normalized = _normalize_input(data)
    return zlib.crc32(normalized) & 0xFFFFFFFF


def hash_file(file_path: Union[str, bytes], algorithm: str = "sha256") -> str:
    """Compute the hash of a file.

    Args:
        file_path: Path to the file to hash.
        algorithm: Hash algorithm name (md5, sha1, sha256, sha512).
        Defaults to "sha256".

    Returns:
        Hexadecimal digest of the file hash.

    Raises:
        TypeError: If file_path is not str or bytes.
        ValueError: If algorithm is not supported.
        FileNotFoundError: If the file does not exist.
        IOError: If there is an error reading the file.
    """
    if not isinstance(file_path, (str, bytes)):
        raise TypeError("file_path must be str or bytes")

    path_str = file_path.decode("utf-8") if isinstance(file_path, bytes) else file_path

    algorithm = algorithm.lower()
    hash_func = hashlib.new(algorithm) if algorithm in (
        "md5",
        "sha1",
        "sha256",
        "sha512",
    ) else None

    if hash_func is None:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    try:
        with open(path_str, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path_str}")
    except (IOError, OSError) as e:
        raise IOError(f"Error reading file {path_str}: {e}")
