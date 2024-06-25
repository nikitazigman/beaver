from algorithms.classic_algorithms.graph_dijkstra.src.main import dijkstra
from algorithms.classic_algorithms.oriented_graph.src.main import Graph


def test_djkstra():
    graph = Graph()
    graph.add_edge(1, 2, 2)
    graph.add_edge(1, 3, 3)
    graph.add_edge(2, 4, 3)
    graph.add_edge(2, 6, 2)
    graph.add_edge(3, 4, 1)
    graph.add_edge(3, 5, 1)
    graph.add_edge(4, 5, 2)
    graph.add_edge(4, 6, 4)
    graph.add_edge(5, 6, 1)
    assert (4, [1, 2, 6]) == dijkstra(graph, 1, 6)
    assert dijkstra(graph, 4, 3) is None
    assert (2, [3, 5, 6]) == dijkstra(graph, 3, 6)
