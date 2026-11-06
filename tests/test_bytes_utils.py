import unittest

from bytes_utils import (
    bit_count,
    capitalize,
    casefold,
    chunk,
    concat,
    contains,
    decode_ascii,
    encode_ascii,
    ends_with,
    expandtabs,
    from_hex,
    index,
    index_of,
    is_zero,
    isalnum,
    isalpha,
    isascii,
    isdigit,
    islower,
    isspace,
    istitle,
    isupper,
    join,
    lower,
    maketrans,
    partition,
    removeprefix,
    removesuffix,
    repeat,
    reverse,
    rfind,
    rpartition,
    splitlines,
    starts_with,
    swapcase,
    title,
    to_hex,
    translate,
    upper,
    xor,
)
import bytes_utils


class TestBytesUtils(unittest.TestCase):
    def test_to_hex(self):
        self.assertEqual(to_hex(b"abc"), "616263")

    def test_from_hex(self):
        self.assertEqual(from_hex("616263"), b"abc")

    def test_xor(self):
        self.assertEqual(xor(b"abc", b"\x01"), b"`cb")

    def test_chunk(self):
        self.assertEqual(chunk(b"abcdef", 2), [b"ab", b"cd", b"ef"])

    def test_chunk_bool_size(self):
        with self.assertRaises(ValueError):
            chunk(b"ab", True)

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
        with self.assertRaises(ValueError):
            repeat(b"ab", True)

    def test_reverse(self):
        self.assertEqual(reverse(b"abc"), b"cba")
        self.assertEqual(reverse(bytearray(b"ab")), b"ba")

    def test_upper(self):
        self.assertEqual(upper(b"abc"), b"ABC")
        self.assertEqual(upper(bytearray(b"ab")), b"AB")

    def test_lower(self):
        self.assertEqual(lower(b"ABC"), b"abc")
        self.assertEqual(lower(bytearray(b"AB")), b"ab")

    def test_capitalize(self):
        self.assertEqual(capitalize(b"hello world"), b"Hello world")
        self.assertEqual(capitalize(b"HELLO"), b"Hello")
        self.assertEqual(capitalize(bytearray(b"hello")), b"Hello")
        self.assertEqual(capitalize(b""), b"")

    def test_title(self):
        self.assertEqual(title(b"hello world"), b"Hello World")
        self.assertEqual(title(b"hello-world"), b"Hello-World")
        self.assertEqual(title(b"HELLO WORLD"), b"Hello World")
        self.assertEqual(title(bytearray(b"hello world")), b"Hello World")
        self.assertEqual(title(b""), b"")

    def test_swapcase(self):
        self.assertEqual(swapcase(b"Hello World"), b"hELLO wORLD")
        self.assertEqual(swapcase(b"HELLO"), b"hello")
        self.assertEqual(swapcase(b"hello"), b"HELLO")
        self.assertEqual(swapcase(bytearray(b"Hello")), b"hELLO")
        self.assertEqual(swapcase(b""), b"")

    def test_casefold(self):
        self.assertEqual(casefold(b"Hello"), b"hello")
        self.assertEqual(casefold(bytearray(b"Hello")), b"hello")
        self.assertEqual(casefold(b""), b"")

    def test_join(self):
        self.assertEqual(join([b"ab", b"cd"]), b"abcd")
        self.assertEqual(join([b"a", b"b"], b"-"), b"a-b")
        self.assertEqual(join([], b"-"), b"")
        with self.assertRaises(TypeError):
            join([b"ab"], "x")

    def test_expandtabs(self):
        self.assertEqual(expandtabs(b"a\tb"), b"a       b")
        self.assertEqual(expandtabs(b"a\tb", 4), b"a   b")
        self.assertEqual(expandtabs(bytearray(b"a\tb")), b"a       b")
        with self.assertRaises(TypeError):
            expandtabs("a\tb")
        with self.assertRaises(TypeError):
            expandtabs(b"a\tb", "4")

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


