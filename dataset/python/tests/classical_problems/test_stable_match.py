from algorithms.classical_problems.stable_match.main import StableMatch


def test_stable_pairs():
    preferences = [
        [1, 0, 2, 3, 4],
        [4, 1, 2, 3, 0],
        [2, 3, 1, 0, 4],
        [1, 4, 3, 2, 0],
        [2, 0, 4, 1, 3],
    ]
    estimations = [
        [12, 8, 3, 5, 10],
        [11, 13, 7, 9, 10],
        [14, 10, 9, 5, 8],
        [13, 14, 10, 8, 11],
        [11, 13, 14, 9, 15],
    ]
    stable_match = StableMatch(preferences, estimations)
    pairs_by_estimations = stable_match.get_stable_pairs_by_estimations()
    pairs_by_preferences = stable_match.get_stable_pairs_by_preferences()
    assert pairs_by_estimations == {0: 4, 1: 0, 2: 3, 3: 1, 4: 2}
    assert stable_match.total_efficiency(pairs_by_estimations) == 46
    assert stable_match.total_efficiency(pairs_by_preferences) == 51
