import pytest

from src.main import count_sort


@pytest.mark.parametrize(
    "array, expected",
    [
        ([4, 2, 2, 8, 3, 3, 1], [1, 2, 2, 3, 3, 4, 8]),
        ([1, 4, 1, 2, 7, 5, 2], [1, 1, 2, 2, 4, 5, 7]),
        ([9, 4, 10, 8, 2, 4], [2, 4, 4, 8, 9, 10]),
        ([5, 5, 5, 5, 5], [5, 5, 5, 5, 5]),
        ([3, 6, 4, 1, 3, 4, 1, 4], [1, 1, 3, 3, 4, 4, 4, 6]),
    ],
)
def test_count_sort(array, expected):
    assert count_sort(array) == expected
