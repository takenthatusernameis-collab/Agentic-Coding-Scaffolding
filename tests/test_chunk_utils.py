"""Tests for chunk_utils."""

from chunk_utils import (
    chunk,
    chunk_count,
    chunk_pad,
    chunked,
    chunks,
    even_chunks,
    ichunk,
    iter_chunked,
)


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


def test_chunk_count_basic():
    assert chunk_count([1, 2, 3, 4, 5], 2) == 3


def test_chunk_count_exact():
    assert chunk_count([1, 2, 3, 4], 2) == 2


def test_chunk_count_single():
    assert chunk_count([1, 2, 3], 10) == 1


def test_chunk_count_empty():
    assert chunk_count([], 3) == 0


def test_chunk_count_invalid_type():
    try:
        chunk_count([1, 2], "2")
        assert False
    except TypeError:
        pass


def test_chunk_count_invalid_value():
    try:
        chunk_count([1, 2], 0)
        assert False
    except ValueError:
        pass


def test_even_chunks_basic():
    assert even_chunks([1, 2, 3, 4, 5], 2) == [[1, 2, 3], [4, 5]]


def test_even_chunks_exact():
    assert even_chunks([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_even_chunks_more_than_items():
    assert even_chunks([1, 2], 5) == [[1], [2]]


def test_even_chunks_empty():
    assert even_chunks([], 3) == []


def test_even_chunks_one():
    assert even_chunks([1, 2, 3], 1) == [[1, 2, 3]]


def test_even_chunks_type_error():
    import pytest

    with pytest.raises(TypeError):
        even_chunks([1, 2], True)
    with pytest.raises(TypeError):
        even_chunks([1, 2], "2")


def test_even_chunks_value_error():
    import pytest

    with pytest.raises(ValueError):
        even_chunks([1, 2], 0)
    with pytest.raises(ValueError):
        even_chunks([1, 2], -1)


def test_chunk_pad_basic():
    assert chunk_pad([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5, None]]


def test_chunk_pad_exact():
    assert chunk_pad([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunk_pad_empty():
    assert chunk_pad([], 3) == []


def test_chunk_pad_custom_pad():
    assert chunk_pad([1, 2, 3], 4, pad_value=0) == [[1, 2, 3, 0]]


def test_chunk_pad_invalid_size_type():
    try:
        chunk_pad([1, 2, 3], "2")
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")


def test_chunk_pad_invalid_size_value():
    try:
        chunk_pad([1, 2, 3], 0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
