import unittest

from hostname_utils import (
    get_local_hostname,
    is_fully_qualified,
    is_valid_hostname,
    normalize_hostname,
    split_hostname,
)


class TestHostnameUtils(unittest.TestCase):
    def test_valid_hostnames(self):
        for hostname in [
            "example.com",
            "localhost",
            "my-host.example.org",
            "a.b.c",
            "EXAMPLE.COM",
            "sub.domain.co.uk",
        ]:
            self.assertTrue(is_valid_hostname(hostname), hostname)

    def test_fully_qualified_form_is_valid(self):
        self.assertTrue(is_valid_hostname("example.com."))

    def test_invalid_hostnames(self):
        for hostname in [
            "",
            "-example.com",
            "example-.com",
            "..",
            "ex*mple.com",
            "example..com",
            "-",
            "a" * 64 + ".com",
        ]:
            self.assertFalse(is_valid_hostname(hostname), hostname)

    def test_hostname_too_long_is_invalid(self):
        self.assertFalse(is_valid_hostname("a" * 254))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            is_valid_hostname(None)
        with self.assertRaises(TypeError):
            normalize_hostname(123)
        with self.assertRaises(TypeError):
            split_hostname(["example.com"])
        with self.assertRaises(TypeError):
            is_fully_qualified(b"example.com")

    def test_normalize_hostname(self):
        self.assertEqual(normalize_hostname("Example.COM."), "example.com")
        self.assertEqual(normalize_hostname("My-Host.ORG"), "my-host.org")
        self.assertEqual(normalize_hostname("example.com"), "example.com")

    def test_normalize_invalid_raises(self):
        with self.assertRaises(ValueError):
            normalize_hostname("-bad")

    def test_get_local_hostname(self):
        self.assertIsInstance(get_local_hostname(), str)

    def test_is_fully_qualified(self):
        self.assertTrue(is_fully_qualified("example.com."))
        self.assertTrue(is_fully_qualified("example.com"))
        self.assertFalse(is_fully_qualified("localhost"))
        self.assertFalse(is_fully_qualified(""))

    def test_split_hostname(self):
        self.assertEqual(split_hostname("example.com."), ["example", "com"])
        self.assertEqual(split_hostname("a.b.c"), ["a", "b", "c"])
        self.assertEqual(split_hostname("Example.Com"), ["Example", "Com"])

    def test_split_invalid_raises(self):
        with self.assertRaises(ValueError):
            split_hostname("-bad")


if __name__ == "__main__":
    unittest.main()
