"""Compileall utility functions."""

from __future__ import annotations

import compileall
from pathlib import Path
from typing import Any, Iterable, Optional, Union

__all__ = [
    "compile_dir",
    "compile_file",
    "compile_path",
    "main",
]

PathLikeOrStr = Union[str, Path]


def compile_file(
    fullname: Union[str, Path],
    ddir: Optional[str] = None,
    force: bool = False,
    rx: Any = None,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    invalidation_mode: Any = None,
    *,
    stripdir: Optional[Union[str, Path]] = None,
    prependdir: Optional[Union[str, Path]] = None,
    limit_sl_dest: Any = None,
    hardlink_dupes: bool = False,
) -> bool:
    """Byte-compile a single Python source file."""
    if not isinstance(fullname, (str, Path)):
        raise TypeError(f"fullname must be a str or Path, got {type(fullname).__name__}")
    if ddir is not None and not isinstance(ddir, str):
        raise TypeError(f"ddir must be a str or None, got {type(ddir).__name__}")
    if not isinstance(force, bool):
        raise TypeError(f"force must be a bool, got {type(force).__name__}")
    if not isinstance(quiet, int) or isinstance(quiet, bool):
        raise TypeError(f"quiet must be an int, got {type(quiet).__name__}")
    if not isinstance(legacy, bool):
        raise TypeError(f"legacy must be a bool, got {type(legacy).__name__}")
    if not isinstance(optimize, int) or isinstance(optimize, bool):
        raise TypeError(f"optimize must be an int, got {type(optimize).__name__}")
    if optimize not in (-1, 0, 1, 2):
        raise ValueError(f"optimize must be one of -1, 0, 1, 2, got {optimize}")
    if quiet not in (0, 1, 2):
        raise ValueError(f"quiet must be one of 0, 1, 2, got {quiet}")
    return compileall.compile_file(  # type: ignore[call-arg, arg-type, return-value]
        fullname=str(fullname),
        ddir=ddir,
        force=force,
        rx=rx,
        quiet=quiet,
        legacy=legacy,
        optimize=optimize,
        invalidation_mode=invalidation_mode,
        stripdir=str(stripdir) if stripdir is not None else None,
        prependdir=str(prependdir) if prependdir is not None else None,
        limit_sl_dest=limit_sl_dest,
        hardlink_dupes=hardlink_dupes,
    )


def compile_dir(
    dir: Union[str, Path],
    maxlevels: int = 10,
    ddir: Optional[str] = None,
    force: bool = False,
    rx: Any = None,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    workers: int = 1,
    invalidation_mode: Any = None,
    *,
    stripdir: Optional[Union[str, Path]] = None,
    prependdir: Optional[Union[str, Path]] = None,
    limit_sl_dest: Any = None,
    hardlink_dupes: bool = False,
) -> bool:
    """Byte-compile every Python source file in a directory tree."""
    if not isinstance(dir, (str, Path)):
        raise TypeError(f"dir must be a str or Path, got {type(dir).__name__}")
    if not isinstance(maxlevels, int) or isinstance(maxlevels, bool):
        raise TypeError(f"maxlevels must be an int, got {type(maxlevels).__name__}")
    if ddir is not None and not isinstance(ddir, str):
        raise TypeError(f"ddir must be a str or None, got {type(ddir).__name__}")
    if not isinstance(force, bool):
        raise TypeError(f"force must be a bool, got {type(force).__name__}")
    if not isinstance(quiet, int) or isinstance(quiet, bool):
        raise TypeError(f"quiet must be an int, got {type(quiet).__name__}")
    if not isinstance(legacy, bool):
        raise TypeError(f"legacy must be a bool, got {type(legacy).__name__}")
    if not isinstance(optimize, int) or isinstance(optimize, bool):
        raise TypeError(f"optimize must be an int, got {type(optimize).__name__}")
    if optimize not in (-1, 0, 1, 2):
        raise ValueError(f"optimize must be one of -1, 0, 1, 2, got {optimize}")
    if not isinstance(workers, int) or isinstance(workers, bool):
        raise TypeError(f"workers must be an int, got {type(workers).__name__}")
    if workers < 1:
        raise ValueError(f"workers must be >= 1, got {workers}")
    if quiet not in (0, 1, 2):
        raise ValueError(f"quiet must be one of 0, 1, 2, got {quiet}")
    return compileall.compile_dir(  # type: ignore[call-arg, arg-type, return-value]
        dir=str(dir),
        maxlevels=maxlevels,
        ddir=ddir,
        force=force,
        rx=rx,
        quiet=quiet,
        legacy=legacy,
        optimize=optimize,
        workers=workers,
        invalidation_mode=invalidation_mode,
        stripdir=str(stripdir) if stripdir is not None else None,
        prependdir=str(prependdir) if prependdir is not None else None,
        limit_sl_dest=limit_sl_dest,  # type: ignore[arg-type]
        hardlink_dupes=hardlink_dupes,
    )


def compile_path(
    skip_curdir: bool = False,
    maxlevels: int = 0,
    force: bool = False,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    invalidation_mode: Any = None,
) -> bool:
    """Byte-compile modules found on sys.path."""
    if not isinstance(skip_curdir, bool):
        raise TypeError(f"skip_curdir must be a bool, got {type(skip_curdir).__name__}")
    if not isinstance(maxlevels, int) or isinstance(maxlevels, bool):
        raise TypeError(f"maxlevels must be an int, got {type(maxlevels).__name__}")
    if not isinstance(force, bool):
        raise TypeError(f"force must be a bool, got {type(force).__name__}")
    if not isinstance(quiet, int) or isinstance(quiet, bool):
        raise TypeError(f"quiet must be an int, got {type(quiet).__name__}")
    if not isinstance(legacy, bool):
        raise TypeError(f"legacy must be a bool, got {type(legacy).__name__}")
    if not isinstance(optimize, int) or isinstance(optimize, bool):
        raise TypeError(f"optimize must be an int, got {type(optimize).__name__}")
    if optimize not in (-1, 0, 1, 2):
        raise ValueError(f"optimize must be one of -1, 0, 1, 2, got {optimize}")
    if quiet not in (0, 1, 2):
        raise ValueError(f"quiet must be one of 0, 1, 2, got {quiet}")
    return compileall.compile_path(  # type: ignore[call-arg, arg-type, return-value]
        skip_curdir=skip_curdir,
        maxlevels=maxlevels,
        force=force,
        quiet=quiet,
        legacy=legacy,
        optimize=optimize,
        invalidation_mode=invalidation_mode,  # type: ignore[arg-type]
    )


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Run the ``compileall`` command-line interface and return its exit code."""
    if argv is not None and not isinstance(argv, (list, tuple)):
        raise TypeError(f"argv must be a list, tuple, or None, got {type(argv).__name__}")
    return int(compileall.main(list(argv) if argv is not None else None))  # type: ignore[attr-defined]
