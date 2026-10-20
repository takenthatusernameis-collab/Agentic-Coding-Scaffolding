"""Resource usage utilities wrapping the standard library :mod:`resource` module.

The :mod:`resource` module reports how much CPU time, memory, and I/O a process
used, and it exposes the limits the operating system enforces on that process.
A program reads the usage of itself with :func:`resource.getrusage`, reads and
writes the limits of a resource with :func:`resource.getrlimit` and
:func:`resource.setrlimit`, and reads the limits of another process with
:func:`resource.prlimit`.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear ``TypeError`` or ``ValueError`` instead of an opaque
failure from the C layer.  It also adds three conveniences the standard
library does not offer:

* every limit can be named with a string such as ``"RLIMIT_NOFILE"``, so a
  program does not have to hard-code the numeric value of the host platform,
* the limits are returned in a :class:`Limit` named tuple with a ``soft`` and a
  ``hard`` field instead of a bare tuple,
* the usage record is returned in a :class:`Usage` named tuple that has the same
  fields on every platform, because the record of the standard library differs
  between the supported systems.

.. note::

   The :mod:`resource` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while the pure helpers keep working.  The same applies to
   :func:`prlimit`, which only the Linux systems provide.

The helpers never lower a limit of the running process on their own.  A limit
is only changed when the caller asks for it with :func:`set_rlimit` or
:func:`prlimit`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, NamedTuple, Optional, Sequence, Union

if TYPE_CHECKING:
    # The standard library only ships the limit constants of the host platform,
    # so the names below exist at runtime only when the platform provides them.
    RLIMIT_AS: int
    RLIMIT_CORE: int
    RLIMIT_CPU: int
    RLIMIT_DATA: int
    RLIMIT_FSIZE: int
    RLIMIT_MEMLOCK: int
    RLIMIT_MSGQUEUE: int
    RLIMIT_NICE: int
    RLIMIT_NOFILE: int
    RLIMIT_NPROC: int
    RLIMIT_OFILE: int
    RLIMIT_RSS: int
    RLIMIT_RTPRIO: int
    RLIMIT_RTTIME: int
    RLIMIT_SIGPENDING: int
    RLIMIT_STACK: int

try:
    import resource as _resource
except ImportError:  # pragma: no cover - the module is Unix-only
    _resource = None  # type: ignore[assignment]


class Limit(NamedTuple):
    """The soft and the hard limit of a resource limit.

    Attributes:
        soft: The limit the process may raise up to on its own.
        hard: The limit only a privileged process may raise.
    """

    soft: int
    hard: int


class Usage(NamedTuple):
    """The resource usage of a process.

    The standard library returns a record whose fields differ between the
    supported systems.  This named tuple always has the same fields, and a
    field the host platform does not report is zero.

    Attributes:
        user_time: The user time of the process in seconds.
        system_time: The system time of the process in seconds.
        max_rss: The maximum resident set size in kilobytes.
        minor_faults: The number of minor page faults.
        major_faults: The number of major page faults.
        swapped_out: The number of times the process was swapped out.
        blocks_in: The number of blocks the process read from the file system.
        blocks_out: The number of blocks the process wrote to the file system.
        messages_sent: The number of messages the process sent.
        messages_received: The number of messages the process received.
        signals: The number of signals the process received.
        voluntary_context_switches: The number of voluntary context switches.
        involuntary_context_switches: The number of involuntary context switches.
    """

    user_time: float
    system_time: float
    max_rss: int
    minor_faults: int
    major_faults: int
    swapped_out: int
    blocks_in: int
    blocks_out: int
    messages_sent: int
    messages_received: int
    signals: int
    voluntary_context_switches: int
    involuntary_context_switches: int


#: The names of the limit constants the standard library module may provide.
_LIMIT_NAMES: tuple[str, ...] = (
    "RLIMIT_AS",
    "RLIMIT_CORE",
    "RLIMIT_CPU",
    "RLIMIT_DATA",
    "RLIMIT_FSIZE",
    "RLIMIT_MEMLOCK",
    "RLIMIT_MSGQUEUE",
    "RLIMIT_NICE",
    "RLIMIT_NOFILE",
    "RLIMIT_NPROC",
    "RLIMIT_OFILE",
    "RLIMIT_RSS",
    "RLIMIT_RTPRIO",
    "RLIMIT_RTTIME",
    "RLIMIT_SIGPENDING",
    "RLIMIT_STACK",
)


def _constant(name: str, fallback: int) -> int:
    """Return the standard library constant *name*, or *fallback*.

    The limit constants are defined by the C library of the host, so the
    standard library values win over the POSIX defaults whenever the
    interpreter ships the :mod:`resource` module.
    """
    if _resource is None:
        return fallback
    value = getattr(_resource, name, None)
    return value if isinstance(value, int) and not isinstance(value, bool) else fallback


def _collect_limits() -> Dict[str, int]:
    """Return the limit constants the host platform provides."""
    limits: Dict[str, int] = {}
    if _resource is not None:
        for name in _LIMIT_NAMES:
            value = getattr(_resource, name, None)
            if isinstance(value, int) and not isinstance(value, bool):
                limits[name] = value
    return limits


#: The value of an unlimited resource limit.
RLIM_INFINITY: int = _constant("RLIM_INFINITY", -1)

#: The usage target that reports on the calling process.
RUSAGE_SELF: int = _constant("RUSAGE_SELF", 0)

#: The usage target that reports on the children the process has waited for.
RUSAGE_CHILDREN: int = _constant("RUSAGE_CHILDREN", -1)

#: The usage target that reports on the calling thread.
RUSAGE_THREAD: int = _constant("RUSAGE_THREAD", 1)

#: The limit constants of the host platform, keyed by their name.
_LIMITS: Dict[str, int] = _collect_limits()

globals().update(_LIMITS)

__all__: list[str] = [
    "Limit",
    "RLIM_INFINITY",
    "RUSAGE_CHILDREN",
    "RUSAGE_SELF",
    "RUSAGE_THREAD",
    "Usage",
    "get_page_size",
    "get_rlimit",
    "get_rusage",
    "is_available",
    "limit_name",
    "limit_names",
    "limit_value",
    "prlimit",
    "set_rlimit",
    "usage_as_dict",
    "usage_names",
] + sorted(_LIMITS)


def _resource_module() -> Any:
    """Return the standard library ``resource`` module.

    Returns:
        The imported :mod:`resource` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``resource`` module.
    """
    if _resource is None:  # pragma: no cover - the module is Unix-only
        raise RuntimeError(
            "the standard library 'resource' module is not available on this platform; "
            "it is only shipped on Unix-like systems"
        )
    return _resource


def is_available() -> bool:
    """Return ``True`` when the interpreter ships the standard library module."""
    return _resource is not None


def limit_names() -> Dict[str, int]:
    """Return the resource limit constants of the host platform.

    Returns:
        The ``RLIMIT_*`` constants of the platform, keyed by their name.
    """
    return dict(_LIMITS)


def usage_names() -> Dict[str, int]:
    """Return the usage constants of the host platform.

    Returns:
        The ``RUSAGE_*`` constants of the platform, keyed by their name.
    """
    return {
        "RUSAGE_CHILDREN": RUSAGE_CHILDREN,
        "RUSAGE_SELF": RUSAGE_SELF,
        "RUSAGE_THREAD": RUSAGE_THREAD,
    }


def limit_value(name: str) -> int:
    """Return the value of the resource limit called *name*.

    Args:
        name: The name of the limit, such as ``"RLIMIT_NOFILE"``.  The name may
            be written with or without the ``RLIMIT_`` prefix, and it is
            matched case-insensitively.

    Returns:
        The value of the limit.

    Raises:
        TypeError: If *name* is not a str.
        ValueError: If the host platform does not provide the limit.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    key = name.strip().upper().replace("-", "_")
    if not key.startswith("RLIMIT_"):
        key = f"RLIMIT_{key}"
    limits = limit_names()
    if key not in limits:
        available = ", ".join(sorted(limits)) or "none"
        raise ValueError(f"unknown resource limit {name!r}; available limits are: {available}")
    return limits[key]


