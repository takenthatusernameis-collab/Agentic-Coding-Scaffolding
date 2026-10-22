"""Password hashing utilities wrapping the standard library :mod:`crypt` module.

The :mod:`crypt` module wraps the POSIX ``crypt(3)`` library call and the
associated salt generation.  It hashes a password with a salt and returns a
string that can be compared against a stored hash.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It adds the conveniences the standard
library leaves to the caller: a hash can be inspected without a password, the
method of a hash can be identified, and two hashes can be compared in constant
time.

.. note::

   The :mod:`crypt` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module, while the helpers that
   need no standard library keep working.
"""

from __future__ import annotations

import hmac
import warnings
from typing import Any, List, Optional

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
    "mksalt",
    "methods",
    "verify",
]

PathLike = str

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import crypt as _crypt
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _crypt = None  # type: ignore[assignment]


def _crypt_module() -> Any:
    if _crypt is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'crypt' module was removed in Python 3.13; "
            "use hashlib or a dedicated library such as bcrypt instead"
        )
    return _crypt


def is_available() -> bool:
    return _crypt is not None


def crypt(word: str, salt: str) -> str:
    if not isinstance(word, str):
        raise TypeError(f"word must be str, not {type(word).__name__}")
    if not isinstance(salt, str):
        raise TypeError(f"salt must be str, not {type(salt).__name__}")
    return str(_crypt_module().crypt(word, salt))


def mksalt(method: Any = None, *, rounds: Optional[int] = None) -> str:
    if method is not None and not hasattr(method, "name"):
        raise TypeError("method must be a crypt method")
    if rounds is not None and not isinstance(rounds, int):
        raise TypeError(f"rounds must be int, not {type(rounds).__name__}")
    return str(_crypt_module().mksalt(method, rounds=rounds))


def hash_password(word: str, method: Any = None, *, rounds: Optional[int] = None) -> str:
    return crypt(word, mksalt(method, rounds=rounds))


def identify_method(hashed: str) -> Optional[str]:
    if not isinstance(hashed, str):
        raise TypeError(f"hashed must be str, not {type(hashed).__name__}")
    if hashed.startswith("$"):
        parts = hashed.split("$")
        if len(parts) >= 2 and parts[1]:
            return parts[1]
    return None


def verify(word: str, hashed: str) -> bool:
    if not isinstance(word, str):
        raise TypeError(f"word must be str, not {type(word).__name__}")
    if not isinstance(hashed, str):
        raise TypeError(f"hashed must be str, not {type(hashed).__name__}")
    candidate = crypt(word, hashed)
    return hmac.compare_digest(candidate, hashed)


def methods() -> List[Any]:
    return list(_crypt_module().methods)


METHOD_BLOWFISH = getattr(_crypt, "METHOD_BLOWFISH", None) if _crypt is not None else None
METHOD_CRYPT = getattr(_crypt, "METHOD_CRYPT", None) if _crypt is not None else None
METHOD_MD5 = getattr(_crypt, "METHOD_MD5", None) if _crypt is not None else None
METHOD_SHA256 = getattr(_crypt, "METHOD_SHA256", None) if _crypt is not None else None
METHOD_SHA512 = getattr(_crypt, "METHOD_SHA512", None) if _crypt is not None else None
