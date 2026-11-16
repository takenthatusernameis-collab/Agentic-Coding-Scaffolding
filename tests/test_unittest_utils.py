import unittest

import unittest_utils


class TestReExportedClasses(unittest.TestCase):
    """Verify the classes re-exported from the standard library."""

    def test_test_case_is_reexported(self) -> None:
        self.assertIs(unittest_utils.TestCase, unittest.TestCase)

    def test_test_suite_is_reexported(self) -> None:
        self.assertIs(unittest_utils.TestSuite, unittest.TestSuite)

    def test_test_loader_is_reexported(self) -> None:
        self.assertIs(unittest_utils.TestLoader, unittest.TestLoader)

    def test_text_test_runner_is_reexported(self) -> None:
        self.assertIs(unittest_utils.TextTestRunner, unittest.TextTestRunner)

    def test_default_test_loader_is_reexported(self) -> None:
        self.assertIs(unittest_utils.defaultTestLoader, unittest.defaultTestLoader)


class TestUnittestUtils(unittest.TestCase):
    def test_make_suite_and_run(self):
        class MyTests(unittest_utils.TestCase):
            def test_ok(self):
                self.assertTrue(True)

        suite = unittest_utils.make_suite(MyTests)
        result = unittest_utils.run_tests(suite, verbosity=0)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(result.testsRun, 1)


if __name__ == "__main__":
    unittest.main()
