from bisect_utils import (
    bisect_left,
    bisect_right,
    find_leftmost,
    find_rightmost,
    insort_left,
    insort_right,
)


def test_bisect_left():
    a = [1, 2, 2, 3]
    assert bisect_left(a, 2) == 1
    assert bisect_left(a, 0) == 0
    assert bisect_left(a, 5) == 4


def test_bisect_right():
    a = [1, 2, 2, 3]
    assert bisect_right(a, 2) == 3


def test_insort():
    a = [1, 3, 5]
    insort_left(a, 2)
    assert a == [1, 2, 3, 5]
    insort_right(a, 3)
    assert a == [1, 2, 3, 3, 5]


def test_find():
    a = [1, 2, 2, 3]
    assert find_leftmost(a, 2) == 1
    assert find_rightmost(a, 2) == 2
    assert find_leftmost(a, 9) is None
    assert find_rightmost(a, 9) is None
