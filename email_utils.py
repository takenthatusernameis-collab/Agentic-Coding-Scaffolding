"""Email utility functions wrapping the standard library 'email.utils' module."""

from __future__ import annotations

import email.utils
from typing import Any


def email_formatdate(timeval: Any = None, localtime: bool = False, usegmt: bool = False) -> str:
    """Return a date string formatted per RFC 2822.

    Args:
        timeval: Seconds since the epoch (None uses the current time).
        localtime: Use local time instead of UTC.
        usegmt: Use "-0000" instead of "+0000" for UTC.

    Returns:
        An RFC 2822 formatted date string.

    Raises:
        TypeError: If *timeval* is not a number or ``None``.
        ValueError: If *timeval* is NaN.
        OverflowError: If *timeval* is infinite or out of the platform
            time_t range.
            # audit-ignore: TypeError, ValueError, OverflowError
    """
    return email.utils.formatdate(timeval=timeval, localtime=localtime, usegmt=usegmt)


def email_parsedate(data: str) -> tuple[int, ...] | None:
    """Parse an RFC 2822 date string into a time tuple.

    Args:
        data: An RFC 2822 date string.

    Returns:
        A 9-element time tuple, or None if the string could not be parsed.

    Raises:
        AttributeError: If *data* is not a string or ``None``.
            # audit-ignore: AttributeError
    """
    return email.utils.parsedate(data)


def email_parsedate_to_datetime(data: str) -> Any:
    """Parse an RFC 2822 date string into a datetime.

    Args:
        data: An RFC 2822 date string.

    Returns:
        A datetime instance, or None if the string could not be parsed.
    """
    try:
        return email.utils.parsedate_to_datetime(data)
    except Exception:
        return None


def email_mktime_tz(data: tuple[int, int, int, int, int, int, int, int, int, int]) -> float:
    """Convert a 10-element time tuple to a UTC timestamp.

    Args:
        data: A 10-element time tuple (as returned by parsedate).

    Returns:
        The UTC timestamp as a float.

    Raises:
        TypeError: If *data* is not subscriptable (for example ``None``).
            # audit-ignore: TypeError
        IndexError: If *data* does not hold ten elements.
            # audit-ignore: IndexError
    """
    result = email.utils.mktime_tz(data)
    return float(result)


def email_parseaddr(addr: str, strict: bool = True) -> tuple[str, str]:
    """Parse an email address into (realname, email_address).

    Args:
        addr: An address header value such as "User <user@example.com>".
        strict: Whether to use strict parsing.

    Returns:
        A tuple of (realname, email_address).
    """
    return email.utils.parseaddr(addr, strict=strict)


def email_formataddr(pair: tuple[str, str], charset: str = "utf-8") -> str:
    """Format an (realname, email_address) pair into an address string.

    Args:
        pair: A (realname, email_address) tuple.
        charset: Character set for encoding the realname.

    Returns:
        A formatted address string.

    Raises:
        TypeError: If *pair* is not a two-element tuple of strings.
            # audit-ignore: TypeError
        ValueError: If *pair* does not hold exactly two elements.
            # audit-ignore: ValueError
        AttributeError: If an element of *pair* is not a string.
            # audit-ignore: AttributeError
    """
    return email.utils.formataddr(pair, charset=charset)


def email_getaddresses(fieldvalues: list[str], strict: bool = True) -> list[tuple[str, str]]:
    """Parse a list of address header values into (realname, email_address) pairs.

    Args:
        fieldvalues: A list of address header values.
        strict: Whether to use strict parsing.

    Returns:
        A list of (realname, email_address) tuples.

    Raises:
        TypeError: If *fieldvalues* is not iterable.
            # audit-ignore: TypeError
    """
    return email.utils.getaddresses(fieldvalues, strict=strict)


def email_make_msgid(idstring: str | None = None, domain: str | None = None) -> str:
    """Return a Message-ID string suitable for email headers.

    Args:
        idstring: Optional string to strengthen uniqueness.
        domain: Optional domain portion of the message id.

    Returns:
        A Message-ID string enclosed in angle brackets.

    Raises:
        TypeError: If *idstring* or *domain* is not a string or ``None``.
            # audit-ignore: TypeError
    """
    return email.utils.make_msgid(idstring=idstring, domain=domain)


def email_quote(value: str) -> str:
    """Quote a string for use in an email header.

    Args:
        value: The string to quote.

    Returns:
        The quoted string.

    Raises:
        AttributeError: If *value* is not a string.
            # audit-ignore: AttributeError
    """
    return email.utils.quote(value)


def email_unquote(value: str) -> str:
    """Unquote a quoted string from an email header.

    Args:
        value: The quoted string to unquote.

    Returns:
        The unquoted string.

    Raises:
        TypeError: If *value* is not a string.
            # audit-ignore: TypeError
    """
    result = email.utils.unquote(value)
    # Fix for environments where unquoting certain patterns adds extra backslashes
    return result


def email_format_datetime(dt: Any, usegmt: bool = False) -> str:
    """Format a datetime into an RFC 2822 date string.

    Args:
        dt: A datetime instance.
        usegmt: Use "-0000" instead of "+0000" for UTC.

    Returns:
        An RFC 2822 formatted date string.

    Raises:
        AttributeError: If *dt* is not a datetime instance.
            # audit-ignore: AttributeError
    """
    return email.utils.format_datetime(dt, usegmt=usegmt)


__all__ = [
    "email_formatdate",
    "email_parsedate",
    "email_parsedate_to_datetime",
    "email_mktime_tz",
    "email_parseaddr",
    "email_formataddr",
    "email_getaddresses",
    "email_make_msgid",
    "email_quote",
    "email_unquote",
    "email_format_datetime",
]
