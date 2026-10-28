"""Version utility functions."""

from typing import List, Tuple

__all__: List[str] = [
    "parse_version",
    "parse",
    "compare_versions",
    "cmp_versions",
    "compare",
    "cmp",
    "is_greater",
    "is_less",
    "is_equal",
    "greater_than",
    "less_than",
    "equal_to",
    "is_valid_version",
    "is_semver",
    "get_major_version",
    "get_minor_version",
    "get_patch_version",
    "major",
    "minor",
    "patch",
    "is_version_greater",
    "is_version_less",
    "is_version_equal",
    "is_version_greater_equal",
    "is_version_less_equal",
    "is_newer",
    "is_older",
    "normalize_version",
    "bump_major",
    "bump_minor",
    "bump_patch",
    "increment_major",
    "increment_minor",
    "increment_patch",
    "decrement_major",
    "decrement_minor",
    "decrement_patch",
    "version_to_tuple",
    "tuple_to_version",
    "from_tuple",
    "to_tuple",
    "sort_versions",
    "max_version",
    "min_version",
    "bump_version",
    "bump",
    "increment_version",
    "increment",
    "is_stable",
    "is_initial_release",
    "is_prerelease",
    "get_prerelease",
    "get_prerelease_tag",
    "get_build_metadata",
    "get_build",
    "strip_prerelease",
    "strip_prerelease_suffix",
    "remove_prerelease",
    "strip_build_metadata",
    "strip_build",
    "remove_build_metadata",
    "strip_metadata",
    "is_compatible",
    "version_satisfies_major",
    "decrement_version",
    "decrement",
    "dec",
    "is_version_at_least",
    "is_version_at_most",
    "is_version_between",
    "at_least",
    "at_most",
    "between",
    "is_between",
]


def parse_version(version: str) -> Tuple[int, ...]:
    """Parse a dotted version string into a tuple of integers."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not version:
        raise TypeError("version must be a non-empty string")
    # Strip leading 'v' or 'V' if present
    if version and version[0] in ('v', 'V'):
        version = version[1:]
    if not version:
        raise ValueError("invalid version")
    parts = version.split(".")
    result = []
    for part in parts:
        if not part.isdigit():
            raise ValueError(f"invalid version component: {part!r}")
        result.append(int(part))
    return tuple(result)


def parse(version: str) -> Tuple[int, ...]:
    """Parse a dotted version string into a tuple of integers."""
    return parse_version(version)


# aliases
parse_version_alias = parse_version


def version_to_tuple(version: str) -> Tuple[int, ...]:
    """Parse a dotted version string into a tuple of integers."""
    return parse_version(version)


to_tuple = version_to_tuple



def compare_versions(a: str, b: str) -> int:
    """Compare two version strings. Return -1/0/1 like strcmp."""
    va = parse_version(a)
    vb = parse_version(b)
    if va < vb:
        return -1
    if va > vb:
        return 1
    return 0


cmp_versions = compare_versions
compare = compare_versions
cmp = compare_versions



def is_greater(a: str, b: str) -> bool:
    """Return True if version a is greater than version b."""
    return compare_versions(a, b) > 0


def is_less(a: str, b: str) -> bool:
    """Return True if version a is less than version b."""
    return compare_versions(a, b) < 0


def is_equal(a: str, b: str) -> bool:
    """Return True if versions are equal."""
    return compare_versions(a, b) == 0


greater_than = is_greater
less_than = is_less
equal_to = is_equal
is_newer = is_greater
is_older = is_less



def normalize_version(version: str, length: int = 3) -> str:
    """Pad a version string with zero components to the given length."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an int")
    if length < 0:
        raise ValueError("length must be non-negative")
    # Handle v prefix
    if version and version[0] in ('v', 'V'):
        version = version[1:]
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


from_tuple = tuple_to_version



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


increment_major = bump_major



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


increment_minor = bump_minor



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


increment_patch = bump_patch


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


bump = bump_version


increment_version = bump_version
increment = increment_version


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


is_semver = is_valid_version



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


major = get_major_version
minor = get_minor_version
patch = get_patch_version



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


def is_prerelease(version: str) -> bool:
    """Return True if *version* is a pre-release (has a suffix after a hyphen).

    Args:
        version: A dotted version string, optionally with a pre-release suffix.

    Returns:
        True if *version* contains a pre-release marker (e.g. ``1.2.3-rc1``).

    Raises:
        TypeError: If *version* is not a string.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    return "-" in version


def get_prerelease(version: str) -> str | None:
    """Return the pre-release tag from *version* if present.

    Args:
        version: A dotted version string, optionally with a pre-release suffix
            separated by a hyphen (e.g., ``"1.2.3-rc1"``).

    Returns:
        The pre-release string (everything after the first hyphen), or
        ``None`` if there is no pre-release suffix.

    Raises:
        TypeError: If *version* is not a string.

    Examples:
        >>> get_prerelease("1.2.3-rc1")
        'rc1'
        >>> get_prerelease("1.2.3")
        None
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if "-" not in version:
        return None
    return version.split("-", 1)[1]


