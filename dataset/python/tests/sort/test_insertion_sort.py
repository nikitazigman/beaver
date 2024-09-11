import pytest

from algorithms.sort.insertion_sort.main import insertion_sort


@pytest.mark.parametrize(
    "array, expected",
    [
        ([12, 11, 13, 5, 6], [5, 6, 11, 12, 13]),
        ([4, 3, 2, 10, 12, 1, 5, 6], [1, 2, 3, 4, 5, 6, 10, 12]),
        ([1, 1, 1, 1], [1, 1, 1, 1]),
        ([1, 3, 2, 3, 1], [1, 1, 2, 3, 3]),
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5]),
    ],
)
def test_insertion_sort(array, expected):
    insertion_sort(array)
    assert array == expected
