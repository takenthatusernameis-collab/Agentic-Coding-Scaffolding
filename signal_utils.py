"""Signal utilities (wrapping :mod:`signal`).

This module provides helpers for working with POSIX signals using the
standard library :mod:`signal` module. All functions validate inputs and
raise :class:`TypeError` or :class:`ValueError` for invalid arguments where
applicable.
"""

from __future__ import annotations

import signal
from typing import Any, Callable, Dict, List

__all__: list[str] = [
    "alarm",
    "get_handler",
    "get_signal_name",
    "interrupt_handler",
    "is_valid_signal",
    "pause",
    "register_handler",
    "register_int_handler",
    "register_term_handler",
    "set_handler",
    "signal_info",
    "signal_names",
    "suspend_handler",
    "unregister_handler",
]


def is_valid_signal(sig: Any) -> bool:
    """Return True if ``sig`` is a valid signal number on this platform."""
    if not isinstance(sig, int):
        return False
    try:
        signal.Signals(sig)
    except ValueError:
        return False
    return True


def get_signal_name(sig: int) -> str:
    """Return the name of the signal identified by ``sig``.

    Args:
        sig: Signal number.

    Returns:
        Signal name (e.g., ``"SIGINT"``).

    Raises:
        TypeError: If ``sig`` is not an int.
        ValueError: If ``sig`` is not a valid signal number.
    """
    if not isinstance(sig, int):
        raise TypeError("sig must be an int")
    try:
        return signal.Signals(sig).name
    except ValueError as exc:
        raise ValueError(f"invalid signal number: {sig!r}") from exc


def signal_names() -> List[str]:
    """Return a sorted list of all signal names available on this platform."""
    return sorted(s.name for s in signal.Signals)


def get_handler(sig: int) -> Any:
    """Return the current handler for ``sig``.

    Args:
        sig: Signal number.

    Returns:
        The current handler (callable, ``signal.SIG_DFL``, or
        ``signal.SIG_IGN``).

    Raises:
        TypeError: If ``sig`` is not an int.
        ValueError: If ``sig`` is not a valid signal number.
    """
    if not isinstance(sig, int):
        raise TypeError("sig must be an int")
    if not is_valid_signal(sig):
        raise ValueError(f"invalid signal number: {sig!r}")
    return signal.getsignal(sig)


def set_handler(sig: int, handler: Any) -> None:
    """Set the handler for ``sig``.

    Args:
        sig: Signal number.
        handler: A callable, ``signal.SIG_DFL``, or ``signal.SIG_IGN``.

    Raises:
        TypeError: If ``sig`` is not an int.
        ValueError: If ``sig`` is not a valid signal number.
    """
    if not isinstance(sig, int):
        raise TypeError("sig must be an int")
    if not is_valid_signal(sig):
        raise ValueError(f"invalid signal number: {sig!r}")
    signal.signal(sig, handler)


def register_handler(sig: int, handler: Callable[[int, Any], Any]) -> None:
    """Register a callable ``handler`` for ``sig``.

    Args:
        sig: Signal number.
        handler: Callable invoked with (signum, frame) when the signal fires.

    Raises:
        TypeError: If ``sig`` is not an int or ``handler`` is not callable.
        ValueError: If ``sig`` is not a valid signal number.
    """
    if not isinstance(sig, int):
        raise TypeError("sig must be an int")
    if not callable(handler):
        raise TypeError("handler must be callable")
    if not is_valid_signal(sig):
        raise ValueError(f"invalid signal number: {sig!r}")
    signal.signal(sig, handler)


def register_int_handler(handler: Callable[[int, Any], Any]) -> None:
    """Register ``handler`` for ``SIGINT`` (KeyboardInterrupt).

    Raises:
        TypeError: If ``handler`` is not callable.
    """
    if not callable(handler):
        raise TypeError("handler must be callable")
    signal.signal(signal.SIGINT, handler)


def register_term_handler(handler: Callable[[int, Any], Any]) -> None:
    """Register ``handler`` for ``SIGTERM``.

    Raises:
        TypeError: If ``handler`` is not callable.
    """
    if not callable(handler):
        raise TypeError("handler must be callable")
    signal.signal(signal.SIGTERM, handler)


def interrupt_handler(signum: int, frame: Any) -> None:
    """Default ``SIGINT`` handler that raises :class:`KeyboardInterrupt`."""
    raise KeyboardInterrupt


def suspend_handler(signum: int, frame: Any) -> None:
    """No-op signal handler used to suppress or ignore a signal."""
    return None


def unregister_handler(sig: int) -> None:
    """Reset the handler for ``sig`` to its default (``SIG_DFL``).

    Args:
        sig: Signal number.

    Raises:
        TypeError: If ``sig`` is not an int.
        ValueError: If ``sig`` is not a valid signal number.
    """
    if not isinstance(sig, int):
        raise TypeError("sig must be an int")
    if not is_valid_signal(sig):
        raise ValueError(f"invalid signal number: {sig!r}")
    signal.signal(sig, signal.SIG_DFL)


def alarm(seconds: int) -> int:
    """Schedule a ``SIGALRM`` to be delivered after ``seconds`` seconds.

    Args:
        seconds: Number of seconds before the signal is delivered.

    Returns:
        The number of seconds remaining on any previously scheduled alarm.

    Raises:
        TypeError: If ``seconds`` is not an int.
        ValueError: If ``seconds`` is negative.
    """
    if not isinstance(seconds, int):
        raise TypeError("seconds must be an int")
    if seconds < 0:
        raise ValueError("seconds must be non-negative")
    return signal.alarm(seconds)


def pause() -> None:
    """Wait for the next signal to be delivered."""
    signal.pause()


def signal_info() -> Dict[str, Any]:
    """Return a dictionary with signal-related information.

    Returns:
        Dictionary with signal names, the SIGINT handler, and whether
        SIGALRM is available.
    """
    return {
        "names": signal_names(),
        "sigint_handler": signal.getsignal(signal.SIGINT),
        "alarm_available": hasattr(signal, "alarm"),
    }
