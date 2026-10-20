"""FTP utility functions wrapping the standard library :mod:`ftplib`."""

from __future__ import annotations

import ftplib
from typing import Any

__all__: list[str] = [
    "FTP",
    "FTP_TLS",
    "error_reply",
    "error_temp",
    "error_perm",
    "error_proto",
    "all_errors",
    "FTP_PORT",
    "MAXLINE",
    "create_ftp",
    "create_ftp_tls",
    "connect_ftp",
    "parse257",
    "parse150",
    "parse227",
    "parse229",
]

FTP_PORT = ftplib.FTP_PORT
MAXLINE = ftplib.MAXLINE

FTP = ftplib.FTP
FTP_TLS = ftplib.FTP_TLS
error_reply = ftplib.error_reply
error_temp = ftplib.error_temp
error_perm = ftplib.error_perm
error_proto = ftplib.error_proto
all_errors = ftplib.all_errors


def create_ftp(
    host: str = "",
    user: str = "",
    passwd: str = "",
    acct: str = "",
    timeout: float | None = None,
    source_address: tuple[str, int] | None = None,
    encoding: str = "utf-8",
) -> ftplib.FTP:
    """Create and optionally log in to an FTP connection."""
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(user, str):
        raise TypeError("user must be a str")
    if not isinstance(passwd, str):
        raise TypeError("passwd must be a str")
    if not isinstance(acct, str):
        raise TypeError("acct must be a str")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    if source_address is not None:
        if not isinstance(source_address, tuple) or len(source_address) != 2:
            raise TypeError("source_address must be a (host, port) tuple or None")
        if (not isinstance(source_address[0], str)
                or not isinstance(source_address[1], int)
                or isinstance(source_address[1], bool)):
            raise TypeError("source_address must be a (host, port) tuple or None")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a str")
    ftp = ftplib.FTP(
        host=host,
        user=user,
        passwd=passwd,
        acct=acct,
        timeout=timeout,
        source_address=source_address,
        encoding=encoding,
    )  # type: ignore[arg-type]
    return ftp


def create_ftp_tls(
    host: str = "",
    user: str = "",
    passwd: str = "",
    acct: str = "",
    *,
    context: Any = None,
    timeout: float | None = None,
    source_address: tuple[str, int] | None = None,
    encoding: str = "utf-8",
) -> ftplib.FTP_TLS:
    """Create an FTP_TLS connection."""
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(user, str):
        raise TypeError("user must be a str")
    if not isinstance(passwd, str):
        raise TypeError("passwd must be a str")
    if not isinstance(acct, str):
        raise TypeError("acct must be a str")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    if source_address is not None:
        if not isinstance(source_address, tuple) or len(source_address) != 2:
            raise TypeError("source_address must be a (host, port) tuple or None")
        if (not isinstance(source_address[0], str)
                or not isinstance(source_address[1], int)
                or isinstance(source_address[1], bool)):
            raise TypeError("source_address must be a (host, port) tuple or None")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a str")
    ftp = ftplib.FTP_TLS(
        host=host,
        user=user,
        passwd=passwd,
        acct=acct,
        context=context,
        timeout=timeout,
        source_address=source_address,
        encoding=encoding,
    )  # type: ignore[arg-type]
    return ftp


def connect_ftp(
    ftp: ftplib.FTP,
    host: str,
    port: int = FTP_PORT,
    timeout: float | None = None,
    source_address: tuple[str, int] | None = None,
) -> str:
    """Connect to a host using an existing FTP instance."""
    if not isinstance(ftp, ftplib.FTP):
        raise TypeError("ftp must be an ftplib.FTP instance")
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    if source_address is not None:
        if not isinstance(source_address, tuple) or len(source_address) != 2:
            raise TypeError("source_address must be a (host, port) tuple or None")
        if (not isinstance(source_address[0], str)
                or not isinstance(source_address[1], int)
                or isinstance(source_address[1], bool)):
            raise TypeError("source_address must be a (host, port) tuple or None")
    return ftp.connect(host, port, timeout, source_address)  # type: ignore[arg-type]


def parse257(resp: str) -> str:
    """Parse the 257 response for a directory name."""
    if not isinstance(resp, str):
        raise TypeError("resp must be a str")
    return ftplib.parse257(resp)


def parse150(resp: str) -> Any:
    """Parse the 150 response."""
    if not isinstance(resp, str):
        raise TypeError("resp must be a str")
    return ftplib.parse150(resp)


def parse227(resp: str) -> tuple[str, int]:
    """Parse the 227 response and return (host, port)."""
    if not isinstance(resp, str):
        raise TypeError("resp must be a str")
    return ftplib.parse227(resp)


def parse229(resp: str, peer: Any = None) -> tuple[str, int]:
    """Parse the 229 response and return (host, port)."""
    if not isinstance(resp, str):
        raise TypeError("resp must be a str")
    try:
        if peer is not None:
            return ftplib.parse229(resp, peer)  # type: ignore[call-arg]
        # Try without peer first (some Python versions)
        return ftplib.parse229(resp)  # type: ignore[call-arg]
    except TypeError:
        return ftplib.parse229(resp, peer)  # type: ignore[call-arg]
