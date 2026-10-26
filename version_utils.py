"""Version utility functions."""

from typing import List, Tuple

__all__: List[str] = [
    "parse_version",
    "compare_versions",
    "is_greater",
    "is_less",
    "is_equal",
    "is_valid_version",
    "get_major_version",
    "get_minor_version",
    "get_patch_version",
    "is_version_greater",
    "is_version_less",
    "is_version_equal",
    "is_version_greater_equal",
    "is_version_less_equal",
    "normalize_version",
    "bump_major",
    "bump_minor",
    "bump_patch",
    "version_to_tuple",
    "tuple_to_version",
    "sort_versions",
    "max_version",
    "min_version",
    "bump_version",
    "is_stable",
    "is_initial_release",
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
    """Bump the major version component.

    Args:
        version: A dotted version string.

    Returns:
        The version string with the major component incremented.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = list(parse_version(version))
    if not parts:
        return "1"
    parts[0] = parts[0] + 1
    for i in range(1, len(parts)):
        parts[i] = 0
    return ".".join(str(p) for p in parts)


def bump_minor(version: str) -> str:
    """Bump the minor version component.

    Args:
        version: A dotted version string.

    Returns:
        The version string with the minor component incremented.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = list(parse_version(version))
    if not parts:
        return "0.1"
    if len(parts) == 1:
        parts.append(1)
    else:
        parts[1] = parts[1] + 1
        for i in range(2, len(parts)):
            parts[i] = 0
    return ".".join(str(p) for p in parts)


def bump_patch(version: str) -> str:
    """Bump the patch version component.

    Args:
        version: A dotted version string.

    Returns:
        The version string with the patch component incremented.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = list(parse_version(version))
    if not parts:
        return "0.0.1"
    idx = 2 if len(parts) > 2 else len(parts) - 1
    if len(parts) < 3:
        while len(parts) < 3:
            parts.append(0)
        idx = 2
    parts[idx] = parts[idx] + 1
    return ".".join(str(p) for p in parts)


def bump_version(version: str, part: str = "patch") -> str:
    """Bump a specific component of a version string.

    Args:
        version: A dotted version string.
        part: Which component to bump: ``"major"``, ``"minor"``, or
            ``"patch"``. Defaults to ``"patch"``.

    Returns:
        The version string with the chosen component incremented and all
        lower-significance components reset to zero.

    Raises:
        TypeError: If *version* is not a string or *part* is not a string.
        ValueError: If *version* is invalid or *part* is not one of the
            recognized component names.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not isinstance(part, str):
        raise TypeError("part must be a string")
    normalized = part.lower()
    if normalized == "major":
        return bump_major(version)
    if normalized == "minor":
        return bump_minor(version)
    if normalized == "patch":
        return bump_patch(version)
    raise ValueError(
        "part must be one of 'major', 'minor', or 'patch', "
        f"got {part!r}"
    )


def is_version_greater(v1: str, v2: str) -> bool:
    """Return True if v1 > v2."""
    return compare_versions(v1, v2) > 0


def is_version_less(v1: str, v2: str) -> bool:
    """Return True if v1 < v2."""
    return compare_versions(v1, v2) < 0


def is_version_equal(v1: str, v2: str) -> bool:
    """Return True if v1 == v2."""
    return compare_versions(v1, v2) == 0


def is_version_greater_equal(v1: str, v2: str) -> bool:
    """Return True if v1 >= v2."""
    return compare_versions(v1, v2) >= 0


def is_version_less_equal(v1: str, v2: str) -> bool:
    """Return True if v1 <= v2."""
    return compare_versions(v1, v2) <= 0


def sort_versions(versions: List[str]) -> List[str]:
    """Sort a list of version strings in ascending order.

    Args:
        versions: A list of dotted version strings.

    Returns:
        A new list of version strings sorted in ascending order.

    Raises:
        TypeError: If *versions* is not a list or contains non-string elements.
        ValueError: If any version string is invalid.
    """
    if not isinstance(versions, list):
        raise TypeError("versions must be a list")
    for i, v in enumerate(versions):
        if not isinstance(v, str):
            raise TypeError(f"versions[{i}] must be a string, got {type(v).__name__}")
    return sorted(versions, key=parse_version)


def max_version(versions: List[str]) -> str:
    """Return the greatest version string from a list.

    Args:
        versions: A list of dotted version strings.

    Returns:
        The greatest version string in the list.

    Raises:
        TypeError: If *versions* is not a list or contains non-string elements.
        ValueError: If the list is empty or any version string is invalid.
    """
    if not isinstance(versions, list):
        raise TypeError("versions must be a list")
    if not versions:
        raise ValueError("versions must not be empty")
    for i, v in enumerate(versions):
        if not isinstance(v, str):
            raise TypeError(f"versions[{i}] must be a string, got {type(v).__name__}")
    return max(versions, key=parse_version)


def min_version(versions: List[str]) -> str:
    """Return the least version string from a list.

    Args:
        versions: A list of dotted version strings.

    Returns:
        The least version string in the list.

    Raises:
        TypeError: If *versions* is not a list or contains non-string elements.
        ValueError: If the list is empty or any version string is invalid.
    """
    if not isinstance(versions, list):
        raise TypeError("versions must be a list")
    if not versions:
        raise ValueError("versions must not be empty")
    for i, v in enumerate(versions):
        if not isinstance(v, str):
            raise TypeError(f"versions[{i}] must be a string, got {type(v).__name__}")
    return min(versions, key=parse_version)


def is_valid_version(version: object) -> bool:
    """Return True if *version* is a valid dotted version string.

    Args:
        version: The value to check.

    Returns:
        True if *version* is a non-empty string whose components are all
        non-negative integer strings, False otherwise.
    """
    if not isinstance(version, str):
        return False
    if not version:
        return False
    return all(part.isdigit() for part in version.split("."))


def get_major_version(version: str) -> int:
    """Return the major version component.

    Args:
        version: A dotted version string.

    Returns:
        The major version component.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = parse_version(version)
    return parts[0] if parts else 0


def get_minor_version(version: str) -> int:
    """Return the minor version component.

    Args:
        version: A dotted version string.

    Returns:
        The minor version component.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = parse_version(version)
    return parts[1] if len(parts) > 1 else 0


def get_patch_version(version: str) -> int:
    """Return the patch version component.

    Args:
        version: A dotted version string.

    Returns:
        The patch version component.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = parse_version(version)
    return parts[2] if len(parts) > 2 else 0


def is_stable(version: str) -> bool:
    """Return True if *version* is a stable release (major >= 1)."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = parse_version(version)
    return bool(parts) and parts[0] >= 1


def is_initial_release(version: str) -> bool:
    """Return True if *version* is an initial (major 0) release."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = parse_version(version)
    return bool(parts) and parts[0] == 0
