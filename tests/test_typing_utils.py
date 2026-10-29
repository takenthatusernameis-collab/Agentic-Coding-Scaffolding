import typing
import unittest
from typing import List, Optional, TypedDict

from typing_utils import (
    ClassVar,
    Final,
    Literal,
    get_args,
    get_origin,
    get_type_hints,
    is_literal,
    is_typeddict,
    overload,
)


class TestTypingUtils(unittest.TestCase):
    def test_get_type_hints(self):
        def greet(name: str) -> str:
            return f"hello {name}"

        hints = get_type_hints(greet)
        self.assertEqual(hints["name"], str)
        self.assertEqual(hints["return"], str)

    def test_get_origin(self):
        self.assertEqual(get_origin(List[int]), list)
        self.assertIsNone(get_origin(int))

    def test_get_args(self):
        self.assertEqual(get_args(List[int]), (int,))
        self.assertEqual(get_args(dict), ())
        self.assertEqual(get_args(Optional[str]), (str, type(None)))

    def test_is_typeddict(self):
        class Point(TypedDict):
            x: int
            y: int

        self.assertTrue(is_typeddict(Point))
        self.assertFalse(is_typeddict(int))

    def test_is_literal(self):
        self.assertTrue(is_literal(Literal["a", "b"]))
        self.assertTrue(is_literal(Literal[1, 2]))
        self.assertFalse(is_literal(int))
        self.assertFalse(is_literal(str))

    def test_reexports_match_typing(self):
        self.assertIs(overload, typing.overload)
        self.assertIs(Final, typing.Final)
        self.assertIs(Literal, typing.Literal)
        self.assertIs(ClassVar, typing.ClassVar)


if __name__ == "__main__":
    unittest.main()
