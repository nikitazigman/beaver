import pytest

from algorithms.classic_algorithms.k_merge.src.main import k_merge


@pytest.mark.parametrize(
    "arrays, expected",
    [
        (([1, 4, 7], [2, 5, 8], [3, 6, 9]), [1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (([1, 3, 5], [2, 4, 6]), [1, 2, 3, 4, 5, 6]),
        (
            ([5, 10, 15], [3, 8, 9, 12], [0, 6, 11]),
            [0, 3, 5, 6, 8, 9, 10, 11, 12, 15],
        ),
        (([], [1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6]),
        (([10, 20], [15, 25], [5, 30]), [5, 10, 15, 20, 25, 30]),
    ],
)
def test_k_merge(arrays, expected):
    assert k_merge(*arrays) == expected
