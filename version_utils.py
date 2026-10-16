"""Version utility functions."""

from typing import Tuple


def parse_version(version: str) -> Tuple[int, ...]:
    """Parse a dotted version string into a tuple of integers."""
    if not isinstance(version, str) or not version:
        raise TypeError("version must be a non-empty string")
    parts = version.split(".")
    result = []
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"invalid version component: {part!r}")
        result.append(int(part))
    return tuple(result)


def compare_versions(a: str, b: str) -> int:
    """Compare two version strings. Return -1/0/1 like strcmp."""
    va = parse_version(a)
    vb = parse_version(b)
    if va < vb:
        return -1
    if va > vb:
        return 1
    return 0


def is_greater(a: str, b: str) -> bool:
    """Return True if version a is greater than version b."""
    return compare_versions(a, b) > 0


def normalize_version(version: str, length: int = 3) -> str:
    """Pad a version string with zero components to the given length."""
    parts = list(parse_version(version))
    while len(parts) < length:
        parts.append(0)
    return ".".join(str(p) for p in parts[:length])
