import heapq

from graph_list import Graph
from union_find import UnionFind


def kruskal(graph):
    total_cost = 0
    min_cost_tree = Graph()
    connected_components = UnionFind(graph.get_all_vertices())
    edges_queue = graph.get_all_edges()
    heapq.heapify(edges_queue)
    while edges_queue:
        cost, edge = heapq.heappop(edges_queue)
        if is_valid_edge(edge, min_cost_tree, connected_components):
            total_cost += cost
            min_cost_tree.add_edge(edge[0], edge[1], cost)
            connected_components.union(edge[0], edge[1])
    return total_cost, min_cost_tree


def is_valid_edge(edge, graph, components):
    if graph.is_edge_in_graph(edge) or components.find(
        edge[0]
    ) == components.find(edge[1]):
        return False
    return True
