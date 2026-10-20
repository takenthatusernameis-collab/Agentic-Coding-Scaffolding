"""Compileall utility functions.

Thin, validated wrappers around the standard library ``compileall`` module.
The helpers only ever byte-compile files; they never import the compiled
modules and never touch the network.
"""

from __future__ import annotations

import compileall
import importlib.util
import py_compile
import re
import sys
from pathlib import Path
from typing import Iterable, Optional, Union

__all__ = [
    "compile_dir",
    "compile_file",
    "compile_path",
    "main",
    "pyc_path",
]

PathLikeOrStr = Union[str, Path]

#: Valid values for the ``optimize`` argument of the standard library helpers.
VALID_OPTIMIZE = (-1, 0, 1, 2)

#: Valid values for the ``quiet`` argument of the standard library helpers.
VALID_QUIET = (0, 1, 2)

#: The invalidation modes understood by the standard library compiler.
InvalidationMode = py_compile.PycInvalidationMode


def _validate_optimize(optimize: object) -> int:
    """Return *optimize* as an int, raising for invalid values."""
    if not isinstance(optimize, int) or isinstance(optimize, bool):
        raise TypeError(f"optimize must be an int, got {type(optimize).__name__}")
    if optimize not in VALID_OPTIMIZE:
        raise ValueError(f"optimize must be one of {VALID_OPTIMIZE}, got {optimize}")
    return optimize


def _validate_quiet(quiet: object) -> int:
    """Return *quiet* as an int, raising for invalid values."""
    if not isinstance(quiet, int) or isinstance(quiet, bool):
        raise TypeError(f"quiet must be an int, got {type(quiet).__name__}")
    if quiet not in VALID_QUIET:
        raise ValueError(f"quiet must be one of {VALID_QUIET}, got {quiet}")
    return quiet


def _validate_rx(rx: object) -> Optional[re.Pattern[str]]:
    """Return *rx* as a compiled pattern, raising for invalid values."""
    if rx is None:
        return None
    if isinstance(rx, re.Pattern):
        return rx
    raise TypeError(f"rx must be a compiled regular expression or None, got {type(rx).__name__}")


def _validate_invalidation_mode(
    invalidation_mode: Union[str, InvalidationMode, None],
) -> Optional[InvalidationMode]:
    """Return *invalidation_mode* as a :class:`PycInvalidationMode` member.

    ``None`` is passed through so the interpreter default applies.
    """
    if invalidation_mode is None:
        return None
    if isinstance(invalidation_mode, InvalidationMode):
        return invalidation_mode
    if not isinstance(invalidation_mode, str):
        raise TypeError(
            f"invalidation_mode must be a str, PycInvalidationMode, or None, "
            f"got {type(invalidation_mode).__name__}"
        )
    try:
        return py_compile.PycInvalidationMode[invalidation_mode.strip().upper().replace("-", "_")]
    except KeyError as exc:
        valid = ", ".join(mode.name for mode in InvalidationMode)
        raise ValueError(
            f"unknown invalidation_mode {invalidation_mode!r}; valid modes are: {valid}"
        ) from exc


def _validate_paths(**values: object) -> None:
    """Raise ``TypeError`` when any of *values* is not a string, path, or ``None``."""
    for name, value in values.items():
        if value is not None and not isinstance(value, (str, Path)):
            raise TypeError(f"{name} must be a str, Path, or None, got {type(value).__name__}")


def compile_file(
    fullname: PathLikeOrStr,
    ddir: Optional[str] = None,
    force: bool = False,
    rx: Optional[re.Pattern[str]] = None,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    invalidation_mode: Union[str, InvalidationMode, None] = None,
    *,
    stripdir: Optional[PathLikeOrStr] = None,
    prependdir: Optional[PathLikeOrStr] = None,
    limit_sl_dest: Optional[PathLikeOrStr] = None,
    hardlink_dupes: bool = False,
) -> bool:
    """Byte-compile a single Python source file.

    Returns ``True`` when the file was compiled successfully and ``False``
    otherwise. Invalid arguments raise ``TypeError`` or ``ValueError`` instead
    of letting the standard library fail with a less specific error.
    """
    if not isinstance(fullname, (str, Path)):
        raise TypeError(f"fullname must be a str or Path, got {type(fullname).__name__}")
    if ddir is not None and not isinstance(ddir, str):
        raise TypeError(f"ddir must be a str or None, got {type(ddir).__name__}")
    if not isinstance(force, bool):
        raise TypeError(f"force must be a bool, got {type(force).__name__}")
    if not isinstance(legacy, bool):
        raise TypeError(f"legacy must be a bool, got {type(legacy).__name__}")
    if not isinstance(hardlink_dupes, bool):
        raise TypeError(f"hardlink_dupes must be a bool, got {type(hardlink_dupes).__name__}")
    pattern = _validate_rx(rx)
    _validate_quiet(quiet)
    _validate_optimize(optimize)
    _validate_paths(stripdir=stripdir, prependdir=prependdir, limit_sl_dest=limit_sl_dest)
    mode = _validate_invalidation_mode(invalidation_mode)
    return bool(
        compileall.compile_file(
            str(fullname),
            ddir=ddir,
            force=force,
            rx=pattern,
            quiet=quiet,
            legacy=legacy,
            optimize=optimize,
            invalidation_mode=mode,
            stripdir=str(stripdir) if stripdir is not None else None,
            prependdir=str(prependdir) if prependdir is not None else None,
            limit_sl_dest=str(limit_sl_dest) if limit_sl_dest is not None else None,
            hardlink_dupes=hardlink_dupes,
        )
    )


