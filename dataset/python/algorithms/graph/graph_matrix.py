class Graph:

    def __init__(self, size=100):
        self.size = size
        self.adjacent_matrix = [[0] * size for _ in range(size)]

    def add_edge(self, vertex1, vertex2):
        self.adjacent_matrix[vertex1][vertex2] = 1
        self.adjacent_matrix[vertex2][vertex1] = 1

    def remove_edge(self, vertex1, vertex2):
        self.adjacent_matrix[vertex1][vertex2] = 0
        self.adjacent_matrix[vertex2][vertex1] = 0

    def is_adjacent_vertexes(self, vertex1, vertex2):
        return self.adjacent_matrix[vertex1][vertex2] == 1
