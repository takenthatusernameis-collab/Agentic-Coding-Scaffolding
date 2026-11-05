"""NNTP client utilities wrapping the standard library :mod:`nntplib`."""

from __future__ import annotations

try:
    import nntplib as _nntplib
    _NNTP_LIB_AVAILABLE = True
except Exception:
    _nntplib = None  # type: ignore[assignment]
    _NNTP_LIB_AVAILABLE = False

from typing import Any

__all__: list[str] = [
    "NNTP",
    "NNTP_SSL",
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
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`nntplib` module is available."""
    return _NNTP_LIB_AVAILABLE


if _NNTP_LIB_AVAILABLE:
    NNTP = _nntplib.NNTP
    NNTP_SSL = _nntplib.NNTP_SSL
    NNTPError = _nntplib.NNTPError
    NNTPReplyError = _nntplib.NNTPReplyError
    NNTPTemporaryError = _nntplib.NNTPTemporaryError
    NNTPPermanentError = _nntplib.NNTPPermanentError
    NNTPProtocolError = _nntplib.NNTPProtocolError
    NNTPDataError = _nntplib.NNTPDataError
    GroupInfo = _nntplib.GroupInfo
    ArticleInfo = _nntplib.ArticleInfo
else:
    class NNTP:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise RuntimeError("nntplib module is not available")

    class NNTP_SSL(NNTP):  # type: ignore[no-redef]
        pass

    class NNTPError(Exception):
        pass

    class NNTPReplyError(NNTPError):
        pass

    class NNTPTemporaryError(NNTPError):
        pass

    class NNTPPermanentError(NNTPError):
        pass

    class NNTPProtocolError(NNTPError):
        pass

    class NNTPDataError(NNTPError):
        pass

    GroupInfo = tuple  # type: ignore[assignment]
    ArticleInfo = tuple  # type: ignore[assignment]


def create_nntp(
    host: str = "",
    port: int = 119,
    user: str | None = None,
    password: str | None = None,
    readermode: bool | None = None,
    usenetrc: bool = True,
    timeout: float | None = None,
) -> NNTP:
    if not _NNTP_LIB_AVAILABLE:
        raise RuntimeError("nntplib module is not available")
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    if user is not None and not isinstance(user, str):
        raise TypeError("user must be a str or None")
    if password is not None and not isinstance(password, str):
        raise TypeError("password must be a str or None")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    return NNTP(host, port, user, password, readermode, usenetrc, timeout)


def create_nntp_ssl(
    host: str = "",
    port: int = 563,
    user: str | None = None,
    password: str | None = None,
    ssl_context: Any = None,
    readermode: bool | None = None,
    usenetrc: bool = True,
    timeout: float | None = None,
) -> NNTP_SSL:
    if not _NNTP_LIB_AVAILABLE:
        raise RuntimeError("nntplib module is not available")
    if not isinstance(host, str):
        raise TypeError("host must be a str")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if port < 0 or port > 65535:
        raise ValueError("port must be between 0 and 65535")
    if user is not None and not isinstance(user, str):
        raise TypeError("user must be a str or None")
    if password is not None and not isinstance(password, str):
        raise TypeError("password must be a str or None")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    return NNTP_SSL(host, port, user, password, ssl_context, readermode, usenetrc, timeout)
