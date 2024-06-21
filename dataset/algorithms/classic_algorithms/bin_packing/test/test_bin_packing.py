import pytest

from algorithms.classic_algorithms.bin_packing.src.main import (
    best_fit,
    first_fit,
    next_fit,
)


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ([0.1, 0.2, 0.3, 0.7, 1, 0.8], [[0.1, 0.2, 0.3], [0.7], [1], [0.8]]),
        ([1, 1, 1, 1], [[1], [1], [1], [1]]),
        ([0.5, 0.6, 0.4, 0.3], [[0.5], [0.6, 0.4], [0.3]]),
        ([], []),
    ],
)
def test_next_fit(test_data, expected):
    assert next_fit(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        (
            [0.1, 1, 0.3, 0.6, 0.8, 1, 0.1, 0.5],
            [[0.1, 0.3, 0.6], [1], [0.8, 0.1], [1], [0.5]],
        ),
        ([1, 1, 1, 1], [[1], [1], [1], [1]]),
        ([0.5, 0.6, 0.4, 0.3], [[0.5, 0.4], [0.6, 0.3]]),
        ([], [[]]),
    ],
)
def test_first_fit(test_data, expected):
    assert first_fit(test_data) == expected


@pytest.mark.parametrize(
    "test_data, expected",
    [
        ([0.5, 0.8, 0.1, 0.1, 0.6, 0.4], [[0.5], [0.8, 0.1, 0.1], [0.6, 0.4]]),
        ([1, 1, 1, 1], [[1], [1], [1], [1]]),
        ([0.5, 0.6, 0.4, 0.3], [[0.5, 0.3], [0.6, 0.4]]),
        ([], [[]]),
    ],
)
def test_best_fit(test_data, expected):
    assert best_fit(test_data) == expected
