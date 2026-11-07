"""Tests for collections_abc_utils."""

from __future__ import annotations

import collections.abc as cabc
import unittest

import collections_abc_utils as cau


class TestGetAbc(unittest.TestCase):
    def test_returns_public_abc(self) -> None:
        self.assertIs(cau.get_abc("Sequence"), cabc.Sequence)
        self.assertIs(cau.get_abc("Mapping"), cabc.Mapping)

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            cau.get_abc(123)  # type: ignore[arg-type]

    def test_rejects_private_name(self) -> None:
        with self.assertRaises(ValueError):
            cau.get_abc("_CallableGenericAlias")

    def test_rejects_unknown_name(self) -> None:
        with self.assertRaises(AttributeError):
            cau.get_abc("NotARealABC")


class TestPredicates(unittest.TestCase):
    def test_sequences(self) -> None:
        self.assertTrue(cau.is_sequence([1, 2]))
        self.assertTrue(cau.is_sequence("ab"))
        self.assertFalse(cau.is_sequence({1, 2}))
        self.assertTrue(cau.is_mutable_sequence([1]))
        self.assertFalse(cau.is_mutable_sequence((1,)))

    def test_mappings(self) -> None:
        self.assertTrue(cau.is_mapping({"a": 1}))
        self.assertTrue(cau.is_mutable_mapping({"a": 1}))
        self.assertFalse(cau.is_mapping([1, 2]))

    def test_sets(self) -> None:
        self.assertTrue(cau.is_set({1, 2}))
        self.assertTrue(cau.is_mutable_set({1, 2}))
        self.assertFalse(cau.is_mutable_set(frozenset({1})))

    def test_iterables(self) -> None:
        self.assertTrue(cau.is_iterable([1]))
        self.assertTrue(cau.is_iterable(iter([1])))
        self.assertTrue(cau.is_iterator(iter([1])))
        self.assertFalse(cau.is_iterator([1]))
        self.assertFalse(cau.is_iterable(42))

    def test_generators(self) -> None:
        def gen():
            yield 1

        g = gen()
        self.assertTrue(cau.is_generator(g))
        self.assertTrue(cau.is_iterator(g))

    def test_callable_hashable_sized_container(self) -> None:
        self.assertTrue(cau.is_callable(lambda: None))
        self.assertFalse(cau.is_callable(1))
        self.assertTrue(cau.is_hashable("x"))
        self.assertFalse(cau.is_hashable([1]))
        self.assertTrue(cau.is_sized([1, 2]))
        self.assertTrue(cau.is_container([1, 2]))
        self.assertTrue(cau.is_collection([1, 2]))

    def test_reversible(self) -> None:
        self.assertTrue(cau.is_reversible([1, 2]))
        self.assertFalse(cau.is_reversible({1, 2}))

    def test_async_predicates(self) -> None:
        async def coro():
            return 1

        c = coro()
        try:
            self.assertTrue(cau.is_coroutine(c))
            self.assertTrue(cau.is_awaitable(c))
        finally:
            c.close()

        async def agen():
            yield 1

        a = agen()
        try:
            self.assertTrue(cau.is_async_generator(a))
            self.assertTrue(cau.is_async_iterator(a))
            self.assertTrue(cau.is_async_iterable(a))
        finally:
            # close async generator
            try:
                a.aclose().send(None)
            except StopIteration:
                pass


if __name__ == "__main__":
    unittest.main()
