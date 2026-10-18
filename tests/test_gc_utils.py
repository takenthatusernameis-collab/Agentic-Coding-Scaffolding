"""Tests for gc_utils."""

import gc

from gc_utils import (
    gc_collect,
    gc_disable,
    gc_enable,
    gc_get_count,
    gc_get_objects,
    gc_get_threshold,
    gc_isenabled,
    gc_set_threshold,
)


def test_gc_collect():
    assert isinstance(gc_collect(), int)


def test_gc_enable_disable():
    gc_enable()
    assert gc_isenabled()
    gc_disable()
    assert not gc_isenabled()
    gc_enable()


def test_gc_thresholds():
    orig = gc_get_threshold()
    gc_set_threshold(700, 10, 10)
    assert gc_get_threshold() == (700, 10, 10)
    gc_set_threshold(*orig)


def test_gc_count():
    assert isinstance(gc_get_count(), tuple)


def test_gc_objects():
    assert isinstance(gc_get_objects(), list)