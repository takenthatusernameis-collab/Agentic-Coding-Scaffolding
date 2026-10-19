import tracemalloc

import tracemalloc_utils


def test_is_tracing():
    tracemalloc.stop()
    assert tracemalloc_utils.is_tracing() is False


def test_start_stop():
    tracemalloc_utils.start(1)
    assert tracemalloc_utils.is_tracing() is True
    tracemalloc_utils.stop()
    assert tracemalloc_utils.is_tracing() is False


def test_get_traced_memory():
    tracemalloc_utils.start(1)
    current, peak = tracemalloc_utils.get_traced_memory()
    assert isinstance(current, int)
    assert isinstance(peak, int)
    tracemalloc_utils.stop()


def test_traceback_limit():
    assert isinstance(tracemalloc_utils.get_traceback_limit(), int)


def test_clear_traces():
    tracemalloc_utils.start(1)
    tracemalloc_utils.clear_traces()
    tracemalloc_utils.stop()
