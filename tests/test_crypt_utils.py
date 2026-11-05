"""Tests for crypt_utils."""

import crypt_utils


def test_exports():
    for name in ["crypt", "mksalt", "METHOD_CRYPT", "METHOD_MD5", "METHOD_SHA256",
                 "METHOD_SHA512", "METHOD_BLOWFISH", "hash_password", "verify",
                 "identify_method", "is_hash", "methods", "is_available"]:
        assert hasattr(crypt_utils, name)
