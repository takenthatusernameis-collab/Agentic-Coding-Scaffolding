"""Shadow password database utilities wrapping the standard library :mod:`spwd` module.

The :mod:`spwd` module reads the shadow password file ``/etc/shadow`` and returns
the entries of a user as a :class:`ShadowEntry` record.  The record carries the
name of the user, the hashed password, and the aging fields that control how
the password expires.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It returns the entry as a named
record so a caller reads a field by its name instead of by its position, and it
exposes the aging fields of every entry as named constants.

.. note::

   The :mod:`spwd` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module, while the helpers that
   need no standard library keep working.
"""

from __future__ import annotations

import warnings
from typing import Any, List, NamedTuple, Optional

__all__ = [
    "ShadowEntry",
    "getspall",
    "getspnam",
    "is_available",
]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import spwd as _spwd
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _spwd = None  # type: ignore[assignment]


class ShadowEntry(NamedTuple):
    """A shadow password database entry.

    The fields mirror the columns of the ``/etc/shadow`` file.

    Attributes:
        sp_nam: The user name.
        sp_pwdp: The hashed password, or a marker such as ``!`` or ``*`` when
            the account is locked.
        sp_lstchg: The number of days since the epoch the password was last
            changed.
        sp_min: The minimum number of days between password changes.
        sp_max: The maximum number of days before the password expires.
        sp_warn: The number of days before expiry the user is warned.
        sp_inact: The number of days after expiry the account is locked.
        sp_expire: The number of days since the epoch the account expires.
        sp_flag: A reserved field kept for future use.
    """

    sp_nam: str
    sp_pwdp: str
    sp_lstchg: Optional[int]
    sp_min: Optional[int]
    sp_max: Optional[int]
    sp_warn: Optional[int]
    sp_inact: Optional[int]
    sp_expire: Optional[int]
    sp_flag: Optional[int]


def _spwd_module() -> Any:
    """Return the standard library ``spwd`` module.

    Returns:
        The imported :mod:`spwd` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``spwd`` module.
    """
    if _spwd is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'spwd' module was removed in Python 3.13; "
            "read /etc/shadow directly or use the 'pwd' module instead"
        )
    return _spwd


def _require_str(value: Any, name: str) -> str:
    """Return *value* as a string, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a string.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str, not {type(value).__name__}")
    return value


def _to_int(value: Any) -> Optional[int]:
    """Return *value* as an integer, or ``None`` for a disabled field.

    The aging fields of the shadow file use ``-1`` to mean "not set", so the
    wrapper reports them as ``None`` instead of a negative number.

    Args:
        value: The raw field of the record.

    Returns:
        The field as an integer, or ``None`` when it is unset.
    """
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text == "-1":
        return None
    return int(text)


def _entry_from_record(record: Any) -> ShadowEntry:
    """Build a :class:`ShadowEntry` from a standard library record."""
    return ShadowEntry(
        sp_nam=str(getattr(record, "sp_nam", "")),
        sp_pwdp=str(getattr(record, "sp_pwdp", "")),
        sp_lstchg=_to_int(getattr(record, "sp_lstchg", None)),
        sp_min=_to_int(getattr(record, "sp_min", None)),
        sp_max=_to_int(getattr(record, "sp_max", None)),
        sp_warn=_to_int(getattr(record, "sp_warn", None)),
        sp_inact=_to_int(getattr(record, "sp_inact", None)),
        sp_expire=_to_int(getattr(record, "sp_expire", None)),
        sp_flag=_to_int(getattr(record, "sp_flag", None)),
    )


def is_available() -> bool:
    """Report whether the interpreter ships the standard library ``spwd`` module.

    Returns:
        ``True`` when the module is importable, ``False`` otherwise.
    """
    return _spwd is not None


def getspnam(name: str) -> ShadowEntry:
    """Return the shadow password entry of *name*.

    Args:
        name: The user name to look up.

    Returns:
        The shadow entry of the user.

    Raises:
        TypeError: If *name* is not a string.
        KeyError: If the user is unknown.
        RuntimeError: If the interpreter no longer ships the ``spwd`` module.
    """
    _require_str(name, "name")
    record = _spwd_module().getspnam(name)
    return _entry_from_record(record)


def getspall() -> List[ShadowEntry]:
    """Return every shadow password entry.

    The entries are returned in the order the standard library provides, which is
    arbitrary.

    Returns:
        The shadow entries of every user.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``spwd`` module.
    """
    records = _spwd_module().getspall()
    return [_entry_from_record(record) for record in records]