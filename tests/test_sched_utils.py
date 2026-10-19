import sched

import sched_utils


def test_scheduler():
    s = sched_utils.scheduler()
    assert isinstance(s, sched.scheduler)


def test_enter_and_empty():
    s = sched_utils.scheduler()
    sched_utils.enter(s, 0, 1, lambda: None)
    assert not sched_utils.empty(s)


def test_cancel():
    s = sched_utils.scheduler()
    e = sched_utils.enter(s, 10, 1, lambda: None)
    sched_utils.cancel(s, e)
    assert sched_utils.empty(s)


def test_run():
    results = []
    s = sched_utils.scheduler()
    sched_utils.enter(s, 0, 1, results.append, 42)
    sched_utils.run(s)
    assert results == [42]


def test_queue():
    s = sched_utils.scheduler()
    sched_utils.enter(s, 0, 1, lambda: None)
    assert len(sched_utils.queue(s)) == 1
