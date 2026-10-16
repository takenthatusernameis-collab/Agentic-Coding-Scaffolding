"""Utility helpers for queue operations."""

from collections import deque


class Queue:
    """A simple FIFO queue."""

    def __init__(self, items=None):
        self._data = deque(items or [])

    def enqueue(self, value):
        self._data.append(value)

    def dequeue(self):
        if not self._data:
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def peek(self):
        if not self._data:
            raise IndexError("peek from empty queue")
        return self._data[0]

    def is_empty(self):
        return not self._data

    def size(self):
        return len(self._data)

    def clear(self):
        self._data.clear()

    def to_list(self):
        return list(self._data)

    @classmethod
    def from_list(cls, items):
        return cls(items)


def create(items=None):
    return Queue(items)


def enqueue(queue, value):
    queue.enqueue(value)
    return queue


def dequeue(queue):
    return queue.dequeue()


def peek(queue):
    return queue.peek()


def is_empty(queue):
    return queue.is_empty()


def size(queue):
    return queue.size()
