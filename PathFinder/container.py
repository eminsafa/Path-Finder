from PathFinder.node import Node


class Container:

    def __init__(self, route_solver):
        self.RS = route_solver
        self._nodes = {}

    def add_edge(self, node_id_1: int, node_id_2: int, distance: int):
        node_1 = self.get_node_by_id(node_id_1)
        node_2 = self.get_node_by_id(node_id_2)
        node_1.add_edge(node_2, distance)

    def get_node_by_id(self, node_id) -> Node:
        return self._nodes[node_id]

    def get_or_create_node_by_id(self, node_id: int) -> Node:
        if node_id in self._nodes.keys():
            return self._nodes[node_id]
        else:
            return self.create_node(node_id)

    def create_node(self, node_id: int):
        node = Node(node_id, self.RS)
        self._nodes[node_id] = node
        return node

    def parse_edge_data(self, data: str) -> (Node, Node, int):
        split = data.strip().split()
        node_1 = int(split[0])
        node_2 = int(split[1])
        distance = int(split[2])
        return node_1, node_2, distance

    def importer(self, path: str):
        with open(path) as f:
            number_of_nodes = int(f.readline().strip())
            #print(f"Number of Nodes: {number_of_nodes}")
            for n in range(number_of_nodes):
                node_id = int(f.readline().strip())
                self.create_node(node_id)
            number_of_edges = int(f.readline().strip())
            #print(f"Number of Edges: {number_of_edges}")
            for e in range(number_of_edges):
                n1, n2, d = self.parse_edge_data(f.readline())
                self.add_edge(n1, n2, d)
        #print("IMPORT PROCESS COMPLETED")
