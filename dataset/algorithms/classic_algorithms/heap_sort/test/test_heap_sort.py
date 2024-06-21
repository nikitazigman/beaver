import pytest

from algorithms.classic_algorithms.heap_sort.src.main import heap_sort


@pytest.mark.parametrize(
    "array, expected",
    [
        ([4, 10, 3, 5, 1], [1, 3, 4, 5, 10]),
        ([12, 11, 13, 5, 6, 7], [5, 6, 7, 11, 12, 13]),
        ([1, 3, 9, 4, 7], [1, 3, 4, 7, 9]),
        ([10, 20, 15, 30, 40], [10, 15, 20, 30, 40]),
        ([6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6]),
    ]
)
def test_heap_sort(array, expected):
    assert heap_sort(array) == expected
