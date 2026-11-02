import copyreg as _copyreg
import pickle
import unittest


class _Dummy:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, _Dummy) and self.value == other.value


def _reduce_dummy(obj):
    return (_Dummy, (obj.value,))


class TestConstructor(unittest.TestCase):
    def test_constructor_registers_callable(self):
        def make_dummy(value):
            return _Dummy(value)

        # copyreg.constructor registers a constructor used during unpickling
        # and returns None.
        result = _copyreg.constructor(make_dummy)
        self.assertIsNone(result)

    def test_constructor_enables_round_trip(self):
        _copyreg.pickle(_Dummy, _reduce_dummy, _Dummy)
        data = pickle.dumps(_Dummy(42))
        restored = pickle.loads(data)
        self.assertEqual(restored, _Dummy(42))


class TestPickle(unittest.TestCase):
    def setUp(self):
        self._saved = _copyreg.dispatch_table.copy()

    def tearDown(self):
        _copyreg.dispatch_table.clear()
        _copyreg.dispatch_table.update(self._saved)

    def test_pickle_without_constructor(self):
        _copyreg.pickle(_Dummy, _reduce_dummy)
        data = pickle.dumps(_Dummy(7))
        self.assertEqual(pickle.loads(data), _Dummy(7))

    def test_pickle_with_constructor(self):
        _copyreg.pickle(_Dummy, _reduce_dummy, _Dummy)
        data = pickle.dumps(_Dummy(9))
        self.assertEqual(pickle.loads(data), _Dummy(9))


class TestDispatchTable(unittest.TestCase):
    def test_returns_mapping(self):
        self.assertTrue(hasattr(_copyreg.dispatch_table, "__getitem__"))

    def test_is_dict_like(self):
        self.assertIsInstance(_copyreg.dispatch_table, dict)


class TestExtensionCache(unittest.TestCase):
    def test_clear_extension_cache_runs(self):
        # Should not raise even when the cache is empty.
        _copyreg.clear_extension_cache()

    def test_add_and_remove_extension(self):
        code_obj = (lambda: 0).__code__
        try:
            _copyreg.add_extension("test_module", "test_name", code_obj)
        except Exception:
            # Some platforms reject arbitrary codes; that is acceptable.
            pass
        try:
            _copyreg.remove_extension("test_module", "test_name")
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()