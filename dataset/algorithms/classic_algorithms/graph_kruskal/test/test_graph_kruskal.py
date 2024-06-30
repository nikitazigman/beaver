import pytest

from algorithms.classic_algorithms.graph_list.src.main import Graph


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_vertices(['A', 'B', 'C', 'D'])
    g.add_edges([('A', 'B', 1), ('A', 'C', 3), ('B', 'C', 1), ('C', 'D', 2)])
    return g

def test_add_vertex(sample_graph):
    sample_graph.add_vertex('E')
    assert 'E' in sample_graph.adjacency_list

def test_add_edge(sample_graph):
    sample_graph.add_edge('D', 'E', 4)
    assert sample_graph.is_edge_in_graph(('D', 'E'))

def test_breadth_first_search(sample_graph):
    bfs_result = list(sample_graph.breadth_first_search('A'))
    assert bfs_result == ['A', 'B', 'C', 'D']

def test_depth_first_search(sample_graph):
    dfs_result = sample_graph.depth_first_search()
    assert dfs_result == ['A', 'B', 'C', 'D']

def test_connected_components(sample_graph):
    sample_graph.add_vertex('E')
    assert len(sample_graph.connected_components()) == 2
