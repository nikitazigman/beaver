from copy import copy


def _get_potential_vertices_gis(
    not_colored_vertices, adjacent_vertices_colors, color
):
    vertices = []
    for vertex in not_colored_vertices:
        if color not in adjacent_vertices_colors[vertex]:
            vertices.append(vertex)
    return vertices


def gis(graph):
    not_colored_vertices = set(graph.get_all_vertices())
    adjacent_vertices_colors = {
        vertex: set() for vertex in not_colored_vertices
    }
    last_color = 0
    vertices_colors = {}
    copy_graph = copy(graph)
    while len(not_colored_vertices) != 0:
        vertices = _get_potential_vertices_gis(
            not_colored_vertices, adjacent_vertices_colors, last_color
        )
        vertices_count = [
            (v, len(copy_graph.get_vertex_environment(v))) for v in vertices
        ]
        for vertex, _ in sorted(vertices_count, key=lambda item: item[1]):
            if last_color not in adjacent_vertices_colors[vertex]:
                vertices_colors[vertex] = last_color
                not_colored_vertices.remove(vertex)
                for adjacent_vertex in copy_graph.get_vertex_environment(
                    vertex
                ).copy():
                    adjacent_vertices_colors[adjacent_vertex].add(last_color)
                    copy_graph.remove_edge(adjacent_vertex, vertex)
        last_color += 1
    return vertices_colors, last_color
