from src.main import max_independent_intervals


def test_max_independent_intervals():
    intervals = [(1, 3), (2, 4), (3, 5), (6, 8)]
    result = max_independent_intervals(intervals)
    assert result == [(1, 3), (3, 5), (6, 8)]


def test_single_interval():
    intervals = [(1, 2)]
    result = max_independent_intervals(intervals)
    assert result == [(1, 2)]


def test_no_intervals():
    intervals = []
    result = max_independent_intervals(intervals)
    assert result == []


def test_overlapping_intervals():
    intervals = [(1, 3), (2, 5), (4, 7), (6, 9)]
    result = max_independent_intervals(intervals)
    assert result == [(1, 3), (4, 7)]


def test_all_intervals_overlapping():
    intervals = [(1, 4), (2, 5), (3, 6)]
    result = max_independent_intervals(intervals)
    assert result == [(1, 4)]
