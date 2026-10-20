"""Mailbox utilities (wrapping :mod:`mailbox`)."""

from __future__ import annotations

import mailbox as _mailbox
import os
from email.message import Message
from typing import Any, Callable, Iterator, List, Optional, Type, Union, cast

__all__ = [
    "Babyl",
    "Maildir",
    "Message",
    "MH",
    "mbox",
    "MMDF",
    "Mailbox",
    "add_message",
    "create_babyl",
    "create_maildir",
    "create_mbox",
    "create_mh",
    "create_mmdf",
    "get_message",
    "iter_message_keys",
    "iter_messages",
    "list_message_keys",
    "lock_mailbox",
    "open_mailbox",
    "remove_message",
    "unlock_mailbox",
]

Babyl = _mailbox.Babyl
Maildir = _mailbox.Maildir
mbox = _mailbox.mbox
MH = _mailbox.MH
MMDF = _mailbox.MMDF
Mailbox = _mailbox.Mailbox


def _require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_bool(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _require_path_exists(value: str, name: str) -> str:
    if not os.path.lexists(value):
        raise FileNotFoundError(f"{name} {value!r} does not exist")
    return value


def create_mbox(path: str, create: bool = True) -> _mailbox.mbox:
    path = _require_str(path, "path")
    create = _require_bool(create, "create")
    if create and not os.path.lexists(path):
        parent = os.path.dirname(os.path.abspath(path)) or "."
        os.makedirs(parent, exist_ok=True)
        open(path, "a").close()
    elif not create:
        _require_path_exists(path, "path")
    return _mailbox.mbox(path, create=create)


def create_maildir(path: str, create: bool = True) -> _mailbox.Maildir:
    path = _require_str(path, "path")
    create = _require_bool(create, "create")
    if create and not os.path.lexists(path):
        os.makedirs(path, exist_ok=True)
    elif not create:
        _require_path_exists(path, "path")
    return _mailbox.Maildir(path, create=create)


def create_mh(path: str, create: bool = True) -> _mailbox.MH:
    path = _require_str(path, "path")
    create = _require_bool(create, "create")
    if create and not os.path.lexists(path):
        os.makedirs(path, exist_ok=True)
    elif not create:
        _require_path_exists(path, "path")
    return _mailbox.MH(path, create=create)


def create_babyl(path: str, create: bool = True) -> _mailbox.Babyl:
    path = _require_str(path, "path")
    create = _require_bool(create, "create")
    if create and not os.path.lexists(path):
        parent = os.path.dirname(os.path.abspath(path)) or "."
        os.makedirs(parent, exist_ok=True)
        open(path, "a").close()
    elif not create:
        _require_path_exists(path, "path")
    return _mailbox.Babyl(path, create=create)


def create_mmdf(path: str, create: bool = True) -> _mailbox.MMDF:
    path = _require_str(path, "path")
    create = _require_bool(create, "create")
    if create and not os.path.lexists(path):
        parent = os.path.dirname(os.path.abspath(path)) or "."
        os.makedirs(parent, exist_ok=True)
        open(path, "a").close()
    elif not create:
        _require_path_exists(path, "path")
    return _mailbox.MMDF(path, create=create)


def open_mailbox(
    path: str, factory: Optional[Type[Mailbox]] = None, create: bool = True
) -> Mailbox:
    path = _require_str(path, "path")
    create = _require_bool(create, "create")
    if factory is not None:
        if not isinstance(factory, type) or not issubclass(factory, Mailbox):
            raise TypeError("factory must be a mailbox.Mailbox subclass")
    if hasattr(_mailbox, "open"):
        try:
            return _mailbox.open(path, factory=factory, create=create)  # type: ignore[attr-defined,no-any-return]
        except Exception:
            pass
    if factory is not None:
        constructor = cast(Callable[..., Mailbox], factory)
        return constructor(path, create=create)
    if os.path.isdir(path):
        return _mailbox.Maildir(path, create=create)
    return _mailbox.mbox(path, create=create)


def iter_messages(mailbox_obj: Mailbox) -> Iterator[Message]:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    return iter(mailbox_obj)


def iter_message_keys(mailbox_obj: Mailbox) -> Iterator[str]:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    for k in mailbox_obj.keys():
        yield k if isinstance(k, str) else str(k)


def list_message_keys(mailbox_obj: Mailbox) -> List[str]:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    out = []
    for k in mailbox_obj.keys():
        out.append(k if isinstance(k, str) else str(k))
    return out


def get_message(mailbox_obj: Mailbox, key: str) -> Message:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    key = _require_str(key, "key")
    try:
        return mailbox_obj[key]
    except Exception:
        for k in mailbox_obj.keys():
            kstr = k if isinstance(k, str) else str(k)
            if kstr == key:
                return mailbox_obj[k]
        raise


def add_message(mailbox_obj: Mailbox, message: Union[Message, str, bytes]) -> str:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    result = mailbox_obj.add(message)
    if isinstance(result, str):
        return result
    try:
        if isinstance(result, bytes):
            return result.decode()
    except Exception:
        pass
    return str(result)


def remove_message(mailbox_obj: Mailbox, key: str) -> None:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    key = _require_str(key, "key")
    try:
        del mailbox_obj[key]
    except Exception:
        for k in list(mailbox_obj.keys()):
            kstr = k if isinstance(k, str) else str(k)
            if kstr == key:
                del mailbox_obj[k]
                return
        raise


def lock_mailbox(mailbox_obj: Mailbox) -> None:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    mailbox_obj.lock()


def unlock_mailbox(mailbox_obj: Mailbox) -> None:
    if not isinstance(mailbox_obj, Mailbox):
        raise TypeError("mailbox_obj must be a mailbox.Mailbox instance")
    mailbox_obj.unlock()