class TestPredicates(unittest.TestCase):
    def test_isalnum(self):
        self.assertTrue(isalnum(b"abc123"))
        self.assertTrue(isalnum(bytearray(b"abc123")))
        self.assertFalse(isalnum(b"abc 123"))
        self.assertFalse(isalnum(b""))
        self.assertFalse(isalnum(b"!@#"))

    def test_isalpha(self):
        self.assertTrue(isalpha(b"abc"))
        self.assertTrue(isalpha(bytearray(b"ABC")))
        self.assertFalse(isalpha(b"abc123"))
        self.assertFalse(isalpha(b""))
        self.assertFalse(isalpha(b"ab c"))

    def test_isascii(self):
        self.assertTrue(isascii(b"abc"))
        self.assertTrue(isascii(bytearray(b"123")))
        self.assertFalse(isascii(b"\x80"))
        self.assertTrue(isascii(b""))

    def test_isdigit(self):
        self.assertTrue(isdigit(b"123"))
        self.assertTrue(isdigit(bytearray(b"0")))
        self.assertFalse(isdigit(b"12a"))
        self.assertFalse(isdigit(b""))
        self.assertFalse(isdigit(b"1.5"))

    def test_islower(self):
        self.assertTrue(islower(b"abc"))
        self.assertTrue(islower(bytearray(b"abc123")))
        self.assertFalse(islower(b"ABC"))
        self.assertFalse(islower(b"Abc"))
        self.assertFalse(islower(b""))
        self.assertFalse(islower(b" "))

    def test_isspace(self):
        self.assertTrue(isspace(b"   "))
        self.assertTrue(isspace(bytearray(b"\t\n")))
        self.assertFalse(isspace(b""))
        self.assertFalse(isspace(b"a"))

    def test_istitle(self):
        self.assertTrue(istitle(b"Hello World"))
        self.assertTrue(istitle(bytearray(b"Hello")))
        self.assertFalse(istitle(b"hello world"))
        self.assertFalse(istitle(b"HelloWorld"))
        self.assertFalse(istitle(b""))

    def test_isupper(self):
        self.assertTrue(isupper(b"ABC"))
        self.assertTrue(isupper(bytearray(b"ABC123")))
        self.assertFalse(isupper(b"abc"))
        self.assertFalse(isupper(b"Abc"))
        self.assertFalse(isupper(b""))
        self.assertFalse(isupper(b" "))

    def test_type_errors(self):
        for fn in (
            isalnum,
            isalpha,
            isascii,
            isdigit,
            islower,
            isspace,
            istitle,
            isupper,
        ):
            with self.assertRaises(TypeError):
                fn("abc")
            with self.assertRaises(TypeError):
                fn(123)


class TestAsciiHelpers(unittest.TestCase):
    def test_decode_ascii(self):
        self.assertEqual(decode_ascii(b"abc"), "abc")
        self.assertEqual(decode_ascii(bytearray(b"hi")), "hi")
        self.assertEqual(decode_ascii(b"\x00\x01"), "\x00\x01")

    def test_decode_ascii_errors(self):
        with self.assertRaises(UnicodeDecodeError):
            decode_ascii(b"\x80")
        with self.assertRaises(TypeError):
            decode_ascii("abc")
        with self.assertRaises(TypeError):
            decode_ascii(b"abc", errors=123)

    def test_encode_ascii(self):
        self.assertEqual(encode_ascii("abc"), b"abc")
        self.assertEqual(encode_ascii("", errors="ignore"), b"")

    def test_encode_ascii_errors(self):
        with self.assertRaises(UnicodeEncodeError):
            encode_ascii("café")
        with self.assertRaises(TypeError):
            encode_ascii(b"abc")
        with self.assertRaises(TypeError):
            encode_ascii("abc", errors=123)


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


class TestPartition(unittest.TestCase):
    def test_partition_found(self):
        self.assertEqual(partition(b"hello world", b" "), (b"hello", b" ", b"world"))
        self.assertEqual(partition(b"abcabc", b"ab"), (b"", b"ab", b"cabc"))
        self.assertEqual(partition(b"hello world", b"world"), (b"hello ", b"world", b""))

    def test_partition_not_found(self):
        self.assertEqual(partition(b"hello", b"x"), (b"hello", b"", b""))
        self.assertEqual(partition(b"abc", b"abcd"), (b"abc", b"", b""))

    def test_partition_empty_separator(self):
        with self.assertRaises(ValueError):
            partition(b"abc", b"")

    def test_partition_bytearray_input(self):
        self.assertEqual(partition(bytearray(b"hello world"), b" "), (b"hello", b" ", b"world"))
        self.assertEqual(partition(b"hello", bytearray(b"x")), (b"hello", b"", b""))

    def test_partition_type_errors(self):
        with self.assertRaises(TypeError):
            partition("hello", b" ")
        with self.assertRaises(TypeError):
            partition(b"hello", " ")
        with self.assertRaises(TypeError):
            partition(123, b" ")
        with self.assertRaises(TypeError):
            partition(b"hello", 123)


