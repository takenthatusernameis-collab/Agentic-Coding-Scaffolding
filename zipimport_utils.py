"""Zip archive import utilities wrapping the standard library :mod:`zipimport` module.

The :mod:`zipimport` module supports importing Python modules stored inside
a Zip archive.  This wrapper validates every argument before the standard
library is reached, so a caller gets a clear :class:`TypeError` instead of an
opaque failure, and it re-exports :class:`ZipImportError`, the exception
raised when an archive cannot be imported from.

The module is pure computation aside from reading the archive the caller
points it at, so it never touches the network or a subprocess.
"""

from __future__ import annotations

import os as _os
import zipimport as _zipimport

__all__: list[str] = [
    "ZipImportError",
    "invalidate_caches",
    "zip_importer",
]


#: The exception raised when a Zip archive cannot be imported from.
ZipImportError = _zipimport.ZipImportError


def zip_importer(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
) -> _zipimport.zipimporter:
    """Return a :class:`zipimporter` for *archive_path*.

    Args:
        archive_path: Path to a Zip archive.

    Raises:
        TypeError: If *archive_path* is not a path-like object.
        ZipImportError: If the archive cannot be opened.
    """
    if not isinstance(archive_path, (str, bytes, _os.PathLike)):
        raise TypeError(
            f"archive_path must be a path-like object, got {type(archive_path).__name__}"
        )
    return _zipimport.zipimporter(archive_path)


def invalidate_caches() -> None:
    """Clear the cache of Zip directory information."""
    _zipimport._zip_directory_cache.clear()  # type: ignore[attr-defined]
