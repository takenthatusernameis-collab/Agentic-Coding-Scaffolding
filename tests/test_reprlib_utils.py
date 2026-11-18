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


class TestBoolRejection(unittest.TestCase):
    def test_repr_rejects_bool_maxlevel(self):
        with self.assertRaises(TypeError):
            Repr(maxlevel=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxtuple(self):
        with self.assertRaises(TypeError):
            Repr(maxtuple=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxlist(self):
        with self.assertRaises(TypeError):
            Repr(maxlist=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxarray(self):
        with self.assertRaises(TypeError):
            Repr(maxarray=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxdict(self):
        with self.assertRaises(TypeError):
            Repr(maxdict=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxset(self):
        with self.assertRaises(TypeError):
            Repr(maxset=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxfrozenset(self):
        with self.assertRaises(TypeError):
            Repr(maxfrozenset=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxdeque(self):
        with self.assertRaises(TypeError):
            Repr(maxdeque=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxstring(self):
        with self.assertRaises(TypeError):
            Repr(maxstring=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxlong(self):
        with self.assertRaises(TypeError):
            Repr(maxlong=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_maxother(self):
        with self.assertRaises(TypeError):
            Repr(maxother=True)  # type: ignore[arg-type]

    def test_repr_rejects_bool_indent(self):
        with self.assertRaises(TypeError):
            Repr(indent=True)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
