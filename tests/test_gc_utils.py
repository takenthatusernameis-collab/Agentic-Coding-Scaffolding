"""Tests for gc_utils."""

import gc

import gc_utils


def test_enable_disable():
    was_enabled = gc.isenabled()
    try:
        gc.disable()
        gc_utils.enable()
        assert gc.isenabled()
        gc_utils.disable()
        assert not gc.isenabled()
    finally:
        if was_enabled:
            gc.enable()
        else:
            gc.disable()


def test_isenabled():
    was_enabled = gc.isenabled()
    try:
        gc.disable()
        assert gc_utils.isenabled() is False
        gc.enable()
        assert gc_utils.isenabled() is True
    finally:
        if was_enabled:
            gc.enable()
        else:
            gc.disable()


def test_collect_returns_int():
    result = gc_utils.collect()
    assert isinstance(result, int)


def test_get_count():
    count = gc_utils.get_count()
    assert isinstance(count, tuple)


def test_get_threshold():
    threshold = gc_utils.get_threshold()
    assert isinstance(threshold, tuple)


def test_set_get_debug():
    orig = gc_utils.get_debug()
    try:
        gc_utils.set_debug(0)
        assert gc_utils.get_debug() == 0
    finally:
        gc_utils.set_debug(orig)


def test_set_threshold():
    orig = gc_utils.get_threshold()
    try:
        gc_utils.set_threshold(700, 10, 10)
        gc_utils.set_threshold(1000)
    finally:
        gc_utils.set_threshold(*orig)


def test_gc_basic_wrappers():
    assert isinstance(gc_utils.get_stats(), list)
    a = []
    b = [a]
    referents = gc_utils.get_referents(a)
    referrers = gc_utils.get_referrers(b)
    assert isinstance(referents, list)
    assert isinstance(referrers, list)
    objs = gc_utils.get_objects()
    assert isinstance(objs, list)


def test_is_tracked_containers():
    assert gc_utils.is_tracked([1, 2, 3]) is True
    assert gc_utils.is_tracked({"a": [1]}) is True
    assert gc_utils.is_tracked((1, [2])) is True
    assert gc_utils.is_tracked([]) is True


def test_is_tracked_atomic():
    assert gc_utils.is_tracked(42) is False
    assert gc_utils.is_tracked("hello") is False
    assert gc_utils.is_tracked(3.14) is False
    assert gc_utils.is_tracked(True) is False
    assert gc_utils.is_tracked(None) is False


def test_is_tracked_consistent_with_stdlib():
    for obj in ([], {}, 1, "x", None, object()):
        assert gc_utils.is_tracked(obj) is gc.is_tracked(obj)


def test_is_finalized_atomic():
    assert gc_utils.is_finalized(42) is False
    assert gc_utils.is_finalized("hello") is False


def test_is_finalized_consistent_with_stdlib():
    for obj in (1, "x", None, object()):
        assert gc_utils.is_finalized(obj) is gc.is_finalized(obj)
