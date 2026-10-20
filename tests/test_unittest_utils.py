import unittest

from unittest_utils import TestCase, TestSuite, make_suite, run_tests


class TestUnittestUtils(unittest.TestCase):
    def test_make_suite_and_run(self):
        class MyTests(TestCase):
            def test_ok(self):
                self.assertTrue(True)

        suite = make_suite(MyTests)
        result = run_tests(suite, verbosity=0)
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(result.testsRun, 1)


if __name__ == "__main__":
    unittest.main()
