import pytest

from algorithms.sort.bubble_sort.main import bubble_sort


@pytest.mark.parametrize(
    "array, expected",
    [
        ([64, 34, 25, 12, 22, 11, 90], [11, 12, 22, 25, 34, 64, 90]),
        ([5, 1, 4, 2, 8], [1, 2, 4, 5, 8]),
        ([3, 0, 2, 5, -1, 4, 1], [-1, 0, 1, 2, 3, 4, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ],
)
def test_bubble_sort(array: list[int], expected: list[int]) -> None:
    bubble_sort(array=array)
    assert array == expected
