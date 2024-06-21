import pytest

from algorithms.classic_algorithms.MinMaxMatrix.src.main import Solution


@pytest.mark.parametrize(
    "weights, expected",
    (
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
        ([[1, 2, 3], [4, 5, 6]], 12),
        ([[1, 2], [1, 1]], 3),
        ([[5]], 5),
        ([[1, 2, 5], [3, 2, 1]], 6),
    ),
)
def test_min_path_matrix(weights: list[list[int]], expected: int):
    assert Solution().min_path_matrix(weights) == expected
