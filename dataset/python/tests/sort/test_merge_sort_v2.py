import pytest

from algorithms.sort.merge_sort_v2.main import merge_sort


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
def test_merge_sort(array: list[int], expected: list[int]) -> None:
    assert merge_sort(array=array) == expected
