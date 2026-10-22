"""Password hashing utilities wrapping the standard library :mod:`crypt` module.

The :mod:`crypt` module wraps the POSIX ``crypt(3)`` library call and the
associated salt generation.  It hashes a password with a salt and returns the
string that can be compared with a stored hash.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It adds the conveniences the standard
library leaves to the caller: a password can be compared with a stored hash in
constant time, the method of a hash can be identified without the password, the
methods the interpreter supports can be listed, and a salt is generated together
with the hash that uses it.

.. note::

   The :mod:`crypt` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers that hash a password
   raise a :class:`RuntimeError` that names the missing module, while the
   helpers that need no standard library keep working.
"""

from __future__ import annotations

import hmac
import warnings
from typing import Any, Dict, List, Optional

__all__ = [
    "METHOD_BLOWFISH",
    "METHOD_CRYPT",
    "METHOD_MD5",
    "METHOD_SHA256",
    "METHOD_SHA512",
    "crypt",
    "hash_password",
    "identify_method",
    "is_available",
    "is_hash",
    "mksalt",
    "methods",
    "verify",
]

#: The names of the modular crypt methods, by the identifier of the method.
METHOD_NAMES: Dict[str, str] = {
    "1": "MD5",
    "2": "BLOWFISH",
    "2a": "BLOWFISH",
    "2b": "BLOWFISH",
    "2y": "BLOWFISH",
    "5": "SHA256",
    "6": "SHA512",
}

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import crypt as _crypt
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _crypt = None  # type: ignore[assignment]


def _crypt_module() -> Any:
    """Return the standard library ``crypt`` module.

    Returns:
        The imported :mod:`crypt` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``crypt`` module.
    """
    if _crypt is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'crypt' module was removed in Python 3.13; "
            "use hashlib or a dedicated library such as bcrypt instead"
        )
    return _crypt


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for every other type.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as text.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str, not {type(value).__name__}")
    return value


def _require_method(value: Any) -> Any:
    """Return *value* as a crypt method, raising ``TypeError`` for other values.

    Args:
        value: The value to check.

    Returns:
        The value as a crypt method.

    Raises:
        TypeError: If *value* is not a crypt method.
    """
    if not all(hasattr(value, attribute) for attribute in ("name", "ident")):
        raise TypeError("method must be a crypt method")
    return value


def is_available() -> bool:
    """Report whether the interpreter ships the standard library ``crypt`` module.

    Returns:
        ``True`` when the module is importable, ``False`` otherwise.
    """
    return _crypt is not None


def methods() -> List[Any]:
    """Return the hashing methods the interpreter supports.

    The list starts with the strongest method the interpreter supports.

    Returns:
        The methods of the standard library, as a list.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``crypt`` module.
    """
    return list(_crypt_module().methods)


def crypt(word: str, salt: str) -> str:
    """Hash *word* with *salt*.

    Args:
        word: The password to hash.
        salt: The salt to hash the password with, as returned by :func:`mksalt`.

    Returns:
        The hash of the password, with the salt in front of it.

    Raises:
        TypeError: If *word* or *salt* is not a string.
        RuntimeError: If the interpreter no longer ships the ``crypt`` module.
    """
    _require_text(word, "word")
    _require_text(salt, "salt")
    return str(_crypt_module().crypt(word, salt))


def mksalt(method: Any = None, *, rounds: Optional[int] = None) -> str:
    """Return a new salt for *method*.

    Args:
        method: The method to create the salt for.  The strongest method the
            interpreter supports is used when no method is given.
        rounds: The number of rounds the method should use.  Only the SHA-2 and
            the Blowfish methods support it.

    Returns:
        A new salt.

    Raises:
        TypeError: If *method* is not a crypt method or *rounds* is not an
            integer.
        ValueError: If *rounds* is out of the range of the method.
        RuntimeError: If the interpreter no longer ships the ``crypt`` module.
    """
    if method is not None:
        _require_method(method)
    if rounds is not None and not isinstance(rounds, int):
        raise TypeError(f"rounds must be int, not {type(rounds).__name__}")
    return str(_crypt_module().mksalt(method, rounds=rounds))


def hash_password(word: str, method: Any = None, *, rounds: Optional[int] = None) -> str:
    """Hash *word* with a new salt.

    Args:
        word: The password to hash.
        method: The method to hash the password with.  The strongest method the
            interpreter supports is used when no method is given.
        rounds: The number of rounds the method should use.  Only the SHA-2 and
            the Blowfish methods support it.

    Returns:
        The hash of the password, with the salt in front of it.

    Raises:
        TypeError: If *word* is not a string, *method* is not a crypt method, or
            *rounds* is not an integer.
        ValueError: If *rounds* is out of the range of the method.
        RuntimeError: If the interpreter no longer ships the ``crypt`` module.
    """
    _require_text(word, "word")
    return crypt(word, mksalt(method, rounds=rounds))


def verify(word: str, hashed: str) -> bool:
    """Report whether *word* matches *hashed*.

    The comparison takes the same time for every word, so it does not leak how
    much of the hash matched.

    Args:
        word: The password to check.
        hashed: The hash to check the password against.

    Returns:
        ``True`` when the password matches the hash, ``False`` otherwise.

    Raises:
        TypeError: If *word* or *hashed* is not a string.
        RuntimeError: If the interpreter no longer ships the ``crypt`` module.
    """
    _require_text(word, "word")
    _require_text(hashed, "hashed")
    candidate = crypt(word, hashed)
    return hmac.compare_digest(candidate.encode("utf-8"), hashed.encode("utf-8"))


def identify_method(hashed: str) -> Optional[str]:
    """Return the name of the method a hash was created with.

    Args:
        hashed: The hash to inspect.

    Returns:
        The name of the method, such as ``"SHA512"``, or ``None`` when the hash
        was created with the traditional method, which carries no marker.
    """
    _require_text(hashed, "hashed")
    if not hashed.startswith("$"):
        return None
    parts = hashed.split("$")
    if len(parts) < 3 or not parts[1]:
        return None
    return METHOD_NAMES.get(parts[1], parts[1])


def is_hash(hashed: str) -> bool:
    """Report whether *hashed* looks like a crypt hash.

    Args:
        hashed: The value to inspect.

    Returns:
        ``True`` when the value carries the marker of a modular method or has
        the length of a traditional hash, ``False`` otherwise.
    """
    _require_text(hashed, "hashed")
    if hashed.startswith("$"):
        parts = hashed.split("$")
        return len(parts) >= 4 and bool(parts[1])
    return len(hashed) == 13


METHOD_BLOWFISH = getattr(_crypt, "METHOD_BLOWFISH", None) if _crypt is not None else None
METHOD_CRYPT = getattr(_crypt, "METHOD_CRYPT", None) if _crypt is not None else None
METHOD_MD5 = getattr(_crypt, "METHOD_MD5", None) if _crypt is not None else None
METHOD_SHA256 = getattr(_crypt, "METHOD_SHA256", None) if _crypt is not None else None
METHOD_SHA512 = getattr(_crypt, "METHOD_SHA512", None) if _crypt is not None else None
