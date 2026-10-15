"""Tests for priority_queue_utils module."""

import unittest

from priority_queue_utils import (
    PriorityQueue,
    clear_priority,
    create_priority_queue,
    is_empty_priority,
    merge_queues,
    peek_priority,
    pop_priority,
    push_priority,
    size_priority,
)


class TestPriorityQueue(unittest.TestCase):
    def test_empty_queue(self):
        pq = PriorityQueue()
        self.assertTrue(pq.is_empty())
        self.assertEqual(pq.size(), 0)
        self.assertIsNone(pq.pop())
        self.assertIsNone(pq.peek())

    def test_push_and_pop(self):
        pq = PriorityQueue()
        pq.push("task1", priority=2)
        pq.push("task2", priority=1)
        pq.push("task3", priority=3)
        self.assertEqual(pq.pop(), "task2")
        self.assertEqual(pq.pop(), "task1")
        self.assertEqual(pq.pop(), "task3")
        self.assertTrue(pq.is_empty())

    def test_push_with_default_priority(self):
        pq = PriorityQueue()
        pq.push("item1")
        pq.push("item2", priority=1)
        # item2 has lower priority value, so should come out first
        self.assertEqual(pq.pop(), "item2")
        self.assertEqual(pq.pop(), "item1")

    def test_peek(self):
        pq = PriorityQueue()
        pq.push("task", priority=5)
        self.assertEqual(pq.peek(), "task")
        self.assertFalse(pq.is_empty())
        self.assertEqual(pq.size(), 1)
        self.assertEqual(pq.pop(), "task")
        self.assertTrue(pq.is_empty())

    def test_same_priority(self):
        pq = PriorityQueue()
        pq.push("first", priority=1)
        pq.push("second", priority=1)
        pq.push("third", priority=1)
        # With counter to maintain insertion order for equal priorities
        self.assertEqual(pq.pop(), "first")
        self.assertEqual(pq.pop(), "second")
        self.assertEqual(pq.pop(), "third")

    def test_initialization_with_items(self):
        pq = PriorityQueue([("high", 1), ("low", 3), ("medium", 2)])
        self.assertEqual(pq.pop(), "high")
        self.assertEqual(pq.pop(), "medium")
        self.assertEqual(pq.pop(), "low")

    def test_clear(self):
        pq = PriorityQueue()
        pq.push("a", priority=1)
        pq.push("b", priority=2)
        self.assertFalse(pq.is_empty())
        pq.clear()
        self.assertTrue(pq.is_empty())
        self.assertEqual(pq.size(), 0)


class TestHelperFunctions(unittest.TestCase):
    def test_push_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "item", priority=5)
        self.assertEqual(peek_priority(pq), "item")

    def test_pop_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "item", priority=1)
        result = pop_priority(pq)
        self.assertEqual(result, "item")
        self.assertIsNone(pop_priority(pq))

    def test_peek_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "item", priority=2)
        self.assertEqual(peek_priority(pq), "item")
        self.assertFalse(is_empty_priority(pq))

    def test_is_empty_priority(self):
        pq = PriorityQueue()
        self.assertTrue(is_empty_priority(pq))
        push_priority(pq, "item")
        self.assertFalse(is_empty_priority(pq))

    def test_size_priority(self):
        pq = PriorityQueue()
        self.assertEqual(size_priority(pq), 0)
        push_priority(pq, "a")
        push_priority(pq, "b")
        self.assertEqual(size_priority(pq), 2)

    def test_clear_priority(self):
        pq = PriorityQueue()
        push_priority(pq, "a")
        push_priority(pq, "b")
        clear_priority(pq)
        self.assertTrue(is_empty_priority(pq))


class TestConvenienceFunctions(unittest.TestCase):
    def test_create_priority_queue_empty(self):
        pq = create_priority_queue()
        self.assertIsInstance(pq, PriorityQueue)
        self.assertTrue(pq.is_empty())

    def test_create_priority_queue_with_items(self):
        pq = create_priority_queue([(1, "a"), (2, "b")])
        self.assertEqual(pq.pop(), "a")
        self.assertEqual(pq.pop(), "b")

    def test_merge_queues(self):
        pq1 = PriorityQueue()
        pq1.push("a", priority=3)
        pq1.push("b", priority=1)
        pq2 = PriorityQueue()
        pq2.push("c", priority=2)
        pq3 = PriorityQueue()
        pq3.push("d", priority=4)

        merged = merge_queues(pq1, pq2, pq3)
        self.assertEqual(merged.pop(), "b")
        self.assertEqual(merged.pop(), "c")
        self.assertEqual(merged.pop(), "a")
        self.assertEqual(merged.pop(), "d")
        self.assertTrue(merged.is_empty())
        # Original queues should remain unchanged
        self.assertFalse(pq1.is_empty())
        self.assertFalse(pq2.is_empty())
        self.assertFalse(pq3.is_empty())


if __name__ == "__main__":
    unittest.main()
