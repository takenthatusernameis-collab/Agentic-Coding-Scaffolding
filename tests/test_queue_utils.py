import unittest

from queue_utils import Queue, create, dequeue, enqueue, is_empty, peek, size


class TestQueueUtils(unittest.TestCase):
    def test_create_default(self):
        q = create()
        self.assertTrue(is_empty(q))
        self.assertEqual(size(q), 0)

    def test_create_from_items(self):
        q = create([1, 2, 3])
        self.assertEqual(q.to_list(), [1, 2, 3])
        self.assertEqual(size(q), 3)

    def test_enqueue_appends_to_tail(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.to_list(), [1, 2])
        self.assertEqual(size(q), 2)

    def test_enqueue_returns_queue(self):
        q = Queue()
        result = enqueue(q, 1)
        self.assertIs(result, q)
        self.assertEqual(q.to_list(), [1])

    def test_dequeue_removes_head(self):
        q = create([1, 2, 3])
        self.assertEqual(dequeue(q), 1)
        self.assertEqual(q.to_list(), [2, 3])

    def test_dequeue_function_matches_method(self):
        q = create([1, 2])
        self.assertEqual(dequeue(q), 1)
        self.assertEqual(q.dequeue(), 2)

    def test_dequeue_empty_raises(self):
        with self.assertRaises(IndexError):
            dequeue(Queue())

    def test_peek_returns_head_without_removing(self):
        q = create([1, 2, 3])
        self.assertEqual(peek(q), 1)
        self.assertEqual(peek(q), 1)
        self.assertEqual(q.to_list(), [1, 2, 3])

    def test_peek_empty_raises(self):
        with self.assertRaises(IndexError):
            peek(Queue())

    def test_is_empty(self):
        q = Queue()
        self.assertTrue(is_empty(q))
        q.enqueue(1)
        self.assertFalse(is_empty(q))
        dequeue(q)
        self.assertTrue(is_empty(q))

    def test_size(self):
        q = Queue()
        self.assertEqual(size(q), 0)
        q.enqueue(1)
        self.assertEqual(size(q), 1)
        q.enqueue(2)
        self.assertEqual(size(q), 2)
        dequeue(q)
        self.assertEqual(size(q), 1)

    def test_clear(self):
        q = create([1, 2, 3])
        q.clear()
        self.assertTrue(q.is_empty())
        self.assertEqual(q.to_list(), [])

    def test_clear_empty(self):
        q = Queue()
        q.clear()
        self.assertTrue(q.is_empty())

    def test_to_list_returns_copy(self):
        q = create([1, 2, 3])
        result = q.to_list()
        result.append(99)
        self.assertEqual(q.to_list(), [1, 2, 3])

    def test_from_list(self):
        q = Queue.from_list([1, 2, 3])
        self.assertEqual(q.to_list(), [1, 2, 3])

    def test_from_list_default(self):
        q = Queue.from_list([])
        self.assertTrue(q.is_empty())

    def test_roundtrip(self):
        items = list(range(10))
        q = create(items)
        drained = []
        while not q.is_empty():
            drained.append(q.dequeue())
        self.assertEqual(drained, items)
        self.assertTrue(q.is_empty())


if __name__ == "__main__":
    unittest.main()
