"""Utilities for working with temporary files and directories
(wrapping :mod:`tempfile`)."""

import tempfile
from typing import Any, Optional


def get_tempdir() -> str:
    """Return the name of the directory used for temporary files."""
    return tempfile.gettempdir()


def gettempprefix() -> str:
    """Return the prefix for temporary file names."""
    return tempfile.gettempprefix()


def mkstemp(suffix: str = "", prefix: Optional[str] = None, dir: Optional[str] = None) -> tuple:
    """Create a temporary file and return (fd, name)."""
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    if dir is not None and not isinstance(dir, str):
        raise TypeError("dir must be a string")
    return tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)


def mkdtemp(suffix: str = "", prefix: Optional[str] = None, dir: Optional[str] = None) -> str:
    """Create a temporary directory."""
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    if dir is not None and not isinstance(dir, str):
        raise TypeError("dir must be a string")
    return tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)


def NamedTemporaryFile(
    mode: str = "w+b",
    buffering: int = -1,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    suffix: str = "",
    prefix: Optional[str] = None,
    dir: Optional[str] = None,
    delete: bool = True,
    **kwargs,
) -> Any:
    """Return a file-like object for a temporary file."""
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")
    if not isinstance(buffering, int) or isinstance(buffering, bool):
        raise TypeError("buffering must be an integer")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError("encoding must be a string or None")
    if newline is not None and not isinstance(newline, str):
        raise TypeError("newline must be a string or None")
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    if dir is not None and not isinstance(dir, str):
        raise TypeError("dir must be a string")
    if not isinstance(delete, bool):
        raise TypeError("delete must be a bool")
    return tempfile.NamedTemporaryFile(
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        newline=newline,
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        delete=delete,
        **kwargs,
    )


def TemporaryDirectory(
    suffix: str = "",
    prefix: Optional[str] = None,
    dir: Optional[str] = None,
    ignore_cleanup_errors: bool = False,
) -> Any:
    """Return a context manager for a temporary directory."""
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    if dir is not None and not isinstance(dir, str):
        raise TypeError("dir must be a string")
    if not isinstance(ignore_cleanup_errors, bool):
        raise TypeError("ignore_cleanup_errors must be a bool")
    return tempfile.TemporaryDirectory(
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        ignore_cleanup_errors=ignore_cleanup_errors,
    )


def SpooledTemporaryFile(
    max_size: int = 0,
    mode: str = "w+b",
    buffering: int = -1,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    suffix: str = "",
    prefix: Optional[str] = None,
    dir: Optional[str] = None,
) -> Any:
    """Return a spooled temporary file."""
    if not isinstance(max_size, int) or isinstance(max_size, bool):
        raise TypeError("max_size must be an integer")
    if not isinstance(mode, str):
        raise TypeError("mode must be a string")
    if not isinstance(buffering, int) or isinstance(buffering, bool):
        raise TypeError("buffering must be an integer")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError("encoding must be a string or None")
    if newline is not None and not isinstance(newline, str):
        raise TypeError("newline must be a string or None")
    if suffix is not None and not isinstance(suffix, str):
        raise TypeError("suffix must be a string")
    if prefix is not None and not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    if dir is not None and not isinstance(dir, str):
        raise TypeError("dir must be a string")
    return tempfile.SpooledTemporaryFile(
        max_size=max_size,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        newline=newline,
        suffix=suffix,
        prefix=prefix,
        dir=dir,
    )
