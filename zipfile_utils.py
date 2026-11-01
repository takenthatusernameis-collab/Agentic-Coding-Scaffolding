"""Utilities for reading and writing ZIP archives (wrapping :mod:`zipfile`).

This module provides a small, validated layer over the standard library
``zipfile`` module for creating, inspecting, and extracting archives. All
functions validate their inputs and raise ``TypeError`` or ``ValueError``
on invalid arguments.
"""

from pathlib import Path
from typing import Iterable, Union
import zipfile as _zipfile

__all__ = [
    "create_archive",
    "extract_all",
    "is_zipfile",
    "list_names",
]


def _require_path(value: object, name: str = "path") -> Union[str, Path]:
    """Validate that *value* is a path-like object (str or Path).

    Raises:
        TypeError: if *value* is not a str or Path.
    """
    if not isinstance(value, (str, Path)):
        raise TypeError(f"{name} must be a str or Path, got {type(value).__name__}")
    return value


def _as_path_str(value: object, name: str = "path") -> str:
    """Coerce a path-like value to a string for stdlib APIs."""
    path = _require_path(value, name)
    if isinstance(path, Path):
        # pathlib.Path("") string representation is '.' in some cases, but better check parts
        if len(path.parts) == 0 or (len(path.parts) == 1 and path.parts[0] == "."):
            # Could be empty-like; check raw string
            pass
    path_str = str(path)
    # Empty path
    if path_str == "":
        raise ValueError(f"{name} must not be empty")
    # Path('') becomes '.' in string form - treat as empty for our API
    try:
        if isinstance(path, Path) and path == Path(""):
            raise ValueError(f"{name} must not be empty")
    except Exception:
        pass
    if path_str == "." and isinstance(path, Path):
        # Distinguish from actual current dir? Our API says empty paths raise ValueError
        # For Path('') we want ValueError
        try:
            if str(Path("")) == "." or Path(path_str) == Path(""):
                pass
        except Exception:
            pass
    # More robust: if original is Path and it's empty
    if isinstance(value, Path):
        try:
            if str(value) == "" or value == Path(""):
                raise ValueError(f"{name} must not be empty")
        except Exception:
            pass
    if path_str == "":
        raise ValueError(f"{name} must not be empty")
    return path_str


def _require_str_list(value: object, name: str) -> list[str]:
    """Validate that *value* is a list of str or Path."""
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list of strs")
    for f in value:
        if not isinstance(f, (str, Path)):
            raise TypeError(f"{name} must be a list of strs")
    result = []
    for f in value:
        s = str(f)
        if s == "":
            raise ValueError(f"{name} must not contain empty paths")
        result.append(s)
    return result


def create_archive(path: Union[str, Path], files: Iterable[Union[str, Path]]) -> str:
    """Create a ZIP archive at *path* containing *files*.

    Args:
        path: Destination archive path.
        files: Iterable of file paths to add to the archive.

    Returns:
        The archive path *path*.

    Raises:
        TypeError: If *path* is not a str or Path or *files* is not a list of strs.
        ValueError: If *path* is empty or *files* is empty.
    """
    path_str = _as_path_str(path, "path")
    if not isinstance(files, list):
        raise TypeError("files must be a list of strs")
    files_list = _require_str_list(files, "files")
    if not files_list:
        raise ValueError("files must not be empty")
    with _zipfile.ZipFile(path_str, "w", _zipfile.ZIP_DEFLATED) as zf:
        for f in files_list:
            zf.write(f)
    return path_str


def list_names(path: Union[str, Path]) -> list[str]:
    """Return the list of member names in the archive at *path*.

    Args:
        path: Path to a ZIP archive.

    Returns:
        A list of member names.

    Raises:
        TypeError: If *path* is not a str or Path.
        ValueError: If *path* is empty.
    """
    path_str = _as_path_str(path, "path")
    with _zipfile.ZipFile(path_str, "r") as zf:
        return zf.namelist()


def extract_all(path: Union[str, Path], dest: Union[str, Path] = ".") -> None:
    """Extract all members of the archive at *path* into *dest*.

    Args:
        path: Path to a ZIP archive.
        dest: Destination directory.

    Raises:
        TypeError: If *path* or *dest* is not a str or Path.
        ValueError: If *path* or *dest* is empty.
    """
    path_str = _as_path_str(path, "path")
    dest_str = _as_path_str(dest, "dest")
    with _zipfile.ZipFile(path_str, "r") as zf:
        zf.extractall(dest_str)


def is_zipfile(path: Union[str, Path]) -> bool:
    """Return ``True`` if *path* points to a valid ZIP archive.

    Args:
        path: Path to a ZIP archive.

    Returns:
        ``True`` when *path* is a ZIP archive, otherwise ``False``.

    Raises:
        TypeError: If *path* is not a str or Path.
        ValueError: If *path* is empty.
    """
    path_str = _as_path_str(path, "path")
    return _zipfile.is_zipfile(path_str)
