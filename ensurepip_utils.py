"""Bootstrap utilities wrapping the standard library :mod:`ensurepip` package.

The :mod:`ensurepip` package carries the wheel of :command:`pip` that the
interpreter was built with, and it installs that wheel into an environment
without reaching the network.  The standard library offers two entry points:
:func:`ensurepip.bootstrap` installs the wheel into the running environment,
and :func:`ensurepip.version` reports the version of the bundled
:command:`pip`.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure.  It adds the helpers the standard library leaves to the caller:
the wheel the interpreter carries is located, the installation returns a record
of what was installed, the presence of :command:`pip` is reported without
importing it, and the command line interface of the standard library returns
its exit code instead of terminating the interpreter.

.. note::

   The :mod:`ensurepip` package is part of the standard library of every
   CPython interpreter, but a distribution can remove it.  The import below
   degrades gracefully: when the interpreter does not ship the package, the
   helpers raise a :class:`RuntimeError` that names the missing package, while
   :func:`is_available` keeps working.

The helpers never install anything on their own: the wheel is only installed
when :func:`bootstrap` or :func:`run_cli` is called.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
from typing import Any, List, NamedTuple, Optional, Sequence

try:
    import ensurepip as _ensurepip
except ImportError:  # pragma: no cover - a distribution can remove the package
    _ensurepip = None  # type: ignore[assignment]

__all__: List[str] = [
    "BootstrapResult",
    "bootstrap",
    "bundled_wheel",
    "is_available",
    "is_pip_installed",
    "pip_version",
    "run_cli",
]


class BootstrapResult(NamedTuple):
    """Record of an installation of the bundled :command:`pip`.

    The standard library returns nothing from an installation, so the wrapper
    returns a record of what was installed.

    Attributes:
        pip_version: The version of the :command:`pip` that was installed.
        root: The root directory the installation was made in, or ``None``
            when the running environment was used.
        upgrade: Whether an installed :command:`pip` was upgraded.
        user: Whether the installation used the user scheme.
        altinstall: Whether only the versioned scripts were installed.
        default_pip: Whether the unqualified :command:`pip` was installed as
            well.
        verbosity: The verbosity of the installation.
    """

    pip_version: str
    root: Optional[str]
    upgrade: bool
    user: bool
    altinstall: bool
    default_pip: bool
    verbosity: int


def _ensurepip_module() -> Any:
    """Return the standard library ``ensurepip`` module.

    Returns:
        The imported :mod:`ensurepip` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``ensurepip``
            package.
    """
    if _ensurepip is None:  # pragma: no cover - a distribution can remove it
        raise RuntimeError(
            "the standard library 'ensurepip' package is not available on this interpreter"
        )
    return _ensurepip


def _require_bool(value: Any, name: str) -> bool:
    """Return *value* as a boolean, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a boolean.

    Raises:
        TypeError: If *value* is not a boolean.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_root(value: Any) -> Optional[str]:
    """Return *value* as the root directory of an installation.

    Args:
        value: The value to check.

    Returns:
        The root directory as text, or ``None`` when the running environment
        is used.

    Raises:
        TypeError: If *value* is neither ``None`` nor a path.
        ValueError: If *value* is an empty path.
    """
    if value is None:
        return None
    if not isinstance(value, (str, os.PathLike)):
        raise TypeError(f"root must be a path or None, got {type(value).__name__}")
    text = os.fspath(value)
    if not text:
        raise ValueError("root must not be empty")
    return text


