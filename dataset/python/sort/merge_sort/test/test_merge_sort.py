import pytest

from src.main import merge_sort, merge_sort2


@pytest.mark.parametrize(
    "array, expected",
    [
        ([12, 11, 13, 5, 6, 7], [5, 6, 7, 11, 12, 13]),
        ([38, 27, 43, 3, 9, 82, 10], [3, 9, 10, 27, 38, 43, 82]),
        ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]),
        ([6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6]),
        ([5, 5, 5, 5, 5], [5, 5, 5, 5, 5]),
    ],
)
def test_merge_sort(array, expected):
    assert merge_sort(array) == expected


@pytest.mark.parametrize(
    "array, expected",
    [
        ([12, 11, 13, 5, 6, 7], [5, 6, 7, 11, 12, 13]),
        ([38, 27, 43, 3, 9, 82, 10], [3, 9, 10, 27, 38, 43, 82]),
        ([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6]),
        ([6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6]),
        ([5, 5, 5, 5, 5], [5, 5, 5, 5, 5]),
    ],
)
def test_merge_sort2(array, expected):
    assert merge_sort2(array) == expected
