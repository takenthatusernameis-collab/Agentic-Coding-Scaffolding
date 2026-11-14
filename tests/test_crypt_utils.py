"""Tests for crypt_utils."""

import unittest
import warnings

import crypt_utils


class TestExports(unittest.TestCase):
    def test_exports(self) -> None:
        for name in [
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
        ]:
            self.assertTrue(hasattr(crypt_utils, name), name)

    def test_is_available_returns_bool(self) -> None:
        self.assertIsInstance(crypt_utils.is_available(), bool)


class TestIdentifyMethod(unittest.TestCase):
    def test_sha512(self) -> None:
        self.assertEqual(crypt_utils.identify_method("$6$salt$hash"), "SHA512")

    def test_sha256(self) -> None:
        self.assertEqual(crypt_utils.identify_method("$5$salt$hash"), "SHA256")

    def test_md5(self) -> None:
        self.assertEqual(crypt_utils.identify_method("$1$salt$hash"), "MD5")

    def test_blowfish_variants(self) -> None:
        for prefix in ("$2a$", "$2b$", "$2y$"):
            self.assertEqual(crypt_utils.identify_method(prefix + "x"), "BLOWFISH")

    def test_unknown_returns_none(self) -> None:
        self.assertIsNone(crypt_utils.identify_method("plaintext"))

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            crypt_utils.identify_method(123)  # type: ignore[arg-type]


class TestIsHash(unittest.TestCase):
    def test_recognised_hash(self) -> None:
        self.assertTrue(crypt_utils.is_hash("$6$salt$hash"))

    def test_generic_dollar_prefix(self) -> None:
        self.assertTrue(crypt_utils.is_hash("$unknown"))

    def test_plaintext_is_not_hash(self) -> None:
        self.assertFalse(crypt_utils.is_hash("plaintext"))

    def test_non_string_raises(self) -> None:
        with self.assertRaises(TypeError):
            crypt_utils.is_hash(123)  # type: ignore[arg-type]


@unittest.skipUnless(crypt_utils.is_available(), "crypt not available")
class TestHashAndVerify(unittest.TestCase):
    def test_hash_password_returns_str(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            hashed = crypt_utils.hash_password("s3cret")
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, "s3cret")

    def test_verify_roundtrip(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            hashed = crypt_utils.hash_password("s3cret")
            self.assertTrue(crypt_utils.verify("s3cret", hashed))
            self.assertFalse(crypt_utils.verify("wrong", hashed))

    def test_hash_password_with_explicit_salt(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            salted = crypt_utils.hash_password("s3cret", "$6$fixedsalt")
        self.assertTrue(salted.startswith("$6$"))

    def test_hash_password_type_checks(self) -> None:
        with self.assertRaises(TypeError):
            crypt_utils.hash_password(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            crypt_utils.hash_password("pw", 123)  # type: ignore[arg-type]

    def test_verify_type_checks(self) -> None:
        with self.assertRaises(TypeError):
            crypt_utils.verify(123, "x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            crypt_utils.verify("pw", 123)  # type: ignore[arg-type]

    def test_methods_lists_available_methods(self) -> None:
        methods = crypt_utils.methods()
        self.assertIsInstance(methods, list)
        self.assertTrue(methods)


if __name__ == "__main__":
    unittest.main()