class TestRPartition(unittest.TestCase):
    def test_rpartition_found(self):
        self.assertEqual(rpartition(b"hello world", b" "), (b"hello", b" ", b"world"))
        self.assertEqual(rpartition(b"ababab", b"ab"), (b"abab", b"ab", b""))
        self.assertEqual(rpartition(b"hello world", b"hello"), (b"", b"hello", b" world"))

    def test_rpartition_not_found(self):
        self.assertEqual(rpartition(b"hello", b"x"), (b"", b"", b"hello"))
        self.assertEqual(rpartition(b"abc", b"abcd"), (b"", b"", b"abc"))

    def test_rpartition_empty_separator(self):
        with self.assertRaises(ValueError):
            rpartition(b"abc", b"")

    def test_rpartition_bytearray_input(self):
        self.assertEqual(rpartition(bytearray(b"hello world"), b" "), (b"hello", b" ", b"world"))
        self.assertEqual(rpartition(b"hello", bytearray(b"x")), (b"", b"", b"hello"))

    def test_rpartition_type_errors(self):
        with self.assertRaises(TypeError):
            rpartition("hello", b" ")
        with self.assertRaises(TypeError):
            rpartition(b"hello", " ")
        with self.assertRaises(TypeError):
            rpartition(123, b" ")
        with self.assertRaises(TypeError):
            rpartition(b"hello", 123)


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


class TestRSplit(unittest.TestCase):
    def test_rsplit_basic(self):
        self.assertEqual(bytes_utils.rsplit(b"a b c", None, 1), [b"a b", b"c"])
        self.assertEqual(bytes_utils.rsplit(b"a b c", None, 2), [b"a", b"b", b"c"])
        self.assertEqual(bytes_utils.rsplit(b"a,b,c", b",", 1), [b"a,b", b"c"])
        self.assertEqual(bytes_utils.rsplit(b"a,b,c", b",", -1), [b"a", b"b", b"c"])

    def test_rsplit_whitespace_boundaries(self):
        self.assertEqual(bytes_utils.rsplit(b"a b c", None, 0), [b"a b c"])
        self.assertEqual(bytes_utils.rsplit(b"   ", None), [])
        self.assertEqual(bytes_utils.rsplit(b"", None), [])
        self.assertEqual(bytes_utils.rsplit(bytearray(b"a b"), None, 1), [b"a", b"b"])

    def test_rsplit_sep_edges(self):
        self.assertEqual(bytes_utils.rsplit(b"", b","), [b""])
        self.assertEqual(bytes_utils.rsplit(b"a", b","), [b"a"])
        self.assertEqual(bytes_utils.rsplit(bytearray(b"a,b"), bytearray(b","), 1), [b"a", b"b"])
        with self.assertRaises(ValueError):
            bytes_utils.rsplit(b"a", b"")

    def test_rsplit_type_errors(self):
        with self.assertRaises(TypeError):
            bytes_utils.rsplit("a b")
        with self.assertRaises(TypeError):
            bytes_utils.rsplit(b"a b", sep=1)
        with self.assertRaises(TypeError):
            bytes_utils.rsplit(b"a b", maxsplit=True)





class TestSplitlines(unittest.TestCase):
    def test_splitlines_basic(self):
        self.assertEqual(splitlines(b"hello\nworld"), [b"hello", b"world"])
        self.assertEqual(splitlines(b"hello\r\nworld"), [b"hello", b"world"])
        self.assertEqual(splitlines(b"hello\rworld"), [b"hello", b"world"])
        self.assertEqual(splitlines(b"a\nb\nc"), [b"a", b"b", b"c"])

    def test_splitlines_keepends(self):
        self.assertEqual(splitlines(b"hello\nworld", keepends=True), [b"hello\n", b"world"])
        self.assertEqual(splitlines(b"hello\r\n", keepends=True), [b"hello\r\n"])

    def test_splitlines_empty(self):
        self.assertEqual(splitlines(b""), [])

    def test_splitlines_no_newline(self):
        self.assertEqual(splitlines(b"hello"), [b"hello"])

    def test_splitlines_trailing_newline(self):
        self.assertEqual(splitlines(b"hello\n"), [b"hello"])

    def test_splitlines_bytearray(self):
        self.assertEqual(splitlines(bytearray(b"hello\nworld")), [b"hello", b"world"])

    def test_splitlines_type_errors(self):
        with self.assertRaises(TypeError):
            splitlines("hello\n")
        with self.assertRaises(TypeError):
            splitlines(b"hello\n", keepends="true")
        with self.assertRaises(TypeError):
            splitlines(123)


