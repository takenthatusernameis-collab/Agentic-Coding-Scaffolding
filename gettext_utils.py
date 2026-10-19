"""Utilities wrapping :mod:`gettext` for internationalization and localization.

This module provides a small, consistent API around :mod:`gettext` for marking
and translating strings, managing translation domains and catalog bindings, and
installing the translation function into Python's builtins namespace.
"""

import gettext as _gettext
from typing import Container, Iterable, Optional

__all__: list[str] = [
    "bindtextdomain",
    "dngettext",
    "dgettext",
    "gettext",
    "install",
    "ngettext",
    "textdomain",
]


def gettext(message: str) -> str:
    """Return the translated string for *message* in the current domain.

    Args:
        message: The message to translate.

    Returns:
        The translated string, or *message* itself when no translation is
        available.

    Raises:
        TypeError: If ``message`` is not a string.

    Example:
        >>> gettext("Hello")
        'Hello'
    """
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    return _gettext.gettext(message)


def dgettext(domain: str, message: str) -> str:
    """Return the translated string for *message* in *domain*.

    Args:
        domain: The message domain to look up translations in.
        message: The message to translate.

    Returns:
        The translated string, or *message* itself when no translation is
        available.

    Raises:
        TypeError: If ``domain`` or ``message`` is not a string.

    See :func:`gettext.dgettext`.
    """
    if not isinstance(domain, str):
        raise TypeError("domain must be a string")
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    return _gettext.dgettext(domain, message)


def ngettext(singular: str, plural: str, n: int) -> str:
    """Return the translated string for *singular* or *plural* based on *n*.

    Args:
        singular: The singular form of the message.
        plural: The plural form of the message.
        n: The number used to select the singular or plural form.

    Returns:
        The translated singular or plural string.

    Raises:
        TypeError: If ``singular`` or ``plural`` is not a string, or ``n``
            is not an integer.

    See :func:`gettext.ngettext`.
    """
    if not isinstance(singular, str):
        raise TypeError("singular must be a string")
    if not isinstance(plural, str):
        raise TypeError("plural must be a string")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    return _gettext.ngettext(singular, plural, n)


def dngettext(domain: str, singular: str, plural: str, n: int) -> str:
    """Return the translated string for *singular* or *plural* in *domain* based on *n*.

    Args:
        domain: The message domain to look up translations in.
        singular: The singular form of the message.
        plural: The plural form of the message.
        n: The number used to select the singular or plural form.

    Returns:
        The translated singular or plural string.

    Raises:
        TypeError: If ``domain``, ``singular``, or ``plural`` is not a string,
            or ``n`` is not an integer.

    See :func:`gettext.dngettext`.
    """
    if not isinstance(domain, str):
        raise TypeError("domain must be a string")
    if not isinstance(singular, str):
        raise TypeError("singular must be a string")
    if not isinstance(plural, str):
        raise TypeError("plural must be a string")
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an int")
    return _gettext.dngettext(domain, singular, plural, n)


def textdomain(domain: Optional[str] = None) -> str:
    """Set or get the current message domain.

    Args:
        domain: The domain to set, or ``None`` to return the current domain.

    Returns:
        The current message domain after the optional change.

    Raises:
        TypeError: If ``domain`` is not a string or None.

    See :func:`gettext.textdomain`.
    """
    if domain is not None and not isinstance(domain, str):
        raise TypeError("domain must be a string or None")
    return _gettext.textdomain(domain)


def bindtextdomain(domain: str, localedir: Optional[str] = None) -> str:
    """Bind *domain* to the locale directory *localedir*.

    Args:
        domain: The message domain to bind.
        localedir: The directory containing locale data, or ``None`` to return
            the current binding without changing it.

    Returns:
        The bound localedir for *domain*.

    Raises:
        TypeError: If ``domain`` is not a string or ``localedir`` is not a
            string or None.

    See :func:`gettext.bindtextdomain`.
    """
    if not isinstance(domain, str):
        raise TypeError("domain must be a string")
    if localedir is not None and not isinstance(localedir, str):
        raise TypeError("localedir must be a string or None")
    return _gettext.bindtextdomain(domain, localedir)


def install(
    domain: str,
    localedir: Optional[str] = None,
    names: Optional[Container[str]] = None,
) -> None:
    """Install the :func:`gettext` function into Python's builtins namespace.

    After calling this, ``_`` (a common alias for :func:`gettext`) is bound in
    ``builtins`` so it can be used to mark strings for translation.

    Args:
        domain: The message domain to install translations for.
        localedir: The directory containing locale data.
        names: An optional iterable of builtin names to install.

    Raises:
        TypeError: If ``domain`` is not a string or ``names`` is not an
            iterable of strings or None.

    See :func:`gettext.install`.
    """
    if not isinstance(domain, str):
        raise TypeError("domain must be a string")
    if names is not None and not isinstance(names, Iterable):
        raise TypeError("names must be an iterable of strings or None")
    _gettext.install(domain, localedir=localedir, names=names)
