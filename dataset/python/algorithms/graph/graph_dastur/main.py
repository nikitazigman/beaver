def _find_vertex_to_color_dsatur(graph, not_colored_vertices, adjacent_vertices_colors):
    vertex_to_color = next(iter(not_colored_vertices))
    for vertex in not_colored_vertices:
        greater_saturation = len(adjacent_vertices_colors[vertex]) > len(adjacent_vertices_colors[vertex_to_color])
        equal_saturation = len(adjacent_vertices_colors[vertex]) == len(adjacent_vertices_colors[vertex_to_color])
        greater_degree = graph.get_vertex_degree(vertex) > graph.get_vertex_degree(vertex_to_color)
        if greater_saturation or equal_saturation and greater_degree:
            vertex_to_color = vertex
    return vertex_to_color


def dsatur(graph):
    not_colored_vertices = set(graph.get_all_vertices())
    vertices_colors = {}
    adjacent_vertices_colors = {vertex: set() for vertex in not_colored_vertices}
    used_colors_length = 1
    while len(not_colored_vertices) != 0:
        vertex_to_color = _find_vertex_to_color_dsatur(graph, not_colored_vertices, adjacent_vertices_colors)
        color = min(set(range(used_colors_length + 1)) - adjacent_vertices_colors[vertex_to_color])
        used_colors_length = max(used_colors_length, color + 1)
        vertices_colors[vertex_to_color] = color
        not_colored_vertices.remove(vertex_to_color)
        for adjacent_vertex in graph.get_vertex_environment(vertex_to_color):
            adjacent_vertices_colors[adjacent_vertex].add(color)
    return vertices_colors, used_colors_length
