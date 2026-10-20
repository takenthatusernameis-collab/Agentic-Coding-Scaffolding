"""Zipapp utility functions."""

from __future__ import annotations

import zipapp
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
    """Check if a file is a zipapp archive (has shebang or is a zip)."""
    try:
        with open(path, "rb") as f:
            header = f.read(2)
        # Zip files start with PK\x03\x04
        if header == b"PK":
            return True
        # Could also be a Python script with shebang
        with open(path, "rb") as f:
            first_line = f.readline()
        if first_line.startswith(b"#!"):
            # Might be a zipapp with shebang
            try:
                interp = get_interpreter(path)
                if interp is not None:
                    return True
            except Exception:
                pass
        return False
    except Exception:
        return False
