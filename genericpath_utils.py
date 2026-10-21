"""Generic path utilities wrapping the standard library :mod:`genericpath` module.

The :mod:`genericpath` module implements operations common to all :mod:`os.path`
implementations. These functions work on pathnames regardless of the operating
system and form the foundation for path manipulation.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` instead of an opaque failure from
the standard library. It re-exports the constants and functions from
:mod:`genericpath` with the same behavior, while adding input validation for
defensive programming.
"""

from __future__ import annotations

import genericpath as _genericpath
import os
from typing import Any, Callable, List, Sequence, Tuple, Union

#: Special value for use in realpath() indicating missing paths are allowed.
ALLOW_MISSING = _genericpath.ALLOW_MISSING

#: The predicate that reports whether a path is a symbolic link.
_ISLINK: Callable[[Any], bool] = getattr(_genericpath, "islink", os.path.islink)

__all__: List[str] = [
    "ALLOW_MISSING",
    "commonprefix",
    "exists",
    "getatime",
    "getctime",
    "getmtime",
    "getsize",
    "isdir",
    "isfile",
    "islink",
    "samefile",
    "sameopenfile",
    "samestat",
]


def _check_path_like(path: object, name: str) -> Union[str, bytes]:
    """Validate that *path* is a string, bytes, or path-like object.

    Args:
        path: The path object to validate.
        name: The name of the parameter for error messages.

    Returns:
        The validated path.

    Raises:
        TypeError: If *path* is not path-like.
    """
    if isinstance(path, (str, bytes, os.PathLike)):
        return path  # type: ignore[return-value]
    raise TypeError(
        f"{name} must be str, bytes, or os.PathLike object, not {type(path).__name__!r}"
    )


def _check_two_paths(path1: object, path2: object) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Validate two path objects.

    Args:
        path1: The first path.
        path2: The second path.

    Returns:
        The validated paths.

    Raises:
        TypeError: If either path is not path-like.
    """
    return _check_path_like(path1, "path1"), _check_path_like(path2, "path2")


def commonprefix(m: Sequence[Union[str, bytes, os.PathLike]]) -> str:
    """Return the longest common leading component of a list of pathnames.

    Args:
        m: A sequence of pathnames.

    Returns:
        The longest common leading component. Returns an empty string if
        the list is empty.

    Raises:
        TypeError: If *m* is not a sequence.
    """
    if not isinstance(m, (list, tuple)):
        raise TypeError("commonprefix() argument 1 must be a sequence, not %s" % type(m).__name__)
    if not m:
        return ""
    # Validate elements
    for item in m:
        if not isinstance(item, (str, bytes, os.PathLike, list, tuple)):
            raise TypeError(
                "commonprefix() argument must be str, bytes, or os.PathLike object, not %s"
                % type(item).__name__
            )
    return _genericpath.commonprefix(m)


def exists(path: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path exists.

    Returns False for broken symbolic links.

    Args:
        path: The path to test.

    Returns:
        True if the path exists, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return _genericpath.exists(path)


def getatime(filename: Union[str, bytes, os.PathLike]) -> float:
    """Return the last access time of a file, reported by os.stat().

    Args:
        filename: The path to the file.

    Returns:
        The time of last access in seconds since the epoch.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return _genericpath.getatime(filename)


def getctime(filename: Union[str, bytes, os.PathLike]) -> float:
    """Return the metadata change time of a file, reported by os.stat().

    Args:
        filename: The path to the file.

    Returns:
        The time of metadata change in seconds since the epoch.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return _genericpath.getctime(filename)


def getmtime(filename: Union[str, bytes, os.PathLike]) -> float:
    """Return the last modification time of a file, reported by os.stat().

    Args:
        filename: The path to the file.

    Returns:
        The time of last modification in seconds since the epoch.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return _genericpath.getmtime(filename)


def getsize(filename: Union[str, bytes, os.PathLike]) -> int:
    """Return the size of a file, reported by os.stat().

    Args:
        filename: The path to the file.

    Returns:
        The size of the file in bytes.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return _genericpath.getsize(filename)


def isdir(s: Union[str, bytes, os.PathLike]) -> bool:
    """Return True if the pathname refers to an existing directory.

    This follows symbolic links, so both islink() and isdir() can be true
    for the same path on systems that support symlinks.

    Args:
        s: The path to test.

    Returns:
        True if the path is an existing directory, False otherwise.

    Raises:
        TypeError: If *s* is not path-like.
    """
    _check_path_like(s, "s")
    return _genericpath.isdir(s)


def isfile(path: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path is a regular file.

    This follows symbolic links.

    Args:
        path: The path to test.

    Returns:
        True if the path is a regular file, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return _genericpath.isfile(path)


def islink(path: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path is a symbolic link.

    Args:
        path: The path to test.

    Returns:
        True if the path is a symbolic link, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return _ISLINK(path)


def samefile(f1: Union[str, bytes, os.PathLike], f2: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether two pathnames reference the same actual file or directory.

    This is determined by the device number and i-node number and raises an
    exception if an os.stat() call on either pathname fails.

    Args:
        f1: The first path.
        f2: The second path.

    Returns:
        True if both paths reference the same file, False otherwise.

    Raises:
        TypeError: If either path is not path-like.
        OSError: If either path does not exist or cannot be accessed.
    """
    _check_two_paths(f1, f2)
    return _genericpath.samefile(f1, f2)


def sameopenfile(fp1: int, fp2: int) -> bool:
    """Test whether two open file objects reference the same file.

    Args:
        fp1: A file descriptor or file object.
        fp2: A file descriptor or file object.

    Returns:
        True if both reference the same file, False otherwise.

    Raises:
        TypeError: If either argument is not an int.
        OSError: If fstat fails on either file descriptor.
    """
    if not isinstance(fp1, int) or isinstance(fp1, bool):
        raise TypeError(f"sameopenfile() argument 1 must be int, not {type(fp1).__name__!r}")
    if not isinstance(fp2, int) or isinstance(fp2, bool):
        raise TypeError(f"sameopenfile() argument 2 must be int, not {type(fp2).__name__!r}")
    return _genericpath.sameopenfile(fp1, fp2)


def samestat(s1: os.stat_result, s2: os.stat_result) -> bool:
    """Test whether two stat buffers reference the same file.

    Args:
        s1: A stat_result object.
        s2: A stat_result object.

    Returns:
        True if both stat buffers reference the same file, False otherwise.

    Raises:
        TypeError: If either argument is not a stat_result.
    """
    if not isinstance(s1, os.stat_result):
        raise TypeError(f"samestat() argument 1 must be stat_result, not {type(s1).__name__!r}")
    if not isinstance(s2, os.stat_result):
        raise TypeError(f"samestat() argument 2 must be stat_result, not {type(s2).__name__!r}")
    return _genericpath.samestat(s1, s2)
