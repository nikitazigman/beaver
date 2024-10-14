def robot_problem(n):
    matrix = create_matrix(n)
    return matrix[n - 1][n - 1]

def create_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    fill_matrix(matrix)
    return matrix

def fill_matrix(matrix):
    length = len(matrix)
    for i in range(length):
        for j in range(length):
            if i == 0 or j == 0:
                matrix[i][j] = 1
            else:
                matrix[i][j] = matrix[i - 1][j] + matrix[i][j - 1]
