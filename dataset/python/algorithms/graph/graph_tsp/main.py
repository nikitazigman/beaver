def tsp(graph):
    if len(graph) <= 3:
        return list(graph.get_all_vertices())
    best_cycle = list(graph.get_all_vertices())
    best_cycle_weight = graph.cycle_weight(best_cycle)
    i = 1
    improvement = True
    while improvement and i < len(graph):
        improvement = False
        current_cycle = best_cycle[:]
        for j in range(i + 2, len(graph) + i - 1):
            current_cycle[i], current_cycle[j % len(graph)] = (
                current_cycle[j % len(graph)],
                current_cycle[i],
            )
            if (new_length := graph.cycle_weight(current_cycle)) < best_cycle_weight:
                best_cycle = current_cycle[:]
                best_cycle_weight = new_length
                improvement = True
            current_cycle[j % len(graph)], current_cycle[i] = (
                current_cycle[i],
                current_cycle[j % len(graph)],
            )
        i += 1
    return best_cycle
