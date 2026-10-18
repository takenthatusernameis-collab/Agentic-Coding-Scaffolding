"""Utilities for reading and writing ZIP archives (wrapping :mod:`zipfile`).

This module provides a small, validated layer over the standard library
``zipfile`` module for creating, inspecting, and extracting archives. All
functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

import zipfile as _zipfile
from typing import Any


def create_archive(path: str, files: list[str]) -> str:
    """Create a ZIP archive at *path* containing *files*.

    Args:
        path: Destination archive path.
        files: List of file paths to add to the archive.

    Returns:
        The archive path *path*.

    Raises:
        TypeError: If *path* is not a str or *files* is not a list of strs.
        ValueError: If *path* is empty or *files* is empty.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a str")
    if not path:
        raise ValueError("path must not be empty")
    if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
        raise TypeError("files must be a list of strs")
    if not files:
        raise ValueError("files must not be empty")
    with _zipfile.ZipFile(path, "w", _zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f)
    return path


def list_names(path: str) -> list[str]:
    """Return the list of member names in the archive at *path*.

    Args:
        path: Path to a ZIP archive.

    Returns:
        A list of member names.

    Raises:
        TypeError: If *path* is not a str.
        ValueError: If *path* is empty.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a str")
    if not path:
        raise ValueError("path must not be empty")
    with _zipfile.ZipFile(path, "r") as zf:
        return zf.namelist()


def extract_all(path: str, dest: str = ".") -> None:
    """Extract all members of the archive at *path* into *dest*.

    Args:
        path: Path to a ZIP archive.
        dest: Destination directory.

    Raises:
        TypeError: If *path* or *dest* is not a str.
        ValueError: If *path* or *dest* is empty.
    """
    if not isinstance(path, str):
        raise TypeError("path must be a str")
    if not path:
        raise ValueError("path must not be empty")
    if not isinstance(dest, str):
        raise TypeError("dest must be a str")
    if not dest:
        raise ValueError("dest must not be empty")
    with _zipfile.ZipFile(path, "r") as zf:
        zf.extractall(dest)


def is_zipfile(path: Any) -> bool:
    """Return ``True`` if *path* points to a valid ZIP archive.

    Args:
        path: Path to test.

    Returns:
        ``True`` when *path* is a ZIP archive, otherwise ``False``.
    """
    return _zipfile.is_zipfile(path)
