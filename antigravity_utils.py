"""Antigravity utilities wrapping the standard library :mod:`antigravity` module.

The standard library module computes the geohash of a coordinate with the
Munroe algorithm of https://xkcd.com/426/ and opens the XKCD comic about
Python in a browser.

The standard library module opens a browser when it is imported, so this
wrapper does not import it: the algorithm of the standard library is
re-implemented with :mod:`hashlib`, and a browser is only started by
:func:`fly`.  Every helper validates its arguments before the computation
starts, so a caller gets a clear :class:`TypeError` or :class:`ValueError`
instead of an opaque failure.

The module is pure computation, with the single exception of :func:`fly`,
which asks the browser of the system to open a page.
"""

from __future__ import annotations

import hashlib
import webbrowser

__all__: list[str] = [
    "XKCD_URL",
    "fly",
    "geohash",
    "get_xkcd_url",
]

#: The address of the XKCD comic about Python.
XKCD_URL = "https://xkcd.com/353/"

#: The number of hexadecimal characters of the digest that carry a coordinate.
_DIGEST_HALF = 16


def _require_coordinate(value: object, name: str) -> float:
    """Return *value* when it is a finite number.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value, as a float.

    Raises:
        TypeError: If the value is not a number.
        ValueError: If the value is not finite.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be an int or a float, got {type(value).__name__}")
    number = float(value)
    if number != number or number in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be a finite number")
    return number


def _require_datedow(value: object) -> bytes:
    """Return *value* when it is the bytes the algorithm hashes.

    Args:
        value: The value to check.

    Returns:
        The bytes to hash.

    Raises:
        TypeError: If the value is not a bytes object.
    """
    if not isinstance(value, bytes):
        raise TypeError(f"datedow must be bytes, got {type(value).__name__}")
    return value


def _md5_hexdigest(data: bytes) -> str:
    """Return the hexadecimal digest of *data*.

    The digest is computed for a lookup, never for a security decision, so
    the call asks the standard library for a digest that is not used for
    security.  Builds of the standard library that do not know the flag fall
    back to the plain digest.
    """
    try:
        return hashlib.md5(data, usedforsecurity=False).hexdigest()
    except (TypeError, ValueError):  # pragma: no cover - depends on the build
        return hashlib.md5(data).hexdigest()


def _fraction(digest: str) -> str:
    """Return the fraction a digest carries.

    The standard library reads the first half of the digest as a hexadecimal
    fraction and writes the digits that follow the leading zero.
    """
    return ("%f" % float.fromhex("0." + digest))[1:]


def geohash(latitude: float, longitude: float, datedow: bytes) -> str:
    """Return the geohash of a coordinate.

    The geohash is computed with the Munroe algorithm of https://xkcd.com/426/:
    the digest of *datedow* carries the fractions of the coordinate.

    Args:
        latitude: The latitude of the coordinate.
        longitude: The longitude of the coordinate.
        datedow: The bytes that are hashed to compute the geohash.

    Returns:
        The geohash of the coordinate, for example ``"37.857713 -122.544543"``.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If a coordinate is not a finite number.
    """
    lat = _require_coordinate(latitude, "latitude")
    lon = _require_coordinate(longitude, "longitude")
    data = _require_datedow(datedow)
    digest = _md5_hexdigest(data)
    first = _fraction(digest[:_DIGEST_HALF])
    second = _fraction(digest[_DIGEST_HALF:])
    return f"{int(lat)}{first} {int(lon)}{second}"


def get_xkcd_url() -> str:
    """Return the address of the XKCD comic about Python.

    Returns:
        The address of the comic.
    """
    return XKCD_URL


def fly() -> str:
    """Open the XKCD comic about Python in a browser.

    The browser of the system is asked to open the page, and the address of
    the comic is returned, so a caller that only wants the address uses
    :func:`get_xkcd_url` instead.

    Returns:
        The address of the comic, the one that was opened.
    """
    url = get_xkcd_url()
    webbrowser.open(url)
    return url
