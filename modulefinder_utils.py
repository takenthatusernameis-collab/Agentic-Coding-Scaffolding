"""Dependency analysis utilities wrapping the standard library :mod:`modulefinder`.

The :mod:`modulefinder` module answers the question "which modules does this
script need?" by *statically* analysing the byte code of a script and of every
module it imports.  Nothing is imported and nothing is executed, so the
analysis is safe for untrusted sources and never triggers import side effects.

This wrapper exposes validated helpers that answer the question in the shapes
callers usually need: the sorted list of dependency names, the file each
dependency was found in, the modules that could not be located, the importers
of those missing modules, and the textual report of the standard library.

.. note::

   The analysis is purely static.  A script that would raise, block, or open a
   network connection at import time is scanned just like any other script,
   because the byte code is never run.

The standard library reports a missing import either as *certainly* missing or
as *maybe* missing: a name imported with ``from package import *`` may be an
attribute of the package rather than a submodule.  The helpers here follow the
same distinction and expose both views.
"""

from __future__ import annotations

import io
import modulefinder
import os
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union

__all__ = [
    "Module",
    "ModuleFinder",
    "find_dependencies",
    "find_modules",
    "is_package",
    "load_script",
    "missing_importers",
    "missing_modules",
    "module_path",
    "report",
]

#: The standard library module description re-exported for convenience.
Module = modulefinder.Module

#: The standard library module finder re-exported for convenience.
ModuleFinder = modulefinder.ModuleFinder

PathLike = Union[str, "os.PathLike[str]"]

#: The name the standard library gives to the analysed script itself.
MAIN_MODULE_NAME = "__main__"


def _require_script(script: PathLike) -> Path:
    """Return *script* as an existing :class:`~pathlib.Path`.

    Args:
        script: The path of the script to analyse.

    Returns:
        The resolved path of the script.

    Raises:
        TypeError: If *script* is not a string or an ``os.PathLike``.
        FileNotFoundError: If *script* does not point at an existing file.
    """
    if isinstance(script, str):
        path = Path(script)
    elif isinstance(script, os.PathLike):
        path = Path(os.fspath(script))
    else:
        raise TypeError(f"script must be a str or os.PathLike, got {type(script).__name__}")
    if not path.is_file():
        raise FileNotFoundError(f"script not found: {path}")
    return path


def _require_search_path(path: Optional[Iterable[PathLike]]) -> Optional[List[str]]:
    """Return *path* as a list of directory strings.

    Args:
        path: The directories the analysis searches, or ``None``.

    Returns:
        The search path as a list of strings, or ``None`` when no path was given.

    Raises:
        TypeError: If *path* is a string or contains a non-path entry.
    """
    if path is None:
        return None
    if isinstance(path, (str, bytes, os.PathLike)):
        raise TypeError("path must be a sequence of directories, not a single path")
    try:
        entries = list(path)
    except TypeError as exc:
        raise TypeError(
            f"path must be an iterable of directories, got {type(path).__name__}"
        ) from exc
    search_path: List[str] = []
    for entry in entries:
        if isinstance(entry, str):
            search_path.append(entry)
        elif isinstance(entry, os.PathLike):
            search_path.append(os.fspath(entry))
        else:
            raise TypeError(
                f"path entries must be str or os.PathLike, got {type(entry).__name__}"
            )
    return search_path


def _require_excludes(excludes: Optional[Iterable[str]]) -> Optional[List[str]]:
    """Return *excludes* as a list of module names.

    Args:
        excludes: The module names the analysis must ignore, or ``None``.

    Returns:
        The excluded module names, or ``None`` when nothing was excluded.

    Raises:
        TypeError: If *excludes* is a string or contains a non-string entry.
    """
    if excludes is None:
        return None
    if isinstance(excludes, (str, bytes)):
        raise TypeError("excludes must be a sequence of module names, not a single name")
    try:
        names = list(excludes)
    except TypeError as exc:
        raise TypeError(
            f"excludes must be an iterable of module names, got {type(excludes).__name__}"
        ) from exc
    for name in names:
        if not isinstance(name, str):
            raise TypeError(f"excludes entries must be str, got {type(name).__name__}")
    return names


