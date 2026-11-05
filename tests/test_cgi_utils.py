"""Tests for cgi_utils."""

import cgi_utils


def test_exports():
    assert hasattr(cgi_utils, "FieldStorage")
    assert hasattr(cgi_utils, "MiniFieldStorage")
    assert hasattr(cgi_utils, "escape")
    assert hasattr(cgi_utils, "parse")
    assert hasattr(cgi_utils, "parse_header")
    assert hasattr(cgi_utils, "parse_multipart")
    assert hasattr(cgi_utils, "parse_qs")
    assert hasattr(cgi_utils, "parse_qsl")
    assert hasattr(cgi_utils, "is_available")
    assert cgi_utils.is_available() is True
