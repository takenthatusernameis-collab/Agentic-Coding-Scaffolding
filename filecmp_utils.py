"""File comparison utilities wrapping the filecmp module."""

from __future__ import annotations

import filecmp
import os
from typing import Any, Sequence


class _Dircmp(filecmp.dircmp):
    """A :class:`filecmp.dircmp` that honours the ``shallow`` comparison flag.

    :class:`filecmp.dircmp` always compares common files shallowly (its
    ``methodmap`` calls :func:`filecmp.cmpfiles` with the default
    ``shallow=True``), so the ``shallow`` argument of
    :func:`cmp_directories` would otherwise be silently ignored. This subclass
    forwards the flag to :func:`filecmp.cmpfiles`, propagates it to
    subdirectories, and routes lazy attribute access through its own phase
    methods (the base ``methodmap`` points at the base implementations, so
    overriding ``phase3``/``phase4`` alone is not enough).
    """

    def __init__(
        self,
        a: str,
        b: str,
        ignore: Sequence[str] | None = None,
        hide: Sequence[str] | None = None,
        shallow: bool = True,
    ) -> None:
        self.shallow = shallow
        super().__init__(a, b, ignore=ignore, hide=hide)

    def __getattr__(self, attr: str) -> Any:
        if attr in ("same_files", "diff_files", "funny_files"):
            self.phase3()
        elif attr == "subdirs":
            self.phase4()
        elif attr in ("common_dirs", "common_files", "common_funny"):
            self.phase2()
        elif attr in ("common", "left_only", "right_only"):
            self.phase1()
        elif attr in ("left_list", "right_list"):
            self.phase0()
        else:
            raise AttributeError(attr)
        return getattr(self, attr)

    def phase3(self) -> None:
        self.same_files, self.diff_files, self.funny_files = filecmp.cmpfiles(
            self.left, self.right, self.common_files, shallow=self.shallow
        )

    def phase4(self) -> None:
        self.subdirs = {}
        for name in self.common_dirs:
            a_path = os.path.join(self.left, name)
            b_path = os.path.join(self.right, name)
            subdir = self.__class__(a_path, b_path, self.ignore, self.hide)
            subdir.shallow = self.shallow
            self.subdirs[name] = subdir

    def phase4_closure(self) -> None:
        self.phase4()
        for subdir in self.subdirs.values():
            subdir.phase4_closure()


def cmp_files(a: str, b: str, shallow: bool = True) -> bool:
    """Return True if files ``a`` and ``b`` are equal.

    Args:
        a: Path to the first file.
        b: Path to the second file.
        shallow: When True, only stat metadata is compared.

    Returns:
        True if the files are considered equal, False otherwise.

    Raises:
        TypeError: If ``a`` or ``b`` is not a string.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return filecmp.cmp(a, b, shallow=shallow)


def cmp_directories(a: str, b: str, shallow: bool = True, hide: Sequence[str] | None = None) -> Any:
    """Compare two directories and return a dircmp object.

    Args:
        a: Path to the first directory.
        b: Path to the second directory.
        shallow: When True, only stat metadata is compared for files. When
            False, file contents are compared. The flag is propagated to
            subdirectories.
        hide: List of names to hide from the comparison.

    Returns:
        A ``filecmp.dircmp`` instance (a subclass that honours *shallow*).

    Raises:
        TypeError: If ``a`` or ``b`` is not a string.
    """
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return _Dircmp(a, b, hide=None if hide is None else list(hide), shallow=shallow)


def same_file(a: str, b: str) -> bool:
    """Return True if ``a`` and ``b`` refer to the same file (same device and inode)."""
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("a and b must be strings")
    return os.path.samefile(a, b) if os.path.exists(a) and os.path.exists(b) else False


__all__ = ["cmp_files", "cmp_directories", "same_file"]
