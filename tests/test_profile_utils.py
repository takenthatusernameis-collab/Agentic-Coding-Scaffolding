import profile_utils


def test_new_profiler():
    p = profile_utils.new_profiler()
    assert isinstance(p, profile_utils.Profile)


def test_run():
    profile_utils.run("x = 1 + 2")
    assert True


def test_runctx():
    ns = {}
    profile_utils.runctx("x = 1 + 2", ns, ns)
    assert ns["x"] == 3


def test_type_errors():
    try:
        profile_utils.run(123)
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")
