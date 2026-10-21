"""Virtual environment utilities wrapping the standard library :mod:`venv` package.

The :mod:`venv` package creates a virtual environment: a directory that holds
its own copy of the interpreter, its own library directory, and a configuration
file that records where the interpreter came from.  The package also offers a
command line interface that does the same work from a terminal.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It adds the helpers the standard library leaves to the
caller: the configuration of an environment is read as a mapping, the
directories of an environment are computed without creating it, the
interpreter of an environment is located, the environments of a directory tree
are found, and the creation of an environment returns a description of the
result instead of nothing.

The helpers that create an environment write to the directory they are given
and nothing else, so a caller decides where the environment is created.  The
helpers that only read an environment never write to it.
"""

from __future__ import annotations

import os
import sys
import sysconfig
from typing import Any, Dict, List, Optional, Sequence

try:
    import venv as _venv
except ImportError:  # pragma: no cover - the package ships with the interpreter
    _venv = None  # type: ignore[assignment]

__all__: list[str] = [
    "EnvBuilder",
    "activation_scripts",
    "create_environment",
    "describe_environment",
    "environment_paths",
    "environment_python",
    "find_environments",
    "is_environment",
    "read_configuration",
    "run_cli",
]

#: The name of the configuration file of an environment.
CONFIGURATION_FILE = "pyvenv.cfg"

#: The description of a virtual environment.
Environment = Dict[str, Any]

#: The names of the interpreters of an environment, in the order they are tried.
_INTERPRETER_NAMES = ("python", "python3", "python.exe", "pythonw.exe")

#: The names of the scripts that activate an environment.
_ACTIVATION_NAMES = ("activate", "activate.bat", "activate.ps1", "Activate.ps1")


def _venv_module() -> Any:
    """Return the standard library ``venv`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``venv`` package.
    """
    if _venv is None:
        raise RuntimeError("the standard library package 'venv' is not available")
    return _venv


def _require_directory(value: object, name: str) -> str:
    """Return *value* as an absolute path of a directory.

    Args:
        value: The path of the directory.
        name: The name of the argument, used in the error message.

    Returns:
        The absolute path of the directory.

    Raises:
        TypeError: If *value* is not a path.
        ValueError: If *value* is an empty path.
    """
    if isinstance(value, (str, bytes, os.PathLike)):
        text = os.fspath(value)
        if isinstance(text, bytes):
            text = os.fsdecode(text)
    else:
        raise TypeError(f"{name} must be a path, got {type(value).__name__}")
    if not text.strip():
        raise ValueError(f"{name} must not be empty")
    return os.path.abspath(text)


def _require_bool(value: object, name: str) -> bool:
    """Return *value* when it is a boolean.

    Raises:
        TypeError: If *value* is not a boolean.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_optional_text(value: object, name: str) -> Optional[str]:
    """Return *value* when it is a string or ``None``.

    Raises:
        TypeError: If *value* is neither a string nor ``None``.
        ValueError: If *value* is a string that is empty.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")
    return value


def _require_non_negative_int(value: object, name: str) -> int:
    """Return *value* when it is an integer that is not negative.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def _require_sequence(value: object, name: str) -> List[str]:
    """Return *value* as a list of strings.

    Raises:
        TypeError: If *value* is not a sequence of strings.
    """
    if isinstance(value, (str, bytes)):
        raise TypeError(f"{name} must be a sequence of strings, not a single string")
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a list or a tuple, got {type(value).__name__}")
    entries: List[str] = []
    for entry in value:
        if not isinstance(entry, str):
            raise TypeError(f"{name} entries must be strings, got {type(entry).__name__}")
        entries.append(entry)
    return entries


def _scheme_vars(directory: str) -> Dict[str, str]:
    """Return the variables that place the paths of an installation scheme."""
    return {
        "base": directory,
        "platbase": directory,
        "installed_base": directory,
        "installed_platbase": directory,
    }


def _path_of(directory: str, name: str) -> str:
    """Return the path of the *name* directory of an environment."""
    return sysconfig.get_path(name, scheme="venv", vars=_scheme_vars(directory))


def _configuration_path(directory: str) -> str:
    """Return the path of the configuration file of an environment."""
    return os.path.join(directory, CONFIGURATION_FILE)


def _strip_quotes(value: str) -> str:
    """Return *value* without the quotes the standard library writes around it."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def is_environment(directory: object) -> bool:
    """Report whether a directory holds a virtual environment.

    Args:
        directory: The path of the directory.

    Returns:
        ``True`` when the directory holds the configuration file of an
        environment, ``False`` otherwise.
    """
    path = _require_directory(directory, "directory")
    return os.path.isfile(_configuration_path(path))


