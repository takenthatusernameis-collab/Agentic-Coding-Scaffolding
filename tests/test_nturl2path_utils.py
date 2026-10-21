"""Tests for nturl2path_utils."""


from nturl2path_utils import pathname2url, url2pathname


def test_url2pathname_drive():
    assert url2pathname("///C:/foo/bar") == "C:\\foo\\bar"


def test_url2pathname_no_drive():
    assert url2pathname("/foo/bar") == "\\foo\\bar"


def test_pathname2url_drive():
    assert pathname2url("C:\\foo\\bar") == "///C:/foo/bar"


def test_roundtrip():
    path = "C:\\foo\\bar\\spam.foo"
    assert url2pathname(pathname2url(path)) == path
