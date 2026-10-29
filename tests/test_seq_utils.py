"""Unit tests for seq_utils module."""

import unittest

from seq_utils import (
    adjacent_pairs,
    chunk,
    drop_while,
    first,
    head,
    interleave,
    is_sorted,
    last,
    nth,
    split_at,
    tail,
    take_while,
)


class TestFirst(unittest.TestCase):
    def test_first_non_empty(self):
        self.assertEqual(first([1, 2, 3]), 1)
        self.assertEqual(first(("a", "b")), "a")
        self.assertEqual(first("xyz"), "x")

    def test_first_empty(self):
        self.assertIsNone(first([]))
        self.assertIsNone(first(()))

    def test_first_type_error(self):
        with self.assertRaises(TypeError):
            first(123)  # type: ignore[arg-type]


class TestLast(unittest.TestCase):
    def test_last_non_empty(self):
        self.assertEqual(last([1, 2, 3]), 3)
        self.assertEqual(last(("a", "b")), "b")

    def test_last_empty(self):
        self.assertIsNone(last([]))

    def test_last_type_error(self):
        with self.assertRaises(TypeError):
            last(None)  # type: ignore[arg-type]


class TestNth(unittest.TestCase):
    def test_nth_valid(self):
        self.assertEqual(nth([1, 2, 3], 0), 1)
        self.assertEqual(nth([1, 2, 3], 2), 3)
        self.assertEqual(nth([1, 2, 3], -1), 3)
        self.assertEqual(nth([1, 2, 3], -3), 1)

    def test_nth_out_of_range(self):
        self.assertIsNone(nth([1, 2, 3], 5))
        self.assertIsNone(nth([1, 2, 3], -4))
        self.assertIsNone(nth([], 0))

    def test_nth_type_error(self):
        with self.assertRaises(TypeError):
            nth([1, 2, 3], "1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            nth(123, 0)  # type: ignore[arg-type]


class TestHead(unittest.TestCase):
    def test_head(self):
        self.assertEqual(head([1, 2, 3, 4], 2), [1, 2])
        self.assertEqual(head([1, 2, 3]), [1])
        self.assertEqual(head([], 3), [])

    def test_head_zero(self):
        self.assertEqual(head([1, 2, 3], 0), [])

    def test_head_errors(self):
        with self.assertRaises(TypeError):
            head([1, 2, 3], "2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            head([1, 2, 3], -1)
        with self.assertRaises(TypeError):
            head(123, 1)  # type: ignore[arg-type]


class TestTail(unittest.TestCase):
    def test_tail(self):
        self.assertEqual(tail([1, 2, 3, 4], 2), [3, 4])
        self.assertEqual(tail([1, 2, 3]), [3])
        self.assertEqual(tail([], 3), [])

    def test_tail_zero(self):
        self.assertEqual(tail([1, 2, 3], 0), [])

    def test_tail_errors(self):
        with self.assertRaises(TypeError):
            tail([1, 2, 3], "2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            tail([1, 2, 3], -1)
        with self.assertRaises(TypeError):
            tail(123, 1)  # type: ignore[arg-type]


class TestSplitAt(unittest.TestCase):
    def test_split_at(self):
        self.assertEqual(split_at([1, 2, 3, 4], 2), ([1, 2], [3, 4]))
        self.assertEqual(split_at([1, 2, 3], 0), ([], [1, 2, 3]))
        self.assertEqual(split_at([1, 2, 3], 3), ([1, 2, 3], []))
        self.assertEqual(split_at([1, 2, 3], 10), ([1, 2, 3], []))

    def test_split_at_clamped_negative(self):
        self.assertEqual(split_at([1, 2, 3], -5), ([], [1, 2, 3]))

    def test_split_at_type_error(self):
        with self.assertRaises(TypeError):
            split_at([1, 2, 3], "2")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            split_at(123, 1)  # type: ignore[arg-type]


class TestTakeWhile(unittest.TestCase):
    def test_take_while(self):
        self.assertEqual(take_while([1, 2, 3, 4], lambda x: x < 3), [1, 2])
        self.assertEqual(take_while([], lambda x: True), [])
        self.assertEqual(take_while([5, 6, 7], lambda x: x < 3), [])

    def test_take_while_type_error(self):
        with self.assertRaises(TypeError):
            take_while([1, 2, 3], None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            take_while(123, lambda x: True)  # type: ignore[arg-type]


class TestDropWhile(unittest.TestCase):
    def test_drop_while(self):
        self.assertEqual(drop_while([1, 2, 3, 4], lambda x: x < 3), [3, 4])
        self.assertEqual(drop_while([], lambda x: True), [])
        self.assertEqual(drop_while([5, 6, 7], lambda x: x < 3), [5, 6, 7])
        self.assertEqual(drop_while([1, 2, 3], lambda x: x < 10), [])

    def test_drop_while_type_error(self):
        with self.assertRaises(TypeError):
            drop_while([1, 2, 3], None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            drop_while(123, lambda x: True)  # type: ignore[arg-type]


class TestInterleave(unittest.TestCase):
    def test_interleave(self):
        self.assertEqual(interleave([1, 2], [3, 4]), [1, 3, 2, 4])
        self.assertEqual(interleave([1], [2, 3], [4]), [1, 2, 4, 3])
        self.assertEqual(interleave([], []), [])
        self.assertEqual(interleave([1, 2, 3]), [1, 2, 3])

    def test_interleave_type_error(self):
        with self.assertRaises(TypeError):
            interleave([1], 123)  # type: ignore[arg-type]


class TestAdjacentPairs(unittest.TestCase):
    def test_adjacent_pairs(self):
        self.assertEqual(adjacent_pairs([1, 2, 3]), [(1, 2), (2, 3)])
        self.assertEqual(adjacent_pairs([1]), [])
        self.assertEqual(adjacent_pairs([]), [])

    def test_adjacent_pairs_type_error(self):
        with self.assertRaises(TypeError):
            adjacent_pairs(123)  # type: ignore[arg-type]


class TestChunk(unittest.TestCase):
    def test_chunk_basic(self):
        self.assertEqual(chunk([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])
        self.assertEqual(chunk([1, 2, 3, 4], 2), [[1, 2], [3, 4]])
        self.assertEqual(chunk([1], 1), [[1]])

    def test_chunk_larger_than_sequence(self):
        self.assertEqual(chunk([1, 2], 5), [[1, 2]])

    def test_chunk_empty(self):
        self.assertEqual(chunk([], 3), [])

    def test_chunk_string(self):
        self.assertEqual(chunk("abcdef", 3), [["a", "b", "c"], ["d", "e", "f"]])

    def test_chunk_tuple(self):
        self.assertEqual(chunk((1, 2, 3, 4), 2), [[1, 2], [3, 4]])

    def test_chunk_size_one(self):
        self.assertEqual(chunk([1, 2, 3], 1), [[1], [2], [3]])

    def test_chunk_type_error(self):
        with self.assertRaises(TypeError):
            chunk(123, 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            chunk([1, 2], True)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            chunk([1, 2], "2")  # type: ignore[arg-type]

    def test_chunk_value_error(self):
        with self.assertRaises(ValueError):
            chunk([1, 2], 0)
        with self.assertRaises(ValueError):
            chunk([1, 2], -1)


class TestIsSorted(unittest.TestCase):
    def test_is_sorted(self):
        self.assertTrue(is_sorted([1, 2, 3]))
        self.assertFalse(is_sorted([3, 1, 2]))
        self.assertTrue(is_sorted([3, 2, 1], reverse=True))
        self.assertFalse(is_sorted([1, 3, 2], reverse=True))
        self.assertTrue(is_sorted([]))
        self.assertTrue(is_sorted([5]))

    def test_is_sorted_with_key(self):
        self.assertTrue(is_sorted(["a", "bb", "ccc"], key=len))
        self.assertFalse(is_sorted(["ccc", "bb", "a"], key=len))

    def test_is_sorted_type_error(self):
        with self.assertRaises(TypeError):
            is_sorted(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_sorted([1, 2], key=123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
