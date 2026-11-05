"""Password hashing utilities wrapping the standard library :mod:`crypt`."""

from __future__ import annotations

try:
    import crypt as _crypt
    _CRYPT_AVAILABLE = True
except Exception:
    _crypt = None  # type: ignore[assignment]
    _CRYPT_AVAILABLE = False

__all__: list[str] = [
    "crypt",
    "mksalt",
    "METHOD_CRYPT",
    "METHOD_MD5",
    "METHOD_SHA256",
    "METHOD_SHA512",
    "METHOD_BLOWFISH",
    "hash_password",
    "verify",
    "identify_method",
    "is_hash",
    "methods",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`crypt` module is available."""
    return _CRYPT_AVAILABLE


if _CRYPT_AVAILABLE:
    METHOD_CRYPT = getattr(_crypt, "METHOD_CRYPT")
    METHOD_MD5 = getattr(_crypt, "METHOD_MD5")
    METHOD_SHA256 = getattr(_crypt, "METHOD_SHA256")
    METHOD_SHA512 = getattr(_crypt, "METHOD_SHA512")
    METHOD_BLOWFISH = getattr(_crypt, "METHOD_BLOWFISH")
    crypt = _crypt.crypt
    mksalt = _crypt.mksalt
else:
    METHOD_CRYPT = None
    METHOD_MD5 = None
    METHOD_SHA256 = None
    METHOD_SHA512 = None
    METHOD_BLOWFISH = None

    def crypt(word, salt=None):  # type: ignore[no-untyped-def]
        raise RuntimeError("crypt module is not available")

    def mksalt(method=None, *, rounds=None):  # type: ignore[no-untyped-def]
        raise RuntimeError("crypt module is not available")


def hash_password(password: str, salt: str | None = None, method=None) -> str:
    """Hash a password with a salt."""
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if salt is not None and not isinstance(salt, str):
        raise TypeError("salt must be a str or None")
    if salt is None:
        if not _CRYPT_AVAILABLE:
            raise RuntimeError("crypt module is not available")
        salt = mksalt(method)
    result = crypt(password, salt)
    return result


def verify(password: str, hashed: str) -> bool:
    """Verify a password against a hash using constant-time comparison."""
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    if not isinstance(hashed, str):
        raise TypeError("hashed must be a str")
    if not _CRYPT_AVAILABLE:
        raise RuntimeError("crypt module is not available")
    import hmac

    new_hash = crypt(password, hashed)
    try:
        return hmac.compare_digest(new_hash, hashed)
    except Exception:
        return new_hash == hashed


def identify_method(hashed: str) -> str | None:
    """Identify the method used to create a hash."""
    if not isinstance(hashed, str):
        raise TypeError("hashed must be a str")
    if hashed.startswith("$6$"):
        return "SHA512"
    if hashed.startswith("$5$"):
        return "SHA256"
    if hashed.startswith("$1$"):
        return "MD5"
    if hashed.startswith("$2b$") or hashed.startswith("$2y$") or hashed.startswith("$2a$"):
        return "BLOWFISH"
    return None


def is_hash(value: str) -> bool:
    """Return True if value looks like a hash."""
    if not isinstance(value, str):
        raise TypeError("value must be a str")
    return identify_method(value) is not None or value.startswith("$")


def methods() -> list:
    """List supported methods."""
    if not _CRYPT_AVAILABLE:
        return []
    result = []
    for name in ["METHOD_BLOWFISH", "METHOD_SHA512", "METHOD_SHA256", "METHOD_MD5", "METHOD_CRYPT"]:
        if hasattr(_crypt, name):
            result.append(getattr(_crypt, name))
    return result
