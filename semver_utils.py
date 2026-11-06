"""Semantic versioning utilities.

This module provides utilities for working with semantic versions following
the Semantic Versioning specification (semver.org). Versions are expected in
``MAJOR.MINOR.PATCH`` form with optional pre-release and build metadata.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple

SEMVER_RE = re.compile(
    r"^(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z\-]+(?:\.[0-9A-Za-z\-]+)*))?"
    r"(?:\+(?P<build>[0-9A-Za-z\-]+(?:\.[0-9A-Za-z\-]+)*))?$"
)
__all__ = [
    "SemanticVersion",
    "bump_major",
    "bump_minor",
    "bump_patch",
    "compare_semver",
    "is_valid_semver",
    "parse_semver",
]


def _require_component(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def _require_optional_text(name: str, value: object) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string or None")
    return value


class SemanticVersion:
    """A parsed semantic version: MAJOR.MINOR.PATCH with optional pre-release/build."""

    def __init__(
        self,
        major: int,
        minor: int,
        patch: int,
        prerelease: Optional[str] = None,
        build: Optional[str] = None,
    ) -> None:
        self.major = _require_component("major", major)
        self.minor = _require_component("minor", minor)
        self.patch = _require_component("patch", patch)
        self.prerelease = _require_optional_text("prerelease", prerelease)
        self.build = _require_optional_text("build", build)

    def release_tuple(self) -> Tuple[int, int, int]:
        """Return the (major, minor, patch) release tuple."""
        return (self.major, self.minor, self.patch)

    def __str__(self) -> str:
        version = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease is not None:
            version += f"-{self.prerelease}"
        if self.build is not None:
            version += f"+{self.build}"
        return version

    def __repr__(self) -> str:
        return f"SemanticVersion({self.major}, {self.minor}, {self.patch})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return (
            self.release_tuple() == other.release_tuple()
            and self.prerelease == other.prerelease
        )

    def __hash__(self) -> int:
        return hash((self.release_tuple(), self.prerelease))
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented  # type: ignore[return-value]
        if self.release_tuple() != other.release_tuple():
            return self.release_tuple() < other.release_tuple()
        if self.prerelease is None and other.prerelease is None:
            return False
        if self.prerelease is None:
            return False  # release > prerelease
        if other.prerelease is None:
            return True
        return _compare_prerelease(self.prerelease, other.prerelease) < 0

    def __le__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented  # type: ignore[return-value]
        return self < other or self == other

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented  # type: ignore[return-value]
        return other < self

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented  # type: ignore[return-value]
        return not (self < other)

    def is_prerelease(self) -> bool:
        """Return True if this version has a pre-release tag."""
        return self.prerelease is not None


def parse_semver(version: str) -> SemanticVersion:
    """Parse a semantic version string into a :class:`SemanticVersion`.

    Raises:
        ValueError: If the string is not a valid semantic version.
    """
    if not isinstance(version, str) or not version:
        raise ValueError("version must be a non-empty string")
    match = SEMVER_RE.match(version.strip())
    if match is None:
        raise ValueError(f"invalid semantic version: {version!r}")
    return SemanticVersion(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        prerelease=match.group("prerelease"),
        build=match.group("build"),
    )


def compare_semver(a: str, b: str) -> int:
    """Compare two semantic version strings. Return -1/0/1 like strcmp."""
    va = parse_semver(a)
    vb = parse_semver(b)
    if va < vb:
        return -1
    if va > vb:
        return 1
    return 0


def bump_major(version: str) -> str:
    """Bump the major version, resetting minor and patch to zero."""
    parsed = parse_semver(version)
    return str(SemanticVersion(parsed.major + 1, 0, 0))


def bump_minor(version: str) -> str:
    """Bump the minor version, resetting patch to zero."""
    parsed = parse_semver(version)
    return str(SemanticVersion(parsed.major, parsed.minor + 1, 0))


def bump_patch(version: str) -> str:
    """Bump the patch version."""
    parsed = parse_semver(version)
    return str(SemanticVersion(parsed.major, parsed.minor, parsed.patch + 1))


def is_valid_semver(version: str) -> bool:
    """Return True if the string is a valid semantic version."""
    try:
        parse_semver(version)
        return True
    except ValueError:
        return False


def _compare_prerelease(a: str, b: str) -> int:
    """Compare two pre-release identifiers per SemVer spec."""
    a_parts = a.split(".")
    b_parts = b.split(".")
    for left, right in zip(a_parts, b_parts):
        left_digit = left.isdigit() and left.isascii()
        right_digit = right.isdigit() and right.isascii()
        if left_digit and right_digit:
            li, ri = int(left), int(right)
            if li < ri:
                return -1
            if li > ri:
                return 1
        elif left_digit:
            return -1  # numeric identifiers have lower precedence
        elif right_digit:
            return 1
        else:
            if left < right:
                return -1
            if left > right:
                return 1
    if len(a_parts) < len(b_parts):
        return -1
    if len(a_parts) > len(b_parts):
        return 1
    return 0
