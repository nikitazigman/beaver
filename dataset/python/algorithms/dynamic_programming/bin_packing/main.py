def next_fit(elements):
    containers = []
    current_container = []
    current_container_sum = 0
    for i in range(len(elements)):
        element = elements[i]
        if current_container_sum + element <= 1:
            current_container.append(element)
            current_container_sum += element
        else:
            containers.append(current_container)
            current_container = [element]
            current_container_sum = element
            if i == len(elements) - 1:
                containers.append(current_container)
    return containers


def first_fit(elements):
    return _fit(elements, _find_first_fit_container_index)


def best_fit(elements):
    return _fit(elements, _find_best_fit_container_index)


def _find_first_fit_container_index(containers_sum, unfilled_containers, element):
    for i in unfilled_containers:
        if containers_sum[i] + element <= 1:
            return i
    return None


def _find_best_fit_container_index(containers_sum, unfilled_containers, element):
    result_index = None
    for i in unfilled_containers:
        if containers_sum[i] + element <= 1 and (not result_index or containers_sum[i] > containers_sum[result_index]):
            result_index = i
    return result_index


def _fit(elements, find_container_index):
    containers = [[]]
    unfilled_containers = set([0])
    containers_sum = {0: 0}
    for element in elements:
        container_index = find_container_index(containers_sum, unfilled_containers, element)
        if container_index is not None:
            container = containers[container_index]
            container.append(element)
            containers_sum[container_index] += element
        else:
            new_container = [element]
            containers_sum[len(containers)] = element
            container_index = len(containers)
            containers.append(new_container)
        if containers_sum[container_index] != 1:
            unfilled_containers.add(container_index)
        else:
            unfilled_containers.discard(container_index)
    return containers