class TestMaketrans(unittest.TestCase):
    def test_basic_mapping(self):
        table = maketrans(b"ab", b"xy")
        self.assertEqual(table[97], 120)  # ord('a') -> ord('x')
        self.assertEqual(table[98], 121)  # ord('b') -> ord('y')

    def test_identity_for_unmapped_bytes(self):
        table = maketrans(b"ab", b"xy")
        self.assertEqual(table[99], 99)  # ord('c') unchanged
        self.assertEqual(table[0], 0)
        self.assertEqual(table[255], 255)

    def test_empty_inputs_identity(self):
        self.assertEqual(maketrans(b"", b""), bytes(range(256)))

    def test_multiple_pairs(self):
        table = maketrans(b"abc", b"123")
        self.assertEqual(table[97], 49)  # 'a' -> '1'
        self.assertEqual(table[98], 50)  # 'b' -> '2'
        self.assertEqual(table[99], 51)  # 'c' -> '3'

    def test_bytearray_input(self):
        table = maketrans(bytearray(b"ab"), bytearray(b"xy"))
        self.assertEqual(table[97], 120)
        self.assertEqual(table[98], 121)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            maketrans("ab", b"xy")
        with self.assertRaises(TypeError):
            maketrans(b"ab", "xy")
        with self.assertRaises(TypeError):
            maketrans(123, b"xy")

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            maketrans(b"ab", b"xyz")
        with self.assertRaises(ValueError):
            maketrans(b"abc", b"xy")


class TestTranslate(unittest.TestCase):
    def test_basic_translation(self):
        self.assertEqual(translate(b"abc", maketrans(b"ab", b"xy")), b"xyc")

    def test_identity_table(self):
        self.assertEqual(translate(b"abc", bytes(range(256))), b"abc")

    def test_empty_data(self):
        self.assertEqual(translate(b"", maketrans(b"ab", b"xy")), b"")

    def test_bytearray_input(self):
        self.assertEqual(translate(bytearray(b"abc"), maketrans(b"ab", b"xy")), b"xyc")

    def test_full_byte_range(self):
        self.assertEqual(
            translate(bytes(range(256)), maketrans(b"\x00\x01", b"\x01\x00")),
            bytes([1, 0]) + bytes(range(2, 256)),
        )

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            translate("abc", maketrans(b"ab", b"xy"))
        with self.assertRaises(TypeError):
            translate(b"abc", "table")
        with self.assertRaises(TypeError):
            translate(123, maketrans(b"ab", b"xy"))

    def test_table_length_errors(self):
        with self.assertRaises(ValueError):
            translate(b"abc", b"short")
        with self.assertRaises(ValueError):
            translate(b"abc", bytes(range(255)))


class TestBitCount(unittest.TestCase):
    def test_zero_byte(self):
        self.assertEqual(bit_count(b"\x00"), 0)

    def test_all_set(self):
        self.assertEqual(bit_count(b"\xff"), 8)

    def test_mixed(self):
        self.assertEqual(bit_count(b"\x0f\x00"), 4)
        self.assertEqual(bit_count(b"\x01\x02\x04"), 3)

    def test_empty(self):
        self.assertEqual(bit_count(b""), 0)

    def test_bytearray(self):
        self.assertEqual(bit_count(bytearray(b"\xff\x00")), 8)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            bit_count("ff")
        with self.assertRaises(TypeError):
            bit_count(255)
        with self.assertRaises(TypeError):
            bit_count(None)


class TestIsZero(unittest.TestCase):
    def test_all_zero(self):
        self.assertTrue(is_zero(b"\x00\x00\x00"))

    def test_contains_nonzero(self):
        self.assertFalse(is_zero(b"\x00\x01\x00"))
        self.assertFalse(is_zero(b"\xff"))

    def test_empty(self):
        self.assertTrue(is_zero(b""))

    def test_single_zero(self):
        self.assertTrue(is_zero(b"\x00"))

    def test_bytearray(self):
        self.assertTrue(is_zero(bytearray(b"\x00\x00")))
        self.assertFalse(is_zero(bytearray(b"\x00\x01")))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_zero("00")
        with self.assertRaises(TypeError):
            is_zero(0)
        with self.assertRaises(TypeError):
            is_zero(None)