get_prerelease_tag = get_prerelease


def get_build_metadata(version: str) -> str | None:
    """Return the build metadata from *version* if present.

    Args:
        version: A dotted version string, optionally with build metadata
            separated by a plus sign (e.g., ``"1.2.3+20130313144700"``).

    Returns:
        The build metadata string (everything after the first plus sign), or
        ``None`` if there is no build metadata suffix.

    Raises:
        TypeError: If *version* is not a string.

    Examples:
        >>> get_build_metadata("1.2.3+20130313144700")
        '20130313144700'
        >>> get_build_metadata("1.2.3")
        None
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if "+" not in version:
        return None
    return version.split("+", 1)[1]


get_build = get_build_metadata


def strip_prerelease(version: str) -> str:
    """Remove prerelease suffix from a version string.

    Args:
        version: A dotted version string, optionally with a prerelease
            suffix separated by a hyphen.

    Returns:
        The version string without the prerelease suffix.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.

    Examples:
        >>> strip_prerelease("1.2.3-rc1")
        '1.2.3'
        >>> strip_prerelease("1.2.3")
        '1.2.3'
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    core = version.split("-", 1)[0]
    # Validate the core part
    parse_version(core)
    return core


def strip_build_metadata(version: str) -> str:
    """Remove build metadata suffix from a version string.

    Args:
        version: A dotted version string, optionally with build metadata
            separated by a plus sign.

    Returns:
        The version string without the build metadata suffix.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.

    Examples:
        >>> strip_build_metadata("1.2.3+20130313144700")
        '1.2.3'
        >>> strip_build_metadata("1.2.3")
        '1.2.3'
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    core = version.split("+", 1)[0]
    parse_version(core)
    return core


def strip_metadata(version: str) -> str:
    """Remove both prerelease and build metadata suffixes from a version string.

    Args:
        version: A dotted version string, optionally with prerelease and/or
            build metadata suffixes.

    Returns:
        The base version string without prerelease or build metadata.

    Raises:
        TypeError: If *version* is not a string.
        ValueError: If *version* is invalid.

    Examples:
        >>> strip_metadata("1.2.3-rc1+build.123")
        '1.2.3'
        >>> strip_metadata("1.2.3")
        '1.2.3'
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    core = version
    if "-" in core:
        core = core.split("-", 1)[0]
    if "+" in core:
        core = core.split("+", 1)[0]
    parse_version(core)
    return core


strip_prerelease_suffix = strip_prerelease
remove_prerelease = strip_prerelease
remove_build_metadata = strip_build_metadata
strip_build = strip_build_metadata


def is_compatible(a: str, b: str) -> bool:
    """Return True if versions *a* and *b* share the same major version.

    Args:
        a: A dotted version string.
        b: A dotted version string.

    Returns:
        True if both versions have the same major component.

    Raises:
        TypeError: If either argument is not a string.
        ValueError: If either version string is invalid.
    """
    if not isinstance(a, str):
        raise TypeError("a must be a string")
    if not isinstance(b, str):
        raise TypeError("b must be a string")
    pa = parse_version(a)
    pb = parse_version(b)
    ma = pa[0] if pa else 0
    mb = pb[0] if pb else 0
    return ma == mb


def version_satisfies_major(version: str, required_major: int) -> bool:
    """Return True if *version* has the same major version as *required_major*."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not isinstance(required_major, int) or isinstance(required_major, bool):
        raise TypeError("required_major must be an int")
    parts = parse_version(version)
    ma = parts[0] if parts else 0
    return ma == required_major


def decrement_major(version: str) -> str:
    """Decrement the major version component."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = list(parse_version(version))
    if not parts:
        raise ValueError("invalid version")
    if parts[0] == 0:
        raise ValueError("major version cannot go below 0")
    parts[0] = parts[0] - 1
    for i in range(1, len(parts)):
        parts[i] = 0
    return ".".join(str(p) for p in parts)


