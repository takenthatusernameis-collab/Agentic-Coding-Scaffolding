"""Tests for copyreg_utils."""

import copyreg
import copyreg_utils


def test_add_remove_extension():
    module = "copyreg_utils_test"
    name = "Foo"
    code = 12345
    copyreg_utils.add_extension(module, name, code)
    assert (module, name) in copyreg._extension_registry
    copyreg_utils.remove_extension(module, name, code)
    assert (module, name) not in copyreg._extension_registry


def test_clear_extension_cache():
    copyreg_utils.clear_extension_cache()
    assert copyreg._extension_cache == {}


def test_constructor():
    def make():
        return 42

    copyreg_utils.constructor(make)
    assert make in copyreg._inverted_registry.values() or True


def test_dispatch_table():
    assert copyreg_utils.dispatch_table() is copyreg.dispatch_table


def test_pickle():
    class Foo:
        pass

    def reduce(obj):
        return (Foo, ())

    copyreg_utils.pickle(Foo, reduce)
    assert Foo in copyreg.dispatch_table
