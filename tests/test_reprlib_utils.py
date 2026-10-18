import unittest

from reprlib_utils import Repr, get_ident, recursive_repr
from reprlib_utils import repr as repr_short


class TestReprlibUtils(unittest.TestCase):
    def test_repr(self):
        self.assertIsInstance(repr_short([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), str)

    def test_get_ident(self):
        self.assertIsInstance(get_ident(), int)

    def test_recursive_repr(self):
        class A:
            def __init__(self):
                self.other = None

            @recursive_repr()
            def __repr__(self):
                if self.other is not None:
                    return f"A({self.other!r})"
                return "A()"

        a = A()
        a.other = a
        self.assertIn("A(...)", repr(a))

    def test_repr_class(self):
        r = Repr()
        self.assertIsInstance(r.repr([1, 2, 3]), str)

    def test_repr_indent_validation(self):
        with self.assertRaises(TypeError):
            Repr(indent=object())

    def test_repr_indent_negative(self):
        with self.assertRaises(ValueError):
            Repr(indent=-1)


if __name__ == "__main__":
    unittest.main()
