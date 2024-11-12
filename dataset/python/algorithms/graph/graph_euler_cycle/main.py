from copy import copy


def find_euler_cycle(graph, start_vertex=None):
    if not _euler_cycle_exist(graph) or graph.count_vertices() == 0:
        return None
    copy_graph = copy(graph)
    start_vertex = start_vertex or graph.get_start_vertex()

    def find_euler_cycle_helper(vertex):
        euler_cycle = []
        stack = [vertex]
        while len(stack) > 0:
            peek_vertex = stack.pop()
            euler_cycle.append(peek_vertex)
            if copy_graph.get_vertex_degree(peek_vertex) > 0:
                peek_environment = copy_graph.get_vertex_environment(peek_vertex)
                next_vertex = peek_environment[0]
                copy_graph.remove_edge(peek_vertex, next_vertex)
                stack.append(next_vertex)
            else:
                for vertex in euler_cycle[1:]:
                    if copy_graph.get_vertex_degree(vertex) != 0:
                        euler_cycle = euler_cycle[0:1] + find_euler_cycle_helper(vertex) + euler_cycle[2:]
        return euler_cycle

    return find_euler_cycle_helper(start_vertex)


def _euler_cycle_exist(graph):
    return all(
        map(
            lambda vertex: graph.get_vertex_degree(vertex) % 2 == 0,
            graph.get_all_vertices(),
        )
    )
