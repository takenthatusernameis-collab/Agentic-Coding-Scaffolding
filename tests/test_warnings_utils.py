import warnings

import warnings_utils


def test_warn_emits():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        warnings_utils.warn("hello")
        assert len(w) == 1
        assert str(w[0].message) == "hello"


def test_warn_type_error():
    try:
        warnings_utils.warn(123)
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")


def test_simplefilter_invalid():
    try:
        warnings_utils.simplefilter("bogus")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_catch_warnings_context():
    with warnings_utils.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        warnings.warn("x")
        assert len(w) == 1


def test_resetwarnings():
    warnings_utils.resetwarnings()