def limit_name(limit: int) -> str:
    """Return the name of *limit*.

    Args:
        limit: The value of a resource limit.

    Returns:
        The name of the limit, such as ``"RLIMIT_NOFILE"``.

    Raises:
        TypeError: If *limit* is not an int.
        ValueError: If the host platform does not provide the limit.
    """
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError(f"limit must be an int, got {type(limit).__name__}")
    value = _require_limit(limit)
    for name, candidate in limit_names().items():
        if candidate == value:
            return name
    raise ValueError(f"unknown resource limit: {limit}")


def _require_limit(limit: Union[int, str]) -> int:
    """Return the numeric value of *limit*.

    Args:
        limit: The value of a resource limit or the name of one.

    Returns:
        The numeric value of the limit.

    Raises:
        TypeError: If *limit* is neither an int nor a str.
        ValueError: If the host platform does not provide the limit.
    """
    if isinstance(limit, str):
        return limit_value(limit)
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError(f"limit must be an int or a str, got {type(limit).__name__}")
    limits = limit_names()
    if limit not in limits.values():
        raise ValueError(f"unknown resource limit: {limit}")
    return limit


def _require_limits(limits: Sequence[int]) -> tuple[int, int]:
    """Return the soft and the hard limit of *limits*.

    Args:
        limits: A sequence with the soft limit first and the hard limit second.

    Returns:
        The soft and the hard limit.

    Raises:
        TypeError: If *limits* is not a sequence of two ints.
        ValueError: If *limits* does not hold exactly two values.
    """
    if isinstance(limits, (str, bytes)) or not isinstance(limits, (tuple, list)):
        raise TypeError(
            f"limits must be a tuple or a list of two ints, got {type(limits).__name__}"
        )
    if len(limits) != 2:
        raise ValueError(f"limits must hold exactly two values, got {len(limits)}")
    soft, hard = limits
    for name, value in (("soft", soft), ("hard", hard)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"the {name} limit must be an int, got {type(value).__name__}")
    return int(soft), int(hard)


