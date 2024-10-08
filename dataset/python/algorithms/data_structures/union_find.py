class UnionFind1:

    def __init__(self, elements):
        self.parents = {key: key for key in elements}

    def find(self, element):
        return self.parents[element]

    def is_same_set(self, element1, element2):
        return self.parents[element1] == self.parents[element2]

    def union(self, element1, element2):
        for key in self.parents:
            if self.parents[key] == element2:
                self.parents[key] = element1
        return element1


class UnionFind2:

    def __init__(self, elements):
        self.parents = {key: key for key in elements}

    def find(self, element):
        while self.parents[element] != element:
            element = self.parents[element]
        return element

    def is_same_set(self, element1, element2):
        return self.find(element1) == self.find(element2)

    def union(self, element1, element2):
        if element1 not in self.parents or element2 not in self.parents:
            return None
        parent1, parent2 = self.find(element1), self.find(element2)
        self.parents[parent2] = parent1
        return parent1


class UnionFind3:

    def __init__(self, nodes):
        self.parents = {node: node for node in nodes}
        self.components_count = len(nodes)
        self.sizes = {node: 1 for node in nodes}

    def union(self, node1, node2):
        parent1, parent2 = self.find(node1), self.find(node2)
        self.components_count -= 1
        if self.sizes[parent1] > self.sizes[parent2]:
            self.parents[parent2] = parent1
            self.sizes[parent1] += self.sizes[parent2]
            return parent1
        else:
            self.parents[parent1] = parent2
            self.sizes[parent2] += self.sizes[parent1]
            return parent2


    def find(self, node):
        while self.parents[node] != node:
            self.parents[node] = self.parents[self.parents[node]]
            node = self.parents[node]
        return node

    def connected(self, node1, node2):
        return self.find(node1) == self.find(node2)

    def count(self):
        return self.components_count


class UnionFind4:

    def __init__(self, nodes):
        self.parents = {node: node for node in nodes}
        self.heights = {node: 1 for node in nodes}
        self.components_count = len(nodes)

    def union(self, node1, node2):
        parent1, parent2 = self.find(node1), self.find(node2)
        self.components_count -= 1
        if self.heights[parent1] > self.heights[parent2]:
            self.parents[parent2] = parent1
            return parent1
        elif self.heights[parent2] == self.heights[parent1]:
            self.parents[parent2] = parent1
            self.heights[parent1] += 1
        else:
            self.parents[parent1] = parent2
            return parent2

    def find(self, node):
        while self.parents[node] != node:
            self.parents[node] = self.parents[self.parents[node]]
            node = self.parents[node]
        return node

    def connected(self, node1, node2):
        return self.find(node1) == self.find(node2)

    def count(self):
        return self.components_count
