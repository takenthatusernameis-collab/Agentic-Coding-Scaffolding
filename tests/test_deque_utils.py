import unittest
from deque_utils import (
    create_deque,
    append_left,
    append_right,
    pop_left,
    pop_right,
    deque_to_list,
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
