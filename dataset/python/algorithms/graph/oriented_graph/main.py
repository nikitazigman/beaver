class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.costs = {}

    def add_vertex(self, vertex):
        if self.adjacency_list.get(vertex) is not None:
            raise Exception("Such vertex already exist!")
        self.adjacency_list[vertex] = []

    def add_vertices(self, vertices):
        for vertex in vertices:
            self.add_vertex(vertex)

    def add_edge(self, vertex1, vertex2, cost=0):
        self.adjacency_list[vertex1] = (self.adjacency_list.get(vertex1) or []) + [vertex2]
        self.adjacency_list[vertex2] = self.adjacency_list.get(vertex2) or []
        self.costs[(vertex1, vertex2)] = cost

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge[0], edge[1])

    def remove_edge(self, vertex1, vertex2):
        adjacency_list = self.adjacency_list.get(vertex1)
        vertex_index = adjacency_list.index(vertex2)
        adjacency_list.pop(vertex_index)

    def get_vertex_environment(self, vertex):
        return self.adjacency_list.get(vertex) or []

    def get_edge_cost(self, edge):
        return self.costs.get(edge)

    def depth_first_search(self):
        def depth_first_search_helper(current_vertex):
            visited_vertices.add(current_vertex)
            vertices_list.append(current_vertex)
            for vertex in self.get_vertex_environment(current_vertex):
                if vertex not in visited_vertices:
                    depth_first_search_helper(vertex)

        if len(self.adjacency_list) == 0:
            return []
        visited_vertices = set()
        vertices_list = []
        incoming_vertices = self._get_incoming_vertices()
        start_vertices = [vertex for (vertex, income) in incoming_vertices.items() if len(income) == 0]
        for vertex in start_vertices:
            depth_first_search_helper(vertex)
        return vertices_list

    def topological_sort(self):
        def topological_sort_helper(vertex):
            topological_path.append(vertex)
            visited_vertices.add(vertex)
            for adjacency_vertex in self.get_vertex_environment(vertex):
                if (
                    adjacency_vertex not in visited_vertices
                    and len(incoming_vertices[adjacency_vertex] - visited_vertices) == 0
                ):
                    topological_sort_helper(adjacency_vertex)

        if len(self.adjacency_list) == 0:
            return []
        visited_vertices = set()
        incoming_vertices = self._get_incoming_vertices()
        start_vertices = [vertex for (vertex, income) in incoming_vertices.items() if len(income) == 0]
        topological_path = []
        for vertex in start_vertices:
            topological_sort_helper(vertex)
        if len(topological_path) != len(self.get_all_vertices()):
            return None
        return topological_path

    def _get_incoming_vertices(self):
        vertices = self.get_all_vertices()
        incoming_vertices = {vertex: set() for vertex in vertices}
        for vertex in vertices:
            for v in vertices:
                if vertex in self.get_vertex_environment(v):
                    incoming_vertices[vertex].add(v)
        return incoming_vertices

    def get_all_vertices(self):
        return self.adjacency_list.keys()
