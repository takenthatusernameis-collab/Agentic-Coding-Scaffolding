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
    pop_left,
    pop_right,
    remove_from_deque,
    reverse_deque,
    rotate_deque,
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


if __name__ == "__main__":
    unittest.main()