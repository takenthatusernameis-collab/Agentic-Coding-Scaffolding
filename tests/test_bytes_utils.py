import unittest

import bytes_utils
from bytes_utils import (
    bit_count,
    capitalize,
    casefold,
    chunk,
    concat,
    contains,
    count,
    decode_ascii,
    encode_ascii,
    ends_with,
    expandtabs,
    find,
    from_hex,
    from_int,
    has_null_byte,
    highest_set_bit,
    index,
    index_of,
    is_all_ones,
    is_power_of_two,
    is_zero,
    isalnum,
    isalpha,
    isascii,
    isdigit,
    isidentifier,
    islower,
    isprintable,
    isspace,
    istitle,
    isupper,
    join,
    lower,
    lowest_set_bit,
    maketrans,
    partition,
    removeprefix,
    removesuffix,
    repeat,
    replace,
    reverse,
    rfind,
    rindex,
    rpartition,
    split,
    splitlines,
    starts_with,
    swapcase,
    title,
    to_hex,
    to_int,
    translate,
    upper,
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
        self.assertEqual(upper(b"Ab1!"), b"AB1!")
        self.assertEqual(upper(b""), b"")
        with self.assertRaises(TypeError):
            upper("abc")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            upper(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            upper(None)  # type: ignore[arg-type]

    def test_lower(self):
        self.assertEqual(lower(b"ABC"), b"abc")
        self.assertEqual(lower(bytearray(b"AB")), b"ab")
        self.assertEqual(lower(b"Ab1!"), b"ab1!")
        self.assertEqual(lower(b""), b"")
        with self.assertRaises(TypeError):
            lower("ABC")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            lower(123)  # type: ignore[arg-type]

    def test_capitalize(self):
        self.assertEqual(capitalize(b"hello world"), b"Hello world")
        self.assertEqual(capitalize(b"HELLO"), b"Hello")
        self.assertEqual(capitalize(bytearray(b"hello")), b"Hello")
        self.assertEqual(capitalize(b""), b"")
        with self.assertRaises(TypeError):
            capitalize("hello")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            capitalize(None)  # type: ignore[arg-type]
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

    def test_case_helpers_type_and_bytearray(self):
        from bytes_utils import capitalize, casefold, lower, swapcase, title, upper
        for fn in (upper, lower, capitalize, title, swapcase, casefold):
            self.assertEqual(fn(bytearray(b"AbC")), fn(b"AbC"))
            self.assertEqual(fn(b""), b"")
            with self.assertRaises(TypeError):
                fn("abc")

    def test_predicate_type_and_empty(self):
        from bytes_utils import (
            isalnum,
            isalpha,
            isascii,
            isdigit,
            islower,
            isspace,
            istitle,
            isupper,
        )
        preds = (isalnum, isalpha, isascii, isdigit, islower, isspace, istitle, isupper)
        for fn in preds:
            self.assertIsInstance(fn(bytearray(b"a")), bool)
            with self.assertRaises(TypeError):
                fn("abc")
            with self.assertRaises(TypeError):
                fn(None)


    def test_type_errors(self):
        for fn in (
            isalnum,
            isalpha,
            isascii,
            isdigit,
            islower,
            isprintable,
            isidentifier,
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
        with self.assertRaises(TypeError):
            index(b"abc", b"a", start=True)
        with self.assertRaises(TypeError):
            index(b"abc", b"a", end=True)

    def test_negative_indices(self):
        self.assertEqual(index(b"abcabc", b"bc", -3), 4)
        self.assertEqual(index(b"abcabc", b"bc", 0, -1), 1)


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
        with self.assertRaises(TypeError):
            rfind(b"abc", b"a", start=True)
        with self.assertRaises(TypeError):
            rfind(b"abc", b"a", end=True)

    def test_negative_indices(self):
        self.assertEqual(rfind(b"abcabc", b"bc", -5, -1), 1)
        self.assertEqual(rfind(b"abcabc", b"bc", -3), 4)


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
        self.assertEqual(splitlines(bytearray(b"a\r\nb"), keepends=True), [b"a\r\n", b"b"])

    def test_splitlines_empty(self):
        self.assertEqual(splitlines(b""), [])

    def test_splitlines_no_newline(self):
        self.assertEqual(splitlines(b"hello"), [b"hello"])

    def test_splitlines_trailing_newline(self):
        self.assertEqual(splitlines(b"hello\n"), [b"hello"])
        self.assertEqual(splitlines(b"hello\r"), [b"hello"])

    def test_splitlines_bytearray(self):
        self.assertEqual(splitlines(bytearray(b"hello\nworld")), [b"hello", b"world"])

    def test_splitlines_uncommon_separators_not_boundaries(self):
        # bytes.splitlines recognizes only \n, \r, \r\n.
        for sep in [b"\x0b", b"\x0c", b"\x1c", b"\x1d", b"\x1e", b"\x85"]:
            data = b"a" + sep + b"b"
            self.assertEqual(splitlines(data), [data])
            self.assertEqual(splitlines(data, keepends=True), [data])

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

    def test_bytearray_table(self):
        self.assertEqual(translate(b"abc", bytearray(range(256))), b"abc")
        table = maketrans(b"ab", b"xy")
        self.assertEqual(translate(b"abc", bytearray(table)), b"xyc")

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


class TestTitle(unittest.TestCase):
    def test_title(self):
        self.assertEqual(title(b"hello world"), b"Hello World")
        self.assertEqual(title(b"hello-world"), b"Hello-World")
        self.assertEqual(title(b"HELLO WORLD"), b"Hello World")
        self.assertEqual(title(bytearray(b"hello world")), b"Hello World")
        self.assertEqual(title(b""), b"")
        with self.assertRaises(TypeError):
            title("hello")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            title([])  # type: ignore[arg-type]
        self.assertEqual(title(b"a b c"), b"A B C")

    def test_empty(self):
        self.assertEqual(title(b""), b"")

    def test_bytearray(self):
        self.assertEqual(title(bytearray(b"hello world")), b"Hello World")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            title("hello")
        with self.assertRaises(TypeError):
            title(123)
        with self.assertRaises(TypeError):
            title(None)


class TestSwapcase(unittest.TestCase):
    def test_swapcase(self):
        self.assertEqual(swapcase(b"Hello"), b"hELLO")
        self.assertEqual(swapcase(b"AbCd123"), b"aBcD123")
        self.assertEqual(swapcase(b"all lower"), b"ALL LOWER")
        self.assertEqual(swapcase(b"ALL UPPER"), b"all upper")

    def test_empty(self):
        self.assertEqual(swapcase(b""), b"")

    def test_bytearray(self):
        self.assertEqual(swapcase(bytearray(b"Hello")), b"hELLO")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            swapcase("hello")
        with self.assertRaises(TypeError):
            swapcase(123)
        with self.assertRaises(TypeError):
            swapcase(None)


class TestCasefold(unittest.TestCase):
    def test_casefold(self):
        self.assertEqual(casefold(b"Hello"), b"hello")
        self.assertEqual(casefold(b"HELLO"), b"hello")

    def test_german_sharp_s(self):
        self.assertEqual(casefold(b"\xc3\x9f"), b"ss")

    def test_empty(self):
        self.assertEqual(casefold(b""), b"")

    def test_bytearray(self):
        self.assertEqual(casefold(bytearray(b"Hello")), b"hello")

    def test_invalid_utf8_fallback(self):
        self.assertEqual(casefold(b"\xff"), b"\xff".lower())

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            casefold("hello")
        with self.assertRaises(TypeError):
            casefold(123)
        with self.assertRaises(TypeError):
            casefold(None)


class TestHasNullByte(unittest.TestCase):
    def test_has_null(self):
        self.assertTrue(has_null_byte(b"\x00\x00\x00"))

    def test_no_null(self):
        self.assertFalse(has_null_byte(b"\x01\x02\x03"))
        self.assertFalse(has_null_byte(b"\xff"))

    def test_empty(self):
        self.assertFalse(has_null_byte(b""))

    def test_single_null(self):
        self.assertTrue(has_null_byte(b"\x00"))

    def test_bytearray(self):
        self.assertTrue(has_null_byte(bytearray(b"\x00\x00")))
        self.assertFalse(has_null_byte(bytearray(b"\x01\x02")))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            has_null_byte("00")
        with self.assertRaises(TypeError):
            has_null_byte(0)
        with self.assertRaises(TypeError):
            has_null_byte(None)


class TestIsPowerOfTwo(unittest.TestCase):
    def test_single_bit_set(self):
        self.assertTrue(is_power_of_two(b"\x01"))
        self.assertTrue(is_power_of_two(b"\x80"))
        self.assertTrue(is_power_of_two(from_hex("0100")))
        self.assertTrue(is_power_of_two(from_hex("0001")))
        self.assertTrue(is_power_of_two(bytearray(b"\x01")))

    def test_not_power_of_two(self):
        self.assertFalse(is_power_of_two(b"\x00"))
        self.assertFalse(is_power_of_two(b"\xff"))
        self.assertFalse(is_power_of_two(b"\x0f"))
        self.assertFalse(is_power_of_two(b"\x03"))
        self.assertFalse(is_power_of_two(b"\x01\x01"))

    def test_empty(self):
        self.assertFalse(is_power_of_two(b""))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_power_of_two("01")
        with self.assertRaises(TypeError):
            is_power_of_two(255)
        with self.assertRaises(TypeError):
            is_power_of_two(None)


class TestLowestSetBit(unittest.TestCase):
    def test_no_set_bits(self):
        self.assertEqual(lowest_set_bit(b""), -1)
        self.assertEqual(lowest_set_bit(from_hex("00")), -1)
        self.assertEqual(lowest_set_bit(from_hex("0000")), -1)

    def test_least_significant_set_bit(self):
        self.assertEqual(lowest_set_bit(from_hex("01")), 0)
        self.assertEqual(lowest_set_bit(from_hex("02")), 1)
        self.assertEqual(lowest_set_bit(from_hex("04")), 2)
        self.assertEqual(lowest_set_bit(from_hex("80")), 7)
        self.assertEqual(lowest_set_bit(from_hex("ff")), 0)

    def test_multi_byte_position(self):
        self.assertEqual(lowest_set_bit(from_hex("0100")), 8)
        self.assertEqual(lowest_set_bit(from_hex("0001")), 0)
        self.assertEqual(lowest_set_bit(from_hex("0200")), 9)

    def test_bytearray(self):
        self.assertEqual(lowest_set_bit(bytearray(b"\x01")), 0)
        self.assertEqual(lowest_set_bit(bytearray(b"\x80")), 7)
        self.assertEqual(lowest_set_bit(bytearray(b"")), -1)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            lowest_set_bit("01")
        with self.assertRaises(TypeError):
            lowest_set_bit(255)
        with self.assertRaises(TypeError):
            lowest_set_bit(None)


class TestHighestSetBit(unittest.TestCase):
    def test_no_set_bits(self):
        self.assertEqual(highest_set_bit(b""), -1)
        self.assertEqual(highest_set_bit(from_hex("00")), -1)
        self.assertEqual(highest_set_bit(from_hex("0000")), -1)

    def test_most_significant_set_bit(self):
        self.assertEqual(highest_set_bit(from_hex("01")), 0)
        self.assertEqual(highest_set_bit(from_hex("02")), 1)
        self.assertEqual(highest_set_bit(from_hex("04")), 2)
        self.assertEqual(highest_set_bit(from_hex("80")), 7)
        self.assertEqual(highest_set_bit(from_hex("ff")), 7)

    def test_multi_byte_position(self):
        self.assertEqual(highest_set_bit(from_hex("0100")), 8)
        self.assertEqual(highest_set_bit(from_hex("0001")), 0)
        self.assertEqual(highest_set_bit(from_hex("0200")), 9)

    def test_bytearray(self):
        self.assertEqual(highest_set_bit(bytearray(b"\x01")), 0)
        self.assertEqual(highest_set_bit(bytearray(b"\x80")), 7)
        self.assertEqual(highest_set_bit(bytearray(b"")), -1)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            highest_set_bit("01")
        with self.assertRaises(TypeError):
            highest_set_bit(255)
        with self.assertRaises(TypeError):
            highest_set_bit(None)


class TestRIndex(unittest.TestCase):
    def test_found(self):
        self.assertEqual(rindex(b"hello world", b"o"), 7)
        self.assertEqual(rindex(b"abcabc", b"bc"), 4)

    def test_not_found_raises(self):
        with self.assertRaises(ValueError):
            rindex(b"hello", b"x")

    def test_bytearray_input(self):
        self.assertEqual(rindex(bytearray(b"hello"), bytearray(b"lo")), 3)

    def test_negative_indices(self):
        self.assertEqual(rindex(b"abcabc", b"bc", -4), 4)
        self.assertEqual(rindex(b"abcabc", b"bc", -5, -1), 1)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            rindex("abc", b"a")
        with self.assertRaises(TypeError):
            rindex(b"abc", "a")
        with self.assertRaises(TypeError):
            rindex(b"abc", b"a", start=True)
        with self.assertRaises(TypeError):
            rindex(b"abc", b"a", end=True)


class TestFind(unittest.TestCase):
    def test_found(self):
        self.assertEqual(find(b"hello world", b"world"), 6)
        self.assertEqual(find(b"abcabc", b"bc"), 1)

    def test_not_found(self):
        self.assertEqual(find(b"hello", b"x"), -1)

    def test_bytearray_input(self):
        self.assertEqual(find(bytearray(b"hello"), bytearray(b"ll")), 2)

    def test_negative_indices(self):
        self.assertEqual(find(b"abcabc", b"bc", -3), 4)
        self.assertEqual(find(b"abcabc", b"bc", -10), 1)
        self.assertEqual(find(b"abcabc", b"bc", 0, -1), 1)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            find("abc", b"a")
        with self.assertRaises(TypeError):
            find(b"abc", "a")
        with self.assertRaises(TypeError):
            find(b"abc", b"a", start=True)
        with self.assertRaises(TypeError):
            find(b"abc", b"a", end=True)


class TestSplit(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(split(b"a,b,c", b","), [b"a", b"b", b"c"])
        self.assertEqual(split(b"a b c", None), [b"a", b"b", b"c"])

    def test_maxsplit(self):
        self.assertEqual(split(b"a b c", None, 1), [b"a", b"b c"])

    def test_bytearray_input(self):
        self.assertEqual(split(bytearray(b"a,b"), bytearray(b",")), [b"a", b"b"])

    def test_empty_separator(self):
        with self.assertRaises(ValueError):
            split(b"a", b"")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            split("a b")
        with self.assertRaises(TypeError):
            split(b"a b", 1)
        with self.assertRaises(TypeError):
            split(b"a b", None, True)


class TestReplace(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(replace(b"aa", b"a", b"b"), b"bb")
        self.assertEqual(replace(b"aa", b"a", b"b", 1), b"ba")

    def test_negative_count(self):
        self.assertEqual(replace(b"aa", b"a", b"b", -1), b"bb")

    def test_bytearray_input(self):
        self.assertEqual(
            replace(bytearray(b"aa"), bytearray(b"a"), bytearray(b"b")),
            b"bb",
        )

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            replace("aa", b"a", b"b")
        with self.assertRaises(TypeError):
            replace(b"aa", "a", b"b")
        with self.assertRaises(TypeError):
            replace(b"aa", b"a", "b")
        with self.assertRaises(TypeError):
            replace(b"aa", b"a", b"b", True)


class TestCount(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count(b"abcabc", b"bc"), 2)
        self.assertEqual(count(b"aaa", b"a"), 3)
        self.assertEqual(count(b"abc", b"x"), 0)

    def test_bytearray_input(self):
        self.assertEqual(count(bytearray(b"abcabc"), bytearray(b"bc")), 2)

    def test_negative_indices(self):
        self.assertEqual(count(b"abcabc", b"bc", -3), 1)
        self.assertEqual(count(b"abcabc", b"bc", 0, -1), 1)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            count("abc", b"a")
        with self.assertRaises(TypeError):
            count(b"abc", "a")
        with self.assertRaises(TypeError):
            count(b"abc", b"a", True)
        with self.assertRaises(TypeError):
            count(b"abc", b"a", 0, True)


class TestToInt(unittest.TestCase):
    def test_big_endian(self):
        self.assertEqual(to_int(from_hex("0100")), 256)
        self.assertEqual(to_int(b"\x00\x01"), 1)

    def test_little_endian(self):
        self.assertEqual(to_int(from_hex("0001"), byteorder="little"), 256)

    def test_signed(self):
        self.assertEqual(to_int(from_hex("ff"), signed=True), -1)
        self.assertEqual(to_int(b"\x80", signed=True), -128)

    def test_empty(self):
        self.assertEqual(to_int(b""), 0)
        self.assertEqual(to_int(bytearray(b""), signed=True), 0)

    def test_bytearray_input(self):
        self.assertEqual(to_int(bytearray(b"\x01\x00")), 256)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            to_int("0100")
        with self.assertRaises(TypeError):
            to_int(b"\x01", byteorder=1)
        with self.assertRaises(TypeError):
            to_int(b"\xff", signed=1)

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            to_int(b"\x01", byteorder="middle")


class TestFromInt(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(to_hex(from_int(256, 2)), "0100")
        self.assertEqual(from_int(256, 2, byteorder="little"), b"\x00\x01")
        self.assertEqual(from_int(-1, 1, signed=True), b"\xff")

    def test_length_zero(self):
        self.assertEqual(from_int(0, 0), b"")
        self.assertEqual(from_int(0, 0, byteorder="little", signed=True), b"")
        self.assertEqual(from_int(-1, 0, signed=True), b"")

    def test_length(self):
        self.assertEqual(len(from_int(0, 4)), 4)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            from_int(True, 1)
        with self.assertRaises(TypeError):
            from_int(1.5, 1)
        with self.assertRaises(TypeError):
            from_int(1, True)
        with self.assertRaises(TypeError):
            from_int(1, 1, byteorder=1)
        with self.assertRaises(TypeError):
            from_int(1, 1, signed=1)

    def test_value_errors(self):
        with self.assertRaises(ValueError):
            from_int(1, -1)
        with self.assertRaises(ValueError):
            from_int(1, 1, byteorder="middle")

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            from_int(256, 1)
        with self.assertRaises(OverflowError):
            from_int(-1, 1)
        with self.assertRaises(OverflowError):
            from_int(1, 0)
        with self.assertRaises(OverflowError):
            from_int(-2, 0, signed=True)
        with self.assertRaises(OverflowError):
            from_int(1, 0, signed=True)


class TestCodecAndPadding(unittest.TestCase):
    def test_decode_encode_utf8(self):
        from bytes_utils import decode_utf8, encode_utf8

        self.assertEqual(decode_utf8(b"hello"), "hello")
        self.assertEqual(decode_utf8(bytearray(b"caf\xc3\xa9")), "café")
        self.assertEqual(decode_utf8(b"\xff", errors="ignore"), "")
        self.assertEqual(decode_utf8(b"\xff", errors="replace"), "\ufffd")
        self.assertEqual(encode_utf8("café"), b"caf\xc3\xa9")
        self.assertEqual(encode_utf8("\udcff", errors="surrogatepass"), b"\xed\xb3\xbf")
        with self.assertRaises(TypeError):
            decode_utf8("abc")
        with self.assertRaises(TypeError):
            decode_utf8(b"a", errors=True)
        with self.assertRaises(TypeError):
            encode_utf8(b"abc")
        with self.assertRaises(TypeError):
            encode_utf8("a", errors=True)

    def test_decode_encode_ascii(self):
        self.assertEqual(decode_ascii(b"abc"), "abc")
        self.assertEqual(decode_ascii(bytearray(b"hi")), "hi")
        self.assertEqual(decode_ascii(b"\x80", errors="ignore"), "")
        self.assertEqual(decode_ascii(b"\x80", errors="replace"), "\ufffd")
        self.assertEqual(encode_ascii("abc"), b"abc")
        self.assertEqual(encode_ascii("café", errors="ignore"), b"caf")
        self.assertEqual(encode_ascii("é", errors="xmlcharrefreplace"), b"&#233;")
        with self.assertRaises(UnicodeDecodeError):
            decode_ascii(b"\x80")
        with self.assertRaises(UnicodeEncodeError):
            encode_ascii("café")
        with self.assertRaises(TypeError):
            decode_ascii("abc")
        with self.assertRaises(TypeError):
            decode_ascii(b"abc", errors=123)
        with self.assertRaises(TypeError):
            encode_ascii(b"abc")
        with self.assertRaises(TypeError):
            encode_ascii("abc", errors=123)

    def test_center_ljust_rjust_zfill(self):
        from bytes_utils import center, ljust, rjust, zfill

        self.assertEqual(center(bytearray(b"a"), 5, bytearray(b".")), b"..a..")
        self.assertEqual(ljust(b"a", 3, b"."), b"a..")
        self.assertEqual(rjust(b"a", 3, b"."), b"..a")
        self.assertEqual(zfill(bytearray(b"-42"), 5), b"-0042")
        self.assertEqual(center(b"abc", 2), b"abc")
        self.assertEqual(ljust(b"abc", -1), b"abc")
        self.assertEqual(rjust(b"abc", 0), b"abc")
        self.assertEqual(zfill(b"42", 1), b"42")
        with self.assertRaises(TypeError):
            center(b"a", True)
        with self.assertRaises(TypeError):
            ljust(b"a", 3, ".")
        with self.assertRaises(TypeError):
            rjust("a", 3)
        with self.assertRaises(TypeError):
            zfill(b"a", True)
        with self.assertRaises(ValueError):
            center(b"a", 3, b"")
        with self.assertRaises(ValueError):
            ljust(b"a", 3, b"xx")

    def test_strip_helpers(self):
        from bytes_utils import lstrip, rstrip, strip

        self.assertEqual(strip(bytearray(b"  hi  ")), b"hi")
        self.assertEqual(lstrip(bytearray(b"  hi  ")), b"hi  ")
        self.assertEqual(rstrip(bytearray(b"  hi  ")), b"  hi")
        self.assertEqual(strip(bytearray(b"xxax"), bytearray(b"x")), b"a")
        self.assertEqual(lstrip(b"xxax", b"x"), b"ax")
        self.assertEqual(rstrip(b"xxax", b"x"), b"xxa")
        self.assertEqual(strip(b"xxax", b""), b"xxax")
        with self.assertRaises(TypeError):
            strip("a")
        with self.assertRaises(TypeError):
            lstrip(b"a", "x")
        with self.assertRaises(TypeError):
            rstrip(1)

    def test_join_expandtabs(self):
        self.assertEqual(join([bytearray(b"a"), b"b"], bytearray(b"-")), b"a-b")
        self.assertEqual(join(iter((b"a", b"b"))), b"ab")
        self.assertEqual(join([]), b"")
        self.assertEqual(expandtabs(bytearray(b"a\tb"), 4), b"a   b")
        self.assertEqual(expandtabs(b"a\tb", 0), b"ab")
        self.assertEqual(expandtabs(b"ab", 4), b"ab")
        with self.assertRaises(TypeError):
            join([b"a", "b"])
        with self.assertRaises(TypeError):
            join(123)
        with self.assertRaises(TypeError):
            join([b"a"], "-")
        with self.assertRaises(TypeError):
            expandtabs("a\tb")
        with self.assertRaises(TypeError):
            expandtabs(b"a\tb", True)


class TestIsAllOnes(unittest.TestCase):
    def test_all_ones(self):
        self.assertTrue(is_all_ones(b"\xff\xff\xff"))
        self.assertTrue(is_all_ones(from_hex("ffffff")))

    def test_not_all_ones(self):
        self.assertFalse(is_all_ones(b"\xff\xfe\xff"))
        self.assertFalse(is_all_ones(from_hex("fffeff")))
        self.assertFalse(is_all_ones(b"\x00"))

    def test_empty(self):
        self.assertTrue(is_all_ones(b""))

    def test_single(self):
        self.assertTrue(is_all_ones(b"\xff"))
        self.assertFalse(is_all_ones(b"\xfe"))

    def test_bytearray(self):
        self.assertTrue(is_all_ones(bytearray(b"\xff\xff")))
        self.assertFalse(is_all_ones(bytearray(b"\xff\x00")))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            is_all_ones("ff")
        with self.assertRaises(TypeError):
            is_all_ones(255)
        with self.assertRaises(TypeError):
            is_all_ones(None)


class TestIsPrintable(unittest.TestCase):
    def test_printable(self):
        self.assertTrue(isprintable(b"hello"))
        self.assertTrue(isprintable(b"hi there"))
        self.assertTrue(isprintable(bytearray(b"abc")))
        self.assertTrue(isprintable(b" !@#$%^&*()_+"))

    def test_not_printable(self):
        self.assertTrue(isprintable(b""))
        self.assertFalse(isprintable(b"no\ttabs"))
        self.assertFalse(isprintable(b"line\nbreak"))
        self.assertFalse(isprintable(b"\x00\x01"))
        self.assertFalse(isprintable(b"\x7f\x80"))

    def test_bytearray(self):
        self.assertTrue(isprintable(bytearray(b"abc")))
        self.assertFalse(isprintable(bytearray(b"\t")))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            isprintable("abc")
        with self.assertRaises(TypeError):
            isprintable(123)
        with self.assertRaises(TypeError):
            isprintable(None)


class TestIsIdentifier(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(isidentifier(b"foo_bar"))
        self.assertTrue(isidentifier(b"_private"))
        self.assertTrue(isidentifier(bytearray(b"CamelCase")))

    def test_invalid(self):
        self.assertFalse(isidentifier(b"9abc"))
        self.assertFalse(isidentifier(b""))
        self.assertFalse(isidentifier(b"foo bar"))
        self.assertFalse(isidentifier(b"caf\xc3\xa9"))

    def test_non_ascii(self):
        self.assertFalse(isidentifier(b"\xc3\xa9"))

    def test_bytearray(self):
        self.assertTrue(isidentifier(bytearray(b"foo")))
        self.assertFalse(isidentifier(bytearray(b"123")))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            isidentifier("abc")
        with self.assertRaises(TypeError):
            isidentifier(123)
        with self.assertRaises(TypeError):
            isidentifier(None)
