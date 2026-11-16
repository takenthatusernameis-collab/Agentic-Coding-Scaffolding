"""Zipapp utility functions."""

from __future__ import annotations

import zipapp
import zipfile
from pathlib import Path
from typing import Callable, Optional, Union

__all__ = [
    "ZipAppError",
    "create_archive",
    "get_interpreter",
    "create_zipapp",
    "get_zipapp_interpreter",
    "is_zipapp_archive",
]


# Re-export exception
ZipAppError = zipapp.ZipAppError

PathLikeOrStr = Union[str, Path]


def create_archive(
    source: Union[str, Path],
    target: Optional[Union[str, Path]] = None,
    interpreter: Optional[str] = None,
    main: Optional[str] = None,
    filter: Optional[Callable[[Path], bool]] = None,
    compressed: bool = False,
) -> None:
    """Create an application archive from source."""
    return zipapp.create_archive(
        source=source,
        target=target,
        interpreter=interpreter,
        main=main,
        filter=filter,
        compressed=compressed,
    )


# Aliases for convenience
create_zipapp = create_archive


def get_interpreter(archive: Union[str, Path]) -> Optional[str]:
    """Get the interpreter from an application archive."""
    return zipapp.get_interpreter(archive)


get_zipapp_interpreter = get_interpreter


def is_zipapp_archive(path: str) -> bool:
    """Check if a file is a zipapp archive.

    A zipapp is a ZIP archive, optionally prefixed with a ``#!`` interpreter
    line so the file can be executed directly. A file qualifies when its
    content is a ZIP archive, whether the archive starts at the first byte or
    after a leading shebang line. A plain script or text file that merely
    starts with ``#!`` is not a zipapp and is reported as ``False``.
    """
    try:
        return zipfile.is_zipfile(path)
    except (OSError, ValueError):
        return False
