import copy
import itertools


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
        if vertex1 == vertex2:
            return
        self.adjacency_list[vertex1] = (self.adjacency_list.get(vertex1) or []) + [vertex2]
        self.adjacency_list[vertex2] = (self.adjacency_list.get(vertex2) or []) + [vertex1]
        self.costs[(vertex1, vertex2)] = cost
        self.costs[(vertex2, vertex1)] = cost

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge)

    def get_edge_cost(self, edge):
        return self.costs.get(edge) if edge in self.costs else self.costs.get(edge[::-1], 0)

    def remove_edge(self, vertex1, vertex2):
        list1, list2 = self.adjacency_list.get(vertex1), self.adjacency_list.get(vertex2)
        if list1 is None or list2 is None:
            raise Exception("There is no such edge!")
        index1, index2 = list1.index(vertex2), list2.index(vertex1)
        list1.pop(index1)
        list2.pop(index2)
        self.costs[(vertex1, vertex2)] = None
        self.costs[(vertex2, vertex1)] = None

    def get_vertex_degree(self, vertex):
        return len(self.adjacency_list[vertex])

    def get_all_vertices(self):
        return self.adjacency_list.keys()

    def get_all_edges(self):
        vertices = self.adjacency_list.keys()
        edges = []
        for vertex in vertices:
            for adjacent_vertex in self.get_vertex_environment(vertex):
                edge = (vertex, adjacent_vertex)
                edges.append((self.get_edge_cost(edge), edge))
        return edges

    def is_edge_in_graph(self, edge):
        vertex1, vertex2 = edge[0], edge[1]
        list1, list2 = self.adjacency_list.get(vertex1), self.adjacency_list.get(vertex2)
        if list1 is not None and vertex2 in list1:
            return True
        if list2 is not None and vertex1 in list2:
            return True
        return False

    def is_vertex_in_graph(self, vertex):
        return self.adjacency_list.get(vertex) is not None

    def get_vertex_environment(self, vertex):
        return self.adjacency_list.get(vertex) or []

    def is_adjacent_vertices(self, vertex1, vertex2):
        vertex1_environment = self.get_vertex_environment(vertex1)
        if vertex1_environment is None:
            return False
        return vertex2 in vertex1_environment

    def get_start_vertex(self):
        if len(self.adjacency_list) == 0:
            return None
        return list(self.adjacency_list)[0]

    def breadth_first_search(self, start_vertex=None):
        if len(self.adjacency_list) == 0:
            return
        start_vertex = start_vertex or self.get_start_vertex()
        queue = [start_vertex]
        used_vertices = set()
        while len(queue) > 0:
            vertex = queue.pop(0)
            used_vertices.add(vertex)
            unvisited_vertices = [v for v in self.adjacency_list[vertex] if v not in used_vertices and v not in queue]
            queue += unvisited_vertices
            yield vertex

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
        depth_first_search_helper(self.get_start_vertex())
        return vertices_list

    def count_vertices(self):
        return len(self.adjacency_list)

    def connected_components(self):
        if len(self.adjacency_list) == 0:
            return []
        vertices = set(self.adjacency_list.keys())
        components = [list(self.breadth_first_search())]
        collected_vertices = set(itertools.chain.from_iterable(components))
        while collected_vertices != vertices:
            difference = vertices - collected_vertices
            components.append(list(self.breadth_first_search(difference.pop())))
            collected_vertices = set(itertools.chain.from_iterable(components))
        return components

    def is_empty(self):
        return all(
            map(
                lambda adjacency_list: adjacency_list == [],
                self.adjacency_list.values(),
            )
        )

    def cycle_weight(self, cycle):
        weight = 0
        for i in range(len(cycle) - 1):
            weight += self.get_edge_cost((cycle[i], cycle[i + 1]))
        return weight + self.get_edge_cost((cycle[-1], cycle[0]))

    def __copy__(self):
        copy_graph = Graph()
        copy_graph.costs = copy.deepcopy(self.costs)
        copy_graph.adjacency_list = copy.deepcopy(self.adjacency_list)
        return copy_graph

    def __contains__(self, item):
        return item in self.adjacency_list

    def __len__(self):
        return len(self.adjacency_list)
