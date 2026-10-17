import unittest
from dataclasses import dataclass

from dataclasses_utils import (
    MISSING,
    asdict,
    astuple,
    dataclass_fields,
    field,
    fields,
    get_field_default,
    get_field_names,
    has_field,
    is_dataclass,
    is_dataclass_instance,
    make_dataclass,
    replace,
    to_dict,
    to_tuple,
)


@dataclass
class Simple:
    x: int
    y: int = 10


@dataclass
class Nested:
    a: int
    b: Simple


class TestDataclassesUtils(unittest.TestCase):
    def test_is_dataclass(self):
        self.assertTrue(is_dataclass(Simple))
        self.assertTrue(is_dataclass(Simple(1, 2)))
        self.assertFalse(is_dataclass("not a dataclass"))
        self.assertFalse(is_dataclass(42))
        self.assertFalse(is_dataclass(None))

    def test_is_dataclass_instance(self):
        self.assertTrue(is_dataclass_instance(Simple(1, 2)))
        self.assertFalse(is_dataclass_instance(Simple))
        self.assertFalse(is_dataclass_instance("not a dataclass"))
        self.assertFalse(is_dataclass_instance(42))

    def test_fields(self):
        f = fields(Simple)
        self.assertEqual(len(f), 2)
        names = [x.name for x in f]
        self.assertIn("x", names)
        self.assertIn("y", names)

    def test_fields_on_instance(self):
        f = fields(Simple(1, 2))
        self.assertEqual(len(f), 2)

    def test_fields_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            fields("not a dataclass")  # type: ignore[arg-type]

    def test_dataclass_fields(self):
        f = dataclass_fields(Simple)
        self.assertEqual(len(f), 2)

    def test_asdict(self):
        s = Simple(5, 20)
        d = asdict(s)
        self.assertEqual(d, {"x": 5, "y": 20})

    def test_asdict_with_factory(self):
        s = Simple(1, 2)
        d = asdict(s, dict_factory=dict)
        self.assertIsInstance(d, dict)
        self.assertEqual(d, {"x": 1, "y": 2})

    def test_asdict_raises_on_class(self):
        with self.assertRaises(TypeError):
            asdict(Simple)  # type: ignore[arg-type]

    def test_asdict_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            asdict("not a dataclass")  # type: ignore[arg-type]

    def test_to_dict(self):
        s = Simple(3, 4)
        self.assertEqual(to_dict(s), {"x": 3, "y": 4})

    def test_astuple(self):
        s = Simple(5, 6)
        t = astuple(s)
        self.assertEqual(t, (5, 6))

    def test_astuple_with_factory(self):
        s = Simple(1, 2)
        t = astuple(s, tuple_factory=tuple)
        self.assertIsInstance(t, tuple)
        self.assertEqual(t, (1, 2))

    def test_astuple_raises_on_class(self):
        with self.assertRaises(TypeError):
            astuple(Simple)  # type: ignore[arg-type]

    def test_astuple_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            astuple("not a dataclass")  # type: ignore[arg-type]

    def test_to_tuple(self):
        s = Simple(7, 8)
        self.assertEqual(to_tuple(s), (7, 8))

    def test_replace(self):
        s = Simple(1, 2)
        s2 = replace(s, x=10)
        self.assertEqual(s2.x, 10)
        self.assertEqual(s2.y, 2)
        self.assertNotEqual(s, s2)

    def test_replace_raises_on_class(self):
        with self.assertRaises(TypeError):
            replace(Simple, x=5)  # type: ignore[arg-type]

    def test_replace_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            replace("not a dataclass", x=5)  # type: ignore[arg-type]

    def test_make_dataclass(self):
        Point = make_dataclass("Point", [("x", int), ("y", int)])
        p = Point(x=1, y=2)
        self.assertTrue(is_dataclass(Point))
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)

    def test_make_dataclass_with_defaults(self):
        Point = make_dataclass("Point", [("x", int), ("y", int, 5)])
        p = Point(x=1)
        self.assertEqual(p.y, 5)

    def test_make_dataclass_with_field_specs(self):
        Point = make_dataclass("Point", [("x", int), ("y", int, field(default=10))])
        p = Point(1)
        self.assertEqual(p.y, 10)

    def test_make_dataclass_validation(self):
        with self.assertRaises(TypeError):
            make_dataclass(123, [("x", int)])  # type: ignore[arg-type]

        with self.assertRaises(TypeError):
            make_dataclass("P", "not iterable")  # type: ignore[arg-type]

        with self.assertRaises(TypeError):
            make_dataclass("P", [("x", int)], bases="not tuple")  # type: ignore[arg-type]

        with self.assertRaises(TypeError):
            make_dataclass("P", [("x", int)], namespace="not dict")  # type: ignore[arg-type]

    def test_get_field_names(self):
        self.assertEqual(get_field_names(Simple), ["x", "y"])
        self.assertEqual(get_field_names(Simple(1)), ["x", "y"])

    def test_get_field_names_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            get_field_names("not a dataclass")  # type: ignore[arg-type]

    def test_get_field_default(self):
        self.assertEqual(get_field_default(Simple, "y"), 10)
        self.assertIs(get_field_default(Simple, "x"), MISSING)

    def test_get_field_default_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            get_field_default("not a dataclass", "x")  # type: ignore[arg-type]

    def test_get_field_default_raises_on_bad_field_name(self):
        with self.assertRaises(TypeError):
            get_field_default(Simple, 123)  # type: ignore[arg-type]

    def test_get_field_default_raises_on_missing_field(self):
        with self.assertRaises(KeyError):
            get_field_default(Simple, "nonexistent")

    def test_has_field(self):
        self.assertTrue(has_field(Simple, "x"))
        self.assertTrue(has_field(Simple, "y"))
        self.assertFalse(has_field(Simple, "z"))

    def test_has_field_on_instance(self):
        self.assertTrue(has_field(Simple(1), "x"))

    def test_has_field_raises_on_non_dataclass(self):
        with self.assertRaises(TypeError):
            has_field("not a dataclass", "x")  # type: ignore[arg-type]

    def test_has_field_raises_on_bad_field_name(self):
        with self.assertRaises(TypeError):
            has_field(Simple, 123)  # type: ignore[arg-type]

    def test_field_and_missing_exist(self):
        from dataclasses_utils import field as du_field
        from dataclasses_utils import MISSING as du_missing

        from dataclasses import field as dc_field
        from dataclasses import MISSING as dc_missing

        self.assertIs(du_field, dc_field)
        self.assertIs(du_missing, dc_missing)


if __name__ == "__main__":
    unittest.main()
