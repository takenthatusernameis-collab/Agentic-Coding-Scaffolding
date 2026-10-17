import gc
import unittest
import weakref

from weakref_utils import (
    WeakMethod,
    WeakRef,
    create_finalizer,
    create_proxy,
    create_weakref,
    get_object,
    is_alive,
)


class TestWeakRef(unittest.TestCase):
    def test_weakref_get(self):
        class Dummy:
            pass

        d = Dummy()
        wr = WeakRef(d)
        self.assertIs(wr.get(), d)
        del d
        gc.collect()
        self.assertIsNone(wr.get())

    def test_weakref_is_alive(self):
        class Dummy:
            pass

        d = Dummy()
        wr = WeakRef(d)
        self.assertTrue(wr.is_alive())
        del d
        gc.collect()
        self.assertFalse(wr.is_alive())


class TestWeakMethod(unittest.TestCase):
    def test_weakmethod_get(self):
        class Dummy:
            def method(self):
                return "hi"

        d = Dummy()
        wm = WeakMethod(d.method)
        self.assertIsNotNone(wm.get())
        self.assertEqual(wm.get()(), "hi")  # type: ignore[union-attr]
        del d
        gc.collect()
        self.assertIsNone(wm.get())

    def test_weakmethod_is_alive(self):
        class Dummy:
            def method(self):
                return "hi"

        d = Dummy()
        wm = WeakMethod(d.method)
        self.assertTrue(wm.is_alive())
        del d
        gc.collect()
        self.assertFalse(wm.is_alive())


class TestCreateWeakref(unittest.TestCase):
    def test_create_weakref(self):
        class Dummy:
            pass

        d = Dummy()
        wr = create_weakref(d)
        self.assertIsInstance(wr, weakref.ref)
        self.assertIs(wr(), d)
        del d
        gc.collect()
        self.assertIsNone(wr())


class TestCreateProxy(unittest.TestCase):
    def test_create_proxy(self):
        class Dummy:
            def value(self):
                return 42

        d = Dummy()
        proxy = create_proxy(d)
        self.assertEqual(proxy.value(), 42)
        del d
        gc.collect()
        with self.assertRaises(ReferenceError):
            _ = proxy.value()


class TestGetObject(unittest.TestCase):
    def test_get_object_ref(self):
        class Dummy:
            pass

        d = Dummy()
        wr = weakref.ref(d)
        self.assertIs(get_object(wr), d)
        del d
        gc.collect()
        self.assertIsNone(get_object(wr))

    def test_get_object_proxy(self):
        class Dummy:
            pass

        d = Dummy()
        proxy = weakref.proxy(d)
        self.assertIs(get_object(proxy), proxy)  # get_object returns proxy if alive
        del d
        gc.collect()
        self.assertIsNone(get_object(proxy))


class TestIsAlive(unittest.TestCase):
    def test_is_alive_ref(self):
        class Dummy:
            pass

        d = Dummy()
        wr = weakref.ref(d)
        self.assertTrue(is_alive(wr))
        del d
        gc.collect()
        self.assertFalse(is_alive(wr))


class TestCreateFinalizer(unittest.TestCase):
    def test_create_finalizer(self):
        results = []

        class Dummy:
            pass

        d = Dummy()

        def callback():
            results.append(True)

        fin = create_finalizer(d, callback)
        self.assertIsInstance(fin, weakref.finalize)
        # Finalizer is alive if the object is alive; after deletion and GC, it may be dead
        self.assertTrue(fin.alive)
        del d
        gc.collect()
        gc.collect()
        # Callback may have fired
        self.assertFalse(fin.alive)


if __name__ == "__main__":
    unittest.main()
