"""Posixpath utilities wrapping the standard library :mod:`posixpath` module.

The :mod:`posixpath` module implements the pathname operations of POSIX: it
splits a path into a head and a tail, it joins the components of a path with
a slash, and it collapses the redundant parts of a path.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` instead of an opaque failure from
the standard library. It re-exports the constants and the functions of
:mod:`posixpath` with the same behavior, and it adds the helpers the standard
library leaves to the caller: a caller can ask whether a path is rooted, and
it can compare two paths the way the operating system compares them.
"""

from __future__ import annotations

import os
import posixpath as _posixpath
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union, cast

#: The separator of a POSIX path.
sep: str = _posixpath.sep
#: The alternative separator of a POSIX path, which is None on POSIX.
altsep: Optional[str] = _posixpath.altsep
#: The current directory of a POSIX path.
curdir: str = _posixpath.curdir
#: The parent directory of a POSIX path.
pardir: str = _posixpath.pardir
#: The separator between the name and the extension of a file.
extsep: str = _posixpath.extsep
#: The separator of the entries of the search path.
pathsep: str = _posixpath.pathsep
#: The default search path of the commands.
defpath: str = _posixpath.defpath
#: The name of the device of the null file.
devnull: str = _posixpath.devnull
#: Whether the file names of the platform support the Unicode characters.
supports_unicode_filenames: bool = _posixpath.supports_unicode_filenames
#: Special value for use in realpath() indicating missing paths are allowed.
ALLOW_MISSING: Any = _posixpath.ALLOW_MISSING

#: The splitter of a path into a drive, a root, and a tail.
_SPLITROOT: Optional[Callable[[Any], Tuple[Any, Any, Any]]] = getattr(
    _posixpath, "splitroot", None
)
#: The predicate that reports whether a path is a junction.
_ISJUNCTION: Optional[Callable[[Any], bool]] = getattr(_posixpath, "isjunction", None)

