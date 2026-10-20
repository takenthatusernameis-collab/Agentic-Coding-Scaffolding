"""Mailcap utility functions wrapping the standard library 'mailcap' module."""

from __future__ import annotations

import mailcap
from typing import Any

__all__: list[str] = [
    "getcaps",
    "list_mailcap_files",
    "read_mailcap_file",
    "parse_line",
    "parse_field",
    "find_match",
    "lookup",
    "subst",
    "find_param",
]


def getcaps() -> dict[str, list[dict[str, Any]]]:
    """Return the mailcap database as a dict keyed by MIME type."""
    return mailcap.getcaps()


def list_mailcap_files() -> list[str]:
    """Return the list of mailcap files found on the system."""
    return mailcap.listmailcapfiles()  # type: ignore[attr-defined,no-any-return]


def read_mailcap_file(fp: Any) -> dict[str, list[dict[str, Any]]]:
    """Read a mailcap file and return a dict keyed by MIME type."""
    return mailcap.readmailcapfile(fp)  # type: ignore[attr-defined,no-any-return]


def parse_line(line: str) -> tuple[Any, Any]:
    """Parse one mailcap entry line."""
    return mailcap.parseline(line)  # type: ignore[attr-defined,no-any-return]


def parse_field(line: str, i: int, n: int) -> tuple[str, int]:
    """Separate one key-value pair in a mailcap entry."""
    return mailcap.parsefield(line, i, n)  # type: ignore[attr-defined,no-any-return]


def find_match(
    caps: dict[str, list[dict[str, Any]]],
    mime_type: str,
    key: str = "view",
    filename: str = "/dev/null",
    plist: list[str] | None = None,
) -> tuple[Any, Any]:
    """Find a match for a mailcap entry."""
    if plist is None:
        plist = []
    return mailcap.findmatch(caps, mime_type, key=key, filename=filename, plist=plist)


def lookup(
    caps: dict[str, list[dict[str, Any]]],
    mime_type: str,
    key: str | None = None,
) -> list[dict[str, Any]]:
    """Look up mailcap entries for a MIME type."""
    return mailcap.lookup(caps, mime_type, key=key)  # type: ignore[attr-defined,no-any-return]


def subst(
    field: str,
    mime_type: str,
    filename: str,
    plist: list[str] | None = None,
) -> str | None:
    """Substitute fields into a mailcap command string."""
    if plist is None:
        plist = []
    return mailcap.subst(field, mime_type, filename, plist)  # type: ignore[attr-defined,no-any-return]


def find_param(name: str, plist: list[str]) -> str:
    """Find a parameter value in a plist."""
    return mailcap.findparam(name, plist)  # type: ignore[attr-defined,no-any-return]
