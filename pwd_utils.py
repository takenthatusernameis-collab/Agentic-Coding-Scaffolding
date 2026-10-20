"""Password database utilities wrapping the standard library :mod:`pwd` module.

The :mod:`pwd` module provides access to the Unix password database.  A
program looks up a user by name with :func:`pwd.getpwnam` or by numeric
user identifier with :func:`pwd.getpwuid`, and enumerates all entries with
:func:`pwd.getpwall`.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It returns records as :class:`Passwd`
named tuples with stable field names on every platform, and it adds helpers to
look up entries and to enumerate the database.

.. note::

   The :mod:`pwd` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while the pure helpers keep working.

The helpers never modify the password database.
"""

from __future__ import annotations

from typing import Any, List, NamedTuple

try:
    import pwd as _pwd
except ImportError:  # pragma: no cover - the module is Unix-only
    _pwd = None  # type: ignore[assignment]


class Passwd(NamedTuple):
    """A password database entry.

    Attributes:
        name: The login name.
        passwd: The encrypted password (may be ``'x'`` or ``'*'``).
        uid: The numeric user identifier.
        gid: The numeric group identifier.
        gecos: The user name or comment field.
        dir: The home directory.
        shell: The login shell.
    """

    name: str
    passwd: str
    uid: int
    gid: int
    gecos: str
    dir: str
    shell: str


__all__: list[str] = [
    "Passwd",
    "getpwall",
    "getpwnam",
    "getpwuid",
    "is_available",
]


def _pwd_module() -> Any:
    """Return the standard library ``pwd`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pwd`` module.
    """
    if _pwd is None:
        raise RuntimeError("the standard library module 'pwd' is not available")
    return _pwd


def is_available() -> bool:
    """Return ``True`` if the ``pwd`` module is available."""
    return _pwd is not None


def _record_to_passwd(record: Any) -> Passwd:
    """Convert a ``pwd.struct_passwd`` to a :class:`Passwd` named tuple."""
    return Passwd(
        name=str(record.pw_name),
        passwd=str(record.pw_passwd),
        uid=int(record.pw_uid),
        gid=int(record.pw_gid),
        gecos=str(record.pw_gecos),
        dir=str(record.pw_dir),
        shell=str(record.pw_shell),
    )


def getpwuid(uid: int) -> Passwd:
    """Return the password database entry for the user with numeric *uid*.

    Args:
        uid: The numeric user identifier.

    Returns:
        The :class:`Passwd` record for the user.

    Raises:
        TypeError: If *uid* is not an int.
        ValueError: If *uid* is negative.
        KeyError: If no user has the given identifier.
        RuntimeError: If the interpreter does not ship the ``pwd`` module.
    """
    if isinstance(uid, bool) or not isinstance(uid, int):
        raise TypeError(f"uid must be an int, got {type(uid).__name__}")
    if uid < 0:
        raise ValueError(f"uid must not be negative, got {uid}")
    try:
        record = _pwd_module().getpwuid(uid)
    except KeyError:
        raise KeyError(f"getpwuid(): uid not found: {uid}") from None
    return _record_to_passwd(record)


def getpwnam(name: str) -> Passwd:
    """Return the password database entry for the user with *name*.

    Args:
        name: The login name.

    Returns:
        The :class:`Passwd` record for the user.

    Raises:
        TypeError: If *name* is not a str.
        ValueError: If *name* is empty.
        KeyError: If no user has the given name.
        RuntimeError: If the interpreter does not ship the ``pwd`` module.
    """
    if not isinstance(name, str):
        raise TypeError(f"name must be a str, got {type(name).__name__}")
    if name == "":
        raise ValueError("name must not be empty")
    try:
        record = _pwd_module().getpwnam(name)
    except KeyError:
        raise KeyError(f"getpwnam(): name not found: {name!r}") from None
    return _record_to_passwd(record)


def getpwall() -> List[Passwd]:
    """Return every entry in the password database.

    Returns:
        A list of :class:`Passwd` records.

    Raises:
        RuntimeError: If the interpreter does not ship the ``pwd`` module.
    """
    records = _pwd_module().getpwall()
    return [_record_to_passwd(record) for record in records]
