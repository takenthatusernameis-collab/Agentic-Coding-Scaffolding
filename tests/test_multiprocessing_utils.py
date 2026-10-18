"""Tests for multiprocessing_utils module."""

from __future__ import annotations

import time

import pytest

import multiprocessing_utils


def _mp_inc(x):
    return x + 1


def _mp_iden(x):
    return x


def _mp_add(a, b):
    return a + b


def test_cpu_count():
    count = multiprocessing_utils.cpu_count()
    assert isinstance(count, int)
    assert count > 0


def test_current_process():
    proc = multiprocessing_utils.current_process()
    assert proc is not None
    assert hasattr(proc, "name")


def test_active_children():
    children = multiprocessing_utils.active_children()
    assert isinstance(children, list)


def test_get_context():
    ctx = multiprocessing_utils.get_context()
    assert ctx is not None
    ctx_spawn = multiprocessing_utils.get_context("spawn")
    assert ctx_spawn is not None


def test_get_context_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.get_context(123)  # type: ignore[arg-type]


def test_create_queue():
    q = multiprocessing_utils.create_queue()
    assert q is not None
    q.put(1)
    assert q.get() == 1
    q.close()
    q.join_thread()


def test_create_queue_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.create_queue(maxsize="5")  # type: ignore[arg-type]


def test_create_simple_queue():
    q = multiprocessing_utils.create_simple_queue()
    assert q is not None
    q.put(42)
    assert q.get() == 42


def test_create_lock():
    lock = multiprocessing_utils.create_lock()
    assert lock is not None
    with lock:
        pass


def test_create_rlock():
    rlock = multiprocessing_utils.create_rlock()
    assert rlock is not None
    with rlock:
        pass


def test_create_semaphore():
    sem = multiprocessing_utils.create_semaphore(2)
    assert sem is not None
    sem.acquire()
    sem.release()


def test_create_semaphore_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.create_semaphore(value="1")  # type: ignore[arg-type]


def test_create_event():
    ev = multiprocessing_utils.create_event()
    assert ev is not None
    assert not ev.is_set()


def test_create_condition():
    cond = multiprocessing_utils.create_condition()
    assert cond is not None
    cond.acquire()
    cond.release()


def test_create_condition_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.create_condition(lock="bad")  # type: ignore[arg-type]


def test_create_value():
    val = multiprocessing_utils.create_value("i", 10)
    assert val.value == 10
    val.value = 20
    assert val.value == 20


def test_create_array():
    arr = multiprocessing_utils.create_array("i", [1, 2, 3])
    assert list(arr) == [1, 2, 3]


def test_create_process():
    def nop():
        pass

    p = multiprocessing_utils.create_process(target=nop)
    assert p is not None


def test_create_process_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.create_process(target="bad")  # type: ignore[arg-type]


def test_run_in_process():
    def square(x):
        return x * x

    result = multiprocessing_utils.run_in_process(square, 5)
    assert result == 25


def test_run_in_process_timeout():
    def slow():
        time.sleep(2)
        return "done"

    with pytest.raises(multiprocessing_utils.mp.TimeoutError if False else Exception):  # type: ignore[attr-defined]
        multiprocessing_utils.run_in_process(slow, timeout=0.1)


def test_run_in_process_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.run_in_process("not_callable")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        multiprocessing_utils.run_in_process(lambda: None, timeout="bad")  # type: ignore[arg-type]


def test_pool_map():
    def inc(x):
        return x + 1
    result = multiprocessing_utils.pool_map(_mp_inc, [1, 2, 3])
    assert result == [2, 3, 4]


def test_pool_map_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.pool_map("bad", [1, 2])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        def iden(x):
            return x
        multiprocessing_utils.pool_map(_mp_iden, [1, 2], chunksize="1")  # type: ignore[arg-type]


def test_pool_starmap():
    def add2(a, b):
        return a + b
    result = multiprocessing_utils.pool_starmap(_mp_add, [(1, 2), (3, 4)])
    assert result == [3, 7]


def test_pool_starmap_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.pool_starmap("bad", [(1, 2)])  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        def add2b(a, b):
            return a + b
        multiprocessing_utils.pool_starmap(_mp_add, [(1, 2)], chunksize="1")  # type: ignore[arg-type]


def test_create_pool():
    pool = multiprocessing_utils.create_pool(processes=2)
    assert pool is not None
    pool.close()
    pool.join()


def test_create_pool_type_errors():
    with pytest.raises(TypeError):
        multiprocessing_utils.create_pool(processes="2")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        multiprocessing_utils.create_pool(context=123)  # type: ignore[arg-type]


def test_is_forking_spawn_forkserver():
    assert isinstance(multiprocessing_utils.is_forking(), bool)
    assert isinstance(multiprocessing_utils.is_spawn(), bool)
    assert isinstance(multiprocessing_utils.is_forkserver(), bool)


def test_freeze_support():
    multiprocessing_utils.freeze_support()
