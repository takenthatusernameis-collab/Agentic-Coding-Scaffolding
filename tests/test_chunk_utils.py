"""Tests for chunk_utils."""

from chunk_utils import chunk, chunked, chunks, ichunk, iter_chunked


def test_chunk_basic():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_exact():
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_size_larger():
    assert chunk([1, 2, 3], 10) == [[1, 2, 3]]


def test_chunk_empty():
    assert chunk([], 3) == []


def test_chunks_alias():
    assert chunks([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunked_alias():
    assert chunked([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_ichunk_lazy():
    result = list(ichunk([1, 2, 3, 4, 5], 2))
    assert result == [[1, 2], [3, 4], [5]]


def test_iter_chunked_alias():
    result = list(iter_chunked([1, 2, 3, 4], 2))
    assert result == [[1, 2], [3, 4]]


def test_chunk_invalid_size_type():
    try:
        chunk([1, 2], "2")
        assert False
    except TypeError:
        pass


def test_chunk_invalid_size_value():
    try:
        chunk([1, 2], 0)
        assert False
    except ValueError:
        pass


def test_chunk_negative_size():
    try:
        chunk([1, 2], -1)
        assert False
    except ValueError:
        pass