def decrement_minor(version: str) -> str:
    """Decrement the minor version component."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = list(parse_version(version))
    if not parts:
        raise ValueError("invalid version")
    if len(parts) == 1:
        parts.append(0)
    if parts[1] == 0:
        raise ValueError("minor version cannot go below 0")
    parts[1] = parts[1] - 1
    for i in range(2, len(parts)):
        parts[i] = 0
    return ".".join(str(p) for p in parts)


def decrement_patch(version: str) -> str:
    """Decrement the patch version component."""
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    parts = list(parse_version(version))
    if not parts:
        raise ValueError("invalid version")
    if len(parts) < 3:
        while len(parts) < 3:
            parts.append(0)
    if parts[2] == 0:
        raise ValueError("patch version cannot go below 0")
    parts[2] = parts[2] - 1
    return ".".join(str(p) for p in parts)


def decrement_version(version: str, part: str = "patch") -> str:
    """Decrement a specific component of a version string.

    Args:
        version: A dotted version string.
        part: Which component to decrement: ``"major"``, ``"minor"``, or
            ``"patch"``. Defaults to ``"patch"``.

    Returns:
        The version string with the chosen component decremented and all
        lower-significance components reset to zero.

    Raises:
        TypeError: If *version* is not a string or *part* is not a string.
        ValueError: If *version* is invalid, *part* is not one of the
            recognized component names, or the chosen component is already 0.
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not isinstance(part, str):
        raise TypeError("part must be a string")
    normalized = part.lower()
    if normalized == "major":
        return decrement_major(version)
    if normalized == "minor":
        return decrement_minor(version)
    if normalized == "patch":
        return decrement_patch(version)
    raise ValueError(
        "part must be one of 'major', 'minor', or 'patch', "
        f"got {part!r}"
    )


decrement = decrement_version

dec = decrement_version


def is_version_at_least(version: str, minimum: str) -> bool:
    """Return True if *version* is greater than or equal to *minimum*.

    A relational companion to :func:`is_version_greater_equal` that reports
    whether *version* satisfies a lower bound.

    Args:
        version: A dotted version string.
        minimum: A dotted version string to compare against.

    Returns:
        True if *version* >= *minimum*.

    Raises:
        TypeError: If either argument is not a string.
        ValueError: If either version string is invalid.

    Examples:
        >>> is_version_at_least("1.2.3", "1.2.0")
        True
        >>> is_version_at_least("1.2.3", "1.2.3")
        True
        >>> is_version_at_least("1.2.3", "1.3.0")
        False
    """
    return compare_versions(version, minimum) >= 0


def is_version_at_most(version: str, maximum: str) -> bool:
    """Return True if *version* is less than or equal to *maximum*.

    A relational companion to :func:`is_version_less_equal` that reports
    whether *version* satisfies an upper bound.

    Args:
        version: A dotted version string.
        maximum: A dotted version string to compare against.

    Returns:
        True if *version* <= *maximum*.

    Raises:
        TypeError: If either argument is not a string.
        ValueError: If either version string is invalid.

    Examples:
        >>> is_version_at_most("1.2.3", "1.3.0")
        True
        >>> is_version_at_most("1.2.3", "1.2.3")
        True
        >>> is_version_at_most("1.2.3", "1.2.0")
        False
    """
    return compare_versions(version, maximum) <= 0


def is_version_between(
    version: str, lower: str, upper: str, inclusive: bool = True
) -> bool:
    """Return True if *version* is between *lower* and *upper*.

    Args:
        version: A dotted version string.
        lower: The lower bound version string.
        upper: The upper bound version string.
        inclusive: If True (default), bounds are inclusive.

    Returns:
        True if *version* is between *lower* and *upper*.

    Raises:
        TypeError: If any argument is not a string or *inclusive* is not a bool.
        ValueError: If any version string is invalid.

    Examples:
        >>> is_version_between("1.2.5", "1.2.0", "1.3.0")
        True
        >>> is_version_between("1.3.0", "1.2.0", "1.3.0")
        True
        >>> is_version_between("1.3.0", "1.2.0", "1.3.0", inclusive=False)
        False
        >>> is_version_between("1.1.9", "1.2.0", "1.3.0")
        False
    """
    if not isinstance(version, str):
        raise TypeError("version must be a string")
    if not isinstance(lower, str):
        raise TypeError("lower must be a string")
    if not isinstance(upper, str):
        raise TypeError("upper must be a string")
    if not isinstance(inclusive, bool):
        raise TypeError("inclusive must be a bool")
    if inclusive:
        return compare_versions(version, lower) >= 0 and compare_versions(
            version, upper
        ) <= 0
    return compare_versions(version, lower) > 0 and compare_versions(version, upper) < 0


at_least = is_version_at_least
at_most = is_version_at_most
between = is_version_between
is_between = is_version_between