def _require_module_name(name: str) -> str:
    """Return *name* as a module name.

    Args:
        name: The name of the module to look up.

    Returns:
        The validated module name.

    Raises:
        TypeError: If *name* is not a string.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    return name


def load_script(
    script: PathLike,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> ModuleFinder:
    """Analyse *script* and return the module finder that holds the result.

    The script is scanned, never executed.  When no *path* is given, the
    directory of the script is searched first, followed by :data:`sys.path`.

    Args:
        script: The path of the script to analyse.
        path: The directories the analysis searches.  Defaults to the script
            directory followed by :data:`sys.path`.
        excludes: The module names the analysis must ignore.

    Returns:
        A :class:`modulefinder.ModuleFinder` whose ``modules`` mapping holds
        every module that was found and whose ``badmodules`` mapping holds the
        imports that could not be resolved.

    Raises:
        TypeError: If an argument has the wrong type.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    script_path = _require_script(script)
    search_path = _require_search_path(path)
    excluded = _require_excludes(excludes)
    if search_path is None:
        search_path = [str(script_path.parent), *sys.path]
    finder = ModuleFinder(path=search_path, debug=0, excludes=excluded or [])
    finder.run_script(str(script_path))
    return finder


def find_dependencies(
    script: PathLike,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> List[str]:
    """Return the sorted names of every module *script* depends on.

    The script itself is registered as ``__main__`` by the standard library and
    is therefore not part of the result.

    Args:
        script: The path of the script to analyse.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        The sorted names of the modules the script imports.

    Raises:
        TypeError: If an argument has the wrong type.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    finder = load_script(script, path, excludes)
    return sorted(name for name in finder.modules if name != MAIN_MODULE_NAME)


def find_modules(
    script: PathLike,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> Dict[str, Optional[str]]:
    """Return every module *script* depends on together with its file.

    Args:
        script: The path of the script to analyse.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        A mapping of module name to the file the module was found in.  Built-in
        modules have no file and map to ``None``.

    Raises:
        TypeError: If an argument has the wrong type.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    finder = load_script(script, path, excludes)
    return {
        name: getattr(module, "__file__", None)
        for name, module in finder.modules.items()
    }


def missing_modules(
    script: PathLike,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> List[str]:
    """Return the names of the modules *script* imports that were not found.

    The result merges the modules that are certainly missing with the modules
    that may be missing, exactly like the standard library does.

    Args:
        script: The path of the script to analyse.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        The sorted names of the unresolved imports.

    Raises:
        TypeError: If an argument has the wrong type.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    finder = load_script(script, path, excludes)
    return sorted(finder.any_missing())


def missing_importers(
    script: PathLike,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> Dict[str, List[str]]:
    """Return the unresolved imports of *script* together with their importers.

    Args:
        script: The path of the script to analyse.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        A mapping of the unresolved module name to the sorted names of the
        modules that import it.

    Raises:
        TypeError: If an argument has the wrong type.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    finder = load_script(script, path, excludes)
    return {
        name: sorted(importers)
        for name, importers in finder.badmodules.items()
    }


def module_path(
    script: PathLike,
    name: str,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> Optional[str]:
    """Return the file the module *name* was found in.

    Args:
        script: The path of the script to analyse.
        name: The name of the module to look up.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        The path of the module, or ``None`` for built-in modules.

    Raises:
        TypeError: If an argument has the wrong type.
        KeyError: If *name* is not a dependency of *script*.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    module_name = _require_module_name(name)
    finder = load_script(script, path, excludes)
    module = finder.modules.get(module_name)
    if module is None:
        raise KeyError(f"module not found in the dependencies of {script}: {module_name}")
    return getattr(module, "__file__", None)


def is_package(
    script: PathLike,
    name: str,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> bool:
    """Return ``True`` when *name* is a package *script* depends on.

    Args:
        script: The path of the script to analyse.
        name: The name of the module to look up.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        ``True`` when the module is a package, ``False`` otherwise.

    Raises:
        TypeError: If an argument has the wrong type.
        KeyError: If *name* is not a dependency of *script*.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    module_name = _require_module_name(name)
    finder = load_script(script, path, excludes)
    module = finder.modules.get(module_name)
    if module is None:
        raise KeyError(f"module not found in the dependencies of {script}: {module_name}")
    return bool(getattr(module, "__path__", None))


def report(
    script: PathLike,
    path: Optional[Iterable[PathLike]] = None,
    excludes: Optional[Iterable[str]] = None,
) -> str:
    """Return the dependency report of *script* as text.

    The standard library prints the report to standard output; this helper
    captures it and returns it instead, so the caller decides where the report
    goes.

    Args:
        script: The path of the script to analyse.
        path: The directories the analysis searches.
        excludes: The module names the analysis must ignore.

    Returns:
        The textual report listing every module that was found and every
        import that could not be resolved.

    Raises:
        TypeError: If an argument has the wrong type.
        FileNotFoundError: If *script* does not point at an existing file.
        SyntaxError: If *script* is not valid Python source.
    """
    finder = load_script(script, path, excludes)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        finder.report()
    return buffer.getvalue()