def _check_limits(soft: int, hard: int, current: Limit) -> None:
    """Raise when the new limits cannot be applied.

    Args:
        soft: The new soft limit.
        hard: The new hard limit.
        current: The limits the process has right now.

    Raises:
        ValueError: If the soft limit exceeds the hard limit or the hard limit
            the process may not raise.
    """
    infinity = RLIM_INFINITY
    if soft != infinity and hard != infinity and soft > hard:
        raise ValueError(f"the soft limit ({soft}) must not exceed the hard limit ({hard})")
    if (
        soft != infinity
        and hard != infinity
        and current.hard != infinity
        and soft > current.hard
    ):
        raise ValueError(
            f"the soft limit ({soft}) must not exceed the hard limit "
            f"the process may raise ({current.hard})"
        )


def get_rlimit(limit: Union[int, str]) -> Limit:
    """Return the limits of *limit* for the running process.

    Args:
        limit: The value of a resource limit or the name of one, such as
            ``"RLIMIT_NOFILE"``.

    Returns:
        The soft and the hard limit of the running process.

    Raises:
        TypeError: If *limit* is neither an int nor a str.
        ValueError: If the host platform does not provide the limit.
        RuntimeError: If the interpreter does not ship the ``resource`` module.
    """
    value = _require_limit(limit)
    soft, hard = _resource_module().getrlimit(value)
    return Limit(int(soft), int(hard))


def set_rlimit(limit: Union[int, str], limits: Sequence[int]) -> None:
    """Set the limits of *limit* for the running process.

    Args:
        limit: The value of a resource limit or the name of one, such as
            ``"RLIMIT_NOFILE"``.
        limits: A sequence with the new soft limit first and the new hard
            limit second.  The value :data:`RLIM_INFINITY` means "no limit".

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If the host platform does not provide the limit, if the
            limits do not hold exactly two values, or if the new limits exceed
            the limits the process may raise.
        RuntimeError: If the interpreter does not ship the ``resource`` module.
    """
    value = _require_limit(limit)
    soft, hard = _require_limits(limits)
    _check_limits(soft, hard, get_rlimit(value))
    _resource_module().setrlimit(value, (soft, hard))


