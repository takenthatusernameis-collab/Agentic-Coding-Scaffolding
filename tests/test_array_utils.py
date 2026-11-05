"""Tests for array_utils."""

import unittest
from array import array

from array_utils import (
    array_append,
    array_buffer_info,
    array_byteswap,
    array_clear,
    array_concat,
    array_count,
    array_create,
    array_extend,
    array_extend_from_list,
    array_from_list,
    array_fromlist,
    array_index,
    array_insert,
    array_pop,
    array_remove,
    array_remove_first,
    array_repeat,
    array_reverse,
    array_to_list,
    array_tolist,
    array_typecode,
)


class TestArrayUtils(unittest.TestCase):

    def test_array_create(self):
        a = array_create("i", [1, 2, 3])
        assert isinstance(a, array)
        assert list(a) == [1, 2, 3]


    def test_array_create_empty(self):
        a = array_create("i")
        assert isinstance(a, array)
        assert len(a) == 0


    def test_array_fromlist(self):
        a = array_fromlist("i", [1, 2, 3])
        assert list(a) == [1, 2, 3]


    def test_array_tolist(self):
        a = array("i", [1, 2, 3])
        assert array_tolist(a) == [1, 2, 3]


    def test_array_append(self):
        a = array("i", [1, 2])
        array_append(a, 3)
        assert list(a) == [1, 2, 3]


    def test_array_extend(self):
        a = array("i", [1, 2])
        array_extend(a, [3, 4])
        assert list(a) == [1, 2, 3, 4]


    def test_array_insert(self):
        a = array("i", [1, 3])
        array_insert(a, 1, 2)
        assert list(a) == [1, 2, 3]


    def test_array_pop(self):
        a = array("i", [1, 2, 3])
        assert array_pop(a) == 3
        assert array_pop(a, 0) == 1


    def test_array_remove(self):
        a = array("i", [1, 2, 3])
        array_remove(a, 2)
        assert list(a) == [1, 3]


    def test_array_reverse(self):
        a = array("i", [1, 2, 3])
        array_reverse(a)
        assert list(a) == [3, 2, 1]


    def test_array_buffer_info(self):
        a = array("i", [1, 2, 3])
        info = array_buffer_info(a)
        assert isinstance(info, tuple)
        assert len(info) == 2


    def test_array_byteswap(self):
        a = array("H", [1, 2])
        array_byteswap(a)


    def test_array_count(self):
        a = array("i", [1, 2, 2, 3])
        assert array_count(a, 2) == 2


    def test_array_index(self):
        a = array("i", [1, 2, 2, 3])
        assert array_index(a, 2) == 1
        assert array_index(a, 2, 2) == 2
        assert array_index(a, 2, 0, 3) == 1


    def test_array_create_rejects_non_string_typecode(self):
        with self.assertRaises(TypeError):
            array_create(123)


    def test_array_create_rejects_string_initial(self):
        with self.assertRaises(TypeError):
            array_create("i", "abc")


    def test_array_fromlist_rejects_invalid(self):
        with self.assertRaises(TypeError):
            array_fromlist(123, [1, 2])
        with self.assertRaises(TypeError):
            array_fromlist("i", (1, 2))


    def test_array_tolist_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_tolist([1, 2, 3])


    def test_array_append_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_append([], 1)


    def test_array_extend_rejects_string(self):
        a = array("i", [1])
        with self.assertRaises(TypeError):
            array_extend(a, "23")


    def test_array_insert_rejects_bad_index(self):
        a = array("i", [1, 2])
        with self.assertRaises(TypeError):
            array_insert(a, 1.5, 3)


    def test_array_pop_rejects_bad_index(self):
        a = array("i", [1, 2])
        with self.assertRaises(TypeError):
            array_pop(a, 1.0)


    def test_array_index_rejects_bad_args(self):
        a = array("i", [1, 2, 3])
        with self.assertRaises(TypeError):
            array_index(a, 1, 0.0)
        with self.assertRaises(TypeError):
            array_index(a, 1, 0, 2.0)


    def test_array_to_list(self):
        a = array("i", [1, 2, 3])
        assert array_to_list(a) == [1, 2, 3]


    def test_array_to_list_empty(self):
        assert array_to_list(array("i")) == []


    def test_array_to_list_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_to_list([1, 2, 3])
        with self.assertRaises(TypeError):
            array_to_list("abc")


    def test_array_from_list(self):
        a = array_from_list("i", [1, 2])
        assert isinstance(a, array)
        assert a.tolist() == [1, 2]


    def test_array_from_list_floats(self):
        a = array_from_list("f", [1.0, 2.5])
        assert a.tolist() == [1.0, 2.5]


    def test_array_from_list_errors(self):
        with self.assertRaises(TypeError):
            array_from_list(1, [1])
        with self.assertRaises(TypeError):
            array_from_list("i", (1, 2))
        with self.assertRaises(TypeError):
            array_from_list("i", "ab")


    def test_array_extend_from_list(self):
        a = array("i", [1])
        array_extend_from_list(a, [2, 3])
        assert a.tolist() == [1, 2, 3]


    def test_array_extend_from_list_empty(self):
        a = array("i", [1, 2])
        array_extend_from_list(a, [])
        assert a.tolist() == [1, 2]


    def test_array_extend_from_list_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_extend_from_list([1, 2], [3])


    def test_array_extend_from_list_rejects_non_list(self):
        with self.assertRaises(TypeError):
            array_extend_from_list(array("i", [1]), (2, 3))


    def test_array_remove_first(self):
        a = array("i", [1, 2, 1])
        array_remove_first(a, 1)
        assert a.tolist() == [2, 1]


    def test_array_remove_first_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_remove_first([1, 2], 1)


    def test_array_remove_first_missing_raises(self):
        a = array("i", [1, 2])
        with self.assertRaises(ValueError):
            array_remove_first(a, 99)


    def test_array_clear(self):
        a = array("i", [1, 2, 3])
        array_clear(a)
        assert a.tolist() == []
        assert len(a) == 0


    def test_array_clear_empty(self):
        a = array("i")
        array_clear(a)
        assert a.tolist() == []


    def test_array_clear_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_clear([1, 2, 3])


    def test_array_typecode(self):
        a = array("d", [1.0])
        assert array_typecode(a) == "d"


    def test_array_concat(self):
        a = array("i", [1, 2])
        b = array("i", [3, 4])
        assert array_concat(a, b).tolist() == [1, 2, 3, 4]


    def test_array_concat_empty(self):
        assert array_concat(array("i"), array("i", [1])).tolist() == [1]
        assert array_concat(array("i", [1]), array("i")).tolist() == [1]
        assert array_concat(array("i"), array("i")).tolist() == []


    def test_array_concat_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_concat([1, 2], array("i"))
        with self.assertRaises(TypeError):
            array_concat(array("i"), [1, 2])


    def test_array_repeat(self):
        assert array_repeat(array("i", [1, 2]), 3).tolist() == [1, 2, 1, 2, 1, 2]
        assert array_repeat(array("i", [1, 2]), 1).tolist() == [1, 2]
        assert array_repeat(array("i", [1, 2]), 0).tolist() == []


    def test_array_repeat_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_repeat([1, 2], 3)


    def test_array_repeat_rejects_bad_n(self):
        with self.assertRaises(TypeError):
            array_repeat(array("i", [1]), 1.5)
        with self.assertRaises(TypeError):
            array_repeat(array("i", [1]), True)

if __name__ == "__main__":
    unittest.main()
