"""Tests for pattern_utils module."""

import unittest

from pattern_utils import (
    Factory,
    Observable,
    Observer,
    Singleton,
    SingletonBase,
    Strategy,
    StrategyContext,
)


class TestSingleton(unittest.TestCase):
    def test_same_instance(self):
        class Service(metaclass=Singleton):
            def __init__(self):
                self.value = 0

        self.assertIs(Service(), Service())

    def test_distinct_classes_distinct_instances(self):
        class Alpha(metaclass=Singleton):
            pass

        class Beta(metaclass=Singleton):
            pass

        self.assertIsNot(Alpha(), Beta())

    def test_singleton_base(self):
        class Logger(SingletonBase):
            pass

        self.assertIs(Logger(), Logger())


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory()

    def test_register_and_create(self):
        self.factory.register("adder", lambda a, b: a + b)
        self.assertEqual(self.factory.create("adder", 2, 3), 5)

    def test_create_unknown_raises(self):
        with self.assertRaises(KeyError):
            self.factory.create("missing")

    def test_unregister(self):
        self.factory.register("x", lambda: 1)
        self.factory.unregister("x")
        self.assertEqual(self.factory.types(), [])
        with self.assertRaises(KeyError):
            self.factory.unregister("x")

    def test_register_non_callable_raises(self):
        with self.assertRaises(TypeError):
            self.factory.register("bad", 42)  # type: ignore[arg-type]

    def test_types_sorted(self):
        self.factory.register("zeta", lambda: 1)
        self.factory.register("alpha", lambda: 1)
        self.factory.register("mid", lambda: 1)
        self.assertEqual(self.factory.types(), ["alpha", "mid", "zeta"])


class RecordingObserver(Observer):
    def __init__(self):
        self.calls = []

    def update(self, subject, data=None):
        self.calls.append((subject, data))


class TestObservable(unittest.TestCase):
    def setUp(self):
        self.subject = Observable()
        self.observer = RecordingObserver()

    def test_attach_and_notify(self):
        self.subject.attach(self.observer)
        self.subject.notify("hello")
        self.assertEqual(len(self.observer.calls), 1)
        self.assertEqual(self.observer.calls[0], (self.subject, "hello"))

    def test_detach_stops_notification(self):
        self.subject.attach(self.observer)
        self.subject.detach(self.observer)
        self.subject.notify("hello")
        self.assertEqual(self.observer.calls, [])

    def test_detach_unattached_raises(self):
        with self.assertRaises(ValueError):
            self.subject.detach(self.observer)

    def test_attach_non_observer_raises(self):
        with self.assertRaises(TypeError):
            self.subject.attach("not an observer")  # type: ignore[arg-type]

    def test_multiple_observers(self):
        other = RecordingObserver()
        self.subject.attach(self.observer)
        self.subject.attach(other)
        self.subject.notify("data")
        self.assertEqual(len(self.observer.calls), 1)
        self.assertEqual(len(other.calls), 1)


class ConcreteStrategy(Strategy):
    def __init__(self, label):
        self.label = label

    def execute(self, *args, **kwargs):
        return self.label


class TestStrategy(unittest.TestCase):
    def test_strategy_abstract(self):
        with self.assertRaises(NotImplementedError):
            Strategy().execute()

    def test_context_delegates(self):
        context = StrategyContext(ConcreteStrategy("first"))
        self.assertEqual(context.execute(), "first")
        self.assertIsInstance(context.strategy, ConcreteStrategy)

    def test_context_swap_strategy(self):
        context = StrategyContext(ConcreteStrategy("first"))
        context.strategy = ConcreteStrategy("second")
        self.assertEqual(context.execute(), "second")
        self.assertEqual(context.strategy.label, "second")

    def test_context_invalid_strategy_raises(self):
        with self.assertRaises(TypeError):
            StrategyContext("not a strategy")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            StrategyContext(ConcreteStrategy("x")).strategy = 42  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()
