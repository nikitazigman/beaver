import pytest

from src.main import count_inversions


@pytest.mark.parametrize(
    "array, n, expected",
    [
        ([1, 20, 6, 4, 5], 5, 5),
        ([2, 4, 1, 3, 5], 5, 3),
        ([1, 3, 5, 2, 4, 6], 6, 3),
        ([10, 10, 10], 3, 0),
    ],
)
def test_count_inversions(array, n, expected):
    assert count_inversions(array, n) == expected
