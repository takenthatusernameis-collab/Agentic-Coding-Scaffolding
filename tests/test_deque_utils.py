import unittest

from deque_utils import (
    append_left,
    append_right,
    create_deque,
    deque_to_list,
    pop_left,
    pop_right,
)


class TestDequeUtils(unittest.TestCase):
    def test_create_deque(self):
        d = create_deque([1, 2, 3])
        self.assertEqual(deque_to_list(d), [1, 2, 3])

    def test_append_pop(self):
        d = create_deque()
        append_right(d, 1)
        append_left(d, 0)
        self.assertEqual(pop_left(d), 0)
        self.assertEqual(pop_right(d), 1)


if __name__ == "__main__":
    unittest.main()
