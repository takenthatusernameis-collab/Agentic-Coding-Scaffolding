"""Tests for pathlib_utils."""


from pathlib_utils import (
    ensure_dir,
    exists,
    glob,
    is_dir,
    is_file,
    join,
    parent,
    read_text,
    rglob,
    stem,
    suffix,
    write_text,
)


def test_join(tmp_path):
    assert join(tmp_path, "a", "b.txt") == tmp_path / "a" / "b.txt"


def test_ensure_dir(tmp_path):
    d = ensure_dir(tmp_path / "nested" / "dir")
    assert d.is_dir()
    assert is_dir(d)


def test_write_read_text(tmp_path):
    p = tmp_path / "f.txt"
    n = write_text(p, "hello")
    assert n == 5
    assert read_text(p) == "hello"
    assert exists(p)
    assert is_file(p)


def test_glob_rglob(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.txt").write_text("y")
    assert [p.name for p in glob(tmp_path, "*.txt")] == ["a.txt"]
    assert sorted(p.name for p in rglob(tmp_path, "*.txt")) == ["a.txt", "b.txt"]


def test_suffix_stem_parent(tmp_path):
    p = tmp_path / "foo.bar.txt"
    assert suffix(p) == ".txt"
    assert stem(p) == "foo.bar"
    assert parent(p) == tmp_path
