import unittest

from queue_utils import Queue, create, dequeue, enqueue, is_empty, peek, size


class TestQueueUtils(unittest.TestCase):
    def test_basic(self):
        q = create([1, 2])
        self.assertFalse(is_empty(q))
        self.assertEqual(size(q), 2)
        self.assertEqual(peek(q), 1)
        self.assertEqual(dequeue(q), 1)
        self.assertEqual(dequeue(q), 2)
        self.assertTrue(is_empty(q))

    def test_enqueue(self):
        q = Queue()
        enqueue(q, 5)
        self.assertEqual(q.to_list(), [5])

    def test_errors(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()
        with self.assertRaises(IndexError):
            q.peek()


if __name__ == "__main__":
    unittest.main()
