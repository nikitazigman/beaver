# tests/test_graph_algorithms.py

import pytest

from algorithms.classic_algorithms.oriented_graph.src.main import Graph


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D", "E"])
    g.add_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
    return g


def test_add_vertex(sample_graph):
    sample_graph.add_vertex("F")
    assert "F" in sample_graph.adjacency_list


def test_add_edge(sample_graph):
    sample_graph.add_edge("E", "F")
    assert sample_graph.get_vertex_environment("E") == ["F"]


def test_remove_edge(sample_graph):
    sample_graph.remove_edge("A", "B")
    assert "B" not in sample_graph.get_vertex_environment("A")


def test_depth_first_search(sample_graph):
    dfs_result = sample_graph.depth_first_search()
    assert dfs_result == ["A", "B", "D", "E", "C"] or dfs_result == [
        "A",
        "C",
        "D",
        "E",
        "B",
    ]


def test_topological_sort(sample_graph):
    topo_sort_result = sample_graph.topological_sort()
    assert topo_sort_result == [
        "A",
        "B",
        "C",
        "D",
        "E",
    ] or topo_sort_result == ["A", "C", "B", "D", "E"]


def test_get_edge_cost(sample_graph):
    sample_graph.add_edge("A", "F", cost=5)
    assert sample_graph.get_edge_cost(("A", "F")) == 5
