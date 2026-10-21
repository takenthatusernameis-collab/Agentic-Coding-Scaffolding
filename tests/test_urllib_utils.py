"""Tests for urllib_utils."""

import unittest
from urllib import parse as _urllib_parse

import urllib_utils
from urllib_utils import (
    build_url,
    defrag,
    join_url,
    parse_qs,
    parse_qsl,
    parse_url,
    quote,
    quote_plus,
    unquote,
    unquote_plus,
    unquote_to_bytes,
    urlencode,
    urlsplit,
    urlunsplit,
)


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(urllib_utils.__all__, sorted(set(urllib_utils.__all__)))

    def test_every_name_exists(self):
        for name in urllib_utils.__all__:
            self.assertTrue(hasattr(urllib_utils, name), name)


class TestParseUrl(unittest.TestCase):
    """Verify parsing a URL into its components."""

    def test_parse_url_matches_the_standard_library(self):
        self.assertEqual(parse_url("https://example.com:8080/path;params?q=1#frag"), _urllib_parse.urlparse("https://example.com:8080/path;params?q=1#frag"))

    def test_parse_url_reports_the_components(self):
        result = parse_url("https://user:pass@example.com:8080/path;params?key=value#fragment")
        self.assertEqual(result.scheme, "https")
        self.assertEqual(result.netloc, "user:pass@example.com:8080")
        self.assertEqual(result.path, "/path")
        self.assertEqual(result.params, "params")
        self.assertEqual(result.query, "key=value")
        self.assertEqual(result.fragment, "fragment")

    def test_parse_url_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            parse_url(42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            parse_url(None)  # type: ignore[arg-type]


class TestBuildUrl(unittest.TestCase):
    """Verify building a URL from its components."""

    def test_build_url_matches_the_standard_library(self):
        components = ["https", "example.com", "/path", "params", "q=1", "frag"]
        self.assertEqual(build_url(components), _urllib_parse.urlunparse(components))

    def test_build_url_accepts_a_tuple(self):
        self.assertEqual(
            build_url(("https", "example.com", "/path", "", "q=1", "")),
            "https://example.com/path?q=1",
        )

    def test_build_url_rejects_a_single_string(self):
        with self.assertRaises(TypeError):
            build_url("https://example.com")  # type: ignore[arg-type]

    def test_build_url_rejects_the_wrong_number_of_components(self):
        with self.assertRaises(ValueError):
            build_url(["https", "example.com", "/path"])
        with self.assertRaises(ValueError):
            build_url(["https", "example.com", "/path", "", "q=1", "frag", "extra"])

    def test_build_url_rejects_a_non_string_component(self):
        with self.assertRaises(TypeError):
            build_url(["https", "example.com", "/path", "", "q=1", 42])  # type: ignore[list-item]


class TestUrlsplit(unittest.TestCase):
    """Verify splitting a URL without separating the parameters."""

    def test_urlsplit_matches_the_standard_library(self):
        self.assertEqual(urlsplit("https://example.com/path;params?q=1#frag"), _urllib_parse.urlsplit("https://example.com/path;params?q=1#frag"))

    def test_urlsplit_reports_the_components(self):
        result = urlsplit("https://example.com/path?q=1#frag")
        self.assertEqual(result.scheme, "https")
        self.assertEqual(result.netloc, "example.com")
        self.assertEqual(result.path, "/path")
        self.assertEqual(result.query, "q=1")
        self.assertEqual(result.fragment, "frag")

    def test_urlsplit_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            urlsplit(None)  # type: ignore[arg-type]


class TestUrlunsplit(unittest.TestCase):
    """Verify building a URL from its split components."""

    def test_urlunsplit_matches_the_standard_library(self):
        components = ["https", "example.com", "/path", "q=1", "frag"]
        self.assertEqual(urlunsplit(components), _urllib_parse.urlunsplit(components))

    def test_urlunsplit_rejects_the_wrong_number_of_components(self):
        with self.assertRaises(ValueError):
            urlunsplit(["https", "example.com", "/path"])


class TestJoinUrl(unittest.TestCase):
    """Verify joining a base URL with a relative URL."""

    def test_join_url_resolves_a_relative_reference(self):
        self.assertEqual(
            join_url("https://example.com/base/", "extra"),
            _urllib_parse.urljoin("https://example.com/base/", "extra"),
        )

    def test_join_url_ignores_the_base_for_an_absolute_url(self):
        self.assertEqual(
            join_url("https://example.com/base/", "https://other.com/absolute"),
            "https://other.com/absolute",
        )

    def test_join_url_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            join_url(42, "extra")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            join_url("https://example.com/", None)  # type: ignore[arg-type]


class TestQuote(unittest.TestCase):
    """Verify percent-encoding a string."""

    def test_quote_matches_the_standard_library(self):
        self.assertEqual(quote("/a b/c"), _urllib_parse.quote("/a b/c"))
        self.assertEqual(quote("a&b=c"), _urllib_parse.quote("a&b=c"))

    def test_quote_leaves_the_safe_characters_untouched(self):
        self.assertEqual(quote("/a b/c", safe="/"), "/a%20b/c")

    def test_quote_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            quote(42)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            quote("a b", safe=42)  # type: ignore[arg-type]


class TestQuotePlus(unittest.TestCase):
    """Verify percent-encoding a string with plus signs for spaces."""

    def test_quote_plus_matches_the_standard_library(self):
        self.assertEqual(quote_plus("a b c"), _urllib_parse.quote_plus("a b c"))

    def test_quote_plus_replaces_spaces_with_plus_signs(self):
        self.assertEqual(quote_plus("a b c"), "a+b+c")

    def test_quote_plus_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            quote_plus(None)  # type: ignore[arg-type]


class TestUnquote(unittest.TestCase):
    """Verifying decoding a percent-encoded string."""

    def test_unquote_matches_the_standard_library(self):
        self.assertEqual(unquote("/a%20b/c"), _urllib_parse.unquote("/a%20b/c"))

    def test_unquote_decodes_percent_encoded_text(self):
        self.assertEqual(unquote("a%20b%20c"), "a b c")

    def test_unquote_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            unquote(42)  # type: ignore[arg-type]


class TestUnquotePlus(unittest.TestCase):
    """Verify decoding a percent-encoded string with plus signs as spaces."""

    def test_unquote_plus_matches_the_standard_library(self):
        self.assertEqual(unquote_plus("a+b+c"), _urllib_parse.unquote_plus("a+b+c"))

    def test_unquote_plus_turns_plus_signs_into_spaces(self):
        self.assertEqual(unquote_plus("a+b+c"), "a b c")

    def test_unquote_plus_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            unquote_plus(None)  # type: ignore[arg-type]


class TestUnquoteToBytes(unittest.TestCase):
    """Verify decoding a percent-encoded string into bytes."""

    def test_unquote_to_bytes_matches_the_standard_library(self):
        self.assertEqual(unquote_to_bytes("a%20b"), _urllib_parse.unquote_to_bytes("a%20b"))

    def test_unquote_to_bytes_returns_bytes(self):
        self.assertIsInstance(unquote_to_bytes("a%20b"), bytes)

    def test_unquote_to_bytes_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            unquote_to_bytes(42)  # type: ignore[arg-type]


class TestUrlencode(unittest.TestCase):
    """Verify encoding a query into a string."""

    def test_urlencode_matches_the_standard_library(self):
        self.assertEqual(
            urlencode({"q": "a b", "n": 1}), _urllib_parse.urlencode({"q": "a b", "n": 1})
        )
        self.assertEqual(
            urlencode([("q", "a b"), ("n", "1")]),
            _urllib_parse.urlencode([("q", "a b"), ("n", "1")]),
        )

    def test_urlencode_encodes_spaces_as_plus_signs_by_default(self):
        self.assertEqual(urlencode({"q": "a b"}), "q=a+b")

    def test_urlencode_accepts_a_sequence_of_pairs(self):
        self.assertEqual(urlencode([("a", "1"), ("b", "2")]), "a=1&b=2")

    def test_urlencode_rejects_bad_arguments(self):
        with self.assertRaises(TypeError):
            urlencode("a=1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            urlencode({"a": 1}, safe=42)  # type: ignore[arg-type]


class TestParseQs(unittest.TestCase):
    """Verify parsing a query string into names and lists of values."""

    def test_parse_qs_matches_the_standard_library(self):
        self.assertEqual(parse_qs("a=1&b=2&a=3"), _urllib_parse.parse_qs("a=1&b=2&a=3"))

    def test_parse_qs_returns_lists_of_values(self):
        self.assertEqual(parse_qs("a=1&a=2&b=3"), {"a": ["1", "2"], "b": ["3"]})

    def test_parse_qs_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            parse_qs(42)  # type: ignore[arg-type]


class TestParseQsl(unittest.TestCase):
    """Verify parsing a query string into name/value pairs."""

    def test_parse_qsl_matches_the_standard_library(self):
        self.assertEqual(parse_qsl("a=1&b=2"), _urllib_parse.parse_qsl("a=1&b=2"))

    def test_parse_qsl_returns_pairs(self):
        self.assertEqual(parse_qsl("a=1&a=2&b=3"), [("a", "1"), ("a", "2"), ("b", "3")])

    def test_parse_qsl_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            parse_qsl(None)  # type: ignore[arg-type]


class TestDefrag(unittest.TestCase):
    """Verify removing the fragment from a URL."""

    def test_defrag_matches_the_standard_library(self):
        self.assertEqual(defrag("https://example.com/path#frag"), _urllib_parse.urldefrag("https://example.com/path#frag"))

    def test_defrag_returns_the_url_and_the_fragment(self):
        self.assertEqual(
            defrag("https://example.com/path#frag"),
            ("https://example.com/path", "frag"),
        )

    def test_defrag_returns_none_for_a_missing_fragment(self):
        self.assertEqual(defrag("https://example.com/path"), ("https://example.com/path", None))

    def test_defrag_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            defrag(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
