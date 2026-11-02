"""Utilities for working with temporary files and directories
(wrapping :mod:`tempfile`)."""

import tempfile
from pathlib import Path
from typing import IO, Any, Optional, Tuple, Union

__all__ = [
    "NamedTemporaryFile",
    "SpooledTemporaryFile",
    "TemporaryDirectory",
    "TemporaryFile",
    "get_tempdir",
    "gettempprefix",
    "mkdtemp",
    "mkstemp",
]


def _require_path_or_none(value: object, name: str) -> Optional[Union[str, Path]]:
    """Validate that *value* is a str or Path, or None."""
    if value is None:
        return None
    if not isinstance(value, (str, Path)):
        raise TypeError(f"{name} must be a str or Path, got {type(value).__name__}")
    return value


def _coerce_path_or_none(value: object) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def get_tempdir() -> str:
    """Return the name of the directory used for temporary files.

    Returns:
        str: The directory name used for temporary files.
    """
    return tempfile.gettempdir()


def gettempprefix() -> str:
    """Return the prefix for temporary file names.

    Returns:
        str: The prefix string.
    """
    return tempfile.gettempprefix()


def mkstemp(
    suffix: Union[str, Path] = "",
    prefix: Optional[Union[str, Path]] = None,
    dir: Optional[Union[str, Path]] = None,
) -> Tuple[int, str]:
    """Create a temporary file and return (fd, name).

    Args:
        suffix: Suffix for the temporary file name.
        prefix: Prefix for the temporary file name.
        dir: Directory in which the file is created.

    Returns:
        tuple: (file descriptor, absolute path of the file).

    Raises:
        TypeError: If suffix, prefix, or dir is not a str or Path (or None).
    """
    suffix = _require_path_or_none(suffix, "suffix")
    prefix = _require_path_or_none(prefix, "prefix")
    dir = _require_path_or_none(dir, "dir")
    return tempfile.mkstemp(suffix=_coerce_path_or_none(suffix) if suffix is not None else "", prefix=_coerce_path_or_none(prefix), dir=_coerce_path_or_none(dir))


def mkdtemp(
    suffix: Union[str, Path] = "",
    prefix: Optional[Union[str, Path]] = None,
    dir: Optional[Union[str, Path]] = None,
) -> str:
    """Create a temporary directory.

    Args:
        suffix: Suffix for the temporary directory name.
        prefix: Prefix for the temporary directory name.
        dir: Directory in which the directory is created.

    Returns:
        str: The absolute path of the created directory.

    Raises:
        TypeError: If suffix, prefix, or dir is not a str or Path (or None).
    """
    suffix = _require_path_or_none(suffix, "suffix")
    prefix = _require_path_or_none(prefix, "prefix")
    dir = _require_path_or_none(dir, "dir")
    return tempfile.mkdtemp(suffix=_coerce_path_or_none(suffix) if suffix is not None else "", prefix=_coerce_path_or_none(prefix), dir=_coerce_path_or_none(dir))


def NamedTemporaryFile(
    mode: str = "w+b",
    buffering: int = -1,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    suffix: Union[str, Path] = "",
    prefix: Optional[Union[str, Path]] = None,
    dir: Optional[Union[str, Path]] = None,
    delete: bool = True,
    **kwargs: Any,
) -> IO[Any]:
    """Return a file-like object for a temporary file.

    Args:
        mode: File opening mode.
        buffering: Buffering policy.
        encoding: Text encoding.
        newline: Newline handling.
        suffix: Suffix for the temporary file name.
        prefix: Prefix for the temporary file name.
        dir: Directory in which the file is created.
        delete: Whether to delete the file on close.
        **kwargs: Additional arguments passed to :func:`tempfile.NamedTemporaryFile`.

    Returns:
        IO: A file-like object.

    Raises:
        TypeError: If arguments have invalid types.
    """
    if not isinstance(mode, str):
        raise TypeError(f"mode must be a str, got {type(mode).__name__}")
    if not isinstance(buffering, int) or isinstance(buffering, bool):
        raise TypeError(f"buffering must be an int, got {type(buffering).__name__}")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    if newline is not None and not isinstance(newline, str):
        raise TypeError(f"newline must be a str or None, got {type(newline).__name__}")
    suffix = _require_path_or_none(suffix, "suffix")
    prefix = _require_path_or_none(prefix, "prefix")
    dir = _require_path_or_none(dir, "dir")
    if not isinstance(delete, bool):
        raise TypeError(f"delete must be a bool, got {type(delete).__name__}")
    return tempfile.NamedTemporaryFile(
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        newline=newline,
        suffix=_coerce_path_or_none(suffix) if suffix is not None else "",
        prefix=_coerce_path_or_none(prefix),
        dir=_coerce_path_or_none(dir),
        delete=delete,
        **kwargs,
    )