def compile_dir(
    dir: PathLikeOrStr,
    maxlevels: Optional[int] = None,
    ddir: Optional[str] = None,
    force: bool = False,
    rx: Optional[re.Pattern[str]] = None,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    workers: int = 1,
    invalidation_mode: Union[str, InvalidationMode, None] = None,
    *,
    stripdir: Optional[PathLikeOrStr] = None,
    prependdir: Optional[PathLikeOrStr] = None,
    limit_sl_dest: Optional[PathLikeOrStr] = None,
    hardlink_dupes: bool = False,
) -> bool:
    """Byte-compile every Python source file found below a directory.

    Returns ``True`` when every file compiled successfully and ``False``
    otherwise. Invalid arguments raise ``TypeError`` or ``ValueError``.
    """
    if not isinstance(dir, (str, Path)):
        raise TypeError(f"dir must be a str or Path, got {type(dir).__name__}")
    if maxlevels is not None:
        if not isinstance(maxlevels, int) or isinstance(maxlevels, bool):
            raise TypeError(f"maxlevels must be an int or None, got {type(maxlevels).__name__}")
        if maxlevels < 0:
            raise ValueError(f"maxlevels must be >= 0, got {maxlevels}")
    if ddir is not None and not isinstance(ddir, str):
        raise TypeError(f"ddir must be a str or None, got {type(ddir).__name__}")
    if not isinstance(force, bool):
        raise TypeError(f"force must be a bool, got {type(force).__name__}")
    if not isinstance(legacy, bool):
        raise TypeError(f"legacy must be a bool, got {type(legacy).__name__}")
    if not isinstance(hardlink_dupes, bool):
        raise TypeError(f"hardlink_dupes must be a bool, got {type(hardlink_dupes).__name__}")
    if not isinstance(workers, int) or isinstance(workers, bool):
        raise TypeError(f"workers must be an int, got {type(workers).__name__}")
    if workers < 1:
        raise ValueError(f"workers must be >= 1, got {workers}")
    pattern = _validate_rx(rx)
    _validate_quiet(quiet)
    _validate_optimize(optimize)
    _validate_paths(stripdir=stripdir, prependdir=prependdir, limit_sl_dest=limit_sl_dest)
    mode = _validate_invalidation_mode(invalidation_mode)
    return bool(
        compileall.compile_dir(
            str(dir),
            maxlevels=maxlevels,
            ddir=ddir,
            force=force,
            rx=pattern,
            quiet=quiet,
            legacy=legacy,
            optimize=optimize,
            workers=workers,
            invalidation_mode=mode,
            stripdir=str(stripdir) if stripdir is not None else None,
            prependdir=str(prependdir) if prependdir is not None else None,
            limit_sl_dest=str(limit_sl_dest) if limit_sl_dest is not None else None,
            hardlink_dupes=hardlink_dupes,
        )
    )


def compile_path(
    skip_curdir: bool = True,
    maxlevels: int = 0,
    force: bool = False,
    quiet: int = 0,
    legacy: bool = False,
    optimize: int = -1,
    invalidation_mode: Union[str, InvalidationMode, None] = None,
) -> bool:
    """Byte-compile the modules found on ``sys.path``.

    The standard library walks every entry of ``sys.path``, so callers should
    narrow ``sys.path`` when they do not want the whole import path compiled.
    Invalid arguments raise ``TypeError`` or ``ValueError``.
    """
    if not isinstance(skip_curdir, bool):
        raise TypeError(f"skip_curdir must be a bool, got {type(skip_curdir).__name__}")
    if not isinstance(maxlevels, int) or isinstance(maxlevels, bool):
        raise TypeError(f"maxlevels must be an int, got {type(maxlevels).__name__}")
    if maxlevels < 0:
        raise ValueError(f"maxlevels must be >= 0, got {maxlevels}")
    if not isinstance(force, bool):
        raise TypeError(f"force must be a bool, got {type(force).__name__}")
    if not isinstance(legacy, bool):
        raise TypeError(f"legacy must be a bool, got {type(legacy).__name__}")
    _validate_quiet(quiet)
    _validate_optimize(optimize)
    mode = _validate_invalidation_mode(invalidation_mode)
    return bool(
        compileall.compile_path(
            skip_curdir=skip_curdir,
            maxlevels=maxlevels,
            force=force,
            quiet=quiet,
            legacy=legacy,
            optimize=optimize,
            invalidation_mode=mode,
        )
    )


def main(argv: Optional[Iterable[str]] = None) -> int:
    """Run the ``compileall`` command-line interface and return its exit code.

    ``argv`` accepts any iterable of strings; ``None`` runs the interface with
    the real process arguments. The standard library entry point reads
    ``sys.argv`` directly, so the arguments are installed temporarily.
    """
    if argv is not None and not isinstance(argv, (list, tuple)):
        raise TypeError(f"argv must be a list, tuple, or None, got {type(argv).__name__}")
    original_argv = sys.argv
    if argv is not None:
        sys.argv = ["compileall", *[str(item) for item in argv]]
    try:
        success = compileall.main()  # type: ignore[attr-defined]
    finally:
        sys.argv = original_argv
    return 0 if success else 1


def pyc_path(source: PathLikeOrStr) -> Path:
    """Return the bytecode path the compiler would use for *source*.

    The location follows the PEP 3147 cache layout
    (``__pycache__/<name>.<tag>.pyc``). The file is not created.
    """
    if not isinstance(source, (str, Path)):
        raise TypeError(f"source must be a str or Path, got {type(source).__name__}")
    return Path(importlib.util.cache_from_source(str(source)))
