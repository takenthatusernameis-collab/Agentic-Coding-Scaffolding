"""Py_compile utility functions."""

from __future__ import annotations

import os
import py_compile
from pathlib import Path
from typing import Optional, Union

__all__ = [
    "PyCompileError",
    "PycInvalidationMode",
    "compile_file",
    "py_compile_file",
    "get_invalidation_mode",
    "parse_invalidation_mode",
    "is_pyc_file",
    "main",
]

# Re-export exception and enum
PyCompileError = py_compile.PyCompileError
PycInvalidationMode = py_compile.PycInvalidationMode

PathLikeOrStr = Union[str, Path]


def parse_invalidation_mode(value: Union[str, PycInvalidationMode, None]) -> PycInvalidationMode:
    """Parse an invalidation mode from a string, enum, or None."""
    if value is None:
        return PycInvalidationMode.TIMESTAMP
    if isinstance(value, PycInvalidationMode):
        return value
    if not isinstance(value, str):
        raise TypeError(
            f"invalidation_mode must be a str, PycInvalidationMode, or None, "
            f"got {type(value).__name__}"
        )
    try:
        return PycInvalidationMode[value.strip().upper()]
    except KeyError as exc:
        valid = ", ".join(m.name for m in PycInvalidationMode)
        raise ValueError(
            f"unknown invalidation_mode {value!r}; valid modes are: {valid}"
        ) from exc


def get_invalidation_mode(
    mode: Union[str, PycInvalidationMode, None] = None,
) -> PycInvalidationMode:
    """Return the invalidation mode, defaulting to the interpreter's choice."""
    if mode is None:
        return py_compile._get_default_invalidation_mode()
    return parse_invalidation_mode(mode)


def compile_file(
    file: Union[str, Path],
    cfile: Optional[Union[str, Path]] = None,
    dfile: Optional[Union[str, Path]] = None,
    doraise: bool = False,
    optimize: int = -1,
    invalidation_mode: Union[str, PycInvalidationMode, None] = None,
    quiet: int = 0,
) -> Path:
    """Byte-compile one Python source file to Python bytecode.

    Returns the path to the resulting ``.pyc`` file. Raises ``TypeError`` or
    ``ValueError`` on invalid arguments instead of letting the standard
    library raise its own errors.
    """
    if not isinstance(file, (str, Path)):
        raise TypeError(f"file must be a str or Path, got {type(file).__name__}")
    if not isinstance(doraise, bool):
        raise TypeError(f"doraise must be a bool, got {type(doraise).__name__}")
    if not isinstance(optimize, int) or isinstance(optimize, bool):
        raise TypeError(f"optimize must be an int, got {type(optimize).__name__}")
    if optimize not in (-1, 0, 1, 2):
        raise ValueError(f"optimize must be one of -1, 0, 1, 2, got {optimize}")
    if not isinstance(quiet, int) or isinstance(quiet, bool):
        raise TypeError(f"quiet must be an int, got {type(quiet).__name__}")
    if quiet not in (0, 1, 2):
        raise ValueError(f"quiet must be one of 0, 1, 2, got {quiet}")
    if cfile is not None and not isinstance(cfile, (str, Path)):
        raise TypeError(f"cfile must be a str, Path, or None, got {type(cfile).__name__}")
    if dfile is not None and not isinstance(dfile, (str, Path)):
        raise TypeError(f"dfile must be a str, Path, or None, got {type(dfile).__name__}")

    mode = get_invalidation_mode(invalidation_mode)
    compiled = py_compile.compile(
        file=str(file),
        cfile=str(cfile) if cfile is not None else None,
        dfile=str(dfile) if dfile is not None else None,
        doraise=doraise,
        optimize=optimize,
        invalidation_mode=mode,
        quiet=quiet,
    )
    return Path(compiled)


# Aliases for convenience
py_compile_file = compile_file


def is_pyc_file(path: Union[str, Path]) -> bool:
    """Check whether a path looks like a compiled bytecode file (``.pyc``)."""
    if not isinstance(path, (str, Path)):
        return False
    name = os.path.basename(str(path))
    if not name.endswith(".pyc"):
        return False
    # PEP 3147 bytecode files embed the source name as ``<name>.<tag>.pyc``.
    stem = name[:-4]
    return stem != "" and not stem.endswith(".py")


def main(argv: Optional[list[str]] = None) -> int:
    """Run the ``py_compile`` command-line interface and return its exit code."""
    return py_compile.main(argv)
