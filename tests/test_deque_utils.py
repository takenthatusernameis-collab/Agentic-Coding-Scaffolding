import unittest

from deque_utils import (
    append_left,
    append_right,
    clear_deque,
    count_in_deque,
    create_deque,
    deque_to_list,
    extend_left,
    extend_right,
    find_index_in_deque,
    has_in_deque,
    has_items,
    index_in_deque,
    is_empty,
    pop_left,
    pop_right,
    remove_from_deque,
    reverse_deque,
    rotate_deque,
    size,
)


class TestDequeUtils(unittest.TestCase):
    def test_create_deque(self):
        self.assertEqual(deque_to_list(create_deque([1, 2, 3])), [1, 2, 3])

    def test_create_deque_default(self):
        self.assertEqual(deque_to_list(create_deque()), [])

    def test_create_deque_maxlen_drops_oldest(self):
        d = create_deque([1, 2, 3], maxlen=2)
        self.assertEqual(deque_to_list(d), [2, 3])

    def test_create_deque_maxlen_none(self):
        d = create_deque(maxlen=None)
        self.assertEqual(deque_to_list(d), [])

    def test_append_pop(self):
        d = create_deque()
        append_right(d, 1)
        append_left(d, 0)
        self.assertEqual(pop_left(d), 0)
        self.assertEqual(pop_right(d), 1)

    def test_append_left_preserves_order(self):
        d = create_deque([1, 2])
        append_left(d, 0)
        self.assertEqual(deque_to_list(d), [0, 1, 2])

    def test_append_right_preserves_order(self):
        d = create_deque([1, 2])
        append_right(d, 3)
        self.assertEqual(deque_to_list(d), [1, 2, 3])

    def test_pop_left_empty_raises(self):
        with self.assertRaises(IndexError):
            pop_left(create_deque())

    def test_pop_right_empty_raises(self):
        with self.assertRaises(IndexError):
            pop_right(create_deque())

    def test_extend_right(self):
        d = create_deque([1])
        extend_right(d, [2, 3])
        self.assertEqual(deque_to_list(d), [1, 2, 3])

    def test_extend_left_preserves_order(self):
        d = create_deque([3])
        extend_left(d, [2, 1])
        self.assertEqual(deque_to_list(d), [1, 2, 3])

    def test_extend_left_empty(self):
        d = create_deque([1])
        extend_left(d, [])
        self.assertEqual(deque_to_list(d), [1])

    def test_rotate_positive(self):
        d = create_deque([1, 2, 3])
        rotate_deque(d, 1)
        self.assertEqual(deque_to_list(d), [3, 1, 2])

    def test_rotate_negative(self):
        d = create_deque([1, 2, 3])
        rotate_deque(d, -1)
        self.assertEqual(deque_to_list(d), [2, 3, 1])

    def test_rotate_default(self):
        d = create_deque([1, 2, 3])
        rotate_deque(d)
        self.assertEqual(deque_to_list(d), [3, 1, 2])

    def test_rotate_full_cycle(self):
        d = create_deque([1, 2, 3])
        rotate_deque(d, 3)
        self.assertEqual(deque_to_list(d), [1, 2, 3])

    def test_clear_deque(self):
        d = create_deque([1, 2, 3])
        clear_deque(d)
        self.assertEqual(deque_to_list(d), [])

    def test_clear_deque_empty(self):
        d = create_deque()
        clear_deque(d)
        self.assertEqual(deque_to_list(d), [])

    def test_count_in_deque(self):
        d = create_deque([1, 2, 1, 3, 1])
        self.assertEqual(count_in_deque(d, 1), 3)
        self.assertEqual(count_in_deque(d, 2), 1)
        self.assertEqual(count_in_deque(d, 9), 0)

    def test_has_in_deque_present(self):
        d = create_deque([1, 2, 1, 3, 1])
        self.assertTrue(has_in_deque(d, 1))
        self.assertTrue(has_in_deque(d, 2))
        self.assertTrue(has_in_deque(d, 3))

    def test_has_in_deque_absent(self):
        d = create_deque([1, 2, 1, 3, 1])
        self.assertFalse(has_in_deque(d, 9))
        self.assertFalse(has_in_deque(d, 0))

    def test_has_in_deque_empty(self):
        d = create_deque()
        self.assertFalse(has_in_deque(d, 1))

    def test_has_in_deque_single_present(self):
        d = create_deque([42])
        self.assertTrue(has_in_deque(d, 42))

    def test_has_in_deque_single_absent(self):
        d = create_deque([42])
        self.assertFalse(has_in_deque(d, 7))

    def test_has_in_deque_duplicates(self):
        d = create_deque([5, 5, 5])
        self.assertTrue(has_in_deque(d, 5))
        self.assertFalse(has_in_deque(d, 6))

    def test_has_in_deque_consistent_with_count(self):
        d = create_deque([1, 2, 1, 3, 1])
        for x in range(10):
            self.assertEqual(has_in_deque(d, x), count_in_deque(d, x) > 0)

    def test_has_in_deque_strings(self):
        d = create_deque(["a", "b", "a"])
        self.assertTrue(has_in_deque(d, "a"))
        self.assertFalse(has_in_deque(d, "c"))

    def test_remove_from_deque(self):
        d = create_deque([1, 2, 3, 2])
        remove_from_deque(d, 2)
        self.assertEqual(deque_to_list(d), [1, 3, 2])

    def test_remove_from_deque_missing_raises(self):
        with self.assertRaises(ValueError):
            remove_from_deque(create_deque([1, 2, 3]), 9)

    def test_reverse_deque(self):
        d = create_deque([1, 2, 3])
        reverse_deque(d)
        self.assertEqual(deque_to_list(d), [3, 2, 1])

    def test_reverse_deque_single(self):
        d = create_deque([1])
        reverse_deque(d)
        self.assertEqual(deque_to_list(d), [1])

    def test_reverse_deque_empty(self):
        d = create_deque()
        reverse_deque(d)
        self.assertEqual(deque_to_list(d), [])

    def test_deque_to_list(self):
        d = create_deque([1, 2, 3])
        result = deque_to_list(d)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2, 3])
        # The original deque is unchanged.
        self.assertEqual(deque_to_list(d), [1, 2, 3])

    def test_maxlen_enforced_on_append(self):
        d = create_deque(maxlen=2)
        append_right(d, 1)
        append_right(d, 2)
        append_right(d, 3)
        self.assertEqual(deque_to_list(d), [2, 3])




