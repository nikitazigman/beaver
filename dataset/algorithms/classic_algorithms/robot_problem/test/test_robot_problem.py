from algorithms.classic_algorithms.robot_problem.src.main import (
    create_matrix,
    fill_matrix,
    robot_problem,
)


def test_robot_problem():
    assert robot_problem(1) == 1
    assert robot_problem(2) == 2
    assert robot_problem(3) == 6
    assert robot_problem(4) == 20

def test_create_matrix():
    matrix = create_matrix(3)
    assert matrix[0][0] == 1
    assert matrix[2][2] == 6

def test_fill_matrix():
    matrix = [[None] * 3 for _ in range(3)]
    fill_matrix(matrix)
    assert matrix[0][0] == 1
    assert matrix[2][2] == 6
