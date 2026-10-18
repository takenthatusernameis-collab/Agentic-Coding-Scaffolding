"""Tarfile utility functions wrapping the standard library 'tarfile' module."""

from __future__ import annotations

import os
import tarfile
from typing import IO, Iterable


__all__: list[str] = [
    "tarfile_open",
    "tarfile_add",
    "tarfile_extract",
    "tarfile_extractall",
    "tarfile_list",
    "tarfile_create",
]


def tarfile_open(name: str, mode: str = "r:*") -> tarfile.TarFile:
    """Open a tar archive."""
    return tarfile.open(name, mode)


def tarfile_add(archive: str, name: str, arcname: str | None = None) -> None:
    """Add a file to a (possibly new) tar archive."""
    with tarfile.open(archive, "a") as tf:
        tf.add(name, arcname=arcname)


def tarfile_list(archive: str) -> list[str]:
    """List member names in a tar archive."""
    with tarfile.open(archive, "r:*") as tf:
        return tf.getnames()


def tarfile_extract(archive: str, member: str, path: str = ".") -> None:
    """Extract a single member from a tar archive."""
    with tarfile.open(archive, "r:*") as tf:
        tf.extract(member, path=path)


def tarfile_extractall(archive: str, path: str = ".") -> None:
    """Extract all members from a tar archive."""
    with tarfile.open(archive, "r:*") as tf:
        tf.extractall(path=path)


def tarfile_create(archive: str, files: Iterable[str], arcnames: Iterable[str] | None = None) -> None:
    """Create a new tar archive containing the given files."""
    names = list(files)
    arcs = list(arcnames) if arcnames is not None else names
    with tarfile.open(archive, "w") as tf:
        for name, arc in zip(names, arcs):
            tf.add(name, arcname=arc)
