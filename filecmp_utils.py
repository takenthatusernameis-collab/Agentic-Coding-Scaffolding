"""File comparison utilities wrapping the filecmp module."""

from __future__ import annotations

import filecmp
import os
from typing import Any, Sequence


def cmp_files(a: str, b: str, shallow: bool = True) -> bool:
    """Return True if files ``a`` and ``b`` are equal.

    Args:
        a: Path to the first file.
        b: Path to the second file.
        shallow: When True, only stat metadata is compared.

    Returns:
        True if the files are considered equal, False otherwise.

    Raises:
        TypeError: If ``a`` or ``b`` is not a string.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return filecmp.cmp(a, b, shallow=shallow)


def cmp_directories(
    a: str, b: str, shallow: bool = True, hide: Sequence[str] | None = None
) -> Any:
    """Compare two directories and return a dircmp object.

    Args:
        a: Path to the first directory.
        b: Path to the second directory.
        shallow: When True, only stat metadata is compared for files.
        hide: List of names to hide from the comparison.

    Returns:
        A ``filecmp.dircmp`` instance.

    Raises:
        TypeError: If ``a`` or ``b`` is not a string.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return filecmp.dircmp(a, b, hide=None if hide is None else list(hide))


def same_file(a: str, b: str) -> bool:
    """Return True if ``a`` and ``b`` refer to the same file (same device and inode)."""
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return os.path.samefile(a, b) if os.path.exists(a) and os.path.exists(b) else False


__all__ = ["cmp_files", "cmp_directories", "same_file"]