def prlimit(
    pid: int,
    limit: Union[int, str],
    new_limits: Optional[Sequence[int]] = None,
) -> Limit:
    """Return the limits of *limit* for the process *pid*.

    Args:
        pid: The identifier of the process.  The value ``0`` names the calling
            process.
        limit: The value of a resource limit or the name of one, such as
            ``"RLIMIT_NOFILE"``.
        new_limits: A sequence with the new soft limit first and the new hard
            limit second.  When it is omitted, the limits are only read.  The
            interpreters before Python 3.12 require the limits argument, so
            only the limits of the calling process can be read without it.

    Returns:
        The limits the process had before the call.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *pid* is negative, if the host platform does not
            provide the limit, or if the new limits do not hold exactly two
            values.
        RuntimeError: If the interpreter does not ship the ``resource`` module
            or if the platform does not provide ``prlimit``.
        PermissionError: If the process may not read or write the limits of
            the given process.
    """
    if isinstance(pid, bool) or not isinstance(pid, int):
        raise TypeError(f"pid must be an int, got {type(pid).__name__}")
    if pid < 0:
        raise ValueError(f"pid must not be negative, got {pid}")
    value = _require_limit(limit)
    new_values = None if new_limits is None else _require_limits(new_limits)
    module = _resource_module()
    prlimit_function = getattr(module, "prlimit", None)
    if prlimit_function is None:
        raise RuntimeError(
            "the standard library 'resource' module of this platform does not provide "
            "'prlimit'; the helper is only available on Linux"
        )
    if new_values is None:
        try:
            soft, hard = prlimit_function(pid, value)
        except TypeError:
            # Interpreters before Python 3.12 require the limits argument.
            if pid != 0:
                raise RuntimeError(
                    "the standard library 'prlimit' of this interpreter requires the limits "
                    "argument; only the limits of the calling process can be read without it"
                ) from None
            soft, hard = module.getrlimit(value)
    else:
        soft, hard = prlimit_function(pid, value, new_values)
    return Limit(int(soft), int(hard))


def get_rusage(who: int = RUSAGE_SELF) -> Usage:
    """Return the resource usage of the process identified by *who*.

    Args:
        who: The process to report on.  The value :data:`RUSAGE_SELF` reports
            on the calling process, :data:`RUSAGE_CHILDREN` on the children it
            has waited for, and :data:`RUSAGE_THREAD` on the calling thread.

    Returns:
        The resource usage of the process.

    Raises:
        TypeError: If *who* is not an int.
        ValueError: If the host platform does not provide the usage target.
        RuntimeError: If the interpreter does not ship the ``resource`` module.
    """
    if isinstance(who, bool) or not isinstance(who, int):
        raise TypeError(f"who must be an int, got {type(who).__name__}")
    usages = usage_names()
    if who not in usages.values():
        raise ValueError(f"unknown usage target: {who}")
    record = _resource_module().getrusage(who)
    return Usage(
        user_time=float(getattr(record, "ru_utime", 0.0)),
        system_time=float(getattr(record, "ru_stime", 0.0)),
        max_rss=int(getattr(record, "ru_maxrss", 0)),
        minor_faults=int(getattr(record, "ru_minflt", 0)),
        major_faults=int(getattr(record, "ru_majflt", 0)),
        swapped_out=int(getattr(record, "ru_nswap", 0)),
        blocks_in=int(getattr(record, "ru_inblock", 0)),
        blocks_out=int(getattr(record, "ru_oublock", 0)),
        messages_sent=int(getattr(record, "ru_msgsnd", 0)),
        messages_received=int(getattr(record, "ru_msgrcv", 0)),
        signals=int(getattr(record, "ru_nsignals", 0)),
        voluntary_context_switches=int(getattr(record, "ru_nvcsw", 0)),
        involuntary_context_switches=int(getattr(record, "ru_nivcsw", 0)),
    )


def usage_as_dict(usage: Usage) -> Dict[str, Union[float, int]]:
    """Return the fields of *usage* as a dictionary.

    Args:
        usage: The usage record to convert.

    Returns:
        The fields of the record, keyed by their name.

    Raises:
        TypeError: If *usage* is not a :class:`Usage` record.
    """
    if not isinstance(usage, Usage):
        raise TypeError(f"usage must be a Usage record, got {type(usage).__name__}")
    return dict(usage._asdict())


def get_page_size() -> int:
    """Return the size of a memory page in bytes.

    Raises:
        RuntimeError: If the interpreter does not ship the ``resource`` module.
    """
    return int(_resource_module().getpagesize())
