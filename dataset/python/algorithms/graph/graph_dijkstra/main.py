import heapq


def dijkstra(graph, start_vertex, target_vertex):
    queue = [(0, [start_vertex])]
    marked_vertices = set()
    while queue:
        current_cost_path = heapq.heappop(queue)
        last_vertex = current_cost_path[1][-1]
        if last_vertex == target_vertex:
            return current_cost_path
        marked_vertices.add(last_vertex)
        not_marked_vertices = set(graph.get_vertex_environment(last_vertex)) - marked_vertices
        for vertex in not_marked_vertices:
            edge_cost = graph.get_edge_cost((last_vertex, vertex))
            heapq.heappush(
                queue,
                (
                    current_cost_path[0] + edge_cost,
                    current_cost_path[1] + [vertex],
                ),
            )
    return None
