from math import sqrt

import pytest

from algorithms.classic_algorithms.nearest_pair_of_points.src.main import (
    nearest_points,
)


def test_nearest_points():
    points = [(0, 0), (1, 1), (4, 4), (5, 5)]
    result = nearest_points(points)
    assert result == pytest.approx(sqrt(2), 0.0001)

def test_nearest_points_brute_force():
    points = [(0, 0), (1, 1), (2, 2), (3, 3)]
    result = nearest_points(points)
    assert result == pytest.approx(sqrt(2), 0.0001)

def test_nearest_points_single_point():
    points = [(0, 0)]
    result = nearest_points(points)
    assert result == float('inf')

def test_nearest_points_two_points():
    points = [(0, 0), (3, 4)]
    result = nearest_points(points)
    assert result == pytest.approx(5, 0.0001)

def test_nearest_points_no_points():
    points = []
    result = nearest_points(points)
    assert result == float('inf')