def read_configuration(directory: object) -> Dict[str, str]:
    """Return the configuration of a virtual environment.

    The configuration file of an environment records the directory of the
    interpreter the environment was built from, the version of that
    interpreter, whether the environment sees the packages of the system, the
    prompt of the environment, and the command that created it.

    Args:
        directory: The path of the environment.

    Returns:
        A mapping of the names of the settings to their values.

    Raises:
        TypeError: If *directory* is not a path.
        ValueError: If *directory* is empty or holds no environment.
    """
    path = _require_directory(directory, "directory")
    configuration = _configuration_path(path)
    if not os.path.isfile(configuration):
        raise ValueError(f"no virtual environment in {path!r}")
    settings: Dict[str, str] = {}
    with open(configuration, encoding="utf-8") as stream:
        for line in stream:
            text = line.strip()
            if not text or text.startswith("#"):
                continue
            name, separator, value = text.partition("=")
            if not separator:
                continue
            settings[name.strip()] = _strip_quotes(value.strip())
    return settings


def environment_paths(directory: object) -> Dict[str, str]:
    """Return the directories of a virtual environment.

    The directories are computed the way the standard library computes them
    when it creates an environment, so the result describes an environment
    that does not exist yet as well as one that does.

    Args:
        directory: The path of the environment.

    Returns:
        A mapping of the names of the directories to their paths.  The names
        are ``scripts``, ``include``, ``platinclude``, ``purelib``,
        ``platlib``, ``stdlib``, ``platstdlib``, and ``data``.

    Raises:
        TypeError: If *directory* is not a path.
        ValueError: If *directory* is empty.
    """
    path = _require_directory(directory, "directory")
    names = (
        "scripts",
        "include",
        "platinclude",
        "purelib",
        "platlib",
        "stdlib",
        "platstdlib",
        "data",
    )
    return {name: _path_of(path, name) for name in names}


def environment_python(directory: object) -> str:
    """Return the interpreter of a virtual environment.

    Args:
        directory: The path of the environment.

    Returns:
        The path of the interpreter of the environment.  When the environment
        holds no interpreter, the path the interpreter would have is returned.
    """
    path = _require_directory(directory, "directory")
    scripts = _path_of(path, "scripts")
    candidates = list(_INTERPRETER_NAMES)
    candidates.append(f"python{sys.version_info[0]}.{sys.version_info[1]}")
    for name in candidates:
        candidate = os.path.join(scripts, name)
        if os.path.exists(candidate):
            return candidate
    return os.path.join(scripts, "python.exe" if os.name == "nt" else "python")


def activation_scripts(directory: object) -> List[str]:
    """Return the scripts that activate a virtual environment.

    Args:
        directory: The path of the environment.

    Returns:
        The paths of the activation scripts that exist, in ascending order.
        The list is empty when the environment holds no activation script.
    """
    path = _require_directory(directory, "directory")
    scripts = _path_of(path, "scripts")
    found = [os.path.join(scripts, name) for name in _ACTIVATION_NAMES]
    return sorted(script for script in found if os.path.exists(script))


