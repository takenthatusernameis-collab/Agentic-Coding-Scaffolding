"""Posixpath utilities wrapping the standard library :mod:`posixpath` module.

The :mod:`posixpath` module implements POSIX pathname operations. This
wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` instead of an opaque failure
from the standard library. It re-exports the constants and functions from
:mod:`posixpath` with the same behavior, while adding input validation for
defensive programming.
"""

from __future__ import annotations

import os
import posixpath as _posixpath
from typing import Any, List, Optional, Sequence, Tuple, Union


# Re-export all public names from posixpath for compatibility
# Constants
sep = _posixpath.sep
altsep = _posixpath.altsep
curdir = _posixpath.curdir
pardir = _posixpath.pardir
extsep = _posixpath.extsep
pathsep = _posixpath.pathsep
defpath = _posixpath.defpath
devnull = _posixpath.devnull
supports_unicode_filenames = _posixpath.supports_unicode_filenames

# Re-export from genericpath
from posixpath import ALLOW_MISSING  # noqa: F401
from posixpath import commonprefix  # noqa: F401
from posixpath import exists  # noqa: F401
from posixpath import getatime  # noqa: F401
from posixpath import getctime  # noqa: F401
from posixpath import getmtime  # noqa: F401
from posixpath import getsize  # noqa: F401
from posixpath import isdir  # noqa: F401
from posixpath import isfile  # noqa: F401
from posixpath import islink  # noqa: F401
from posixpath import samefile  # noqa: F401
from posixpath import sameopenfile  # noqa: F401
from posixpath import samestat  # noqa: F401

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
    if isinstance(path, (str, bytes, os.PathLike)):
        return path  # type: ignore[return-value]
    raise TypeError(f"{name} must be str, bytes, or os.PathLike object, not {type(path).__name__!r}")


def _check_path_or_none(path: object, name: str) -> Union[str, bytes, None]:
    if path is None:
        return None
    return _check_path_like(path, name)


def abspath(path: Union[str, bytes, os.PathLike]) -> str:
    """Return a normalized absolutized version of the pathname path."""
    _check_path_like(path, "path")
    return _posixpath.abspath(path)


def basename(p: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return the final component of a pathname."""
    _check_path_like(p, "p")
    return _posixpath.basename(p)


def commonpath(paths: Sequence[Union[str, bytes, os.PathLike]]) -> str:
    """Return the longest common sub-path of each pathname in the sequence paths."""
    if not isinstance(paths, (list, tuple, set)):
        raise TypeError("commonpath() argument 1 must be an iterable, not %s" % type(paths).__name__)
    # Validate each element
    paths_list = list(paths)
    for item in paths_list:
        if not isinstance(item, (str, bytes, os.PathLike)):
            raise TypeError(f"Can't mix strings and bytes in path components: {item!r}")
    return _posixpath.commonpath(paths_list)


def dirname(p: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Return the directory component of a pathname."""
    _check_path_like(p, "p")
    return _posixpath.dirname(p)


def expanduser(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Expand ~ and ~user constructions."""
    _check_path_like(path, "path")
    return _posixpath.expanduser(path)


def expandvars(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Expand shell variables of form $var and ${var}."""
    _check_path_like(path, "path")
    return _posixpath.expandvars(path)


def isabs(s: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path is absolute."""
    _check_path_like(s, "s")
    return _posixpath.isabs(s)


def isjunction(path: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path is a junction."""
    _check_path_like(path, "path")
    return _posixpath.isjunction(path)


def ismount(path: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path is a mount point."""
    _check_path_like(path, "path")
    return _posixpath.ismount(path)


def join(a: Union[str, bytes, os.PathLike], *p: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Join two or more pathname components, inserting '/' as needed."""
    _check_path_like(a, "a")
    for i, item in enumerate(p):
        _check_path_like(item, f"p[{i}]")
    return _posixpath.join(a, *p)


def lexists(path: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether a path exists. Returns True for broken symbolic links."""
    _check_path_like(path, "path")
    return _posixpath.lexists(path)


def normcase(s: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Normalize the case of a pathname."""
    _check_path_like(s, "s")
    return _posixpath.normcase(s)


def normpath(path: Union[str, bytes, os.PathLike]) -> Union[str, bytes]:
    """Normalize a pathname by collapsing redundant separators and up-level references."""
    _check_path_like(path, "path")
    return _posixpath.normpath(path)


def realpath(filename: Union[str, bytes, os.PathLike], strict: bool = False) -> str:
    """Return the canonical path of the specified filename."""
    _check_path_like(filename, "filename")
    if not isinstance(strict, bool):
        raise TypeError(f"strict must be bool, not {type(strict).__name__!r}")
    return _posixpath.realpath(filename, strict=strict)


def relpath(path: Union[str, bytes, os.PathLike], start: Optional[Union[str, bytes, os.PathLike]] = None) -> str:
    """Return a relative version of a path."""
    _check_path_like(path, "path")
    if start is not None:
        _check_path_like(start, "start")
    return _posixpath.relpath(path, start=start)


def split(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split a pathname into (tail) and (head)."""
    _check_path_like(p, "p")
    return _posixpath.split(p)


def splitdrive(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split the pathname into a drive specification and the rest of the path."""
    _check_path_like(p, "p")
    return _posixpath.splitdrive(p)


def splitext(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    """Split the extension from a pathname."""
    _check_path_like(p, "p")
    return _posixpath.splitext(p)


def splitroot(p: Union[str, bytes, os.PathLike]) -> Tuple[Union[str, bytes], Union[str, bytes], Union[str, bytes]]:
    """Split a pathname into drive, root and tail."""
    _check_path_like(p, "p")
    return _posixpath.splitroot(p)


def samefile(f1: Union[str, bytes, os.PathLike], f2: Union[str, bytes, os.PathLike]) -> bool:
    """Test whether two pathnames reference the same actual file or directory."""
    _check_two_paths(f1, f2)
    return _posixpath.samefile(f1, f2)


def sameopenfile(fp1: int, fp2: int) -> bool:
    """Test whether two open file objects reference the same file."""
    if not isinstance(fp1, int) or isinstance(fp1, bool):
        raise TypeError(f"sameopenfile() argument 1 must be int, not {type(fp1).__name__!r}")
    if not isinstance(fp2, int) or isinstance(fp2, bool):
        raise TypeError(f"sameopenfile() argument 2 must be int, not {type(fp2).__name__!r}")
    return _posixpath.sameopenfile(fp1, fp2)


def samestat(s1: os.stat_result, s2: os.stat_result) -> bool:
    """Test whether two stat buffers reference the same file."""
    if not isinstance(s1, os.stat_result):
        raise TypeError(f"samestat() argument 1 must be stat_result, not {type(s1).__name__!r}")
    if not isinstance(s2, os.stat_result):
        raise TypeError(f"samestat() argument 2 must be stat_result, not {type(s2).__name__!r}")
    return _posixpath.samestat(s1, s2)


def _check_two_paths(path1: object, path2: object) -> Tuple[Union[str, bytes], Union[str, bytes]]:
    return _check_path_like(path1, "path1"), _check_path_like(path2, "path2")
