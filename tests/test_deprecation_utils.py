import unittest
import warnings

from deprecation_utils import deprecated


class TestDeprecated(unittest.TestCase):
    def test_emits_deprecation_warning(self):
        @deprecated
        def old_func() -> int:
            return 42

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = old_func()

        self.assertEqual(result, 42)
        self.assertEqual(len(caught), 1)
        self.assertTrue(issubclass(caught[0].category, DeprecationWarning))
        self.assertIn("old_func is deprecated", str(caught[0].message))

    def test_preserves_return_value_and_args(self):
        @deprecated(version="1.0", replacement="new_func")
        def add(a: int, b: int) -> int:
            return a + b

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.assertEqual(add(2, 3), 5)

    def test_includes_version_and_replacement(self):
        @deprecated(version="2.0", replacement="use calculate()")
        def compute() -> str:
            return "result"

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            compute()

        message = str(caught[0].message)
        self.assertIn("since version 2.0", message)
        self.assertIn("use calculate() instead", message)

    def test_custom_message(self):
        @deprecated(message="please stop using legacy_mode")
        def legacy_mode() -> None:
            return None

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            legacy_mode()

        self.assertIn("please stop using legacy_mode", str(caught[0].message))

    def test_wraps_metadata(self):
        @deprecated
        def documented() -> int:
            """Docstring for documented."""
            return 1

        self.assertEqual(documented.__name__, "documented")
        self.assertEqual(documented.__doc__, "Docstring for documented.")

    def test_non_callable_raises(self):
        with self.assertRaises(TypeError):
            deprecated(42)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