def describe_environment(directory: object) -> Environment:
    """Return a description of a virtual environment.

    Args:
        directory: The path of the environment.

    Returns:
        A mapping that holds the path of the environment, the path of its
        interpreter, its configuration, its directories, and its activation
        scripts.

    Raises:
        TypeError: If *directory* is not a path.
        ValueError: If *directory* is empty or holds no environment.
    """
    path = _require_directory(directory, "directory")
    if not is_environment(path):
        raise ValueError(f"no virtual environment in {path!r}")
    return {
        "directory": path,
        "python": environment_python(path),
        "configuration": read_configuration(path),
        "paths": environment_paths(path),
        "activation_scripts": activation_scripts(path),
    }


def create_environment(
    directory: object,
    with_pip: bool = False,
    prompt: Optional[str] = None,
    system_site_packages: bool = False,
    clear: bool = False,
    symlinks: Optional[bool] = None,
    upgrade: bool = False,
) -> Environment:
    """Create a virtual environment and describe it.

    The environment is created the way the standard library creates it when
    the command ``python -m venv`` runs, and the description of the result is
    returned, so a caller learns where the interpreter, the configuration, and
    the directories of the environment are.

    Args:
        directory: The path of the environment.  The directory is created when
            it does not exist.
        with_pip: Whether the standard library installs ``pip`` into the
            environment.  The packages are taken from the wheel the
            interpreter ships, so no network is used.
        prompt: The prefix of the prompt of the environment.  The name of the
            directory is used when no prefix is given.
        system_site_packages: Whether the environment sees the packages that
            are installed for the interpreter of the system.
        clear: Whether the content of the directory is deleted before the
            environment is created.
        symlinks: Whether the interpreter is linked instead of copied.  The
            default of the platform is used when no choice is given.
        upgrade: Whether an existing environment is upgraded instead of
            created.

    Returns:
        The description of the environment, in the same shape as the
        description of :func:`describe_environment`.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an argument has an unusable value.
        RuntimeError: If the interpreter does not ship the ``venv`` package.
    """
    module = _venv_module()
    path = _require_directory(directory, "directory")
    _require_bool(with_pip, "with_pip")
    _require_bool(system_site_packages, "system_site_packages")
    _require_bool(clear, "clear")
    _require_bool(upgrade, "upgrade")
    prompt = _require_optional_text(prompt, "prompt")
    use_symlinks = os.name != "nt" if symlinks is None else _require_bool(symlinks, "symlinks")
    builder = module.EnvBuilder(
        system_site_packages=system_site_packages,
        clear=clear,
        symlinks=use_symlinks,
        upgrade=upgrade,
        with_pip=with_pip,
        prompt=prompt,
    )
    builder.create(path)
    return describe_environment(path)


def find_environments(root: object, max_depth: int = 2) -> List[str]:
    """Return the virtual environments of a directory tree.

    Args:
        root: The path of the directory to search.
        max_depth: The number of levels of the tree that are searched.  The
            root itself is always reported when it holds an environment.

    Returns:
        The paths of the environments that were found, in ascending order.
    """
    path = _require_directory(root, "root")
    depth = _require_non_negative_int(max_depth, "max_depth")
    found: List[str] = []
    if is_environment(path):
        found.append(path)
    for current, directories, _files in os.walk(path):
        level = current[len(path) :].count(os.sep)
        if level >= depth:
            directories[:] = []
            continue
        for name in sorted(directories):
            candidate = os.path.join(current, name)
            if is_environment(candidate):
                found.append(candidate)
                directories.remove(name)
    return sorted(found)


def run_cli(args: Optional[Sequence[str]] = None) -> int:
    """Run the command line interface of the standard library.

    The interface is the one of the command ``python -m venv``: it creates an
    environment in every directory it is given.

    Args:
        args: The arguments of the command.  The arguments of the process are
            used when no argument is given.

    Returns:
        The exit code of the command.  The code is ``0`` when every
        environment was created.
    """
    module = _venv_module()
    try:
        module.main(_require_sequence(args, "args") if args is not None else None)
    except SystemExit as error:
        code = error.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        return 1
    return 0


#: The builder of the standard library, re-exported for callers that extend it.
EnvBuilder: Any = _venv.EnvBuilder if _venv is not None else None
