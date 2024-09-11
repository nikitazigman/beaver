from src.main import stable_marriage_problem


def test_stable_marriage_problem():
    man_p = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    girl_p = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
    expected_pairs = {0: 0, 1: 1, 2: 2}
    assert stable_marriage_problem(man_p, girl_p) == expected_pairs
