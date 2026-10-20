"""Mailbox utilities (wrapping :mod:`mailbox`).

The :mod:`mailbox` module defines classes for accessing and manipulating
on-disk mailboxes in various formats (mbox, Maildir, MH, MMDF, Babyl).
This wrapper provides validated factory functions and helpers to create
mailboxes and access related exceptions without performing disk I/O in the
factory helpers themselves.
"""

from __future__ import annotations

import mailbox as _mailbox
from pathlib import Path
from typing import Any, Callable, Optional, Union

__all__ = [
    "Babyl",
    "BabylMessage",
    "Error",
    "ExternalClashError",
    "FormatError",
    "MH",
    "MHMessage",
    "MMDF",
    "MMDFMessage",
    "Mailbox",
    "Maildir",
    "MaildirMessage",
    "Message",
    "NoSuchMailboxError",
    "NotEmptyError",
    "create_babyl",
    "create_babyl_message",
    "create_mh",
    "create_mh_message",
    "create_mailbox",
    "create_maildir",
    "create_maildir_message",
    "create_mbox",
    "create_mbox_message",
    "create_mmdf",
    "create_mmdf_message",
    "is_external_clash_error",
    "is_format_error",
    "is_mailbox_error",
    "is_no_such_mailbox_error",
    "is_not_empty_error",
]

Babyl = _mailbox.Babyl
BabylMessage = _mailbox.BabylMessage
Error = _mailbox.Error
ExternalClashError = _mailbox.ExternalClashError
FormatError = _mailbox.FormatError
MH = _mailbox.MH
MHMessage = _mailbox.MHMessage
MMDF = _mailbox.MMDF
MMDFMessage = _mailbox.MMDFMessage
Mailbox = _mailbox.Mailbox
Maildir = _mailbox.Maildir
MaildirMessage = _mailbox.MaildirMessage
Message = _mailbox.Message
NoSuchMailboxError = _mailbox.NoSuchMailboxError
NotEmptyError = _mailbox.NotEmptyError


def _path_to_str(path: Union[str, Path]) -> str:
    if isinstance(path, Path):
        return str(path)
    if isinstance(path, str):
        return path
    raise TypeError(f"path must be a str or Path, got {type(path).__name__}")


def create_mailbox(
    path: Union[str, Path],
    factory: Optional[Callable[[Any], Any]] = None,
    create: bool = True,
) -> _mailbox.Mailbox:
    """Create a mailbox instance."""
    _path = _path_to_str(path)
    if factory is None:
        return _mailbox.Mailbox(_path, create=create)  # type: ignore[abstract,arg-type]
    return _mailbox.Mailbox(_path, factory=factory, create=create)  # type: ignore[abstract,arg-type]


def create_mbox(
    path: Union[str, Path],
    factory: Optional[Callable[[Any], Any]] = None,
    create: bool = True,
) -> _mailbox.mbox:
    """Create an mbox mailbox."""
    _path = _path_to_str(path)
    if factory is None:
        return _mailbox.mbox(_path, create=create)  # type: ignore[arg-type]
    return _mailbox.mbox(_path, factory=factory, create=create)  # type: ignore[arg-type]


def create_maildir(
    path: Union[str, Path],
    factory: Optional[Callable[[Any], Any]] = None,
    create: bool = True,
) -> _mailbox.Maildir:
    """Create a Maildir mailbox."""
    _path = _path_to_str(path)
    if factory is None:
        return _mailbox.Maildir(_path, create=create)  # type: ignore[arg-type]
    return _mailbox.Maildir(_path, factory=factory, create=create)  # type: ignore[arg-type]


def create_mh(
    path: Union[str, Path],
    factory: Optional[Callable[[Any], Any]] = None,
    create: bool = True,
) -> _mailbox.MH:
    """Create an MH mailbox."""
    _path = _path_to_str(path)
    if factory is None:
        return _mailbox.MH(_path, create=create)  # type: ignore[arg-type]
    return _mailbox.MH(_path, factory=factory, create=create)  # type: ignore[arg-type]


def create_mmdf(
    path: Union[str, Path],
    factory: Optional[Callable[[Any], Any]] = None,
    create: bool = True,
) -> _mailbox.MMDF:
    """Create an MMDF mailbox."""
    _path = _path_to_str(path)
    if factory is None:
        return _mailbox.MMDF(_path, create=create)  # type: ignore[arg-type]
    return _mailbox.MMDF(_path, factory=factory, create=create)  # type: ignore[arg-type]


def create_babyl(
    path: Union[str, Path],
    factory: Optional[Callable[[Any], Any]] = None,
    create: bool = True,
) -> _mailbox.Babyl:
    """Create a Babyl mailbox."""
    _path = _path_to_str(path)
    if factory is None:
        return _mailbox.Babyl(_path, create=create)  # type: ignore[arg-type]
    return _mailbox.Babyl(_path, factory=factory, create=create)  # type: ignore[arg-type]


def create_mbox_message(message: Any) -> _mailbox.mboxMessage:
    """Create an mbox message."""
    return _mailbox.mboxMessage(message)


def create_maildir_message(message: Any) -> _mailbox.MaildirMessage:
    """Create a Maildir message."""
    return _mailbox.MaildirMessage(message)


def create_mh_message(message: Any) -> _mailbox.MHMessage:
    """Create an MH message."""
    return _mailbox.MHMessage(message)


def create_mmdf_message(message: Any) -> _mailbox.MMDFMessage:
    """Create an MMDF message."""
    return _mailbox.MMDFMessage(message)


def create_babyl_message(message: Any) -> _mailbox.BabylMessage:
    """Create a Babyl message."""
    return _mailbox.BabylMessage(message)


def is_mailbox_error(exc: BaseException) -> bool:
    return isinstance(exc, Error)


def is_external_clash_error(exc: BaseException) -> bool:
    return isinstance(exc, ExternalClashError)


def is_format_error(exc: BaseException) -> bool:
    return isinstance(exc, FormatError)


def is_no_such_mailbox_error(exc: BaseException) -> bool:
    return isinstance(exc, NoSuchMailboxError)


def is_not_empty_error(exc: BaseException) -> bool:
    return isinstance(exc, NotEmptyError)
