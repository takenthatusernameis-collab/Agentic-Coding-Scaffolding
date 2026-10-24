"""Version utility functions."""

from typing import List, Tuple

__all__: List[str] = [
    "parse_version",
    "compare_versions",
    "is_greater",
    "is_less",
    "is_equal",
    "is_version_greater_equal",
    "is_version_less_equal",
    "normalize_version",
    "bump_major",
    "bump_minor",
    "bump_patch",
    "version_to_tuple",
    "tuple_to_version",
]


def parse_version(version: str) -> Tuple[int, ...]:
    """Parse a dotted version string into a tuple of integers."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not version:
        raise TypeError("version must be a non-empty string")
    parts = version.split(".")
    result = []
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"invalid version component: {part!r}")
        result.append(int(part))
    return tuple(result)


def version_to_tuple(version: str) -> Tuple[int, ...]:
    """Parse a dotted version string into a tuple of integers."""
    return parse_version(version)


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


def is_less(a: str, b: str) -> bool:
    """Return True if version a is less than version b."""
    return compare_versions(a, b) < 0


def is_equal(a: str, b: str) -> bool:
    """Return True if versions are equal."""
    return compare_versions(a, b) == 0


def normalize_version(version: str, length: int = 3) -> str:
    """Pad a version string with zero components to the given length."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an int")
    if length < 0:
        raise ValueError("length must be non-negative")
    parts = list(parse_version(version))
    while len(parts) < length:
        parts.append(0)
    return ".".join(str(p) for p in parts[:length])


def tuple_to_version(version_tuple: Tuple[int, ...]) -> str:
    """Convert a version tuple to a dotted string."""
    if not isinstance(version_tuple, tuple):
        raise TypeError("version_tuple must be a tuple")
    for part in version_tuple:
        if not isinstance(part, int) or isinstance(part, bool):
            raise TypeError("version components must be ints")
    return ".".join(str(p) for p in version_tuple)


def bump_major(version: str) -> str:
    """Bump the major version component."""
    parts = list(parse_version(version))
    parts[0] = parts[0] + 1 if parts else 1
    for i in range(1, len(parts)):
        parts[i] = 0
    return ".".join(str(p) for p in parts)


def bump_minor(version: str) -> str:
    """Bump the minor version component."""
    parts = list(parse_version(version))
    if len(parts) == 0:
        return "0.1"
    parts[1] = (parts[1] if len(parts) > 1 else 0) + 1
    for i in range(2, len(parts)):
        parts[i] = 0
    if len(parts) == 1:
        parts.append(1)
    return ".".join(str(p) for p in parts)


def bump_patch(version: str) -> str:
    """Bump the patch version component."""
    parts = list(parse_version(version))
    if len(parts) == 0:
        return "0.0.1"
    idx = 2 if len(parts) > 2 else len(parts) - 1
    parts[idx] = parts[idx] + 1
    return ".".join(str(p) for p in parts)


def is_version_greater_equal(v1: str, v2: str) -> bool:
    """Return True if v1 >= v2."""
    return compare_versions(v1, v2) >= 0


def is_version_less_equal(v1: str, v2: str) -> bool:
    """Return True if v1 <= v2."""
    return compare_versions(v1, v2) <= 0
