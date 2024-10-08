def is_acyclic_graph(graph):
    if graph.count_vertices() <= 2:
        return True
    visited_vertices = set()
    vertices = list(graph.get_all_vertices())
    colors = {}
    previous_vertex = vertices[0]

    def is_acyclic_graph_helper(vertex):
        nonlocal previous_vertex
        colors[vertex] = True
        visited_vertices.add(vertex)
        for adjacent_vertex in graph.get_vertex_environment(vertex):
            if adjacent_vertex not in visited_vertices:
                previous_vertex = vertex
                return is_acyclic_graph_helper(adjacent_vertex)
            elif adjacent_vertex != previous_vertex and colors.get(
                adjacent_vertex
            ):
                return False
        colors[vertex] = False
        return True

    return is_acyclic_graph_helper(vertices[0])
