"""Tests for the :mod:`crypt_utils` wrapper."""

from __future__ import annotations

import pytest

import crypt_utils


def test_is_available() -> None:
    """``is_available`` reports whether the module ships."""
    result = crypt_utils.is_available()
    assert isinstance(result, bool)


def test_crypt_validates_its_arguments() -> None:
    """``crypt`` rejects arguments that are not text."""
    with pytest.raises(TypeError):
        crypt_utils.crypt(123, "salt")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        crypt_utils.crypt("word", 123)  # type: ignore[arg-type]


def test_mksalt_validates_its_arguments() -> None:
    """``mksalt`` rejects a method and a round count it cannot use."""
    with pytest.raises(TypeError):
        crypt_utils.mksalt("SHA512")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        crypt_utils.mksalt(None, rounds="many")  # type: ignore[arg-type]


def test_hash_password_validates_its_arguments() -> None:
    """``hash_password`` rejects a password that is not text."""
    with pytest.raises(TypeError):
        crypt_utils.hash_password(123)  # type: ignore[arg-type]


def test_verify_validates_its_arguments() -> None:
    """``verify`` rejects a password or a hash that is not text."""
    with pytest.raises(TypeError):
        crypt_utils.verify(123, "hash")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        crypt_utils.verify("word", 123)  # type: ignore[arg-type]


def test_identify_method_validates_its_argument() -> None:
    """``identify_method`` rejects a hash that is not text."""
    with pytest.raises(TypeError):
        crypt_utils.identify_method(123)  # type: ignore[arg-type]


def test_is_hash_validates_its_argument() -> None:
    """``is_hash`` rejects a value that is not text."""
    with pytest.raises(TypeError):
        crypt_utils.is_hash(123)  # type: ignore[arg-type]


def test_identify_method_reports_no_method_for_a_traditional_hash() -> None:
    """A hash without a marker was created with the traditional method."""
    assert crypt_utils.identify_method("lAx9dkenIAUIw") is None


def test_identify_method_reports_an_unknown_identifier() -> None:
    """An identifier the wrapper does not know is returned as it is."""
    assert crypt_utils.identify_method("$9$saltsalt$hash") == "9"


def test_is_hash_recognizes_a_traditional_hash() -> None:
    """A traditional hash has the length of thirteen characters."""
    assert crypt_utils.is_hash("lAx9dkenIAUIw")
    assert not crypt_utils.is_hash("too short")
    assert not crypt_utils.is_hash("$6$salt")


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_methods_lists_the_supported_methods() -> None:
    """``methods`` lists the methods the interpreter supports."""
    methods = crypt_utils.methods()
    assert isinstance(methods, list)
    assert methods
    for method in methods:
        assert hasattr(method, "name")
        assert hasattr(method, "ident")


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_mksalt_returns_a_salt_the_hash_carries() -> None:
    """A salt is the beginning of the hash that uses it."""
    salt = crypt_utils.mksalt()
    assert isinstance(salt, str)
    assert salt
    hashed = crypt_utils.crypt("secret", salt)
    assert hashed.startswith(salt)


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_hash_password_returns_a_hash_of_the_password() -> None:
    """``hash_password`` hashes the password with a new salt."""
    hashed = crypt_utils.hash_password("secret")
    assert isinstance(hashed, str)
    assert crypt_utils.verify("secret", hashed)
    assert not crypt_utils.verify("other", hashed)


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_hash_password_uses_the_method_it_is_given() -> None:
    """``hash_password`` hashes the password with the method it is given."""
    hashed = crypt_utils.hash_password("secret", crypt_utils.METHOD_MD5)
    assert crypt_utils.identify_method(hashed) == "MD5"
    assert crypt_utils.verify("secret", hashed)


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_hash_password_uses_the_rounds_it_is_given() -> None:
    """``hash_password`` hashes the password with the rounds it is given."""
    hashed = crypt_utils.hash_password("secret", crypt_utils.METHOD_SHA512, rounds=5000)
    assert "rounds=5000" in hashed
    assert crypt_utils.verify("secret", hashed)


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_mksalt_rejects_rounds_a_method_does_not_support() -> None:
    """The traditional method does not take a round count."""
    with pytest.raises(ValueError):
        crypt_utils.mksalt(crypt_utils.METHOD_CRYPT, rounds=1000)


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_verify_reports_a_wrong_password() -> None:
    """``verify`` reports a password that does not match the hash."""
    hashed = crypt_utils.hash_password("secret")
    assert crypt_utils.verify("secret", hashed)
    assert not crypt_utils.verify("wrong", hashed)
    assert not crypt_utils.verify("", hashed)


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_identify_method_reports_the_method_of_a_hash() -> None:
    """``identify_method`` reports the method a hash was created with."""
    hashed = crypt_utils.hash_password("secret", crypt_utils.METHOD_SHA512)
    assert crypt_utils.identify_method(hashed) == "SHA512"


@pytest.mark.skipif(not crypt_utils.is_available(), reason="crypt module not available")
def test_is_hash_recognizes_a_modular_hash() -> None:
    """A modular hash carries the marker of its method."""
    hashed = crypt_utils.hash_password("secret")
    assert crypt_utils.is_hash(hashed)


def test_degradation_without_module() -> None:
    """The helpers raise ``RuntimeError`` when the module is missing."""
    original = crypt_utils._crypt
    try:
        crypt_utils._crypt = None  # type: ignore[assignment]
        with pytest.raises(RuntimeError, match="crypt"):
            crypt_utils.crypt("word", "salt")
        with pytest.raises(RuntimeError, match="crypt"):
            crypt_utils.mksalt()
        with pytest.raises(RuntimeError, match="crypt"):
            crypt_utils.hash_password("word")
        with pytest.raises(RuntimeError, match="crypt"):
            crypt_utils.methods()
        with pytest.raises(RuntimeError, match="crypt"):
            crypt_utils.verify("word", "hash")
    finally:
        crypt_utils._crypt = original


def test_exports() -> None:
    """The module exports its public names."""
    for name in crypt_utils.__all__:
        assert hasattr(crypt_utils, name), name
