"""Zip archive import utilities wrapping the standard library :mod:`zipimport` module.

The :mod:`zipimport` module imports Python modules that are stored inside a Zip
archive.  This wrapper validates every argument before the standard library is
reached, so a caller gets a clear :class:`TypeError` or :class:`ValueError`
instead of an opaque failure, and it re-exports :class:`ZipImportError`, the
exception raised when an archive cannot be imported from.

The wrapper adds two conveniences the standard library does not offer.  Every
helper that works with a module inside an archive takes the archive path as an
argument, so a caller does not have to build a :class:`zipimport.zipimporter`
and keep it around, and :func:`archive_names` lists the members of an archive,
which the standard library only exposes through the private
``zipimporter._files`` mapping.

Only the archive the caller points at is read.  The module never touches the
network and never starts a subprocess.
"""

from __future__ import annotations

import os as _os
import types as _types
import zipfile as _zipfile
import zipimport as _zipimport
from importlib.machinery import ModuleSpec as _ModuleSpec

__all__: list[str] = [
    "ZipImportError",
    "archive_names",
    "find_spec",
    "get_code",
    "get_data",
    "get_filename",
    "get_source",
    "invalidate_caches",
    "is_package",
    "zip_importer",
]


#: The exception raised when a Zip archive cannot be imported from.
ZipImportError = _zipimport.ZipImportError


def _archive_path(archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes]) -> str:
    """Return *archive_path* as a string path.

    The standard library only accepts a string, so a bytes path is decoded with
    the file system encoding and a path-like object is expanded first.

    Args:
        archive_path: Path to a Zip archive.

    Returns:
        The archive path as a string.

    Raises:
        TypeError: If *archive_path* is not a path-like object.
    """
    if not isinstance(archive_path, (str, bytes, _os.PathLike)):
        raise TypeError(
            f"archive_path must be a path-like object, got {type(archive_path).__name__}"
        )
    return _os.fsdecode(_os.fspath(archive_path))


def _module_name(fullname: str) -> str:
    """Return *fullname* when it names a module.

    Args:
        fullname: The dotted name of a module.

    Returns:
        The module name unchanged.

    Raises:
        TypeError: If *fullname* is not a string.
        ValueError: If *fullname* is empty or is not a dotted module name.
    """
    if not isinstance(fullname, str):
        raise TypeError(f"fullname must be a string, got {type(fullname).__name__}")
    if not fullname:
        raise ValueError("fullname must not be empty")
    for part in fullname.split("."):
        if not part.isidentifier():
            raise ValueError(f"fullname must be a dotted module name, got {fullname!r}")
    return fullname


def zip_importer(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
) -> _zipimport.zipimporter:
    """Return a :class:`zipimport.zipimporter` for *archive_path*.

    The archive path may point to a directory inside the archive, in which case
    the importer is limited to the modules below that directory.

    Args:
        archive_path: Path to a Zip archive.

    Returns:
        A :class:`zipimport.zipimporter` for the archive.

    Raises:
        TypeError: If *archive_path* is not a path-like object.
        ZipImportError: If the archive cannot be opened.
    """
    return _zipimport.zipimporter(_archive_path(archive_path))


def archive_names(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
) -> list[str]:
    """Return the sorted names of the members of the archive at *archive_path*.

    Args:
        archive_path: Path to a Zip archive.

    Returns:
        The names of the members of the archive.

    Raises:
        TypeError: If *archive_path* is not a path-like object.
        FileNotFoundError: If the archive does not exist.
        zipfile.BadZipFile: If the file is not a Zip archive.
    """
    with _zipfile.ZipFile(_archive_path(archive_path)) as archive:
        return sorted(archive.namelist())


def get_source(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
    fullname: str,
) -> str | None:
    """Return the source code of the module *fullname* inside the archive.

    Args:
        archive_path: Path to a Zip archive.
        fullname: The dotted name of the module.

    Returns:
        The source code of the module, or ``None`` when the archive holds the
        module as byte code only.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fullname* is not a dotted module name.
        ZipImportError: If the module is not in the archive.
    """
    importer = zip_importer(archive_path)
    return importer.get_source(_module_name(fullname))


def get_code(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
    fullname: str,
) -> _types.CodeType:
    """Return the code object of the module *fullname* inside the archive.

    Args:
        archive_path: Path to a Zip archive.
        fullname: The dotted name of the module.

    Returns:
        The code object of the module.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fullname* is not a dotted module name.
        ZipImportError: If the module is not in the archive.
    """
    importer = zip_importer(archive_path)
    return importer.get_code(_module_name(fullname))


def get_filename(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
    fullname: str,
) -> str:
    """Return the file name the module *fullname* would be loaded from.

    Args:
        archive_path: Path to a Zip archive.
        fullname: The dotted name of the module.

    Returns:
        The path of the member of the archive that holds the module.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fullname* is not a dotted module name.
        ZipImportError: If the module is not in the archive.
    """
    importer = zip_importer(archive_path)
    return importer.get_filename(_module_name(fullname))


def get_data(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
    pathname: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
) -> bytes:
    """Return the bytes of the member *pathname* of the archive.

    Args:
        archive_path: Path to a Zip archive.
        pathname: Path of the member inside the archive.

    Returns:
        The content of the member.

    Raises:
        TypeError: If an argument has the wrong type.
        OSError: If the archive does not hold the member.
    """
    importer = zip_importer(archive_path)
    if not isinstance(pathname, (str, bytes, _os.PathLike)):
        raise TypeError(f"pathname must be a path-like object, got {type(pathname).__name__}")
    return importer.get_data(_os.fsdecode(_os.fspath(pathname)))


def is_package(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
    fullname: str,
) -> bool:
    """Return whether the module *fullname* inside the archive is a package.

    Args:
        archive_path: Path to a Zip archive.
        fullname: The dotted name of the module.

    Returns:
        ``True`` when the module is a package.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fullname* is not a dotted module name.
        ZipImportError: If the module is not in the archive.
    """
    importer = zip_importer(archive_path)
    return importer.is_package(_module_name(fullname))


def find_spec(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes],
    fullname: str,
) -> _ModuleSpec | None:
    """Return the import specification of the module *fullname* in the archive.

    Args:
        archive_path: Path to a Zip archive.
        fullname: The dotted name of the module.

    Returns:
        The specification of the module, or ``None`` when the archive does not
        hold it.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *fullname* is not a dotted module name.
    """
    importer = zip_importer(archive_path)
    return importer.find_spec(_module_name(fullname))


def invalidate_caches(
    archive_path: str | bytes | _os.PathLike[str] | _os.PathLike[bytes] | None = None,
) -> None:
    """Drop the cached directory information of Zip archives.

    The standard library caches the table of contents of every archive it has
    opened.  Without dropping that cache, a module that is added to an archive
    after the archive was first read stays invisible.

    Args:
        archive_path: When given, only the directory information of that
            archive is refreshed.  When omitted, the cache of every archive is
            dropped.

    Raises:
        TypeError: If *archive_path* is not a path-like object.
        ZipImportError: If the archive cannot be opened.
    """
    if archive_path is None:
        cache = getattr(_zipimport, "_zip_directory_cache", None)
        if isinstance(cache, dict):
            cache.clear()
        return
    zip_importer(archive_path).invalidate_caches()
