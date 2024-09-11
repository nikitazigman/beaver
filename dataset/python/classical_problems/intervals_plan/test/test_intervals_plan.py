from src.main import plan_intervals


def test_plan_intervals():
    entries = [(3, 2), (1, 1), (2, 3)]
    result = plan_intervals(entries)
    assert result == [(0, 1), (1, 4), (4, 6)]


def test_single_entry():
    entries = [(1, 1)]
    result = plan_intervals(entries)
    assert result == [(0, 1)]


def test_multiple_entries():
    entries = [(3, 1), (2, 2), (1, 3)]
    result = plan_intervals(entries)
    assert result == [(0, 3), (3, 5), (5, 6)]
