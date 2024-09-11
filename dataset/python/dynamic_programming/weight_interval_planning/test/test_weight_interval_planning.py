from src.main import weight_interval_planning, weight_interval_planning_iter


def test_weight_interval_planning():
    intervals1 = [
        ((1, 2), 3),
        ((1.5, 3), 4),
        ((3.5, 5), 6),
        ((4, 4.5), 2),
        ((4.25, 6), 1),
        ((4.5, 7), 5),
        ((5.5, 9), 7),
    ]
    intervals2 = [((1, 3), 7), ((2, 4), 3), ((2.5, 5), 10), ((4, 10), 5)]
    assert weight_interval_planning(intervals1) == 17
    assert weight_interval_planning_iter(intervals1) == 17
    assert weight_interval_planning(intervals2) == 12
    assert weight_interval_planning_iter(intervals2) == 12


def test_weight_interval_planning_single():
    intervals = [((1, 3), 5)]
    assert weight_interval_planning(intervals) == 5


def test_weight_interval_planning_empty():
    intervals = []
    assert weight_interval_planning(intervals) == 0


def test_weight_interval_planning_overlap():
    intervals = [((1, 3), 5), ((2, 5), 6), ((3, 6), 5)]
    assert weight_interval_planning(intervals) == 6


def test_weight_interval_planning_iter_single():
    intervals = [((1, 3), 5)]
    assert weight_interval_planning_iter(intervals) == 5


def test_weight_interval_planning_iter_empty():
    intervals = []
    assert weight_interval_planning_iter(intervals) == 0


def test_weight_interval_planning_iter_overlap():
    intervals = [((1, 3), 5), ((2, 5), 6), ((3, 6), 5)]
    assert weight_interval_planning_iter(intervals) == 6
