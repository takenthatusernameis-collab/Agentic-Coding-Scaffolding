import unittest

from itertools_utils import (
    chain_iterables,
    chunk_iterable,
    combinations_of,
    group_by_key,
    permutations_of,
    product_of,
)


class TestIterToolsUtils(unittest.TestCase):
    def test_chain_iterables(self):
        self.assertEqual(chain_iterables([1, 2], [3, 4]), [1, 2, 3, 4])

    def test_chunk_iterable(self):
        self.assertEqual(chunk_iterable(range(10), 3), [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]])

    def test_combinations(self):
        self.assertEqual(combinations_of([1, 2, 3], 2), [(1, 2), (1, 3), (2, 3)])

    def test_permutations(self):
        self.assertEqual(len(permutations_of([1, 2, 3], 2)), 6)

    def test_product(self):
        self.assertEqual(product_of([[1, 2], [3, 4]]), [(1, 3), (1, 4), (2, 3), (2, 4)])

    def test_group_by_key(self):
        res = group_by_key([1, 2, 3, 4], lambda x: x % 2)
        self.assertEqual(res[0], [2, 4])
        self.assertEqual(res[1], [1, 3])

    def test_invalid_types(self):
        with self.assertRaises(ValueError):
            chunk_iterable([1, 2, 3], 0)
        with self.assertRaises(ValueError):
            chunk_iterable([1, 2, 3], -1)
        with self.assertRaises(TypeError):
            chunk_iterable([1, 2, 3], "x")


if __name__ == "__main__":
    unittest.main()
