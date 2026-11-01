import unittest

from bytes_utils import (
    chunk,
    concat,
    contains,
    ends_with,
    from_hex,
    index,
    index_of,
    removeprefix,
    removesuffix,
    repeat,
    reverse,
    rfind,
    starts_with,
    to_hex,
    xor,
)


class TestBytesUtils(unittest.TestCase):
    def test_to_hex(self):
        self.assertEqual(to_hex(b"abc"), "616263")

    def test_from_hex(self):
        self.assertEqual(from_hex("616263"), b"abc")

    def test_xor(self):
        self.assertEqual(xor(b"abc", b"\x01"), b"`cb")

    def test_chunk(self):
        self.assertEqual(chunk(b"abcdef", 2), [b"ab", b"cd", b"ef"])

    def test_concat(self):
        self.assertEqual(concat(b"ab", b"cd", bytearray(b"ef")), b"abcdef")
        self.assertEqual(concat(), b"")

    def test_concat_type_error(self):
        with self.assertRaises(TypeError):
            concat(b"ab", "cd")

    def test_repeat(self):
        self.assertEqual(repeat(b"ab", 3), b"ababab")
        self.assertEqual(repeat(b"x", 0), b"")

    def test_repeat_errors(self):
        with self.assertRaises(TypeError):
            repeat("ab", 2)
        with self.assertRaises(ValueError):
            repeat(b"ab", -1)

    def test_reverse(self):
        self.assertEqual(reverse(b"abc"), b"cba")
        self.assertEqual(reverse(bytearray(b"ab")), b"ba")

    def test_contains(self):
        self.assertTrue(contains(b"hello", b"ll"))
        self.assertFalse(contains(b"hello", b"world"))

    def test_starts_ends(self):
        self.assertTrue(starts_with(b"hello", b"he"))
        self.assertFalse(starts_with(b"hello", b"lo"))
        self.assertTrue(ends_with(b"hello", b"lo"))
        self.assertFalse(ends_with(b"hello", b"he"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            to_hex("abc")
        with self.assertRaises(TypeError):
            from_hex(123)
        with self.assertRaises(TypeError):
            xor("abc", b"x")
        with self.assertRaises(TypeError):
            chunk(123, 2)
        with self.assertRaises(TypeError):
            reverse("abc")
        with self.assertRaises(TypeError):
            contains("a", b"a")
        with self.assertRaises(TypeError):
            contains(b"a", "a")
        with self.assertRaises(TypeError):
            starts_with("a", b"a")
        with self.assertRaises(TypeError):
            ends_with(b"a", "a")

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            xor(b"abc", b"")
        with self.assertRaises(ValueError):
            chunk(b"abc", 0)


class TestIndexOf(unittest.TestCase):
    def test_found(self):
        self.assertEqual(index_of(b"hello world", b"world"), 6)
        self.assertEqual(index_of(b"hello world", b"hello"), 0)
        self.assertEqual(index_of(b"abcabc", b"bc"), 1)

    def test_not_found(self):
        self.assertEqual(index_of(b"hello", b"x"), -1)
        self.assertEqual(index_of(b"abc", b"abcd"), -1)

    def test_empty_subsequence(self):
        self.assertEqual(index_of(b"abc", b""), 0)
        self.assertEqual(index_of(b"", b""), 0)

    def test_first_occurrence(self):
        self.assertEqual(index_of(b"ababab", b"ab"), 0)
        self.assertEqual(index_of(b"xabxab", b"ab"), 1)

    def test_bytearray_input(self):
        self.assertEqual(index_of(bytearray(b"hello"), b"ll"), 2)
        self.assertEqual(index_of(b"hello", bytearray(b"lo")), 3)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            index_of("abc", b"a")
        with self.assertRaises(TypeError):
            index_of(b"abc", "a")
        with self.assertRaises(TypeError):
            index_of(123, b"a")


class TestIndex(unittest.TestCase):
    def test_found(self):
        self.assertEqual(index(b"hello world", b"world"), 6)
        self.assertEqual(index(b"hello world", b"hello"), 0)
        self.assertEqual(index(b"abcabc", b"bc"), 1)

    def test_not_found_raises(self):
        with self.assertRaises(ValueError):
            index(b"hello", b"x")
        with self.assertRaises(ValueError):
            index(b"abc", b"abcd")

    def test_empty_subsequence(self):
        self.assertEqual(index(b"abc", b""), 0)
        self.assertEqual(index(b"", b""), 0)

    def test_first_occurrence(self):
        self.assertEqual(index(b"ababab", b"ab"), 0)
        self.assertEqual(index(b"xabxab", b"ab"), 1)

    def test_bytearray_input(self):
        self.assertEqual(index(bytearray(b"hello"), b"ll"), 2)
        self.assertEqual(index(b"hello", bytearray(b"lo")), 3)

    def test_start_end(self):
        self.assertEqual(index(b"hello world", b"o", 1, 5), 4)
        self.assertEqual(index(b"ababab", b"ab", 2), 2)
        self.assertEqual(index(b"ababab", b"ab", 0, 4), 0)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            index("abc", b"a")
        with self.assertRaises(TypeError):
            index(b"abc", "a")
        with self.assertRaises(TypeError):
            index(123, b"a")
        with self.assertRaises(TypeError):
            index(b"abc", b"a", start="0")
        with self.assertRaises(TypeError):
            index(b"abc", b"a", end=1.5)


class TestRFind(unittest.TestCase):
    def test_found(self):
        self.assertEqual(rfind(b"hello world", b"o"), 7)
        self.assertEqual(rfind(b"hello world", b"world"), 6)
        self.assertEqual(rfind(b"abcabc", b"bc"), 4)

    def test_not_found(self):
        self.assertEqual(rfind(b"hello", b"x"), -1)
        self.assertEqual(rfind(b"abc", b"abcd"), -1)
        self.assertEqual(rfind(b"", b"a"), -1)

    def test_empty_subsequence(self):
        self.assertEqual(rfind(b"abc", b""), 3)
        self.assertEqual(rfind(b"", b""), 0)

    def test_last_occurrence(self):
        self.assertEqual(rfind(b"ababab", b"ab"), 4)
        self.assertEqual(rfind(b"xabxab", b"ab"), 4)

    def test_bytearray_input(self):
        self.assertEqual(rfind(bytearray(b"hello"), b"ll"), 2)
        self.assertEqual(rfind(b"hello", bytearray(b"lo")), 3)

    def test_start_end(self):
        self.assertEqual(rfind(b"hello world", b"o", 0, 5), 4)
        self.assertEqual(rfind(b"ababab", b"ab", 2), 4)
        self.assertEqual(rfind(b"ababab", b"ab", 0, 4), 2)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            rfind("abc", b"a")
        with self.assertRaises(TypeError):
            rfind(b"abc", "a")
        with self.assertRaises(TypeError):
            rfind(123, b"a")
        with self.assertRaises(TypeError):
            rfind(b"abc", b"a", start="0")
        with self.assertRaises(TypeError):
            rfind(b"abc", b"a", end=1.5)


class TestRemovePrefix(unittest.TestCase):
    def test_removes_prefix(self):
        self.assertEqual(removeprefix(b"hello", b"he"), b"llo")
        self.assertEqual(removeprefix(b"hello world", b"hello "), b"world")

    def test_prefix_not_present(self):
        self.assertEqual(removeprefix(b"hello", b"lo"), b"hello")
        self.assertEqual(removeprefix(b"abc", b"xyz"), b"abc")

    def test_empty_prefix(self):
        self.assertEqual(removeprefix(b"hello", b""), b"hello")

    def test_empty_data(self):
        self.assertEqual(removeprefix(b"", b"x"), b"")
        self.assertEqual(removeprefix(b"", b""), b"")

    def test_full_match(self):
        self.assertEqual(removeprefix(b"abc", b"abc"), b"")

    def test_bytearray_input(self):
        self.assertEqual(removeprefix(bytearray(b"hello"), b"he"), b"llo")
        self.assertEqual(removeprefix(b"hello", bytearray(b"he")), b"llo")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            removeprefix("hello", b"he")
        with self.assertRaises(TypeError):
            removeprefix(b"hello", "he")
        with self.assertRaises(TypeError):
            removeprefix(123, b"he")
        with self.assertRaises(TypeError):
            removeprefix(b"hello", 123)


class TestRemoveSuffix(unittest.TestCase):
    def test_removes_suffix(self):
        self.assertEqual(removesuffix(b"hello", b"lo"), b"hel")
        self.assertEqual(removesuffix(b"hello world", b" world"), b"hello")

    def test_suffix_not_present(self):
        self.assertEqual(removesuffix(b"hello", b"he"), b"hello")
        self.assertEqual(removesuffix(b"abc", b"xyz"), b"abc")

    def test_empty_suffix(self):
        self.assertEqual(removesuffix(b"hello", b""), b"hello")

    def test_empty_data(self):
        self.assertEqual(removesuffix(b"", b"x"), b"")
        self.assertEqual(removesuffix(b"", b""), b"")

    def test_full_match(self):
        self.assertEqual(removesuffix(b"abc", b"abc"), b"")

    def test_bytearray_input(self):
        self.assertEqual(removesuffix(bytearray(b"hello"), b"lo"), b"hel")
        self.assertEqual(removesuffix(b"hello", bytearray(b"lo")), b"hel")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            removesuffix("hello", b"lo")
        with self.assertRaises(TypeError):
            removesuffix(b"hello", "lo")
        with self.assertRaises(TypeError):
            removesuffix(123, b"lo")
        with self.assertRaises(TypeError):
            removesuffix(b"hello", 123)


if __name__ == "__main__":
    unittest.main()
