import heapq

from graph_list.src.main import Graph


def prim(graph):
    total_cost = 0
    min_cost_tree = Graph()
    start_vertex = graph.get_start_vertex()
    vertices_queue = [(0, (start_vertex, start_vertex))]
    while vertices_queue:
        cost, (vertex, orig_vertex) = heapq.heappop(vertices_queue)
        if vertex not in min_cost_tree:
            total_cost += cost
            min_cost_tree.add_edge(vertex, orig_vertex)
            for adjacent_vertex in graph.get_vertex_environment(vertex):
                if adjacent_vertex not in min_cost_tree:
                    heapq.heappush(
                        vertices_queue,
                        (
                            graph.get_edge_cost((vertex, adjacent_vertex)),
                            (adjacent_vertex, vertex),
                        ),
                    )
    return total_cost, min_cost_tree