def TemporaryFile(
    mode: str = "w+b",
    buffering: int = -1,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    suffix: Union[str, Path] = "",
    prefix: Optional[Union[str, Path]] = None,
    dir: Optional[Union[str, Path]] = None,
    **kwargs: Any,
) -> IO[Any]:
    """Return a file-like object for an unnamed temporary file.

    Args:
        mode: File opening mode.
        buffering: Buffering policy.
        encoding: Text encoding.
        newline: Newline handling.
        suffix: Suffix for the temporary file name.
        prefix: Prefix for the temporary file name.
        dir: Directory in which the file is created.
        **kwargs: Additional arguments passed to :func:`tempfile.TemporaryFile`.

    Returns:
        IO: A file-like object.

    Raises:
        TypeError: If arguments have invalid types.

    >>> with TemporaryFile() as f:
    ...     _ = f.write(b"hello")
    ...     f.seek(0)
    ...     f.read()
    b'hello'
    """
    if not isinstance(mode, str):
        raise TypeError(f"mode must be a str, got {type(mode).__name__}")
    if not isinstance(buffering, int) or isinstance(buffering, bool):
        raise TypeError(f"buffering must be an int, got {type(buffering).__name__}")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    if newline is not None and not isinstance(newline, str):
        raise TypeError(f"newline must be a str or None, got {type(newline).__name__}")
    suffix = _require_path_or_none(suffix, "suffix")
    prefix = _require_path_or_none(prefix, "prefix")
    dir = _require_path_or_none(dir, "dir")
    return tempfile.TemporaryFile(
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        newline=newline,
        suffix=_coerce_path_or_none(suffix) if suffix is not None else "",
        prefix=_coerce_path_or_none(prefix),
        dir=_coerce_path_or_none(dir),
        **kwargs,
    )


def TemporaryDirectory(
    suffix: Union[str, Path] = "",
    prefix: Optional[Union[str, Path]] = None,
    dir: Optional[Union[str, Path]] = None,
    ignore_cleanup_errors: bool = False,
) -> Any:
    """Return a context manager for a temporary directory.

    Args:
        suffix: Suffix for the temporary directory name.
        prefix: Prefix for the temporary directory name.
        dir: Directory in which the directory is created.
        ignore_cleanup_errors: Whether to ignore cleanup errors.

    Returns:
        Any: A context manager yielding the directory path.

    Raises:
        TypeError: If arguments have invalid types.
    """
    suffix = _require_path_or_none(suffix, "suffix")
    prefix = _require_path_or_none(prefix, "prefix")
    dir = _require_path_or_none(dir, "dir")
    if not isinstance(ignore_cleanup_errors, bool):
        raise TypeError(f"ignore_cleanup_errors must be a bool, got {type(ignore_cleanup_errors).__name__}")
    return tempfile.TemporaryDirectory(
        suffix=_coerce_path_or_none(suffix) if suffix is not None else "",
        prefix=_coerce_path_or_none(prefix),
        dir=_coerce_path_or_none(dir),
        ignore_cleanup_errors=ignore_cleanup_errors,
    )


def SpooledTemporaryFile(
    max_size: int = 0,
    mode: str = "w+b",
    buffering: int = -1,
    encoding: Optional[str] = None,
    newline: Optional[str] = None,
    suffix: Union[str, Path] = "",
    prefix: Optional[Union[str, Path]] = None,
    dir: Optional[Union[str, Path]] = None,
) -> IO[Any]:
    """Return a spooled temporary file.

    Args:
        max_size: Maximum size before rolling to disk.
        mode: File opening mode.
        buffering: Buffering policy.
        encoding: Text encoding.
        newline: Newline handling.
        suffix: Suffix for the temporary file name.
        prefix: Prefix for the temporary file name.
        dir: Directory in which the file is created.

    Returns:
        IO: A file-like object.

    Raises:
        TypeError: If arguments have invalid types.
    """
    if not isinstance(max_size, int) or isinstance(max_size, bool):
        raise TypeError(f"max_size must be an int, got {type(max_size).__name__}")
    if not isinstance(mode, str):
        raise TypeError(f"mode must be a str, got {type(mode).__name__}")
    if not isinstance(buffering, int) or isinstance(buffering, bool):
        raise TypeError(f"buffering must be an int, got {type(buffering).__name__}")
    if encoding is not None and not isinstance(encoding, str):
        raise TypeError(f"encoding must be a str or None, got {type(encoding).__name__}")
    if newline is not None and not isinstance(newline, str):
        raise TypeError(f"newline must be a str or None, got {type(newline).__name__}")
    suffix = _require_path_or_none(suffix, "suffix")
    prefix = _require_path_or_none(prefix, "prefix")
    dir = _require_path_or_none(dir, "dir")
    return tempfile.SpooledTemporaryFile(
        max_size=max_size,
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        newline=newline,
        suffix=_coerce_path_or_none(suffix) if suffix is not None else "",
        prefix=_coerce_path_or_none(prefix),
        dir=_coerce_path_or_none(dir),
    )
