import unittest

from ring_buffer_utils import (
    RingBuffer,
    append,
    clear,
    create,
    get,
    is_empty,
    is_full,
    peek,
    pop,
    size,
    to_list,
)


class TestRingBuffer(unittest.TestCase):
    def test_append_and_get(self):
        rb = create(3)
        append(rb, 1)
        append(rb, 2)
        append(rb, 3)
        self.assertEqual(to_list(rb), [1, 2, 3])
        self.assertEqual(get(rb, 0), 1)
        self.assertEqual(get(rb, 1), 2)
        self.assertEqual(get(rb, 2), 3)

    def test_overwrites_oldest_when_full(self):
        rb = create(3)
        for value in (1, 2, 3, 4):
            append(rb, value)
        self.assertTrue(is_full(rb))
        self.assertEqual(len(rb), 3)
        self.assertEqual(to_list(rb), [2, 3, 4])

    def test_peek_pop(self):
        rb = create(3)
        append(rb, 10)
        append(rb, 20)
        self.assertEqual(peek(rb), 10)
        self.assertEqual(pop(rb), 10)
        self.assertEqual(pop(rb), 20)
        self.assertTrue(is_empty(rb))

    def test_pop_and_peek_empty_raise(self):
        rb = create(3)
        with self.assertRaises(IndexError):
            pop(rb)
        with self.assertRaises(IndexError):
            peek(rb)

    def test_get_out_of_range_raises(self):
        rb = create(3)
        append(rb, 1)
        with self.assertRaises(IndexError):
            get(rb, 1)
        with self.assertRaises(IndexError):
            get(rb, -1)

    def test_invalid_capacity(self):
        with self.assertRaises(TypeError):
            create("3")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            create(0)
        with self.assertRaises(ValueError):
            create(-1)

    def test_clear(self):
        rb = create(3)
        append(rb, 1)
        append(rb, 2)
        clear(rb)
        self.assertTrue(is_empty(rb))
        self.assertEqual(size(rb), 0)
        self.assertEqual(to_list(rb), [])

    def test_from_list(self):
        rb = RingBuffer.from_list([1, 2, 3, 4], capacity=3)
        self.assertEqual(to_list(rb), [2, 3, 4])
        self.assertEqual(rb.capacity, 3)

    def test_from_list_default_capacity(self):
        rb = RingBuffer.from_list([1, 2, 3])
        self.assertEqual(to_list(rb), [1, 2, 3])
        self.assertEqual(rb.capacity, 3)

    def test_iteration_order(self):
        rb = create(3)
        append(rb, 1)
        append(rb, 2)
        self.assertEqual(list(rb), [1, 2])

    def test_repr(self):
        rb = create(3)
        append(rb, 1)
        append(rb, 2)
        self.assertIn("capacity=3", repr(rb))


if __name__ == "__main__":
    unittest.main()
