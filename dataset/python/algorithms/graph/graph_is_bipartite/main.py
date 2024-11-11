def is_bipartite(graph):
    parts = {0: [], 1: []}
    visited_vertices = set()
    colors = {}
    start_vertex = graph.get_start_vertex()
    queue = [start_vertex]
    proper_color = {start_vertex: 0}
    while len(queue) > 0:
        vertex = queue.pop(0)
        current_color = proper_color[vertex]
        colors[vertex] = current_color
        parts[current_color].append(vertex)
        visited_vertices.add(vertex)
        for adjacent_vertex in graph.get_vertex_environment(vertex):
            if adjacent_vertex in visited_vertices and colors[vertex] == colors[adjacent_vertex]:
                return False, []
            elif adjacent_vertex not in visited_vertices and adjacent_vertex not in queue:
                queue.append(adjacent_vertex)
                proper_color[adjacent_vertex] = not current_color
    return True, [parts[1], parts[0]]
