"""Tests for pickletools_utils module."""

import io
import pickle
import pickletools
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
        dis(data, output=output)
        result = output.getvalue()
        self.assertIn("proto", result.lower() or result)

    def test_dis_with_memo(self) -> None:
        data = pickle.dumps([1, 2, 3])
        output = io.StringIO()
        dis(data, memo={}, output=output)
        self.assertGreater(len(output.getvalue()), 0)

    def test_dis_with_compact(self) -> None:
        data = pickle.dumps("test")
        output = io.StringIO()
        dis(data, output=output, compact=True)
        self.assertGreater(len(output.getvalue()), 0)


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

    def test_get_opcode_info(self) -> None:
        info = get_opcode_info("STOP")
        self.assertIsInstance(info, tuple)


class TestPickletoolsUtils(unittest.TestCase):
    def test_get_pickle_size(self) -> None:
        data = pickle.dumps({"test": 123})
        size = get_pickle_size(data)
        self.assertEqual(size, len(data))

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


if __name__ == "__main__":
    unittest.main()