__all__: List[str] = [
    "ALLOW_MISSING",
    "abspath",
    "altsep",
    "basename",
    "commonpath",
    "commonprefix",
    "curdir",
    "defpath",
    "devnull",
    "dirname",
    "exists",
    "expanduser",
    "expandvars",
    "extsep",
    "getatime",
    "getctime",
    "getmtime",
    "getsize",
    "is_rooted",
    "isabs",
    "isdir",
    "isfile",
    "isjunction",
    "islink",
    "ismount",
    "join",
    "lexists",
    "normcase",
    "normpath",
    "pardir",
    "pathsep",
    "realpath",
    "relpath",
    "samefile",
    "sameopenfile",
    "samestat",
    "sep",
    "split",
    "splitdrive",
    "splitext",
    "splitroot",
    "supports_unicode_filenames",
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


def abspath(path: Union[str, bytes, os.PathLike]) -> str:
    """Return the absolute version of a path.

    The path is resolved against the current working directory when it is
    relative.

    Args:
        path: The path to resolve.

    Returns:
        The absolute path.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(str, _posixpath.abspath(path))


def basename(p: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return the final component of a path.

    Args:
        p: The path to split.

    Returns:
        The final component of the path.

    Raises:
        TypeError: If *p* is not path-like.
    """
    _check_path_like(p, "p")
    return cast(Union[str, bytes], _posixpath.basename(p))


def commonpath(paths: Sequence[Union[str, bytes, os.PathLike]]) -> str:
    """Return the longest common sub-path of a sequence of paths.

    The paths must not mix an absolute path with a relative one.

    Args:
        paths: The sequence of paths.

    Returns:
        The longest common sub-path.

    Raises:
        TypeError: If *paths* is not a sequence of path-like objects.
        ValueError: If *paths* is empty or the paths cannot be compared.
    """
    if not isinstance(paths, (list, tuple)):
        raise TypeError(f"commonpath() argument must be a sequence, not {type(paths).__name__}")
    if not paths:
        raise ValueError("commonpath() arg is an empty sequence")
    for item in paths:
        _check_path_like(item, "path")
    return cast(str, _posixpath.commonpath(cast(Any, list(paths))))


def commonprefix(m: Sequence[Union[str, bytes, os.PathLike]]) -> str:
    """Return the longest common leading part of a list of paths.

    The comparison is made character by character, so the result does not
    have to be a path.

    Args:
        m: The list of paths.

    Returns:
        The longest common leading part, or an empty string when the list is
        empty.

    Raises:
        TypeError: If *m* is not a sequence of path-like objects.
    """
    if not isinstance(m, (list, tuple)):
        raise TypeError(f"commonprefix() argument must be a sequence, not {type(m).__name__}")
    for item in m:
        _check_path_like(item, "path")
    return cast(str, _posixpath.commonprefix(cast(Any, list(m))))


def dirname(p: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return the directory component of a path.

    Args:
        p: The path to split.

    Returns:
        The directory component of the path.

    Raises:
        TypeError: If *p* is not path-like.
    """
    _check_path_like(p, "p")
    return cast(Union[str, bytes], _posixpath.dirname(p))


def exists(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path exists.

    A broken symbolic link does not exist.

    Args:
        path: The path to test.

    Returns:
        True if the path exists, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(bool, _posixpath.exists(path))


def expanduser(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Expand a leading ``~`` or ``~user`` in a path.

    The path is left unchanged when the home directory cannot be found.

    Args:
        path: The path to expand.

    Returns:
        The expanded path, or the path itself when it cannot be expanded.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(Union[str, bytes], _posixpath.expanduser(path))


def expandvars(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Expand the shell variables of a path.

    The variables of the form ``$var`` and ``${var}`` are replaced with their
    value, and an unknown variable is left unchanged.

    Args:
        path: The path to expand.

    Returns:
        The expanded path.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(Union[str, bytes], _posixpath.expandvars(path))


def getatime(filename: Union[str, bytes, os.PathLike]) -> float:
    """Return the last access time of a file.

    Args:
        filename: The path of the file.

    Returns:
        The time of the last access in seconds since the epoch.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return cast(float, _posixpath.getatime(filename))


def getctime(filename: Union[str, bytes, os.PathLike]) -> float:
    """Return the metadata change time of a file.

    Args:
        filename: The path of the file.

    Returns:
        The time of the metadata change in seconds since the epoch.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return cast(float, _posixpath.getctime(filename))


def getmtime(filename: Union[str, bytes, os.PathLike]) -> float:
    """Return the last modification time of a file.

    Args:
        filename: The path of the file.

    Returns:
        The time of the last modification in seconds since the epoch.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return cast(float, _posixpath.getmtime(filename))


def getsize(filename: Union[str, bytes, os.PathLike]) -> int:
    """Return the size of a file.

    Args:
        filename: The path of the file.

    Returns:
        The size of the file in bytes.

    Raises:
        TypeError: If *filename* is not path-like.
        OSError: If the file does not exist or cannot be accessed.
    """
    _check_path_like(filename, "filename")
    return cast(int, _posixpath.getsize(filename))


def is_rooted(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path starts at the root of the file system.

    A path that starts with a separator is rooted even when it is relative,
    so the helper tells a rooted path apart from an absolute one.

    Args:
        path: The path to test.

    Returns:
        True if the path starts at the root, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    text = os.fspath(path)
    if isinstance(text, bytes):
        return text.startswith(b"/")
    return text.startswith("/")


def isabs(s: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is absolute.

    Args:
        s: The path to test.

    Returns:
        True if the path is absolute, False otherwise.

    Raises:
        TypeError: If *s* is not path-like.
    """
    _check_path_like(s, "s")
    return cast(bool, _posixpath.isabs(s))


def isdir(s: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is an existing directory.

    The symbolic links are followed, so a link and its target can both be
    directories.

    Args:
        s: The path to test.

    Returns:
        True if the path is an existing directory, False otherwise.

    Raises:
        TypeError: If *s* is not path-like.
    """
    _check_path_like(s, "s")
    return cast(bool, _posixpath.isdir(s))


def isfile(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is a regular file.

    The symbolic links are followed.

    Args:
        path: The path to test.

    Returns:
        True if the path is a regular file, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(bool, _posixpath.isfile(path))


def isjunction(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is a junction.

    The standard library answers the question on Windows only, and it
    reports False on the other platforms.

    Args:
        path: The path to test.

    Returns:
        True if the path is a junction, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
        RuntimeError: If the interpreter does not ship the helper.
    """
    _check_path_like(path, "path")
    predicate = _ISJUNCTION
    if predicate is None:
        raise RuntimeError("isjunction() requires Python 3.12 or newer")
    return predicate(path)


def islink(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is a symbolic link.

    Args:
        path: The path to test.

    Returns:
        True if the path is a symbolic link, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(bool, _posixpath.islink(path))


def ismount(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is a mount point.

    Args:
        path: The path to test.

    Returns:
        True if the path is a mount point, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(bool, _posixpath.ismount(path))


def join(
    a: Union[str, bytes, os.PathLike], *p: Union[str, bytes, os.PathLike]
) -> Union[str, bytes]:
    """Join the components of a path.

    A slash is inserted between the components when it is missing, and a
    component that starts with a slash starts a new path on its own.

    Args:
        a: The first component of the path.
        *p: The remaining components of the path.

    Returns:
        The joined path.

    Raises:
        TypeError: If a component is not path-like.
    """
    _check_path_like(a, "a")
    for index, item in enumerate(p):
        _check_path_like(item, f"p[{index}]")
    return cast(Union[str, bytes], _posixpath.join(cast(Any, a), *cast(Any, p)))


def lexists(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path exists, including a broken symbolic link.

    Args:
        path: The path to test.

    Returns:
        True if the path exists, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(bool, _posixpath.lexists(path))


def normcase(s: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Normalize the case of a path.

    The case of a path is left unchanged on the platforms that have no case,
    so two paths that name the same file compare equal.

    Args:
        s: The path to normalize.

    Returns:
        The normalized path.

    Raises:
        TypeError: If *s* is not path-like.
    """
    _check_path_like(s, "s")
    return cast(Union[str, bytes], _posixpath.normcase(s))


def normpath(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Normalize a path.

    The redundant separators and the components that name the current or the
    parent directory are collapsed.

    Args:
        path: The path to normalize.

    Returns:
        The normalized path.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(Union[str, bytes], _posixpath.normpath(path))


def realpath(path: Union[str, bytes, os.PathLike], strict: bool = False) -> str:
    """Return the canonical path of a file.

    The symbolic links of the path are resolved.

    Args:
        path: The path to resolve.
        strict: Whether a missing file is an error.

    Returns:
        The canonical path.

    Raises:
        TypeError: If *path* is not path-like or *strict* is not a bool.
        OSError: If *strict* is set and the file does not exist.
    """
    _check_path_like(path, "path")
    if not isinstance(strict, bool):
        raise TypeError(f"strict must be bool, not {type(strict).__name__!r}")
    return cast(str, _posixpath.realpath(cast(Any, path), strict=strict))


def relpath(
    path: Union[str, bytes, os.PathLike],
    start: Optional[Union[str, bytes, os.PathLike]] = None,
) -> str:
    """Return the relative form of a path.

    Args:
        path: The path to make relative.
        start: The directory the path is made relative to. The current
            working directory is used when it is not given.

    Returns:
        The relative path.

    Raises:
        TypeError: If *path* or *start* is not path-like.
        ValueError: If the path is empty.
    """
    _check_path_like(path, "path")
    if start is not None:
        _check_path_like(start, "start")
    return cast(str, _posixpath.relpath(cast(Any, path), cast(Any, start)))


def samefile(f1: Union[str, bytes, os.PathLike], f2: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether two paths name the same file.

    The comparison uses the device number and the inode number of the files,
    so it fails when one of the files does not exist.

    Args:
        f1: The first path.
        f2: The second path.

    Returns:
        True if both paths name the same file, False otherwise.

    Raises:
        TypeError: If either path is not path-like.
        OSError: If one of the files does not exist.
    """
    _check_two_paths(f1, f2)
    return cast(bool, _posixpath.samefile(f1, f2))


def sameopenfile(fp1: int, fp2: int) -> bool:
    """Report whether two open files name the same file.

    Args:
        fp1: The descriptor of the first file.
        fp2: The descriptor of the second file.

    Returns:
        True if both descriptors name the same file, False otherwise.

    Raises:
        TypeError: If a descriptor is not an int.
        OSError: If a descriptor cannot be inspected.
    """
    if not isinstance(fp1, int) or isinstance(fp1, bool):
        raise TypeError(f"sameopenfile() argument 1 must be int, not {type(fp1).__name__}")
    if not isinstance(fp2, int) or isinstance(fp2, bool):
        raise TypeError(f"sameopenfile() argument 2 must be int, not {type(fp2).__name__}")
    return cast(bool, _posixpath.sameopenfile(fp1, fp2))


def samestat(s1: os.stat_result, s2: os.stat_result) -> bool:
    """Report whether two stat buffers name the same file.

    Args:
        s1: The first stat buffer.
        s2: The second stat buffer.

    Returns:
        True if both buffers name the same file, False otherwise.

    Raises:
        TypeError: If a buffer is not a stat result.
    """
    if not isinstance(s1, os.stat_result):
        raise TypeError(f"samestat() argument 1 must be stat_result, not {type(s1).__name__}")
    if not isinstance(s2, os.stat_result):
        raise TypeError(f"samestat() argument 2 must be stat_result, not {type(s2).__name__}")
    return cast(bool, _posixpath.samestat(s1, s2))


def split(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split a path into a head and a tail.

    The tail is everything that follows the last separator, and the head is
    everything that comes before it.

    Args:
        p: The path to split.

    Returns:
        The head and the tail of the path.

    Raises:
        TypeError: If *p* is not path-like.
    """
    _check_path_like(p, "p")
    return cast(Tuple[Union[str, bytes], Union[str, bytes]], _posixpath.split(p))


def splitdrive(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split a path into a drive and the rest of the path.

    A POSIX path has no drive, so the drive is always empty.

    Args:
        p: The path to split.

    Returns:
        The drive and the rest of the path.

    Raises:
        TypeError: If *p* is not path-like.
    """
    _check_path_like(p, "p")
    return cast(Tuple[Union[str, bytes], Union[str, bytes]], _posixpath.splitdrive(p))


def splitroot(
    p: Union[str, bytes, os.PathLike]
) -> Tuple[Union[str, bytes], Union[str, bytes], Union[str, bytes]]:
    """Split a path into a drive, a root, and a tail.

    The drive of a POSIX path is always empty, the root is the separator
    that starts the path, and the tail is everything that comes after it.

    Args:
        p: The path to split.

    Returns:
        The drive, the root, and the tail of the path.

    Raises:
        TypeError: If *p* is not path-like.
        RuntimeError: If the interpreter does not ship the helper.
    """
    _check_path_like(p, "p")
    splitter = _SPLITROOT
    if splitter is None:
        raise RuntimeError("splitroot() requires Python 3.12 or newer")
    return cast(
        Tuple[Union[str, bytes], Union[str, bytes], Union[str, bytes]],
        splitter(p),
    )


def splitext(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split the extension from a path.

    Args:
        p: The path to split.

    Returns:
        The path without the extension and the extension itself, which
        includes the leading dot.

    Raises:
        TypeError: If *p* is not path-like.
    """
    _check_path_like(p, "p")
    return cast(Tuple[Union[str, bytes], Union[str, bytes]], _posixpath.splitext(p))
