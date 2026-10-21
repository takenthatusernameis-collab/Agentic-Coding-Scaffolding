"""Windows path utilities wrapping the standard library :mod:`ntpath` module.

The :mod:`ntpath` module implements the pathname operations of Windows: it
splits a path into a drive, a root, and a tail, it joins the components of a
path with a backslash, and it folds the case of a path. The module is written
in pure Python, so it works on every platform and a caller can work with
Windows paths on a machine that runs a different operating system.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` instead of an opaque failure from
the standard library. It re-exports the constants and the functions of
:mod:`ntpath` with the same behavior, and it adds the helpers the standard
library leaves to the caller: a caller can ask whether a path carries a
drive, whether it names a share or a device, and it can convert the
separators of a path with a single call.
"""

from __future__ import annotations

import inspect
import ntpath as _ntpath
import os
from typing import Any, Callable, List, Optional, Sequence, Tuple, Union, cast

#: The separator of a Windows path.
sep: str = _ntpath.sep
#: The alternative separator of a Windows path.
altsep: str = _ntpath.altsep
#: The current directory of a Windows path.
curdir: str = _ntpath.curdir
#: The parent directory of a Windows path.
pardir: str = _ntpath.pardir
#: The separator between the name and the extension of a file.
extsep: str = _ntpath.extsep
#: The separator of the entries of the search path.
pathsep: str = _ntpath.pathsep
#: The default search path of the commands.
defpath: str = _ntpath.defpath
#: The name of the device of the null file.
devnull: str = _ntpath.devnull
#: Whether the file names of the platform support the Unicode characters.
supports_unicode_filenames: bool = _ntpath.supports_unicode_filenames
#: Special value for use in realpath() indicating missing paths are allowed.
ALLOW_MISSING: Any = _ntpath.ALLOW_MISSING

#: The splitter of a path into a drive, a root, and a tail.
_SPLITROOT: Optional[Callable[[Any], Tuple[Any, Any, Any]]] = getattr(
    _ntpath, "splitroot", None
)
#: The predicate that reports whether a path is a junction.
_ISJUNCTION: Optional[Callable[[Any], bool]] = getattr(_ntpath, "isjunction", None)
#: The predicate that reports whether a path is on a development drive.
_ISDEVDRIVE: Optional[Callable[[Any], bool]] = getattr(_ntpath, "isdevdrive", None)

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
    "has_drive",
    "is_device_path",
    "is_unc_path",
    "isabs",
    "isdevdrive",
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
    "to_backslashes",
    "to_slashes",
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


def _strict_resolver() -> Optional[Callable[[Any], str]]:
    """Return the resolver of the standard library that accepts ``strict``.

    The ``strict`` argument of :func:`ntpath.realpath` is only accepted by
    the resolver of the platform the module is written for, so the helper
    reports whether the interpreter ships a resolver that takes it.

    Returns:
        The resolver, or ``None`` when the interpreter does not support the
        argument.
    """
    try:
        parameters = inspect.signature(_ntpath.realpath).parameters
    except (TypeError, ValueError):  # pragma: no cover - a resolver without a signature
        return None
    if "strict" not in parameters:
        return None
    return cast(Callable[[Any], str], _ntpath.realpath)


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
    return cast(str, _ntpath.abspath(path))


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
    return cast(Union[str, bytes], _ntpath.basename(p))


def commonpath(paths: Sequence[Union[str, bytes, os.PathLike]]) -> str:
    """Return the longest common sub-path of a sequence of paths.

    The paths have to share the same drive, and they must not mix an
    absolute path with a relative one.

    Args:
        paths: The sequence of paths.

    Returns:
        The longest common sub-path.

    Raises:
        TypeError: If *paths* is not a sequence of path-like objects.
        ValueError: If *paths* is empty or the paths do not share a drive.
    """
    if isinstance(paths, (str, bytes, os.PathLike)):
        raise TypeError(f"commonpath() argument must be a sequence, not {type(paths).__name__}")
    if not isinstance(paths, (list, tuple)):
        raise TypeError(f"commonpath() argument must be a sequence, not {type(paths).__name__}")
    if not paths:
        raise ValueError("commonpath() arg is an empty sequence")
    for item in paths:
        _check_path_like(item, "path")
    return cast(str, _ntpath.commonpath(list(paths)))


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
    return cast(str, _ntpath.commonprefix(list(m)))


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
    return cast(Union[str, bytes], _ntpath.dirname(p))


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
    return cast(bool, _ntpath.exists(path))


