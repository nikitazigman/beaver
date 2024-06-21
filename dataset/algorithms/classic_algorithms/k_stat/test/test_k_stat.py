import pytest

from algorithms.classic_algorithms.k_stat.src.main import (
    k_stat,
    k_stat2,
    k_stat3,
)


@pytest.mark.parametrize(
    "arr, position, expected",
    [
        ([3, 2, 1, 5, 4], 2, 3),
        ([12, 3, 5, 7, 19], 1, 5),
        ([7, 10, 4, 3, 20, 15], 3, 10),
        ([1, 2, 3, 4, 5], 0, 1),
        ([5, 4, 3, 2, 1], 4, 5),
    ]
)
def test_k_stat(arr, position, expected):
    assert k_stat(arr, position) == expected

@pytest.mark.parametrize(
    "arr, position, expected",
    [
        ([3, 2, 1, 5, 4], 2, 3),
        ([12, 3, 5, 7, 19], 1, 5),
        ([7, 10, 4, 3, 20, 15], 3, 10),
        ([1, 2, 3, 4, 5], 0, 1),
        ([5, 4, 3, 2, 1], 4, 5),
    ]
)
def test_k_stat2(arr, position, expected):
    assert k_stat2(arr, position) == expected

@pytest.mark.parametrize(
    "arr, position, expected",
    [
        ([3, 2, 1, 5, 4], 2, 3),
        ([12, 3, 5, 7, 19], 1, 5),
        ([7, 10, 4, 3, 20, 15], 3, 10),
        ([1, 2, 3, 4, 5], 0, 1),
        ([5, 4, 3, 2, 1], 4, 5),
    ]
)
def test_k_stat3(arr, position, expected):
    assert k_stat3(arr, position) == expected
