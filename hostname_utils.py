"""Hostname validation and normalization utilities."""

from __future__ import annotations

import socket
from typing import List

__all__: List[str] = [
    "is_valid_hostname",
    "normalize_hostname",
    "get_local_hostname",
    "is_fully_qualified",
    "split_hostname",
]


def _require_string(value: object, name: str) -> str:
    """Validate that *value* is a string, returning it or raising ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _label_is_valid(label: str) -> bool:
    """Return True when *label* is a valid DNS label.

    A DNS label is 1 to 63 characters long, contains only ASCII alphanumeric
    characters and hyphens, and does not start or end with a hyphen.
    """
    if not 1 <= len(label) <= 63:
        return False
    if label[0] == "-" or label[-1] == "-":
        return False
    for char in label:
        if not (char.isascii() and char.isalnum()) and char != "-":
            return False
    return True


def is_valid_hostname(hostname: str) -> bool:
    """Return True if *hostname* is a valid RFC 1123 hostname.

    A valid hostname consists of one or more labels separated by dots. Each
    label must be between 1 and 63 characters long, contain only ASCII
    alphanumeric characters and hyphens, and must not start or end with a
    hyphen. The full hostname must not exceed 253 characters. An optional
    trailing dot (fully qualified domain name form) is accepted.

    Args:
        hostname: The hostname to validate.

    Returns:
        True if *hostname* is valid, False otherwise.

    Raises:
        TypeError: If *hostname* is not a string.
    """
    _require_string(hostname, "hostname")
    if not hostname:
        return False
    if len(hostname) > 253:
        return False
    candidate = hostname[:-1] if hostname.endswith(".") else hostname
    if not candidate:
        return False
    labels = candidate.split(".")
    return all(_label_is_valid(label) for label in labels)


def normalize_hostname(hostname: str) -> str:
    """Return a normalized, lowercase hostname without a trailing dot.

    The hostname is validated first; a trailing dot is stripped and the
    result is lowercased.

    Args:
        hostname: The hostname to normalize.

    Returns:
        The normalized hostname.

    Raises:
        TypeError: If *hostname* is not a string.
        ValueError: If *hostname* is not a valid hostname.
    """
    _require_string(hostname, "hostname")
    if not is_valid_hostname(hostname):
        raise ValueError(f"invalid hostname: {hostname!r}")
    normalized = hostname.lower()
    if normalized.endswith("."):
        normalized = normalized[:-1]
    return normalized


def get_local_hostname() -> str:
    """Return the hostname of the local machine.

    Returns:
        The local hostname as reported by the operating system.
    """
    return socket.gethostname()


def is_fully_qualified(hostname: str) -> bool:
    """Return True if *hostname* is a fully qualified domain name.

    A hostname is fully qualified when it ends with a trailing dot or when it
    contains at least one dot separating multiple labels.

    Args:
        hostname: The hostname to check.

    Returns:
        True if *hostname* is fully qualified, False otherwise.

    Raises:
        TypeError: If *hostname* is not a string.
    """
    _require_string(hostname, "hostname")
    if not hostname:
        return False
    return hostname.endswith(".") or "." in hostname


def split_hostname(hostname: str) -> List[str]:
    """Return the DNS labels of *hostname*.

    An optional trailing dot is ignored. The labels are returned in order and
    preserve their original case.

    Args:
        hostname: The hostname to split.

    Returns:
        A list of DNS labels.

    Raises:
        TypeError: If *hostname* is not a string.
        ValueError: If *hostname* is not a valid hostname.
    """
    _require_string(hostname, "hostname")
    if not is_valid_hostname(hostname):
        raise ValueError(f"invalid hostname: {hostname!r}")
    candidate = hostname[:-1] if hostname.endswith(".") else hostname
    return candidate.split(".")