def expanduser(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Expand a leading ``~`` or ``~user`` in a path.

    The standard library of Windows reads the home directory from the
    ``USERPROFILE`` and ``HOMEPATH`` variables of the environment, and it
    leaves the path unchanged when they are not set.

    Args:
        path: The path to expand.

    Returns:
        The expanded path, or the path itself when it cannot be expanded.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(Union[str, bytes], _ntpath.expanduser(path))


def expandvars(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Expand the shell variables of a path.

    The variables of the form ``$var``, ``${var}`` and ``%var%`` are replaced
    with their value, and an unknown variable is left unchanged.

    Args:
        path: The path to expand.

    Returns:
        The expanded path.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(Union[str, bytes], _ntpath.expandvars(path))


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
    return cast(float, _ntpath.getatime(filename))


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
    return cast(float, _ntpath.getctime(filename))


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
    return cast(float, _ntpath.getmtime(filename))


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
    return cast(int, _ntpath.getsize(filename))


def _drive_of(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return the drive of a path with its separators normalized.

    The standard library returns the drive as it was written, so a share
    that is written with forward slashes keeps them. The helper folds the
    separators, so the callers can compare the drive with a prefix.

    Args:
        path: The path to split.

    Returns:
        The drive of the path, or an empty string when it has none.
    """
    drive, _ = _ntpath.splitdrive(path)
    if isinstance(drive, bytes):
        return drive.replace(b"/", b"\\")
    return drive.replace("/", "\\")


def has_drive(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path carries a drive specification.

    A drive specification is a drive letter such as ``C:``, a share of a
    network such as ``\\\\server\\share``, or a device such as
    ``\\\\?\\C:``.

    Args:
        path: The path to test.

    Returns:
        True if the path carries a drive, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return bool(_drive_of(path))


def is_device_path(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path names a device.

    A device path starts with the prefix ``\\\\.\\`` or with the prefix
    ``\\\\?\\`` that the standard library uses to reach a device without
    interpreting the path.

    Args:
        path: The path to test.

    Returns:
        True if the path names a device, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    drive = _drive_of(path)
    if isinstance(drive, bytes):
        return drive.startswith(b"\\\\.\\") or drive.startswith(b"\\\\?\\")
    return drive.startswith("\\\\.\\") or drive.startswith("\\\\?\\")


def is_unc_path(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path names a share of a network.

    Args:
        path: The path to test.

    Returns:
        True if the path names a share, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    drive = _drive_of(path)
    if isinstance(drive, bytes):
        return drive.startswith(b"\\\\")
    return drive.startswith("\\\\")


def isabs(s: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is absolute.

    A path that starts with a drive or with a separator is absolute, and so
    is the path that starts with the separator of a share.

    Args:
        s: The path to test.

    Returns:
        True if the path is absolute, False otherwise.

    Raises:
        TypeError: If *s* is not path-like.
    """
    _check_path_like(s, "s")
    return cast(bool, _ntpath.isabs(s))


def isdevdrive(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is on a development drive.

    The standard library answers the question on Windows only, and it
    reports False on the other platforms.

    Args:
        path: The path to test.

    Returns:
        True if the path is on a development drive, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
        RuntimeError: If the interpreter does not ship the helper.
    """
    _check_path_like(path, "path")
    predicate = _ISDEVDRIVE
    if predicate is None:
        raise RuntimeError("isdevdrive() requires Python 3.12 or newer")
    return predicate(path)


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
    return cast(bool, _ntpath.isdir(s))


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
    return cast(bool, _ntpath.isfile(path))


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
    return cast(bool, _ntpath.islink(path))


def ismount(path: Union[str, bytes, os.PathLike]) -> bool:
    """Report whether a path is a mount point.

    A mount point is the root of a drive, the root of a share, or a volume
    that is mounted on a directory of the file system.

    Args:
        path: The path to test.

    Returns:
        True if the path is a mount point, False otherwise.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    return cast(bool, _ntpath.ismount(path))


def join(
    a: Union[str, bytes, os.PathLike], *p: Union[str, bytes, os.PathLike]
) -> Union[str, bytes]:
    """Join the components of a path.

    A backslash is inserted between the components when it is missing, and a
    component that carries a drive starts a new path on its own.

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
    return cast(Union[str, bytes], _ntpath.join(cast(Any, a), *cast(Any, p)))


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
    return cast(bool, _ntpath.lexists(path))


def normcase(s: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Fold the case of a path and normalize its separators.

    The letters of the path are lowercased and the forward slashes are
    replaced with backslashes, so two paths that name the same file compare
    equal.

    Args:
        s: The path to normalize.

    Returns:
        The normalized path.

    Raises:
        TypeError: If *s* is not path-like.
    """
    _check_path_like(s, "s")
    return cast(Union[str, bytes], _ntpath.normcase(s))


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
    return cast(Union[str, bytes], _ntpath.normpath(path))


def realpath(path: Union[str, bytes, os.PathLike], strict: bool = False) -> str:
    """Return the canonical path of a file.

    The symbolic links of the path are resolved. The standard library of
    Windows resolves them with the help of the operating system, and the
    standard library of the other platforms returns the absolute path.

    Args:
        path: The path to resolve.
        strict: Whether a missing file is an error.

    Returns:
        The canonical path.

    Raises:
        TypeError: If *path* is not path-like or *strict* is not a bool.
        RuntimeError: If *strict* is set and the interpreter does not accept
            the argument.
        OSError: If *strict* is set and the file does not exist.
    """
    _check_path_like(path, "path")
    if not isinstance(strict, bool):
        raise TypeError(f"strict must be bool, not {type(strict).__name__!r}")
    if not strict:
        return cast(str, _ntpath.realpath(path))
    resolver = _strict_resolver()
    if resolver is None:
        raise RuntimeError("realpath() with strict=True requires Python 3.12 or newer")
    return resolver(path)


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
        ValueError: If the path is empty or the paths are on different
            drives.
    """
    _check_path_like(path, "path")
    if start is not None:
        _check_path_like(start, "start")
    return cast(str, _ntpath.relpath(cast(Any, path), cast(Any, start)))


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
    return cast(bool, _ntpath.samefile(f1, f2))


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
    return cast(bool, _ntpath.sameopenfile(fp1, fp2))


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
    return cast(bool, _ntpath.samestat(s1, s2))


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
    return cast(Tuple[Union[str, bytes], Union[str, bytes]], _ntpath.split(p))


def splitdrive(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split a path into a drive and the rest of the path.

    Args:
        p: The path to split.

    Returns:
        The drive and the rest of the path.

    Raises:
        TypeError: If *p* is not path-like.
    """
    _check_path_like(p, "p")
    return cast(Tuple[Union[str, bytes], Union[str, bytes]], _ntpath.splitdrive(p))


def splitroot(
    p: Union[str, bytes, os.PathLike]
) -> Tuple[Union[str, bytes], Union[str, bytes], Union[str, bytes]]:
    """Split a path into a drive, a root, and a tail.

    The drive is the drive specification of the path, the root is the
    separator that follows it, and the tail is everything that comes after
    the root.

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
    return cast(Tuple[Union[str, bytes], Union[str, bytes]], _ntpath.splitext(p))


def to_backslashes(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return a path whose forward slashes are backslashes.

    Args:
        path: The path to convert.

    Returns:
        The path with backslashes as the only separator.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    text = os.fspath(path)
    if isinstance(text, bytes):
        return text.replace(b"/", b"\\")
    return text.replace("/", "\\")


def to_slashes(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return a path whose backslashes are forward slashes.

    A path that uses forward slashes is understood by Windows, so the
    conversion makes a path portable without changing its meaning.

    Args:
        path: The path to convert.

    Returns:
        The path with forward slashes as the only separator.

    Raises:
        TypeError: If *path* is not path-like.
    """
    _check_path_like(path, "path")
    text = os.fspath(path)
    if isinstance(text, bytes):
        return text.replace(b"\\", b"/")
    return text.replace("\\", "/")