def _require_verbosity(value: Any) -> int:
    """Return *value* as a verbosity, raising an error for other values.

    Args:
        value: The value to check.

    Returns:
        The verbosity.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"verbosity must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"verbosity must be non-negative, got {value}")
    return value


def is_available() -> bool:
    """Report whether the interpreter ships the :mod:`ensurepip` package.

    Returns:
        True when the standard library package is importable, False otherwise.
    """
    return _ensurepip is not None


def pip_version() -> str:
    """Return the version of the :command:`pip` the interpreter carries.

    Older versions of the standard library report the version as a tuple of
    numbers, so the wrapper always reports it as text.

    Returns:
        The version of the bundled :command:`pip`, for example ``"24.0"``.

    Raises:
        RuntimeError: If the interpreter does not ship the ``ensurepip``
            package.
    """
    version = _ensurepip_module().version()
    if isinstance(version, tuple):
        return ".".join(str(part) for part in version)
    return str(version)


def bundled_wheel() -> Optional[str]:
    """Return the wheel of :command:`pip` the interpreter carries.

    The standard library offers no public accessor for the wheel, so the
    directory the interpreter keeps it in is looked up instead.  ``None`` is
    returned when no wheel is found, which happens on an interpreter that
    installs :command:`pip` from another source.

    Returns:
        The path of the wheel of :command:`pip`, or ``None`` when there is
        none.

    Raises:
        RuntimeError: If the interpreter does not ship the ``ensurepip``
            package.
    """
    module = _ensurepip_module()
    directory = getattr(module, "_WHEEL_PKG_DIR", None)
    if directory:
        for path in sorted(Path(directory).glob("pip-*.whl")):
            return str(path)
    package = getattr(module, "__file__", None)
    if package:
        for path in sorted(Path(package).parent.glob("_bundled/pip-*.whl")):
            return str(path)
    return None


def is_pip_installed() -> bool:
    """Report whether the running interpreter can import :command:`pip`.

    The check looks the module up without importing it, so it stays cheap and
    has no side effect.

    Returns:
        True when the interpreter can import :command:`pip`, False otherwise.
    """
    try:
        return importlib.util.find_spec("pip") is not None
    except (ImportError, ValueError):  # pragma: no cover - a broken installation
        return False


def bootstrap(
    root: Any = None,
    upgrade: bool = False,
    user: bool = False,
    altinstall: bool = False,
    default_pip: bool = False,
    verbosity: int = 0,
) -> BootstrapResult:
    """Install the :command:`pip` the interpreter carries.

    The installation uses the wheel the interpreter was built with, so it never
    reaches the network.

    Args:
        root: The root directory the installation is made in.  ``None``
            installs into the running environment.
        upgrade: Whether an installed :command:`pip` is upgraded.
        user: Whether the installation uses the user scheme.
        altinstall: Whether only the versioned scripts are installed.
        default_pip: Whether the unqualified :command:`pip` is installed as
            well.
        verbosity: The verbosity of the installation.

    Returns:
        A record of the installation.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If the root directory is empty or the verbosity is
            negative.
        RuntimeError: If the interpreter does not ship the ``ensurepip``
            package.
    """
    module = _ensurepip_module()
    target = _require_root(root)
    _require_bool(upgrade, "upgrade")
    _require_bool(user, "user")
    _require_bool(altinstall, "altinstall")
    _require_bool(default_pip, "default_pip")
    level = _require_verbosity(verbosity)
    module.bootstrap(
        root=target,
        upgrade=upgrade,
        user=user,
        altinstall=altinstall,
        default_pip=default_pip,
        verbosity=level,
    )
    return BootstrapResult(
        pip_version=pip_version(),
        root=target,
        upgrade=upgrade,
        user=user,
        altinstall=altinstall,
        default_pip=default_pip,
        verbosity=level,
    )


def _cli_parser() -> argparse.ArgumentParser:
    """Return the parser of the command line interface of the standard library.

    The parser accepts the options of ``python -m ensurepip``.

    Returns:
        The parser of the command line interface.
    """
    parser = argparse.ArgumentParser(prog="python -m ensurepip", description="Install pip")
    parser.add_argument(
        "--version",
        action="version",
        version=f"pip {pip_version()}",
        help="Show the version of pip that is bundled with this Python.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbosity",
        help="Give more output. Option is additive, and can be used up to 3 times.",
    )
    parser.add_argument(
        "-U",
        "--upgrade",
        action="store_true",
        default=False,
        help="Upgrade pip and dependencies, even if already installed.",
    )
    parser.add_argument(
        "--user",
        action="store_true",
        default=False,
        help="Install using the user scheme.",
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Install everything relative to this alternate root directory.",
    )
    parser.add_argument(
        "--altinstall",
        action="store_true",
        default=False,
        help="Make an alternate install, installing only the X.Y versioned scripts.",
    )
    parser.add_argument(
        "--default-pip",
        action="store_true",
        default=False,
        help="Make a default pip install, installing the unqualified pip as well.",
    )
    return parser


def run_cli(args: Optional[Sequence[str]] = None) -> int:
    """Run the command line interface of the standard library.

    The interface mirrors ``python -m ensurepip``: it accepts ``--version``,
    ``--verbose``, ``--upgrade``, ``--user``, ``--root``, ``--altinstall``, and
    ``--default-pip``.  The exit code of the run is returned instead of
    terminating the interpreter, so a program that embeds the installation can
    decide what to do next.

    Args:
        args: The arguments of the command line.  ``None`` reads the arguments
            of the running process.

    Returns:
        The exit code of the command: zero when the installation ran, two when
        the arguments could not be parsed.

    Raises:
        TypeError: If *args* is not a sequence of strings.
        RuntimeError: If the interpreter does not ship the ``ensurepip``
            package.
    """
    _ensurepip_module()
    if args is None:
        arguments: Optional[List[str]] = None
    elif isinstance(args, (str, bytes)):
        raise TypeError(f"args must be a sequence of strings, got {type(args).__name__}")
    else:
        arguments = [str(item) for item in args]
    parser = _cli_parser()
    try:
        parsed = parser.parse_args(arguments)
    except SystemExit as exit_error:
        code = exit_error.code
        if code is None:
            return 0
        return int(code)
    bootstrap(
        root=parsed.root,
        upgrade=parsed.upgrade,
        user=parsed.user,
        altinstall=parsed.altinstall,
        default_pip=parsed.default_pip,
        verbosity=parsed.verbosity,
    )
    return 0
