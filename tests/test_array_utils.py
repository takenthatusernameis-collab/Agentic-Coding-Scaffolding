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
    array_from_bytes,
    array_from_list,
    array_from_unicode,
    array_frombytes,
    array_fromfile,
    array_fromlist,
    array_fromunicode,
    array_index,
    array_insert,
    array_itemsize,
    array_pop,
    array_remove,
    array_remove_first,
    array_repeat,
    array_reverse,
    array_to_bytes,
    array_to_file,
    array_to_list,
    array_to_unicode,
    array_tobytes,
    array_tofile,
    array_tolist,
    array_tounicode,
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


class TestArrayBytes(unittest.TestCase):

    def test_array_tobytes(self):
        a = array("i", [1, 2, 3])
        assert array_tobytes(a) == a.tobytes()
        assert isinstance(array_tobytes(a), bytes)

    def test_array_to_bytes_alias(self):
        a = array("i", [1, 2, 3])
        assert array_to_bytes(a) == array_tobytes(a)

    def test_array_tobytes_empty(self):
        assert array_tobytes(array("i")) == b""

    def test_array_tobytes_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_tobytes([1, 2, 3])

    def test_array_frombytes(self):
        a = array("i")
        array_frombytes(a, array("i", [1, 2, 3]).tobytes())
        assert a.tolist() == [1, 2, 3]

    def test_array_from_bytes_alias(self):
        a = array("i")
        array_from_bytes(a, array("i", [4, 5]).tobytes())
        assert a.tolist() == [4, 5]

    def test_array_frombytes_empty(self):
        a = array("i", [1, 2])
        array_frombytes(a, b"")
        assert a.tolist() == [1, 2]

    def test_array_frombytes_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_frombytes([1], b"")

    def test_array_frombytes_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            array_frombytes(array("i"), "abc")  # type: ignore[arg-type]


class TestArrayFile(unittest.TestCase):

    def test_array_tofile_and_fromfile_roundtrip(self):
        import io
        a = array("i", [1, 2, 3])
        buf = io.BytesIO()
        array_tofile(a, buf)
        buf.seek(0)
        b = array("i")
        array_fromfile(b, buf, 3)
        assert b.tolist() == [1, 2, 3]

    def test_array_to_file_alias(self):
        import io
        a = array("i", [7, 8])
        buf = io.BytesIO()
        array_to_file(a, buf)
        assert buf.getvalue() == a.tobytes()

    def test_array_tofile_rejects_non_array(self):
        import io
        with self.assertRaises(TypeError):
            array_tofile([1, 2], io.BytesIO())

    def test_array_fromfile_rejects_non_array(self):
        import io
        with self.assertRaises(TypeError):
            array_fromfile([], io.BytesIO(), 1)

    def test_array_fromfile_rejects_bad_n(self):
        import io
        with self.assertRaises(TypeError):
            array_fromfile(array("i"), io.BytesIO(), 1.5)
        with self.assertRaises(TypeError):
            array_fromfile(array("i"), io.BytesIO(), True)


class TestArrayUnicode(unittest.TestCase):

    def test_array_tounicode(self):
        a = array("u", "abc")
        assert array_tounicode(a) == "abc"
        assert isinstance(array_tounicode(a), str)

    def test_array_to_unicode_alias(self):
        a = array("u", "xyz")
        assert array_to_unicode(a) == array_tounicode(a)

    def test_array_tounicode_empty(self):
        assert array_tounicode(array("u")) == ""

    def test_array_tounicode_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_tounicode("abc")  # type: ignore[arg-type]

    def test_array_fromunicode(self):
        a = array("u")
        array_fromunicode(a, "hello")
        assert a.tolist() == list("hello")

    def test_array_from_unicode_alias(self):
        a = array("u")
        array_from_unicode(a, "world")
        assert a.tounicode() == "world"

    def test_array_fromunicode_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_fromunicode([], "x")  # type: ignore[arg-type]

    def test_array_fromunicode_rejects_non_str(self):
        with self.assertRaises(TypeError):
            array_fromunicode(array("u"), 123)  # type: ignore[arg-type]


class TestArrayItemsize(unittest.TestCase):

    def test_array_itemsize(self):
        assert array_itemsize(array("i", [1])) == array("i", [1]).itemsize

    def test_array_itemsize_charcode_sizes(self):
        # 'b' (signed char) is 1 byte, 'i' (signed int) is at least 2
        assert array_itemsize(array("b", [0])) == 1
        assert array_itemsize(array("i", [0])) >= 2

    def test_array_itemsize_rejects_non_array(self):
        with self.assertRaises(TypeError):
            array_itemsize([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
