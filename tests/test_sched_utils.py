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


def test_enterabs_schedules_event():
    s = sched_utils.scheduler()
    event = sched_utils.enterabs(s, 100, 1, lambda: None)
    assert isinstance(event, sched.Event)
    assert not sched_utils.empty(s)


def test_enterabs_runs_action_at_absolute_time():
    results = []
    s = sched_utils.scheduler(
        timefunc=lambda: 0.0, delayfunc=lambda _: None
    )
    sched_utils.enterabs(s, 0, 1, results.append, 42)
    sched_utils.run(s)
    assert results == [42]


def test_enterabs_passes_argument_and_kwargs():
    received = []

    def action(value, *, flag=False):
        received.append((value, flag))

    s = sched_utils.scheduler(
        timefunc=lambda: 0.0, delayfunc=lambda _: None
    )
    sched_utils.enterabs(s, 0, 1, action, 7, flag=True)
    sched_utils.run(s)
    assert received == [(7, True)]


def test_enterabs_cancel_leaves_queue_empty():
    s = sched_utils.scheduler()
    event = sched_utils.enterabs(s, 100, 1, lambda: None)
    sched_utils.cancel(s, event)
    assert sched_utils.empty(s)


def test_enterabs_future_time_event_is_queued():
    """An ``enterabs`` event scheduled in the future is queued but not run yet."""
    clock = [0.0]
    results = []
    s = sched_utils.scheduler(
        timefunc=lambda: clock[0], delayfunc=lambda _: None
    )
    sched_utils.enterabs(s, 100, 1, results.append, "late")
    assert not sched_utils.empty(s)
    # The event has not fired yet.
    assert results == []
    # Advance the clock to the scheduled time and run.
    clock[0] = 100
    sched_utils.run(s)
    assert results == ["late"]
