import pytest

from algorithms.sort.selection_sort.main import selection_sort


@pytest.mark.parametrize(
    "array, expected",
    [
        ([64, 25, 12, 22, 11], [11, 12, 22, 25, 64]),
        ([29, 10, 14, 37, 13], [10, 13, 14, 29, 37]),
        ([3, 0, 2, 5, -1, 4, 1], [-1, 0, 1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ],
)
def test_selection_sort(array: list[int], expected: list[int]) -> None:
    assert selection_sort(array=array) == expected
