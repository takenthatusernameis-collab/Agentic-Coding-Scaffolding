"""Tests for pickle_utils."""

import io
import pickle
import unittest

from pickle_utils import (
    dump,
    dumps,
    is_valid_protocol,
    load,
    loads,
    pickler,
    unpickler,
    validate_protocol,
)


class TestPickleUtils(unittest.TestCase):
    def test_dumps_loads_roundtrip(self):
        self.assertEqual(loads(dumps({"a": [1, 2, 3]})), {"a": [1, 2, 3]})

    def test_dumps_loads_with_protocol(self):
        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            data = dumps("hello", protocol=protocol)
            self.assertEqual(loads(data), "hello")

    def test_dump_load_with_file(self):
        buffer = io.BytesIO()
        dump({"x": 1}, buffer)
        buffer.seek(0)
        self.assertEqual(load(buffer), {"x": 1})

    def test_pickler_unpickler_streaming(self):
        buffer = io.BytesIO()
        p = pickler(buffer)
        p.dump([1, 2, 3])
        buffer.seek(0)
        u = unpickler(buffer)
        self.assertEqual(u.load(), [1, 2, 3])

    def test_validate_protocol_none_returns_highest(self):
        self.assertEqual(validate_protocol(None), pickle.HIGHEST_PROTOCOL)

    def test_validate_protocol_valid(self):
        self.assertEqual(validate_protocol(2), 2)

    def test_validate_protocol_invalid_type(self):
        with self.assertRaises(TypeError):
            validate_protocol("2")

    def test_validate_protocol_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_protocol(99)

    def test_is_valid_protocol(self):
        self.assertTrue(is_valid_protocol(0))
        self.assertTrue(is_valid_protocol(pickle.HIGHEST_PROTOCOL))
        self.assertFalse(is_valid_protocol("nope"))
        self.assertFalse(is_valid_protocol(99))

    def test_dump_load_with_explicit_protocol(self):
        buffer = io.BytesIO()
        dump("abc", buffer, protocol=2)
        buffer.seek(0)
        self.assertEqual(load(buffer), "abc")


if __name__ == "__main__":
    unittest.main()
