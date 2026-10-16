"""Unit tests for bit_utils module."""

import unittest

from bit_utils import (
    clear_bit,
    count_set_bits,
    get_bit,
    is_even,
    is_odd,
    is_power_of_two,
    next_power_of_two,
    prev_power_of_two,
    reverse_bits,
    rotate_left,
    rotate_right,
    set_bit,
    toggle_bit,
)


class TestCountSetBits(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(count_set_bits(0), 0)

    def test_single_bit(self):
        self.assertEqual(count_set_bits(1), 1)
        self.assertEqual(count_set_bits(8), 1)

    def test_multiple_bits(self):
        self.assertEqual(count_set_bits(5), 2)  # 0b101
        self.assertEqual(count_set_bits(7), 3)  # 0b111
        self.assertEqual(count_set_bits(255), 8)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            count_set_bits("5")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            count_set_bits(True)  # type: ignore[arg-type]

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            count_set_bits(-1)


class TestIsPowerOfTwo(unittest.TestCase):
    def test_powers_of_two(self):
        self.assertTrue(is_power_of_two(1))
        self.assertTrue(is_power_of_two(2))
        self.assertTrue(is_power_of_two(1024))

    def test_not_powers_of_two(self):
        self.assertFalse(is_power_of_two(0))
        self.assertFalse(is_power_of_two(3))
        self.assertFalse(is_power_of_two(18))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_power_of_two("8")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_power_of_two(True)  # type: ignore[arg-type]


class TestNextPrevPowerOfTwo(unittest.TestCase):
    def test_next_power_of_two(self):
        self.assertEqual(next_power_of_two(0), 1)
        self.assertEqual(next_power_of_two(1), 1)
        self.assertEqual(next_power_of_two(5), 8)
        self.assertEqual(next_power_of_two(16), 16)
        self.assertEqual(next_power_of_two(17), 32)

    def test_prev_power_of_two(self):
        self.assertEqual(prev_power_of_two(0), 0)
        self.assertEqual(prev_power_of_two(1), 1)
        self.assertEqual(prev_power_of_two(5), 4)
        self.assertEqual(prev_power_of_two(16), 16)
        self.assertEqual(prev_power_of_two(17), 16)

    def test_errors(self):
        with self.assertRaises(ValueError):
            next_power_of_two(-1)
        with self.assertRaises(ValueError):
            prev_power_of_two(-1)
        with self.assertRaises(TypeError):
            next_power_of_two("5")  # type: ignore[arg-type]


class TestReverseBits(unittest.TestCase):
    def test_reverse_within_width(self):
        self.assertEqual(reverse_bits(0b0001, 4), 0b1000)
        self.assertEqual(reverse_bits(13, 4), 11)  # 1101 -> 1011
        self.assertEqual(reverse_bits(0, 4), 0)

    def test_default_width(self):
        self.assertEqual(reverse_bits(1), 1)
        self.assertEqual(reverse_bits(0), 0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            reverse_bits(-1, 4)
        with self.assertRaises(ValueError):
            reverse_bits(5, 0)
        with self.assertRaises(TypeError):
            reverse_bits(5, "4")  # type: ignore[arg-type]


class TestRotate(unittest.TestCase):
    def test_rotate_left(self):
        self.assertEqual(rotate_left(0b0001, 1, 4), 0b0010)
        self.assertEqual(rotate_left(0b1000, 1, 4), 0b0001)
        self.assertEqual(rotate_left(0b0011, 2, 4), 0b1100)

    def test_rotate_right(self):
        self.assertEqual(rotate_right(0b1000, 1, 4), 0b0100)
        self.assertEqual(rotate_right(0b0001, 1, 4), 0b1000)
        self.assertEqual(rotate_right(0b1100, 2, 4), 0b0011)

    def test_shift_wraps(self):
        self.assertEqual(rotate_left(0b0001, 5, 4), 0b0010)
        self.assertEqual(rotate_right(0b0001, 5, 4), 0b1000)

    def test_errors(self):
        with self.assertRaises(ValueError):
            rotate_left(-1, 1, 4)
        with self.assertRaises(ValueError):
            rotate_left(1, 1, 0)
        with self.assertRaises(TypeError):
            rotate_left(1, "1", 4)  # type: ignore[arg-type]


class TestBitAccess(unittest.TestCase):
    def test_get_bit(self):
        self.assertEqual(get_bit(0b1010, 0), 0)
        self.assertEqual(get_bit(0b1010, 1), 1)
        self.assertEqual(get_bit(0b1010, 2), 0)
        self.assertEqual(get_bit(0b1010, 3), 1)

    def test_set_bit(self):
        self.assertEqual(set_bit(0b0000, 2), 0b0100)
        self.assertEqual(set_bit(0b1010, 0), 0b1011)

    def test_clear_bit(self):
        self.assertEqual(clear_bit(0b1111, 1), 0b1101)
        self.assertEqual(clear_bit(0b1010, 3), 0b0010)

    def test_toggle_bit(self):
        self.assertEqual(toggle_bit(0b1010, 1), 0b1000)
        self.assertEqual(toggle_bit(0b1010, 0), 0b1011)

    def test_errors(self):
        with self.assertRaises(ValueError):
            get_bit(-1, 0)
        with self.assertRaises(ValueError):
            set_bit(0, -1)
        with self.assertRaises(TypeError):
            get_bit(0, "0")  # type: ignore[arg-type]


class TestEvenOdd(unittest.TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(0))
        self.assertTrue(is_even(4))
        self.assertFalse(is_even(7))

    def test_is_odd(self):
        self.assertFalse(is_odd(0))
        self.assertFalse(is_odd(4))
        self.assertTrue(is_odd(7))

    def test_errors(self):
        with self.assertRaises(TypeError):
            is_even("4")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_odd(True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
