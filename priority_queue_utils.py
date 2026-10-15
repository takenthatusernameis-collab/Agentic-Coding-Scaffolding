"""Priority queue utilities for heap-based priority queue implementation.

This module provides a heap-based PriorityQueue class and helper functions
for managing items with priorities.
"""

import heapq
from typing import Generic, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """A heap-based priority queue implementation.

    Items are stored as tuples (priority, item) in a min-heap. If multiple
    items have the same priority, their original insertion order is preserved
    by using an incrementing counter.

    Args:
        items: Optional initial items as (priority, item) tuples.
    """

    def __init__(self, items: Optional[List[Tuple[float, T]]] = None) -> None:
        self._heap: List[Tuple[float, int, T]] = []
        self._counter = 0
        if items is not None:
            for item_pair in items:
                if isinstance(item_pair, tuple) and len(item_pair) == 2:
                    # Could be (priority, item) or (item, priority)
                    first, second = item_pair
                    # Heuristic: if second is a number (int/float), it's likely (item, priority)
                    # If first is a number, it's likely (priority, item)
                    if isinstance(second, (int, float)) and not isinstance(first, (int, float)):
                        item, priority = first, second
                    elif isinstance(first, (int, float)) and not isinstance(second, (int, float)):
                        priority, item = first, second
                    else:
                        # Default to (priority, item) for numeric first
                        priority, item = first, second
                    self.push(item, priority=float(priority))
                else:
                    self.push(item_pair)

    def push(self, item: T, priority: float = 10) -> None:
        """Push an item into the queue with given priority."""
        heapq.heappush(self._heap, (float(priority), self._counter, item))
        self._counter += 1

    def pop(self) -> Optional[T]:
        """Pop the item with highest priority (lowest priority value)."""
        if not self._heap:
            return None
        _, _, item = heapq.heappop(self._heap)
        return item

    def peek(self) -> Optional[T]:
        """Return the item with highest priority without removing it."""
        if not self._heap:
            return None
        _, _, item = self._heap[0]
        return item

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return len(self._heap) == 0

    def size(self) -> int:
        """Return the number of items in the queue."""
        return len(self._heap)

    def __len__(self) -> int:
        """Return the number of items in the queue."""
        return len(self._heap)

    def __bool__(self) -> bool:
        """Return True if the queue is non-empty."""
        return len(self._heap) > 0

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._heap.clear()
        self._counter = 0


def push_priority(pq: PriorityQueue[T], item: T, priority: float = 10) -> None:
    """Push an item into a priority queue."""
    pq.push(item, priority=priority)


def pop_priority(pq: PriorityQueue[T]) -> Optional[T]:
    """Pop the highest priority item from a priority queue."""
    return pq.pop()


def peek_priority(pq: PriorityQueue[T]) -> Optional[T]:
    """Peek at the highest priority item without removing it."""
    return pq.peek()


def is_empty_priority(pq: PriorityQueue[T]) -> bool:
    """Check if a priority queue is empty."""
    return pq.is_empty()


def size_priority(pq: PriorityQueue[T]) -> int:
    """Get the size of a priority queue."""
    return pq.size()


def clear_priority(pq: PriorityQueue[T]) -> None:
    """Clear all items from a priority queue."""
    pq.clear()


def create_priority_queue(items: Optional[List[Tuple[float, T]]] = None) -> PriorityQueue[T]:
    """Create a new PriorityQueue instance."""
    return PriorityQueue(items)


def merge_queues(*queues: PriorityQueue[T]) -> PriorityQueue[T]:
    """Merge multiple priority queues into a single new queue."""
    all_items: List[Tuple[float, T]] = []
    for q in queues:
        for priority, _, item in q._heap:
            all_items.append((priority, item))
    return PriorityQueue(all_items)


if __name__ == "__main__":
    pq: PriorityQueue[str] = PriorityQueue()
    pq.push("high", priority=1)
    pq.push("low", priority=10)
    pq.push("medium", priority=5)
    print(f"Peek: {pq.peek()}")
    while not pq.is_empty():
        print(pq.pop())