class TestIsEmpty(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(is_empty(create_deque()))

    def test_single_element(self):
        self.assertFalse(is_empty(create_deque([1])))

    def test_after_pop(self):
        d = create_deque([1, 2])
        pop_left(d)
        pop_left(d)
        self.assertTrue(is_empty(d))

    def test_after_clear(self):
        d = create_deque([1, 2, 3])
        clear_deque(d)
        self.assertTrue(is_empty(d))

    def test_consistency_with_len(self):
        d = create_deque([1, 2, 3])
        self.assertEqual(is_empty(d), len(deque_to_list(d)) == 0)
        clear_deque(d)
        self.assertEqual(is_empty(d), len(deque_to_list(d)) == 0)


class TestSize(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(size(create_deque()), 0)

    def test_single_element(self):
        self.assertEqual(size(create_deque([1])), 1)

    def test_multiple_elements(self):
        self.assertEqual(size(create_deque([1, 2, 3])), 3)

    def test_after_append(self):
        d = create_deque()
        self.assertEqual(size(d), 0)
        append_right(d, 1)
        self.assertEqual(size(d), 1)
        append_right(d, 2)
        self.assertEqual(size(d), 2)

    def test_after_pop(self):
        d = create_deque([1, 2])
        self.assertEqual(size(d), 2)
        pop_left(d)
        self.assertEqual(size(d), 1)
        pop_left(d)
        self.assertEqual(size(d), 0)

    def test_after_clear(self):
        d = create_deque([1, 2, 3])
        clear_deque(d)
        self.assertEqual(size(d), 0)

    def test_consistency_with_len(self):
        d = create_deque([1, 2, 3])
        self.assertEqual(size(d), len(deque_to_list(d)))
        clear_deque(d)
        self.assertEqual(size(d), len(deque_to_list(d)))

    def test_consistency_with_is_empty(self):
        d = create_deque([1, 2])
        self.assertEqual(size(d) == 0, is_empty(d))
        clear_deque(d)
        self.assertEqual(size(d) == 0, is_empty(d))


class TestIndexInDeque(unittest.TestCase):
    def test_basic(self):
        d = create_deque([1, 2, 3, 2])
        self.assertEqual(index_in_deque(d, 1), 0)
        self.assertEqual(index_in_deque(d, 2), 1)
        self.assertEqual(index_in_deque(d, 3), 2)

    def test_start(self):
        d = create_deque([1, 2, 3, 2])
        self.assertEqual(index_in_deque(d, 2, 2), 3)

    def test_start_stop_found(self):
        d = create_deque([1, 2, 3, 2, 1])
        self.assertEqual(index_in_deque(d, 2, 2, 4), 3)

    def test_start_stop_missing_raises(self):
        d = create_deque([1, 2, 3, 2, 1])
        with self.assertRaises(ValueError):
            index_in_deque(d, 1, 1, 4)

    def test_missing_raises(self):
        d = create_deque([1, 2, 3])
        with self.assertRaises(ValueError):
            index_in_deque(d, 9)

    def test_missing_in_range_raises(self):
        d = create_deque([1, 2, 3, 2])
        with self.assertRaises(ValueError):
            index_in_deque(d, 2, 2, 3)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            index_in_deque(create_deque(), 1)

    def test_consistent_with_list(self):
        d = create_deque([1, 2, 3, 2, 1])
        for v in (1, 2, 3):
            self.assertEqual(index_in_deque(d, v), deque_to_list(d).index(v))


class TestFindIndexInDeque(unittest.TestCase):
    def test_basic(self):
        d = create_deque([1, 2, 3, 2])
        self.assertEqual(find_index_in_deque(d, 1), 0)
        self.assertEqual(find_index_in_deque(d, 2), 1)
        self.assertEqual(find_index_in_deque(d, 3), 2)

    def test_missing_returns_none(self):
        d = create_deque([1, 2, 3])
        self.assertIsNone(find_index_in_deque(d, 9))

    def test_start(self):
        d = create_deque([1, 2, 3, 2])
        self.assertEqual(find_index_in_deque(d, 2, 2), 3)

    def test_start_stop_found(self):
        d = create_deque([1, 2, 3, 2, 1])
        self.assertEqual(find_index_in_deque(d, 2, 2, 4), 3)

    def test_start_stop_missing_returns_none(self):
        d = create_deque([1, 2, 3, 2, 1])
        self.assertIsNone(find_index_in_deque(d, 1, 1, 4))

    def test_empty_returns_none(self):
        self.assertIsNone(find_index_in_deque(create_deque(), 1))

    def test_consistent_with_index_in_deque(self):
        d = create_deque([1, 2, 3, 2, 1])
        for v in (1, 2, 3, 9):
            try:
                expected = index_in_deque(d, v)
            except ValueError:
                expected = None
            self.assertEqual(find_index_in_deque(d, v), expected)


if __name__ == "__main__":
    unittest.main()



class TestHasItems(unittest.TestCase):
    def test_empty(self):
        self.assertFalse(has_items(create_deque()))

    def test_single_element(self):
        self.assertTrue(has_items(create_deque([1])))

    def test_multiple_elements(self):
        self.assertTrue(has_items(create_deque([1, 2, 3])))

    def test_after_clear(self):
        d = create_deque([1, 2, 3])
        self.assertTrue(has_items(d))
        clear_deque(d)
        self.assertFalse(has_items(d))

    def test_consistent_with_size_and_is_empty(self):
        d = create_deque()
        self.assertEqual(has_items(d), size(d) > 0)
        self.assertEqual(has_items(d), not is_empty(d))
