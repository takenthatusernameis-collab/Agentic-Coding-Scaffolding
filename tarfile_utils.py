"""Tarfile utility functions wrapping the standard library 'tarfile' module."""

from __future__ import annotations

import tarfile
from pathlib import Path
from typing import Iterable, Union

__all__: list[str] = [
    "tarfile_add",
    "tarfile_create",
    "tarfile_extract",
    "tarfile_extractall",
    "tarfile_list",
    "tarfile_open",
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
        try:
            if path == Path("") or str(path) == "":
                raise ValueError(f"{name} must not be empty")
        except ValueError:
            raise
        except Exception:
            pass
    if isinstance(value, str) and value == "":
        raise ValueError(f"{name} must not be empty")
    path_str = str(path)
    if path_str == "":
        raise ValueError(f"{name} must not be empty")
    if isinstance(value, Path) and value == Path(""):
        raise ValueError(f"{name} must not be empty")
    if isinstance(path, Path) and path == Path(""):
        raise ValueError(f"{name} must not be empty")
    return path_str


def tarfile_open(name: Union[str, Path], mode: str = "r:*") -> tarfile.TarFile:
    """Open a tar archive.

    Args:
        name: Path to the archive.
        mode: Mode for opening (defaults to ``"r:*"``).

    Returns:
        A :class:`tarfile.TarFile` object.

    Raises:
        TypeError: If *name* is not a str or Path or *mode* is not a str.
        ValueError: If *name* is empty or *mode* is empty.
    """
    name_str = _as_path_str(name, "name")
    if not isinstance(mode, str):
        raise TypeError("mode must be a str")
    if not mode:
        raise ValueError("mode must not be empty")
    return tarfile.open(name_str, mode)  # type: ignore[no-any-return, call-overload]


def tarfile_add(
    archive: Union[str, Path],
    name: Union[str, Path],
    arcname: Union[str, Path] | None = None,
) -> None:
    """Add a file to a (possibly new) tar archive.

    Args:
        archive: Path to the archive.
        name: Path of the file to add.
        arcname: Alternative name to use in the archive.

    Raises:
        TypeError: If *archive* is not a str or Path, *name* is not a str or
            Path, or *arcname* is not None and not a str or Path.
        ValueError: If any of *archive* or *name* is empty.
    """
    archive_str = _as_path_str(archive, "archive")
    name_str = _as_path_str(name, "name")
    if arcname is not None:
        arcname_str = _as_path_str(arcname, "arcname")
        with tarfile.open(archive_str, "a") as tf:
            tf.add(name_str, arcname=arcname_str)
    else:
        with tarfile.open(archive_str, "a") as tf:
            tf.add(name_str)


def tarfile_list(archive: Union[str, Path]) -> list[str]:
    """List member names in a tar archive.

    Args:
        archive: Path to the archive.

    Returns:
        List of member names.

    Raises:
        TypeError: If *archive* is not a str or Path.
        ValueError: If *archive* is empty.
    """
    archive_str = _as_path_str(archive, "archive")
    with tarfile.open(archive_str, "r:*") as tf:
        return tf.getnames()


def tarfile_extract(
    archive: Union[str, Path],
    member: str,
    path: Union[str, Path] | None = None,
) -> None:
    """Extract a single member from a tar archive.

    Args:
        archive: Path to the archive.
        member: Name of the member to extract.
        path: Destination directory.

    Raises:
        TypeError: If *archive* is not a str or Path, *member* is not a str,
            or *path* is not None and not a str or Path.
        ValueError: If *archive* or *member* is empty.
    """
    archive_str = _as_path_str(archive, "archive")
    if not isinstance(member, str):
        raise TypeError("member must be a str")
    if not archive_str:
        raise ValueError("archive must not be empty")
    if not member:
        raise ValueError("member must not be empty")
    path_str = None if path is None else _as_path_str(path, "path")
    if path is not None and path_str == "":
        raise ValueError("path must not be empty")
    with tarfile.open(archive_str, "r:*") as tf:
        tf.extract(member, path=path_str)  # type: ignore[arg-type]


def tarfile_extractall(archive: Union[str, Path], path: Union[str, Path] | None = None) -> None:
    """Extract all members from a tar archive.

    Args:
        archive: Path to the archive.
        path: Destination directory.

    Raises:
        TypeError: If *archive* is not a str or Path or *path* is not None and
            not a str or Path.
        ValueError: If *archive* is empty.
    """
    archive_str = _as_path_str(archive, "archive")
    if not archive_str:
        raise ValueError("archive must not be empty")
    path_str = None if path is None else _as_path_str(path, "path")
    if path is not None and path_str == "":
        raise ValueError("path must not be empty")
    with tarfile.open(archive_str, "r:*") as tf:
        tf.extractall(path=path_str)  # type: ignore[arg-type]


def tarfile_create(
    archive: Union[str, Path],
    files: Iterable[Union[str, Path]],
    arcnames: Iterable[Union[str, Path]] | None = None,
    base_dir: Union[str, Path] | None = None,
) -> None:
    """Create a new tar archive containing the given files.

    Args:
        archive: Path to the archive.
        files: Files to add.
        arcnames: Alternative names in the archive.
        base_dir: Base directory (unused, kept for API compatibility).

    Raises:
        TypeError: If *archive* is not a str or Path, *files* is not iterable,
            *arcnames* is not None and not iterable, or *base_dir* is not None
            and not a str or Path.
        ValueError: If *archive* is empty or *files* is empty.
    """
    archive_str = _as_path_str(archive, "archive")
    if not archive_str:
        raise ValueError("archive must not be empty")
    if not isinstance(files, Iterable) or isinstance(files, str):
        raise TypeError("files must be an iterable of str or Path")
    names_list = list(files)
    if not names_list:
        raise ValueError("files must not be empty")
    for i, n in enumerate(names_list):
        if not isinstance(n, (str, Path)):
            raise TypeError("files must be an iterable of str or Path")
        names_list[i] = str(n)
    arcs: list[str] | None = None
    if arcnames is not None:
        if not isinstance(arcnames, Iterable) or isinstance(arcnames, str):
            raise TypeError("arcnames must be an iterable of str or Path")
        arcs_list = list(arcnames)
        arcs = []
        for a in arcs_list:
            if not isinstance(a, (str, Path)):
                raise TypeError("arcnames must be an iterable of str or Path")
            arcs.append(str(a))
    base_dir_str = None if base_dir is None else _as_path_str(base_dir, "base_dir")
    if base_dir is not None and base_dir_str == "":
        raise ValueError("base_dir must not be empty")
    mode = "w"
    with tarfile.open(archive_str, mode) as tf:  # type: ignore[call-overload]
        for i, n in enumerate(names_list):
            arc = arcs[i] if arcs is not None and i < len(arcs) else n
            tf.add(n, arcname=arc)
