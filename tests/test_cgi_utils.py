"""Tests for cgi_utils."""

from __future__ import annotations

import io
from unittest import mock

import pytest

import cgi_utils


def test_is_available():
    result = cgi_utils.is_available()
    assert isinstance(result, bool)


def test_escape_basic():
    try:
        assert cgi_utils.escape("<b>hi</b>") == "&lt;b&gt;hi&lt;/b&gt;"
        assert cgi_utils.escape("a&b") == "a&amp;b"
        assert cgi_utils.escape('"hi"', quote=True) == '&quot;hi&quot;'
    except RuntimeError:
        if not cgi_utils.is_available():
            raise


def test_escape_validation():
    with pytest.raises(TypeError):
        cgi_utils.escape(123)  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.escape("<b>", quote=1)  # type: ignore


def test_parse_header():
    try:
        key, pdict = cgi_utils.parse_header("text/plain; charset=utf-8")
        assert key == "text/plain"
        assert "charset" in pdict
    except RuntimeError:
        if not cgi_utils.is_available():
            raise


def test_parse_header_validation():
    with pytest.raises(TypeError):
        cgi_utils.parse_header(123)  # type: ignore


def test_parse_qs():
    try:
        result = cgi_utils.parse_qs("a=1&b=2")
        assert result["a"] == ["1"]
        assert result["b"] == ["2"]
    except RuntimeError:
        if not cgi_utils.is_available():
            raise


def test_parse_qs_validation():
    with pytest.raises(TypeError):
        cgi_utils.parse_qs(123)  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_qs("a=1", keep_blank_values="x")  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_qs("a=1", strict_parsing="x")  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_qs("a=1", encoding=123)  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_qs("a=1", errors=123)  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_qs("a=1", max_num_fields="x")  # type: ignore
    with pytest.raises(ValueError):
        cgi_utils.parse_qs("a=1", max_num_fields=0)
    with pytest.raises(TypeError):
        cgi_utils.parse_qs("a=1", separator=123)  # type: ignore


def test_parse_qsl():
    try:
        result = cgi_utils.parse_qsl("a=1&b=2")
        assert ("a", "1") in result
    except RuntimeError:
        if not cgi_utils.is_available():
            raise


def test_parse_qsl_validation():
    with pytest.raises(TypeError):
        cgi_utils.parse_qsl(123)  # type: ignore


def test_parse():
    try:
        result = cgi_utils.parse(environ={"QUERY_STRING": "a=1"})
        assert "a" in result
    except RuntimeError:
        if not cgi_utils.is_available():
            raise


def test_parse_validation():
    with pytest.raises(TypeError):
        cgi_utils.parse(environ="bad")  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse(keep_blank_values="x")  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse(strict_parsing="x")  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse(separator=123)  # type: ignore


def test_parse_multipart_validation():
    with pytest.raises(TypeError):
        cgi_utils.parse_multipart(io.BytesIO(b""), "bad")  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_multipart(io.BytesIO(b""), {}, encoding=123)  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_multipart(io.BytesIO(b""), {}, errors=123)  # type: ignore
    with pytest.raises(TypeError):
        cgi_utils.parse_multipart(io.BytesIO(b""), {}, separator=123)  # type: ignore


def test_degradation_when_missing():
    with mock.patch.object(cgi_utils, "_cgi", None):
        with pytest.raises(RuntimeError, match="cgi.*removed"):
            cgi_utils.parse_header("x")
        with pytest.raises(RuntimeError, match="cgi.*removed"):
            cgi_utils.parse()
