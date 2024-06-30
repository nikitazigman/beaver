from algorithms.classic_algorithms.graph_euler_cycle.src.main import (
    find_euler_cycle,
)
from algorithms.classic_algorithms.graph_list.src.main import Graph


def test_euler_cycle():
    graph = Graph()
    assert find_euler_cycle(graph) is None
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    assert find_euler_cycle(graph) is None
    graph.add_edge(2, 3)
    assert [1, 2, 3, 1] == find_euler_cycle(graph)
    graph.add_edge(2, 4)
    graph.add_edge(2, 6)
    graph.add_edge(3, 6)
    graph.add_edge(3, 5)
    graph.add_edge(5, 6)
    graph.add_edge(5, 4)
    graph.add_edge(4, 6)
    graph.add_edge(4, 7)
    graph.add_edge(5, 7)
    assert [1, 2, 4, 6, 5, 7, 4, 5, 3, 6, 2, 3, 1] == find_euler_cycle(
        graph, 1
    )
