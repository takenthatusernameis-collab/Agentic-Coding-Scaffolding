"""Mailcap utility functions wrapping the standard library 'mailcap' module."""

from __future__ import annotations

from typing import Any

try:
    import mailcap as _mailcap
    _MAILCAP_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when mailcap is unavailable
    _mailcap = None  # type: ignore[assignment]
    _MAILCAP_AVAILABLE = False

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
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`mailcap` module is available."""
    return _MAILCAP_AVAILABLE


def _require_mailcap(name: str) -> None:
    if not _MAILCAP_AVAILABLE:
        raise RuntimeError(f"mailcap module is not available; {name} cannot be used")


def getcaps() -> dict[str, list[dict[str, Any]]]:
    """Return the mailcap database as a dict keyed by MIME type."""
    _require_mailcap("getcaps")
    return _mailcap.getcaps()


def list_mailcap_files() -> list[str]:
    """Return the list of mailcap files found on the system."""
    _require_mailcap("list_mailcap_files")
    return _mailcap.listmailcapfiles()  # type: ignore[attr-defined,no-any-return]


def read_mailcap_file(fp: Any) -> dict[str, list[dict[str, Any]]]:
    """Read a mailcap file and return a dict keyed by MIME type."""
    _require_mailcap("read_mailcap_file")
    return _mailcap.readmailcapfile(fp)  # type: ignore[attr-defined,no-any-return]


def parse_line(line: str) -> tuple[Any, Any]:
    """Parse one mailcap entry line."""
    _require_mailcap("parse_line")
    return _mailcap.parseline(line)  # type: ignore[attr-defined,no-any-return]


def parse_field(line: str, i: int, n: int) -> tuple[str, int]:
    """Separate one key-value pair in a mailcap entry."""
    _require_mailcap("parse_field")
    return _mailcap.parsefield(line, i, n)  # type: ignore[attr-defined,no-any-return]


def find_match(
    caps: dict[str, list[dict[str, Any]]],
    mime_type: str,
    key: str = "view",
    filename: str = "/dev/null",
    plist: list[str] | None = None,
) -> tuple[Any, Any]:
    """Find a match for a mailcap entry."""
    _require_mailcap("find_match")
    if plist is None:
        plist = []
    return _mailcap.findmatch(caps, mime_type, key=key, filename=filename, plist=plist)


def lookup(
    caps: dict[str, list[dict[str, Any]]],
    mime_type: str,
    key: str | None = None,
) -> list[dict[str, Any]]:
    """Look up mailcap entries for a MIME type."""
    _require_mailcap("lookup")
    return _mailcap.lookup(caps, mime_type, key=key)  # type: ignore[attr-defined,no-any-return]


def subst(
    field: str,
    mime_type: str,
    filename: str,
    plist: list[str] | None = None,
) -> str | None:
    """Substitute fields into a mailcap command string."""
    _require_mailcap("subst")
    if plist is None:
        plist = []
    return _mailcap.subst(field, mime_type, filename, plist)  # type: ignore[attr-defined,no-any-return]


def find_param(name: str, plist: list[str]) -> str:
    """Find a parameter value in a plist."""
    _require_mailcap("find_param")
    return _mailcap.findparam(name, plist)  # type: ignore[attr-defined,no-any-return]