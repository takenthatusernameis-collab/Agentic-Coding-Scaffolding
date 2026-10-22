"""NNTP utility functions wrapping the standard library :mod:`nntplib`."""

from __future__ import annotations

import nntplib
from typing import Any

__all__: list[str] = [
    "NNTP",
    "NNTP_SSL",
    "NNTP_PORT",
    "NNTP_SSL_PORT",
    "NNTPError",
    "NNTPReplyError",
    "NNTPTemporaryError",
    "NNTPPermanentError",
    "NNTPProtocolError",
    "NNTPDataError",
    "GroupInfo",
    "ArticleInfo",
    "create_nntp",
    "create_nntp_ssl",
]


NNTP_PORT = nntplib.NNTP_PORT
NNTP_SSL_PORT = nntplib.NNTP_SSL_PORT

NNTP = nntplib.NNTP
NNTP_SSL = nntplib.NNTP_SSL
NNTPError = nntplib.NNTPError
NNTPReplyError = nntplib.NNTPReplyError
NNTPTemporaryError = nntplib.NNTPTemporaryError
NNTPPermanentError = nntplib.NNTPPermanentError
NNTPProtocolError = nntplib.NNTPProtocolError
NNTPDataError = nntplib.NNTPDataError
GroupInfo = nntplib.GroupInfo
ArticleInfo = nntplib.ArticleInfo


def create_nntp(
    host: str,
    port: int = NNTP_PORT,
    user: str | None = None,
    password: str | None = None,
    readermode: bool | None = None,
    usenetrc: bool = False,
    timeout: float | None = None,
) -> nntplib.NNTP:
    """Create an NNTP connection."""
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if isinstance(port, bool) or not isinstance(port, int):
        raise TypeError("port must be an int")
    if user is not None and not isinstance(user, str):
        raise TypeError("user must be a str or None")
    if password is not None and not isinstance(password, str):
        raise TypeError("password must be a str or None")
    if readermode is not None and not isinstance(readermode, bool):
        raise TypeError("readermode must be a bool or None")
    if not isinstance(usenetrc, bool):
        raise TypeError("usenetrc must be a bool")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    return nntplib.NNTP(
        host=host,
        port=port,
        user=user,
        password=password,
        readermode=readermode,
        usenetrc=usenetrc,
        timeout=timeout,
    )


def create_nntp_ssl(
    host: str,
    port: int = NNTP_SSL_PORT,
    user: str | None = None,
    password: str | None = None,
    ssl_context=None,
    readermode: bool | None = None,
    usenetrc: bool = False,
    timeout: float | None = None,
) -> nntplib.NNTP_SSL:
    """Create an NNTP-over-SSL connection."""
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if isinstance(port, bool) or not isinstance(port, int):
        raise TypeError("port must be an int")
    if user is not None and not isinstance(user, str):
        raise TypeError("user must be a str or None")
    if password is not None and not isinstance(password, str):
        raise TypeError("password must be a str or None")
    if readermode is not None and not isinstance(readermode, bool):
        raise TypeError("readermode must be a bool or None")
    if not isinstance(usenetrc, bool):
        raise TypeError("usenetrc must be a bool")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    return nntplib.NNTP_SSL(
        host=host,
        port=port,
        user=user,
        password=password,
        ssl_context=ssl_context,
        readermode=readermode,
        usenetrc=usenetrc,
        timeout=timeout,
    )