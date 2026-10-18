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
