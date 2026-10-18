import abc
import unittest

import abc_utils


class TestAbcUtils(unittest.TestCase):
    def test_abstractmethod(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self):
                ...

        self.assertTrue(Base.__abstractmethods__)

    def test_get_cache_token(self):
        token = abc_utils.get_cache_token()
        self.assertIsInstance(token, int)

    def test_update_abstractmethods(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self):
                ...

        class Sub(Base):
            def method(self):
                return 1

        abc_utils.update_abstractmethods(Sub)
        self.assertEqual(Sub.__abstractmethods__, frozenset())


if __name__ == "__main__":
    unittest.main()
