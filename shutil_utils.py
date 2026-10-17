"""High-level file and directory operation utilities.

This module wraps the :mod:`shutil` standard library module to provide
convenient helpers for copying, moving, removing, and archiving files and
directory trees.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any, Optional, Union

__all__: list[str] = [
    "copy_file",
    "copy_tree",
    "move",
    "remove_tree",
    "disk_usage",
    "make_archive",
    "unpack_archive",
    "which",
]


def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> str:
    """Copy a file from ``src`` to ``dst`` and return the destination path."""
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    return str(shutil.copy2(src, dst))


def copy_tree(src: Union[str, Path], dst: Union[str, Path]) -> str:
    """Recursively copy an entire directory tree from ``src`` to ``dst``."""
    return str(shutil.copytree(src, dst, dirs_exist_ok=True))


def move(src: Union[str, Path], dst: Union[str, Path]) -> str:
    """Move a file or directory from ``src`` to ``dst``."""
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    return str(shutil.move(src, dst))


def remove_tree(path: Union[str, Path]) -> None:
    """Recursively delete a directory tree at ``path``."""
    shutil.rmtree(path)


def disk_usage(path: Union[str, Path]) -> Any:
    """Return disk usage statistics for the filesystem containing ``path``."""
    return shutil.disk_usage(path)


def make_archive(base_name: Union[str, Path], format: str, root_dir: Union[str, Path]) -> str:
    """Create an archive of ``root_dir`` and return its path."""
    return shutil.make_archive(str(base_name), format, root_dir=str(root_dir))


def unpack_archive(
    filename: Union[str, Path], extract_dir: Optional[Union[str, Path]] = None
) -> None:
    """Unpack an archive at ``filename`` into ``extract_dir``."""
    shutil.unpack_archive(filename, extract_dir=extract_dir)


def which(cmd: str) -> Optional[str]:
    """Return the path to an executable, or ``None`` if not found."""
    return shutil.which(cmd)
