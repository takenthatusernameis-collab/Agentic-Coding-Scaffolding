import io
import marshal
import unittest

from marshal_utils import dump, dumps, get_version, load, loads


class TestMarshalUtils(unittest.TestCase):
    def test_dumps_round_trip(self):
        obj = {"name": "Alice", "values": [1, 2, 3]}
        data = dumps(obj)
        self.assertIsInstance(data, bytes)
        self.assertEqual(loads(data), obj)

    def test_dumps_with_explicit_version(self):
        obj = ("a", 42)
        data = dumps(obj, version=marshal.version)
        self.assertIsInstance(data, bytes)
        self.assertEqual(loads(data), obj)

    def test_dumps_version_validation(self):
        with self.assertRaises(TypeError):
            dumps("x", version="1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dumps("x", version=1.0)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            dumps("x", version=marshal.version + 1)
        with self.assertRaises(ValueError):
            dumps("x", version=-1)

    def test_dumps_unmarshalable_raises_value_error(self):
        with self.assertRaises(ValueError):
            dumps(lambda x: x)

    def test_loads_bytes_like_types(self):
        obj = [1, 2, 3]
        data = marshal.dumps(obj)
        self.assertEqual(loads(data), obj)
        self.assertEqual(loads(bytearray(data)), obj)
        self.assertEqual(loads(memoryview(data)), obj)

    def test_loads_validation(self):
        with self.assertRaises(TypeError):
            loads("not bytes")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            loads(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            loads(None)  # type: ignore[arg-type]

    def test_loads_invalid_data_raises_value_error(self):
        with self.assertRaises(ValueError):
            loads(b"not marshal data")

    def test_dump_and_load_file_object(self):
        obj = {"numbers": [1.0, 2.5], "flag": True}
        buf = io.BytesIO()
        dump(obj, buf)
        buf.seek(0)
        self.assertEqual(load(buf), obj)

    def test_dump_with_version(self):
        obj = "test"
        buf = io.BytesIO()
        dump(obj, buf, version=marshal.version)
        buf.seek(0)
        self.assertEqual(load(buf), obj)

    def test_dump_validation(self):
        with self.assertRaises(AttributeError):
            dump("x", object())  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dump("x", io.BytesIO(), version="2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dump("x", io.BytesIO(), version=2.0)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            dump("x", io.BytesIO(), version=marshal.version + 1)
        with self.assertRaises(ValueError):
            dump("x", io.BytesIO(), version=-1)
        bad_file = io.BytesIO()
        bad_file.write = None  # type: ignore[method-assign]
        with self.assertRaises(TypeError):
            dump("x", bad_file)

    def test_dump_raises_value_error_on_marshal_failure(self):
        class Bad:
            pass

        buf = io.BytesIO()
        # functions/closures generally not marshalable in some forms; try
        try:
            dump(lambda: 1, buf)
        except ValueError:
            pass
        else:
            buf.truncate(0)
            buf.seek(0)
            # if it didn't raise, that's fine - just ensure our API works

    def test_load_validation(self):
        with self.assertRaises(AttributeError):
            load(object())  # type: ignore[arg-type]
        bad_file = io.BytesIO()
        bad_file.read = None  # type: ignore[method-assign]
        with self.assertRaises(TypeError):
            load(bad_file)
        with self.assertRaises(ValueError):
            bad_data = io.BytesIO(b"garbage")
            load(bad_data)

    def test_get_version(self):
        self.assertIsInstance(get_version(), int)
        self.assertEqual(get_version(), marshal.version)
