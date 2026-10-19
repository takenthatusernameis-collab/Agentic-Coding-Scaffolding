"""Tests for ctypes_utils."""

import ctypes
import unittest

from ctypes_utils import (
    CFUNCTYPE,
    POINTER,
    Array,
    Structure,
    Union,
    addressof,
    alignment,
    byref,
    c_bool,
    c_byte,
    c_char,
    c_char_p,
    c_double,
    c_float,
    c_int,
    c_int8,
    c_int16,
    c_int32,
    c_int64,
    c_long,
    c_longdouble,
    c_longlong,
    c_short,
    c_size_t,
    c_ssize_t,
    c_ubyte,
    c_uint,
    c_uint8,
    c_uint16,
    c_uint32,
    c_uint64,
    c_ulong,
    c_ulonglong,
    c_ushort,
    c_void_p,
    c_wchar,
    c_wchar_p,
    cast,
    create_string_buffer,
    create_unicode_buffer,
    find_library,
    get_errno,
    get_last_error,
    memmove,
    memset,
    pointer,
    set_errno,
    set_last_error,
    sizeof,
    string_at,
)


class TestCtypesUtilsTypes(unittest.TestCase):
    def test_fundamental_types_match_ctypes(self):
        self.assertIs(c_byte, ctypes.c_byte)
        self.assertIs(c_ubyte, ctypes.c_ubyte)
        self.assertIs(c_short, ctypes.c_short)
        self.assertIs(c_ushort, ctypes.c_ushort)
        self.assertIs(c_int, ctypes.c_int)
        self.assertIs(c_uint, ctypes.c_uint)
        self.assertIs(c_long, ctypes.c_long)
        self.assertIs(c_ulong, ctypes.c_ulong)
        self.assertIs(c_longlong, ctypes.c_longlong)
        self.assertIs(c_ulonglong, ctypes.c_ulonglong)
        self.assertIs(c_float, ctypes.c_float)
        self.assertIs(c_double, ctypes.c_double)
        self.assertIs(c_longdouble, ctypes.c_longdouble)
        self.assertIs(c_char, ctypes.c_char)
        self.assertIs(c_wchar, ctypes.c_wchar)
        self.assertIs(c_bool, ctypes.c_bool)
        self.assertIs(c_void_p, ctypes.c_void_p)
        self.assertIs(c_char_p, ctypes.c_char_p)
        self.assertIs(c_wchar_p, ctypes.c_wchar_p)
        self.assertIs(c_size_t, ctypes.c_size_t)
        self.assertIs(c_ssize_t, ctypes.c_ssize_t)
        self.assertIs(c_int8, ctypes.c_int8)
        self.assertIs(c_uint8, ctypes.c_uint8)
        self.assertIs(c_int16, ctypes.c_int16)
        self.assertIs(c_uint16, ctypes.c_uint16)
        self.assertIs(c_int32, ctypes.c_int32)
        self.assertIs(c_uint32, ctypes.c_uint32)
        self.assertIs(c_int64, ctypes.c_int64)
        self.assertIs(c_uint64, ctypes.c_uint64)

    def test_composite_reexports_match_ctypes(self):
        self.assertIs(Structure, ctypes.Structure)
        self.assertIs(Union, ctypes.Union)
        self.assertIs(POINTER, ctypes.POINTER)
        self.assertIs(Array, ctypes.Array)
        self.assertIs(CFUNCTYPE, ctypes.CFUNCTYPE)


class TestCtypesUtilsSizeofAlignment(unittest.TestCase):
    def test_sizeof_type(self):
        self.assertEqual(sizeof(c_int), ctypes.sizeof(ctypes.c_int))
        self.assertEqual(sizeof(c_double), ctypes.sizeof(ctypes.c_double))
        self.assertEqual(sizeof(c_char), ctypes.sizeof(ctypes.c_char))

    def test_sizeof_instance(self):
        self.assertEqual(sizeof(c_int(5)), ctypes.sizeof(ctypes.c_int(5)))

    def test_alignment(self):
        self.assertEqual(alignment(c_int), ctypes.alignment(ctypes.c_int))
        self.assertEqual(alignment(c_double), ctypes.alignment(ctypes.c_double))


class TestCtypesUtilsAddressofPointer(unittest.TestCase):
    def test_addressof(self):
        value = c_int(42)
        self.assertEqual(addressof(value), ctypes.addressof(value))

    def test_pointer(self):
        value = c_int(7)
        p = pointer(value)
        self.assertEqual(p.contents.value, 7)

    def test_byref(self):
        value = c_int(3)
        ref = byref(value)
        self.assertIsNotNone(ref)
        deref = cast(ref, POINTER(c_int)).contents
        self.assertEqual(deref.value, 3)


class TestCtypesUtilsCast(unittest.TestCase):
    def test_cast_pointer(self):
        value = c_int(255)
        p = pointer(value)
        cp = cast(p, c_void_p)
        self.assertIsInstance(cp, c_void_p)


class TestCtypesUtilsMemory(unittest.TestCase):
    def test_memset_string_at(self):
        buf = create_string_buffer(b"hello")
        memset(buf, ord("x"), 2)
        self.assertEqual(buf.raw[:2], b"xx")

    def test_memmove(self):
        buf = create_string_buffer(b"hello world")
        memmove(buf, addressof(buf) + 6, 5)
        self.assertEqual(buf.value, b"world world")

    def test_string_at(self):
        buf = create_string_buffer(b"abcdef")
        addr = addressof(buf)
        self.assertEqual(string_at(addr, 3), b"abc")

    def test_create_string_buffer(self):
        buf = create_string_buffer(b"hello")
        self.assertEqual(buf.value, b"hello")
        self.assertGreaterEqual(sizeof(buf), 6)

    def test_create_string_buffer_with_size(self):
        buf = create_string_buffer(10)
        self.assertEqual(sizeof(buf), 10)

    def test_create_unicode_buffer(self):
        buf = create_unicode_buffer("hello")
        self.assertEqual(buf.value, "hello")


class TestCtypesUtilsErrno(unittest.TestCase):
    def test_get_errno_set_errno(self):
        set_errno(0)
        self.assertEqual(get_errno(), 0)
        set_errno(42)
        self.assertEqual(get_errno(), 42)
        set_errno(0)


class TestCtypesUtilsLastError(unittest.TestCase):
    def test_get_last_error_set_last_error_platform(self):
        if hasattr(ctypes, "get_last_error"):
            set_last_error(0)
            self.assertEqual(get_last_error(), 0)
            set_last_error(7)
            self.assertEqual(get_last_error(), 7)
            set_last_error(0)
        else:
            with self.assertRaises(AttributeError):
                get_last_error()
            with self.assertRaises(AttributeError):
                set_last_error(0)


class TestCtypesUtilsFindLibrary(unittest.TestCase):
    def test_find_library(self):
        result = find_library("c")
        self.assertTrue(result is None or isinstance(result, str))


class TestCtypesUtilsCFunctype(unittest.TestCase):
    def test_cfunctype_creates_callable_type(self):
        func_type = CFUNCTYPE(c_int, c_int, c_int)
        self.assertTrue(callable(func_type))
        instance = func_type(lambda a, b: a + b)
        self.assertEqual(instance(2, 3), 5)


class TestCtypesUtilsStructure(unittest.TestCase):
    def test_structure_subclass(self):
        class Point(Structure):
            _fields_ = [("x", c_int), ("y", c_int)]

        p = Point(1, 2)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(sizeof(Point), ctypes.sizeof(ctypes.c_int) * 2)


if __name__ == "__main__":
    unittest.main()
