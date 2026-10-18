"""Utilities for file type and mode inspection (wrapping :mod:`stat` and :func:`os.stat`)."""

import os
import stat as _stat
from typing import Any


def file_mode(path: str | os.PathLike[str]) -> int:
    """Return the permission bits of *path* (the low 12 bits of ``st_mode``).

    Args:
        path: Filesystem path to inspect.

    Returns:
        The file permission bits (e.g. ``0o644``).
    """
    return _stat.S_IMODE(os.stat(path).st_mode)


def file_type(path: str | os.PathLike[str]) -> int:
    """Return the file type bits of *path*.

    Args:
        path: Filesystem path to inspect.

    Returns:
        The file type bits (e.g. ``stat.S_IFREG``).
    """
    return _stat.S_IFMT(os.stat(path).st_mode)


def is_directory(path: str | os.PathLike[str]) -> bool:
    """Return True if *path* is a directory."""
    return _stat.S_ISDIR(os.stat(path).st_mode)


def is_regular_file(path: str | os.PathLike[str]) -> bool:
    """Return True if *path* is a regular file."""
    return _stat.S_ISREG(os.stat(path).st_mode)


def is_symlink(path: str | os.PathLike[str]) -> bool:
    """Return True if *path* is a symbolic link."""
    return _stat.S_ISLNK(os.lstat(path).st_mode)


def is_socket(path: str | os.PathLike[str]) -> bool:
    """Return True if *path* is a socket."""
    return _stat.S_ISSOCK(os.stat(path).st_mode)


def is_fifo(path: str | os.PathLike[str]) -> bool:
    """Return True if *path* is a FIFO (named pipe)."""
    return _stat.S_ISFIFO(os.stat(path).st_mode)


def is_device(path: str | os.PathLike[str]) -> bool:
    """Return True if *path* is a character or block device."""
    st_mode = os.stat(path).st_mode
    return _stat.S_ISCHR(st_mode) or _stat.S_ISBLK(st_mode)


def filemode(path: str | os.PathLike[str]) -> str:
    """Return a string like ``-rwxr-xr-x`` describing *path*'s permissions.

    Args:
        path: Filesystem path to inspect.

    Returns:
        The symbolic file mode string.
    """
    return _stat.filemode(os.stat(path).st_mode)


def stat_info(path: str | os.PathLike[str]) -> dict[str, Any]:
    """Return a dictionary of the :func:`os.stat` result fields for *path*.

    Args:
        path: Filesystem path to inspect.

    Returns:
        A mapping of stat result field names to their values.
    """
    result = os.stat(path)
    return {
        "mode": result.st_mode,
        "ino": result.st_ino,
        "dev": result.st_dev,
        "nlink": result.st_nlink,
        "uid": result.st_uid,
        "gid": result.st_gid,
        "size": result.st_size,
        "atime": result.st_atime,
        "mtime": result.st_mtime,
        "ctime": result.st_ctime,
    }
