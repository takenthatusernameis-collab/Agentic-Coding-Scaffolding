"""System logging utilities wrapping the standard library :mod:`syslog` module.

The :mod:`syslog` module forwards messages to the system logger of a Unix-like
operating system.  A program opens the log once with :func:`syslog.openlog`,
writes messages with :func:`syslog.syslog`, restricts the severities that are
recorded with :func:`syslog.setlogmask`, and closes the log again with
:func:`syslog.closelog`.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear ``TypeError`` or ``ValueError`` instead of a message that
is silently dropped.  It also adds small helpers that turn the numeric
priorities and facilities into names and that compute the priority masks
without asking the system logger.

.. note::

   The :mod:`syslog` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers that talk to the system logger raise a :class:`RuntimeError`
   that names the missing module, while the pure helpers keep working.

The helpers never write to the system log on their own.  A message is only
sent when the caller asks for it with :func:`log_message`, and the caller
decides when the log is opened and closed.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

__all__: list[str] = [
    "LOG_ALERT",
    "LOG_AUTH",
    "LOG_AUTHPRIV",
    "LOG_CONS",
    "LOG_CRIT",
    "LOG_CRON",
    "LOG_DAEMON",
    "LOG_DEBUG",
    "LOG_EMERG",
    "LOG_ERR",
    "LOG_FTP",
    "LOG_INFO",
    "LOG_KERN",
    "LOG_LOCAL0",
    "LOG_LOCAL1",
    "LOG_LOCAL2",
    "LOG_LOCAL3",
    "LOG_LOCAL4",
    "LOG_LOCAL5",
    "LOG_LOCAL6",
    "LOG_LOCAL7",
    "LOG_LPR",
    "LOG_MAIL",
    "LOG_MASK",
    "LOG_NDELAY",
    "LOG_NEWS",
    "LOG_NOTICE",
    "LOG_NOWAIT",
    "LOG_ODELAY",
    "LOG_PERROR",
    "LOG_PID",
    "LOG_SYSLOG",
    "LOG_UPTO",
    "LOG_USER",
    "LOG_UUCP",
    "LOG_WARNING",
    "close_log",
    "facility_name",
    "facility_names",
    "is_available",
    "log_mask",
    "log_message",
    "log_upto",
    "open_log",
    "option_names",
    "priority_name",
    "priority_names",
    "set_log_mask",
]

try:
    import syslog as _syslog
except ImportError:  # pragma: no cover - the module is Unix-only
    _syslog = None  # type: ignore[assignment]


def _constant(name: str, fallback: int) -> int:
    """Return the standard library constant *name*, or *fallback*.

    The option flags and a few facilities are defined by the C library of the
    host, so the standard library values win over the POSIX defaults whenever
    the interpreter ships the :mod:`syslog` module.
    """
    if _syslog is None:
        return fallback
    value = getattr(_syslog, name, fallback)
    return value if isinstance(value, int) else fallback


def _syslog_module() -> Any:
    """Return the standard library ``syslog`` module.

    Returns:
        The imported :mod:`syslog` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``syslog`` module.
    """
    if _syslog is None:  # pragma: no cover - the module is Unix-only
        raise RuntimeError(
            "the standard library 'syslog' module is not available on this platform; "
            "it is only shipped on Unix-like systems"
        )
    return _syslog


# Severities, from the most to the least urgent.
LOG_EMERG = _constant("LOG_EMERG", 0)
LOG_ALERT = _constant("LOG_ALERT", 1)
LOG_CRIT = _constant("LOG_CRIT", 2)
LOG_ERR = _constant("LOG_ERR", 3)
LOG_WARNING = _constant("LOG_WARNING", 4)
LOG_NOTICE = _constant("LOG_NOTICE", 5)
LOG_INFO = _constant("LOG_INFO", 6)
LOG_DEBUG = _constant("LOG_DEBUG", 7)

# Facilities, the part of the priority that names the logging subsystem.
LOG_KERN = _constant("LOG_KERN", 0)
LOG_USER = _constant("LOG_USER", 8)
LOG_MAIL = _constant("LOG_MAIL", 16)
LOG_DAEMON = _constant("LOG_DAEMON", 24)
LOG_AUTH = _constant("LOG_AUTH", 32)
LOG_SYSLOG = _constant("LOG_SYSLOG", 40)
LOG_LPR = _constant("LOG_LPR", 48)
LOG_NEWS = _constant("LOG_NEWS", 56)
LOG_UUCP = _constant("LOG_UUCP", 64)
LOG_CRON = _constant("LOG_CRON", 72)
LOG_AUTHPRIV = _constant("LOG_AUTHPRIV", 80)
LOG_FTP = _constant("LOG_FTP", 88)
LOG_LOCAL0 = _constant("LOG_LOCAL0", 128)
LOG_LOCAL1 = _constant("LOG_LOCAL1", 136)
LOG_LOCAL2 = _constant("LOG_LOCAL2", 144)
LOG_LOCAL3 = _constant("LOG_LOCAL3", 152)
LOG_LOCAL4 = _constant("LOG_LOCAL4", 160)
LOG_LOCAL5 = _constant("LOG_LOCAL5", 168)
LOG_LOCAL6 = _constant("LOG_LOCAL6", 176)
LOG_LOCAL7 = _constant("LOG_LOCAL7", 184)

# Options that change how the system logger is reached.
LOG_PID = _constant("LOG_PID", 1)
LOG_CONS = _constant("LOG_CONS", 2)
LOG_ODELAY = _constant("LOG_ODELAY", 4)
LOG_NDELAY = _constant("LOG_NDELAY", 8)
LOG_NOWAIT = _constant("LOG_NOWAIT", 16)
LOG_PERROR = _constant("LOG_PERROR", 32)

_PRIORITY_NAMES: Dict[str, int] = {
    "LOG_EMERG": LOG_EMERG,
    "LOG_ALERT": LOG_ALERT,
    "LOG_CRIT": LOG_CRIT,
    "LOG_ERR": LOG_ERR,
    "LOG_WARNING": LOG_WARNING,
    "LOG_NOTICE": LOG_NOTICE,
    "LOG_INFO": LOG_INFO,
    "LOG_DEBUG": LOG_DEBUG,
}

_FACILITY_NAMES: Dict[str, int] = {
    "LOG_KERN": LOG_KERN,
    "LOG_USER": LOG_USER,
    "LOG_MAIL": LOG_MAIL,
    "LOG_DAEMON": LOG_DAEMON,
    "LOG_AUTH": LOG_AUTH,
    "LOG_SYSLOG": LOG_SYSLOG,
    "LOG_LPR": LOG_LPR,
    "LOG_NEWS": LOG_NEWS,
    "LOG_UUCP": LOG_UUCP,
    "LOG_CRON": LOG_CRON,
    "LOG_AUTHPRIV": LOG_AUTHPRIV,
    "LOG_FTP": LOG_FTP,
    "LOG_LOCAL0": LOG_LOCAL0,
    "LOG_LOCAL1": LOG_LOCAL1,
    "LOG_LOCAL2": LOG_LOCAL2,
    "LOG_LOCAL3": LOG_LOCAL3,
    "LOG_LOCAL4": LOG_LOCAL4,
    "LOG_LOCAL5": LOG_LOCAL5,
    "LOG_LOCAL6": LOG_LOCAL6,
    "LOG_LOCAL7": LOG_LOCAL7,
}

_OPTION_NAMES: Dict[str, int] = {
    "LOG_PID": LOG_PID,
    "LOG_CONS": LOG_CONS,
    "LOG_ODELAY": LOG_ODELAY,
    "LOG_NDELAY": LOG_NDELAY,
    "LOG_NOWAIT": LOG_NOWAIT,
    "LOG_PERROR": LOG_PERROR,
}


def _require_priority(priority: Any) -> int:
    """Return *priority* when it names one of the eight severities."""
    if isinstance(priority, bool) or not isinstance(priority, int):
        raise TypeError(f"priority must be an int, got {type(priority).__name__}")
    if not LOG_EMERG <= priority <= LOG_DEBUG:
        raise ValueError(f"priority must be between {LOG_EMERG} and {LOG_DEBUG}, got {priority}")
    return priority


def _require_facility(facility: Any) -> int:
    """Return *facility* when it names one of the known facilities."""
    if isinstance(facility, bool) or not isinstance(facility, int):
        raise TypeError(f"facility must be an int, got {type(facility).__name__}")
    if facility not in _FACILITY_NAMES.values():
        raise ValueError(f"unknown facility: {facility}")
    return facility


def _require_option(logoption: Any) -> int:
    """Return *logoption* when it only combines the known option flags."""
    if isinstance(logoption, bool) or not isinstance(logoption, int):
        raise TypeError(f"logoption must be an int, got {type(logoption).__name__}")
    if logoption < 0:
        raise ValueError(f"logoption must not be negative, got {logoption}")
    known = 0
    for value in _OPTION_NAMES.values():
        known |= value
    if logoption & ~known:
        raise ValueError(f"unknown logoption flags: {logoption}")
    return logoption


def is_available() -> bool:
    """Return ``True`` when the interpreter ships the standard library module."""
    return _syslog is not None


def open_log(
    ident: Optional[str] = None,
    logoption: int = 0,
    facility: int = LOG_USER,
) -> None:
    """Open the system log for the program.

    Args:
        ident: The identification tag prepended to every message.  When
            omitted, the standard library uses the name of the running
            program.
        logoption: A combination of the option flags, such as :data:`LOG_PID`
            or :data:`LOG_PERROR`.
        facility: The facility the messages are recorded under, such as
            :data:`LOG_USER` or :data:`LOG_LOCAL0`.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an argument has an unusable value.
        RuntimeError: If the interpreter does not ship the ``syslog`` module.
    """
    if ident is not None and not isinstance(ident, str):
        raise TypeError(f"ident must be a str or None, got {type(ident).__name__}")
    if ident is not None and not ident:
        raise ValueError("ident must not be empty")
    _require_option(logoption)
    _require_facility(facility)
    _syslog_module().openlog(ident, logoption, facility)


def log_message(message: str, priority: int = LOG_INFO) -> None:
    """Send *message* to the system logger.

    Args:
        message: The text of the message.
        priority: The severity of the message, such as :data:`LOG_INFO`.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If an argument has an unusable value.
        RuntimeError: If the interpreter does not ship the ``syslog`` module.
    """
    if not isinstance(message, str):
        raise TypeError(f"message must be a str, got {type(message).__name__}")
    if not message:
        raise ValueError("message must not be empty")
    _require_priority(priority)
    module = _syslog_module()
    try:
        module.syslog(priority, message)
    except TypeError:
        # Interpreters that take the message first are supported as well.
        module.syslog(message, priority)


def close_log() -> None:
    """Close the system log.

    Raises:
        RuntimeError: If the interpreter does not ship the ``syslog`` module.
    """
    _syslog_module().closelog()


def set_log_mask(mask: int) -> int:
    """Restrict the severities that are recorded.

    Args:
        mask: A combination of the priority masks, such as
            :func:`log_mask` or :func:`log_upto` produce.

    Returns:
        The mask that was active before the call.

    Raises:
        TypeError: If *mask* is not an int.
        ValueError: If *mask* is negative.
        RuntimeError: If the interpreter does not ship the ``syslog`` module.
    """
    if isinstance(mask, bool) or not isinstance(mask, int):
        raise TypeError(f"mask must be an int, got {type(mask).__name__}")
    if mask < 0:
        raise ValueError(f"mask must not be negative, got {mask}")
    return int(_syslog_module().setlogmask(mask))


def log_mask(priority: int) -> int:
    """Return the mask that selects a single *priority*.

    Args:
        priority: The severity, such as :data:`LOG_WARNING`.

    Returns:
        The mask of the priority.

    Raises:
        TypeError: If *priority* is not an int.
        ValueError: If *priority* does not name a severity.
    """
    level = _require_priority(priority)
    return 1 << level


def log_upto(priority: int) -> int:
    """Return the mask that selects every severity up to *priority*.

    Args:
        priority: The most verbose severity that is recorded, such as
            :data:`LOG_WARNING`.

    Returns:
        The mask of the priority and of every severity before it.

    Raises:
        TypeError: If *priority* is not an int.
        ValueError: If *priority* does not name a severity.
    """
    level = _require_priority(priority)
    return (1 << (level + 1)) - 1


def priority_name(priority: int) -> str:
    """Return the name of *priority*.

    Args:
        priority: The severity, such as :data:`LOG_INFO`.

    Returns:
        The name of the severity, such as ``"LOG_INFO"``.

    Raises:
        TypeError: If *priority* is not an int.
        ValueError: If *priority* does not name a severity.
    """
    level = _require_priority(priority)
    for name, value in _PRIORITY_NAMES.items():
        if value == level:
            return name
    raise ValueError(f"unknown priority: {priority}")


def priority_names() -> Dict[str, int]:
    """Return the severity names mapped to their values."""
    return dict(_PRIORITY_NAMES)


def facility_name(facility: int) -> str:
    """Return the name of *facility*.

    Args:
        facility: The facility, such as :data:`LOG_LOCAL0`.

    Returns:
        The name of the facility, such as ``"LOG_LOCAL0"``.

    Raises:
        TypeError: If *facility* is not an int.
        ValueError: If *facility* does not name a facility.
    """
    value = _require_facility(facility)
    for name, candidate in _FACILITY_NAMES.items():
        if candidate == value:
            return name
    raise ValueError(f"unknown facility: {facility}")


def facility_names() -> Dict[str, int]:
    """Return the facility names mapped to their values."""
    return dict(_FACILITY_NAMES)


def option_names() -> Dict[str, int]:
    """Return the option flag names mapped to their values."""
    return dict(_OPTION_NAMES)


#: Alias of :func:`log_mask`, mirroring the standard library name.
LOG_MASK = log_mask

#: Alias of :func:`log_upto`, mirroring the standard library name.
LOG_UPTO = log_upto
