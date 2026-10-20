"""Tests for pickletools_utils module."""

import io
import pickle
import unittest

from pickletools_utils import (
    decode_long,
    dis,
    encode_long,
    genops,
    get_opcode_info,
    get_pickle_size,
    is_opcode,
    list_opcodes,
    optimize,
)


class TestPickletoolsDis(unittest.TestCase):
    def test_dis_basic(self) -> None:
        data = pickle.dumps({"hello": "world"})
        output = io.StringIO()
        dis(data, out=output)
        result = output.getvalue()
        self.assertIn("proto", result.lower())

    def test_dis_with_memo(self) -> None:
        data = pickle.dumps([1, 2, 3])
        output = io.StringIO()
        dis(data, memo={}, out=output)
        self.assertGreater(len(output.getvalue()), 0)

    def test_dis_with_compact(self) -> None:
        data = pickle.dumps("test")
        output = io.StringIO()
        dis(data, out=output, indentlevel=0)
        self.assertGreater(len(output.getvalue()), 0)

    def test_dis_validates_inputs(self) -> None:
        data = pickle.dumps("test")
        with self.assertRaises(TypeError):
            dis(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dis(data, out="not-a-stream")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dis(data, memo="not-a-dict")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            dis(data, indentlevel=-1)


class TestPickletoolsGenops(unittest.TestCase):
    def test_genops_basic(self) -> None:
        data = pickle.dumps(42)
        ops = list(genops(data))
        self.assertGreater(len(ops), 0)

    def test_genops_returns_opcodes(self) -> None:
        data = pickle.dumps("hello")
        ops = list(genops(data))
        # Each op is a tuple
        self.assertIsInstance(ops[0], tuple)

    def test_genops_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            genops(123)  # type: ignore[arg-type]


class TestPickletoolsOptimize(unittest.TestCase):
    def test_optimize_basic(self) -> None:
        data = pickle.dumps([1, 2, 3, 4, 5])
        optimized = optimize(data)
        self.assertIsInstance(optimized, bytes)
        # Optimized should be valid
        self.assertEqual(pickle.loads(optimized), [1, 2, 3, 4, 5])

    def test_optimize_preserves_data(self) -> None:
        original = {"a": 1, "b": [2, 3]}
        data = pickle.dumps(original)
        optimized = optimize(data)
        self.assertEqual(pickle.loads(optimized), original)

    def test_optimize_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            optimize("not bytes")  # type: ignore[arg-type]


class TestPickletoolsOpcodes(unittest.TestCase):
    def test_list_opcodes(self) -> None:
        opcodes = list_opcodes()
        self.assertIsInstance(opcodes, list)
        self.assertGreater(len(opcodes), 0)
        self.assertIn("PROTO", opcodes)

    def test_is_opcode_valid(self) -> None:
        self.assertTrue(is_opcode("PROTO"))
        self.assertTrue(is_opcode("STOP"))

    def test_is_opcode_invalid(self) -> None:
        self.assertFalse(is_opcode("NOT_AN_OPCODE"))

    def test_is_opcode_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            is_opcode(42)  # type: ignore[arg-type]

    def test_get_opcode_info(self) -> None:
        info = get_opcode_info("STOP")
        self.assertIsInstance(info, tuple)
        self.assertEqual(info[0], "STOP")

    def test_get_opcode_info_rejects_unknown_opcodes(self) -> None:
        with self.assertRaises(KeyError):
            get_opcode_info("NOT_AN_OPCODE")

    def test_get_opcode_info_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            get_opcode_info(42)  # type: ignore[arg-type]


class TestPickletoolsUtils(unittest.TestCase):
    def test_get_pickle_size(self) -> None:
        data = pickle.dumps({"test": 123})
        size = get_pickle_size(data)
        self.assertEqual(size, len(data))

    def test_get_pickle_size_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            get_pickle_size("not bytes")  # type: ignore[arg-type]

    def test_encode_decode_long(self) -> None:
        num = 123456789
        encoded = encode_long(num)
        self.assertIsInstance(encoded, bytes)
        decoded = decode_long(encoded)
        self.assertEqual(decoded, num)

    def test_encode_decode_long_negative(self) -> None:
        num = -42
        encoded = encode_long(num)
        decoded = decode_long(encoded)
        self.assertEqual(decoded, num)

    def test_encode_decode_long_boundaries(self) -> None:
        for num in (0, 1, -1, 127, 128, -128, -129, 2**63 - 1, -(2**63)):
            with self.subTest(value=num):
                self.assertEqual(decode_long(encode_long(num)), num)

    def test_encode_long_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            encode_long("not an int")  # type: ignore[arg-type]

    def test_decode_long_validates_inputs(self) -> None:
        with self.assertRaises(TypeError):
            decode_long("not bytes")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
