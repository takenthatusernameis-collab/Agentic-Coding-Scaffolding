"""Tests for array_utils."""

from array import array

from array_utils import (
    array_append,
    array_buffer_info,
    array_byteswap,
    array_count,
    array_create,
    array_extend,
    array_fromlist,
    array_index,
    array_insert,
    array_pop,
    array_remove,
    array_reverse,
    array_tolist,
)


def test_array_create():
    a = array_create("i", [1, 2, 3])
    assert isinstance(a, array)
    assert list(a) == [1, 2, 3]


def test_array_create_empty():
    a = array_create("i")
    assert isinstance(a, array)
    assert len(a) == 0


def test_array_fromlist():
    a = array_fromlist("i", [1, 2, 3])
    assert list(a) == [1, 2, 3]


def test_array_tolist():
    a = array("i", [1, 2, 3])
    assert array_tolist(a) == [1, 2, 3]


def test_array_append():
    a = array("i", [1, 2])
    array_append(a, 3)
    assert list(a) == [1, 2, 3]


def test_array_extend():
    a = array("i", [1, 2])
    array_extend(a, [3, 4])
    assert list(a) == [1, 2, 3, 4]


def test_array_insert():
    a = array("i", [1, 3])
    array_insert(a, 1, 2)
    assert list(a) == [1, 2, 3]


def test_array_pop():
    a = array("i", [1, 2, 3])
    assert array_pop(a) == 3
    assert array_pop(a, 0) == 1


def test_array_remove():
    a = array("i", [1, 2, 3])
    array_remove(a, 2)
    assert list(a) == [1, 3]


def test_array_reverse():
    a = array("i", [1, 2, 3])
    array_reverse(a)
    assert list(a) == [3, 2, 1]


def test_array_buffer_info():
    a = array("i", [1, 2, 3])
    info = array_buffer_info(a)
    assert isinstance(info, tuple)
    assert len(info) == 2


def test_array_byteswap():
    a = array("H", [1, 2])
    array_byteswap(a)


def test_array_count():
    a = array("i", [1, 2, 2, 3])
    assert array_count(a, 2) == 2


def test_array_index():
    a = array("i", [1, 2, 2, 3])
    assert array_index(a, 2) == 1
    assert array_index(a, 2, 2) == 2
    assert array_index(a, 2, 0, 3) == 1


def test_array_create_rejects_non_string_typecode():
    import pytest

    from array_utils import array_create

    with pytest.raises(TypeError):
        array_create(123)


def test_array_create_rejects_string_initial():
    import pytest

    from array_utils import array_create

    with pytest.raises(TypeError):
        array_create("i", "abc")


def test_array_fromlist_rejects_invalid():
    import pytest

    from array_utils import array_fromlist

    with pytest.raises(TypeError):
        array_fromlist(123, [1, 2])
    with pytest.raises(TypeError):
        array_fromlist("i", (1, 2))


def test_array_tolist_rejects_non_array():
    import pytest

    from array_utils import array_tolist

    with pytest.raises(TypeError):
        array_tolist([1, 2, 3])


def test_array_append_rejects_non_array():
    import pytest

    from array_utils import array_append

    with pytest.raises(TypeError):
        array_append([], 1)


def test_array_extend_rejects_string():
    from array import array

    import pytest

    from array_utils import array_extend

    a = array("i", [1])
    with pytest.raises(TypeError):
        array_extend(a, "23")


def test_array_insert_rejects_bad_index():
    from array import array

    import pytest

    from array_utils import array_insert

    a = array("i", [1, 2])
    with pytest.raises(TypeError):
        array_insert(a, 1.5, 3)


def test_array_pop_rejects_bad_index():
    from array import array

    import pytest

    from array_utils import array_pop

    a = array("i", [1, 2])
    with pytest.raises(TypeError):
        array_pop(a, 1.0)


def test_array_index_rejects_bad_args():
    from array import array

    import pytest

    from array_utils import array_index

    a = array("i", [1, 2, 3])
    with pytest.raises(TypeError):
        array_index(a, 1, 0.0)
    with pytest.raises(TypeError):
        array_index(a, 1, 0, 2.0)


def test_array_to_list():
    from array import array

    from array_utils import array_to_list

    a = array("i", [1, 2, 3])
    assert array_to_list(a) == [1, 2, 3]


def test_array_from_list():
    from array import array

    from array_utils import array_from_list

    a = array_from_list("i", [1, 2])
    assert isinstance(a, array)
    assert a.tolist() == [1, 2]


def test_array_from_list_errors():
    import pytest

    from array_utils import array_from_list

    with pytest.raises(TypeError):
        array_from_list(1, [1])
    with pytest.raises(TypeError):
        array_from_list("i", (1, 2))


def test_array_extend_from_list():
    from array import array

    from array_utils import array_extend_from_list

    a = array("i", [1])
    array_extend_from_list(a, [2, 3])
    assert a.tolist() == [1, 2, 3]


def test_array_remove_first():
    from array import array

    from array_utils import array_remove_first

    a = array("i", [1, 2, 1])
    array_remove_first(a, 1)
    assert a.tolist() == [2, 1]
