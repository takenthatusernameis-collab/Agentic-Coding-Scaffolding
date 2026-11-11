"""Tests for abc_utils module."""

import abc
import unittest

import abc_utils


class TestAbcUtils(unittest.TestCase):
    def test_abstractmethod(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self): ...

        self.assertTrue(Base.__abstractmethods__)

    def test_get_cache_token(self):
        token = abc_utils.get_cache_token()
        self.assertIsInstance(token, int)

    def test_update_abstractmethods(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self): ...

        class Sub(Base):
            def method(self):
                return 1

        abc_utils.update_abstractmethods(Sub)
        self.assertEqual(Sub.__abstractmethods__, frozenset())

    def test_is_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self): ...

        class Sub(Base):
            def method(self):
                return 1

        self.assertTrue(abc_utils.is_abstract(Base))
        self.assertFalse(abc_utils.is_abstract(Sub))
        self.assertFalse(abc_utils.is_abstract(int))


class TestWrapperBindings(unittest.TestCase):
    """Verify the wrapper module exposes its own callable bindings."""

    def test_abcmeta_is_wrapper_binding(self):
        import abc as _abc

        self.assertIs(abc_utils.ABCMeta(), _abc.ABCMeta)

    def test_abc_is_wrapper_binding(self):
        import abc as _abc

        self.assertIs(abc_utils.ABC(), _abc.ABC)

    def test_abstractmethod_is_wrapper_binding(self):
        import abc as _abc

        self.assertIsNot(abc_utils.abstractmethod, _abc.abstractmethod)

    def test_abstractclassmethod_is_wrapper_binding(self):
        import abc as _abc

        self.assertIsNot(abc_utils.abstractclassmethod, _abc.abstractclassmethod)

    def test_abstractstaticmethod_is_wrapper_binding(self):
        import abc as _abc

        self.assertIsNot(abc_utils.abstractstaticmethod, _abc.abstractstaticmethod)

    def test_abstractproperty_is_wrapper_binding(self):
        import abc as _abc

        self.assertIsNot(abc_utils.abstractproperty, _abc.abstractproperty)

    def test_get_cache_token_is_wrapper_binding(self):
        import abc as _abc

        self.assertIsNot(abc_utils.get_cache_token, _abc.get_cache_token)

    def test_update_abstractmethods_is_wrapper_binding(self):
        import abc as _abc

        self.assertIsNot(abc_utils.update_abstractmethods, _abc.update_abstractmethods)


class TestAbcMeta(unittest.TestCase):
    def test_returns_abcmeta(self):
        self.assertIs(abc_utils.ABCMeta(), abc.ABCMeta)

    def test_metaclass_can_be_assigned(self):
        class Base(metaclass=abc_utils.ABCMeta()):
            pass

        self.assertIsInstance(Base, abc.ABCMeta)


class TestAbstractClassMethod(unittest.TestCase):
    def test_marks_classmethod_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractclassmethod
            def method(cls): ...

        self.assertIn("method", Base.__abstractmethods__)

    def test_concrete_classmethod_clears_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractclassmethod
            def method(cls): ...

        class Sub(Base):
            @classmethod
            def method(cls):
                return 1

        abc_utils.update_abstractmethods(Sub)
        self.assertEqual(Sub.__abstractmethods__, frozenset())
        self.assertEqual(Sub.method(), 1)

    def test_instantiation_blocked_until_implemented(self):
        class Base(abc.ABC):
            @abc_utils.abstractclassmethod
            def method(cls): ...

        with self.assertRaises(TypeError):
            Base()


class TestAbstractStaticMethod(unittest.TestCase):
    def test_marks_staticmethod_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractstaticmethod
            def method(): ...

        self.assertIn("method", Base.__abstractmethods__)

    def test_concrete_staticmethod_clears_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractstaticmethod
            def method(): ...

        class Sub(Base):
            @staticmethod
            def method():
                return 2

        abc_utils.update_abstractmethods(Sub)
        self.assertEqual(Sub.__abstractmethods__, frozenset())
        self.assertEqual(Sub.method(), 2)


class TestAbstractProperty(unittest.TestCase):
    def test_marks_property_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractproperty
            def value(self): ...

        self.assertIn("value", Base.__abstractmethods__)

    def test_concrete_property_clears_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractproperty
            def value(self): ...

        class Sub(Base):
            @property
            def value(self):
                return 3

        abc_utils.update_abstractmethods(Sub)
        self.assertEqual(Sub.__abstractmethods__, frozenset())
        self.assertEqual(Sub().value, 3)


class TestIsAbstract(unittest.TestCase):
    def test_abstract_class_is_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self): ...

        self.assertTrue(abc_utils.is_abstract(Base))

    def test_concrete_class_not_abstract(self):
        class Base(abc.ABC):
            @abc_utils.abstractmethod
            def method(self): ...

        class Sub(Base):
            def method(self):
                return 1

        self.assertFalse(abc_utils.is_abstract(Sub))

    def test_non_class_not_abstract(self):
        self.assertFalse(abc_utils.is_abstract(int))
        self.assertFalse(abc_utils.is_abstract("string"))
        self.assertFalse(abc_utils.is_abstract(None))


if __name__ == "__main__":
    unittest.main()
