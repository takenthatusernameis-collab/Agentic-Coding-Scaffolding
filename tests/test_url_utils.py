"""Tests for url_utils module."""

import unittest

from url_utils import (
    add_query_param,
    build_url,
    extract_domain,
    get_query_param,
    get_query_params,
    is_valid_url,
    remove_query_param,
)


class TestIsValidUrl(unittest.TestCase):
    def test_valid_http(self) -> None:
        self.assertTrue(is_valid_url("http://example.com"))

    def test_valid_https(self) -> None:
        self.assertTrue(is_valid_url("https://example.com/path"))

    def test_valid_with_port(self) -> None:
        self.assertTrue(is_valid_url("http://example.com:8080"))

    def test_missing_scheme(self) -> None:
        self.assertFalse(is_valid_url("example.com/path"))

    def test_missing_domain(self) -> None:
        self.assertFalse(is_valid_url("http://"))

    def test_empty_string(self) -> None:
        self.assertFalse(is_valid_url(""))

    def test_scheme_restriction_allowed(self) -> None:
        self.assertTrue(is_valid_url("https://example.com", schemes=["https"]))

    def test_scheme_restriction_not_allowed(self) -> None:
        self.assertFalse(is_valid_url("http://example.com", schemes=["https"]))

    def test_ftp_scheme(self) -> None:
        self.assertTrue(is_valid_url("ftp://example.com"))


class TestExtractDomain(unittest.TestCase):
    def test_extract_domain_basic(self) -> None:
        self.assertEqual(extract_domain("https://example.com/path"), "example.com")

    def test_extract_domain_with_subdomain(self) -> None:
        self.assertEqual(extract_domain("https://api.sub.example.com"), "api.sub.example.com")

    def test_extract_domain_with_port(self) -> None:
        self.assertEqual(extract_domain("http://example.com:8080"), "example.com")

    def test_extract_domain_no_hostname(self) -> None:
        with self.assertRaises(ValueError):
            extract_domain("not-a-url")


class TestGetQueryParams(unittest.TestCase):
    def test_get_params_basic(self) -> None:
        params = get_query_params("https://example.com?name=alice&age=30")
        self.assertEqual(params, {"name": "alice", "age": "30"})

    def test_get_params_empty(self) -> None:
        self.assertEqual(get_query_params("https://example.com"), {})

    def test_get_params_blank_values(self) -> None:
        params = get_query_params("https://example.com?empty=&full=yes")
        self.assertEqual(params, {"empty": "", "full": "yes"})

    def test_get_params_duplicate_uses_first(self) -> None:
        params = get_query_params("https://example.com?color=red&color=blue")
        self.assertEqual(params["color"], "red")


class TestGetQueryParam(unittest.TestCase):
    def test_get_param_exists(self) -> None:
        self.assertEqual(get_query_param("https://example.com?q=test&page=2", "q"), "test")

    def test_get_param_missing(self) -> None:
        self.assertIsNone(get_query_param("https://example.com?q=test", "missing"))


class TestAddQueryParam(unittest.TestCase):
    def test_add_new_param(self) -> None:
        result = add_query_param("https://example.com", "key", "value")
        self.assertIn("key=value", result)

    def test_add_param_preserves_existing(self) -> None:
        result = add_query_param("https://example.com?a=1", "b", "2")
        self.assertIn("a=1", result)
        self.assertIn("b=2", result)

    def test_add_param_overwrites(self) -> None:
        result = add_query_param("https://example.com?a=1", "a", "2")
        self.assertIn("a=2", result)

    def test_add_param_int_value(self) -> None:
        result = add_query_param("https://example.com", "count", 42)
        self.assertIn("count=42", result)


class TestRemoveQueryParam(unittest.TestCase):
    def test_remove_existing(self) -> None:
        result = remove_query_param("https://example.com?a=1&b=2", "a")
        self.assertNotIn("a=1", result)
        self.assertIn("b=2", result)

    def test_remove_missing_no_change(self) -> None:
        result = remove_query_param("https://example.com?a=1", "b")
        self.assertIn("a=1", result)

    def test_remove_last_param(self) -> None:
        result = remove_query_param("https://example.com?a=1", "a")
        self.assertNotIn("a=1", result)
        self.assertNotIn("?", result)


class TestBuildUrl(unittest.TestCase):
    def test_build_basic(self) -> None:
        self.assertEqual(build_url(scheme="https", domain="example.com"), "https://example.com")

    def test_build_with_path(self) -> None:
        url = build_url(scheme="https", domain="example.com", path="/api/v1")
        self.assertEqual(url, "https://example.com/api/v1")

    def test_build_with_port(self) -> None:
        url = build_url(scheme="http", domain="example.com", port=8080)
        self.assertEqual(url, "http://example.com:8080")

    def test_build_with_params(self) -> None:
        url = build_url(
            scheme="https", domain="example.com", path="/search", params={"q": "test", "n": 10}
        )
        self.assertIn("q=test", url)
        self.assertIn("n=10", url)

    def test_build_empty_domain_raises(self) -> None:
        with self.assertRaises(ValueError):
            build_url(domain="")

    def test_build_default_scheme(self) -> None:
        url = build_url(domain="example.com")
        self.assertTrue(url.startswith("https://"))


if __name__ == "__main__":
    unittest.main()
