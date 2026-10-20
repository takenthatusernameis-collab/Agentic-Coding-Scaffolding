"""Group database utilities wrapping the standard library :mod:`grp` module.

The :mod:`grp` module provides access to the Unix group database.  A program
looks up a group by name with :func:`grp.getgrnam` or by numeric group
identifier with :func:`grp.getgrgid`, and enumerates all entries with
:func:`grp.getgrall`.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It returns records as :class:`Group`
named tuples with stable field names on every platform, and it adds helpers to
look up entries and to enumerate the database.

.. note::

   The :mod:`grp` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while the pure helpers keep working.

The helpers never modify the group database.
"""

from __future__ import annotations

from typing import Any, List, NamedTuple

try:
    import grp as _grp
except ImportError:  # pragma: no cover - the module is Unix-only
    _grp = None  # type: ignore[assignment]


class Group(NamedTuple):
    """A group database entry.

    Attributes:
        name: The group name.
        passwd: The encrypted password (may be ``'x'`` or empty).
        gid: The numeric group identifier.
        mem: A list of the login names that are members of the group.
    """

    name: str
    passwd: str
    gid: int
    mem: List[str]


__all__: list[str] = [
    "Group",
    "getgrall",
    "getgrgid",
    "getgrnam",
    "is_available",
]


def _grp_module() -> Any:
    """Return the standard library ``grp`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``grp`` module.
    """
    if _grp is None:
        raise RuntimeError("the standard library module 'grp' is not available")
    return _grp


def is_available() -> bool:
    """Return ``True`` if the ``grp`` module is available."""
    return _grp is not None


def _record_to_group(record: Any) -> Group:
    """Convert a ``grp.struct_group`` to a :class:`Group` named tuple."""
    return Group(
        name=str(record.gr_name),
        passwd=str(record.gr_passwd),
        gid=int(record.gr_gid),
        mem=list(record.gr_mem),
    )


def getgrgid(gid: int) -> Group:
    """Return the group database entry for the group with numeric *gid*.

    Args:
        gid: The numeric group identifier.

    Returns:
        The :class:`Group` record for the group.

    Raises:
        TypeError: If *gid* is not an int.
        ValueError: If *gid* is negative.
        KeyError: If no group has the given identifier.
        RuntimeError: If the interpreter does not ship the ``grp`` module.
    """
    if isinstance(gid, bool) or not isinstance(gid, int):
        raise TypeError(f"gid must be an int, got {type(gid).__name__}")
    if gid < 0:
        raise ValueError(f"gid must not be negative, got {gid}")
    try:
        record = _grp_module().getgrgid(gid)
    except KeyError:
        raise KeyError(f"getgrgid(): gid not found: {gid}") from None
    return _record_to_group(record)


def getgrnam(name: str) -> Group:
    """Return the group database entry for the group with *name*.

    Args:
        name: The group name.

    Returns:
        The :class:`Group` record for the group.

    Raises:
        TypeError: If *name* is not a str.
        ValueError: If *name* is empty.
        KeyError: If no group has the given name.
        RuntimeError: If the interpreter does not ship the ``grp`` module.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    if name == "":
        raise ValueError("name must not be empty")
    try:
        record = _grp_module().getgrnam(name)
    except KeyError:
        raise KeyError(f"getgrnam(): name not found: {name!r}") from None
    return _record_to_group(record)


def getgrall() -> List[Group]:
    """Return every entry in the group database.

    Returns:
        A list of :class:`Group` records.

    Raises:
        RuntimeError: If the interpreter does not ship the ``grp`` module.
    """
    records = _grp_module().getgrall()
    return [_record_to_group(record) for record in records]
