"""Fault handler utilities wrapping the standard library :mod:`faulthandler` module.

The :mod:`faulthandler` module makes the interpreter dump the traceback of the
running threads when the process dies from a fatal signal, when a watchdog
timer fires, or when the program asks for it explicitly.  A program turns the
handler on with :func:`faulthandler.enable`, arms a watchdog with
:func:`faulthandler.dump_traceback_later`, and hooks a user signal with
:func:`faulthandler.register`.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear ``TypeError`` or ``ValueError`` instead of an opaque
failure from the C layer, and it exposes a small, stable set of helpers that
behave the same way on every platform.

.. note::

   The :mod:`faulthandler` module is part of the standard library on every
   platform, but it can be missing from a stripped-down interpreter.  The
   import below degrades gracefully: when the interpreter does not ship the
   module, the helpers raise a :class:`RuntimeError` that names the missing
   module, while :func:`is_available` keeps working.

The helpers never enable the fault handler behind the caller's back.  The
handler is only installed when :func:`enable` is called, and a scheduled dump
is only armed when :func:`dump_traceback_later` is called.
"""

from __future__ import annotations

from typing import Any

__all__: list[str] = [
    "cancel_dump_traceback_later",
    "disable",
    "dump_traceback",
    "dump_traceback_later",
    "enable",
    "is_available",
    "is_enabled",
    "register",
    "unregister",
]

try:
    import faulthandler as _faulthandler
except ImportError:  # pragma: no cover - the module is built into CPython
    _faulthandler = None  # type: ignore[assignment]


def _faulthandler_module() -> Any:
    """Return the standard library ``faulthandler`` module.

    Returns:
        The imported :mod:`faulthandler` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``faulthandler`` module.
    """
    if _faulthandler is None:  # pragma: no cover - the module is built into CPython
        raise RuntimeError(
            "the standard library 'faulthandler' module is not available on this interpreter"
        )
    return _faulthandler


def _validate_file(file: Any) -> None:
    """Validate the *file* argument shared by the fault handler helpers.

    The standard library accepts ``None``, an open file descriptor, or a
    file object with a usable file descriptor.

    Args:
        file: The file the traceback is written to, or ``None`` for the
            standard error stream.

    Raises:
        TypeError: If *file* is neither ``None``, a file descriptor, nor a
            writable file object.
        ValueError: If *file* is a negative file descriptor.
    """
    if file is None:
        return
    if isinstance(file, int) and not isinstance(file, bool):
        if file < 0:
            raise ValueError("file must be a valid file descriptor")
        return
    if not hasattr(file, "write") or not callable(file.write):
        raise TypeError(
            f"file must be a writable file object or None, got {type(file).__name__}"
        )
    fileno = getattr(file, "fileno", None)
    if fileno is None:
        return
    try:
        descriptor = fileno()
    except (OSError, ValueError) as error:
        raise TypeError(
            f"file must have a usable file descriptor, got {type(file).__name__}"
        ) from error
    if not isinstance(descriptor, int) or descriptor < 0:
        raise TypeError(f"file must have a usable file descriptor, got {type(file).__name__}")


def _validate_flag(name: str, value: Any) -> None:
    """Validate that the boolean flag *name* really is a boolean.

    Args:
        name: The name of the flag, used in the error message.
        value: The value to validate.

    Raises:
        TypeError: If *value* is not a boolean.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")


def _validate_signum(signum: Any) -> None:
    """Validate the signal number *signum*.

    Args:
        signum: The signal number to validate.

    Raises:
        TypeError: If *signum* is not an integer.
    """
    if not isinstance(signum, int) or isinstance(signum, bool):
        raise TypeError(f"signum must be an int, got {type(signum).__name__}")


def enable(file: Any = None, all_threads: bool = True) -> None:
    """Enable the fault handler.

    Args:
        file: The file the traceback is written to.  ``None`` selects the
            standard error stream.
        all_threads: When true the traceback of every running thread is
            dumped, otherwise only the thread that faulted is.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    _validate_file(file)
    _validate_flag("all_threads", all_threads)
    _faulthandler_module().enable(file=file, all_threads=all_threads)


def disable() -> None:
    """Disable the fault handler.

    The signal handlers installed by :func:`enable` and :func:`register` are
    removed and the default handlers are restored.
    """
    _faulthandler_module().disable()


def is_enabled() -> bool:
    """Report whether the fault handler is enabled.

    Returns:
        True when the fault handler is installed, False otherwise.
    """
    return bool(_faulthandler_module().is_enabled())


def dump_traceback(file: Any = None, all_threads: bool = True) -> None:
    """Dump the traceback of the running threads.

    Args:
        file: The file the traceback is written to.  ``None`` selects the
            standard error stream.
        all_threads: When true the traceback of every running thread is
            dumped, otherwise only the traceback of the calling thread is.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    _validate_file(file)
    _validate_flag("all_threads", all_threads)
    _faulthandler_module().dump_traceback(file=file, all_threads=all_threads)


def dump_traceback_later(
    timeout: float,
    repeat: bool = False,
    file: Any = None,
    exit: bool = False,
) -> None:
    """Arm a watchdog that dumps the traceback after *timeout* seconds.

    Args:
        timeout: The number of seconds to wait before the traceback is dumped.
        repeat: When true the traceback is dumped every *timeout* seconds
            instead of only once.
        file: The file the traceback is written to.  ``None`` selects the
            standard error stream.
        exit: When true the process is killed after the traceback is dumped.
            Terminating a process is not safe, so this is off by default.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *timeout* is negative.
    """
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if timeout < 0:
        raise ValueError("timeout must be non-negative")
    _validate_flag("repeat", repeat)
    _validate_file(file)
    _validate_flag("exit", exit)
    _faulthandler_module().dump_traceback_later(timeout, repeat=repeat, file=file, exit=exit)


def cancel_dump_traceback_later() -> None:
    """Cancel the watchdog armed by :func:`dump_traceback_later`."""
    _faulthandler_module().cancel_dump_traceback_later()


def register(
    signum: int,
    file: Any = None,
    all_threads: bool = True,
    chain: bool = False,
) -> Any:
    """Register a signal handler that dumps the traceback.

    Args:
        signum: The signal to hook.
        file: The file the traceback is written to.  ``None`` selects the
            standard error stream.
        all_threads: When true the traceback of every running thread is
            dumped, otherwise only the thread that received the signal is.
        chain: When true the previously installed handler still runs after
            the traceback is dumped.

    Returns:
        The previously installed signal handler, or ``None`` when there was
        none.

    Raises:
        TypeError: If an argument has the wrong type.
    """
    _validate_signum(signum)
    _validate_file(file)
    _validate_flag("all_threads", all_threads)
    _validate_flag("chain", chain)
    return _faulthandler_module().register(signum, file=file, all_threads=all_threads, chain=chain)


def unregister(signum: int) -> None:
    """Unregister the signal handler installed for *signum*.

    Args:
        signum: The signal whose handler is removed.

    Raises:
        TypeError: If *signum* is not an integer.
    """
    _validate_signum(signum)
    _faulthandler_module().unregister(signum)


def is_available() -> bool:
    """Report whether the interpreter ships the :mod:`faulthandler` module.

    Returns:
        True when the standard library module is importable, False otherwise.
    """
    return _faulthandler is not None
